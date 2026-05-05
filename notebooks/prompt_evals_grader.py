import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    # Load env variables and create client
    from dotenv import load_dotenv
    from anthropic import Anthropic

    load_dotenv()

    client = Anthropic()
    model = "claude-haiku-4-5"
    return client, model


@app.cell
def _(client, model):
    # Helper functions
    def add_user_message(messages, text):
        user_message = {"role": "user", "content": text}
        messages.append(user_message)


    def add_assistant_message(messages, text):
        assistant_message = {"role": "assistant", "content": text}
        messages.append(assistant_message)


    def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
        params = {
            "model": model,
            "max_tokens": 1000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)
        return message.content[0].text

    return add_assistant_message, add_user_message, chat


@app.cell
def _(add_assistant_message, add_user_message, chat):
    # Function to generate a new dataset
    import json


    def generate_dataset():
        prompt = """
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
    that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
    each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {
            "task": "Description of task",
            "format": "json" or "python" or "regex"
        },
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """

        messages = []
        add_user_message(messages, prompt)
        add_assistant_message(messages, "```json")
        text = chat(messages, stop_sequences=["```"])
        return json.loads(text)

    return generate_dataset, json


@app.cell
def _(generate_dataset, json):
    # Generate the dataset and write it to 'dataset.json'
    _dataset = generate_dataset()
    with open('dataset.json', 'w') as _f:
        json.dump(_dataset, _f, indent=2)
    return


@app.cell
def _(add_assistant_message, add_user_message, chat, json):
    # Function to grade a test case + output using a model
    def grade_by_model(test_case, output):
        eval_prompt = f"""
    You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

    Original Task:
    <task>
    {test_case["task"]}
    </task>

    Solution to Evaluate:
    <solution>
    {output}
    </solution>

    Output Format
    Provide your evaluation as a structured JSON object with the following fields, in this specific order:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your overall assessment
    - "score": A number between 1-10

    Respond with JSON. Keep your response concise and direct.
    Example response shape:
    {{
        "strengths": string[],
        "weaknesses": string[],
        "reasoning": string,
        "score": number
    }}
        """

        messages = []
        add_user_message(messages, eval_prompt)
        add_assistant_message(messages, "```json")
        eval_text = chat(messages, stop_sequences=["```"])
        return json.loads(eval_text)

    return (grade_by_model,)


@app.cell
def _(add_user_message, chat):
    # Passes a test case into Claude
    def run_prompt(test_case):
        prompt = f"""
    Please solve the following task:

    {test_case["task"]}
    """

        messages = []
        add_user_message(messages, prompt)
        output = chat(messages)
        return output

    return (run_prompt,)


@app.cell
def _(grade_by_model, run_prompt):
    # Function to execute a single test case and grade the output
    def run_test_case(test_case):
        """Calls run_prompt, then grades the result"""
        output = run_prompt(test_case)

        model_grade = grade_by_model(test_case, output)
        score = model_grade["score"]
        reasoning = model_grade["reasoning"]

        return {
            "output": output,
            "test_case": test_case,
            "score": score,
            "reasoning": reasoning,
        }

    return (run_test_case,)


@app.cell
def _(run_test_case):
    from statistics import mean

    def run_eval(dataset):
        """Loads the dataset and calls run_test_case with each case"""
        results = []
        for test_case in _dataset:
            result = run_test_case(test_case)
            results.append(result)
        average_score = mean([result['score'] for result in results])
        print(f'Average score: {average_score}')
        return results

    return (run_eval,)


@app.cell
def _(json, run_eval):
    with open('dataset.json', 'r') as _f:
        _dataset = json.load(_f)
    results = run_eval(_dataset)
    return (results,)


@app.cell
def _(json, results):
    print(json.dumps(results, indent=2))
    return


if __name__ == "__main__":
    app.run()
