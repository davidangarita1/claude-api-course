import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
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

    return add_user_message, chat


@app.cell
def _():
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
        },
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """

    return (json,)


@app.cell
def _(add_user_message, chat):
    def run_prompt(test_case):
        """Merges the prompt and test case input, then returns the result"""
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
def _(run_prompt):
    def run_test_case(test_case):
        """Calls run_prompt, then grades the result"""
        output = run_prompt(test_case)
    
        # TODO - Grading
        score = 10
    
        return {
            "output": output,
            "test_case": test_case,
            "score": score
        }

    return (run_test_case,)


@app.cell
def _(run_test_case):
    def run_eval(dataset):
        """Loads the dataset and calls run_test_case with each case"""
        results = []
    
        for test_case in dataset:
            result = run_test_case(test_case)
            results.append(result)
    
        return results

    return (run_eval,)


@app.cell
def _(json, run_eval):
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    results = run_eval(dataset)
    return


if __name__ == "__main__":
    app.run()
