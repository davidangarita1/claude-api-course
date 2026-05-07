import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from dotenv import load_dotenv
    load_dotenv() 

    from anthropic import Anthropic

    client = Anthropic()
    model = "claude-sonnet-4-6"

    messages = []
    return client, messages, mo, model


@app.cell
def _(mo):
    mo.md("""
    ## Building a Flexible Chat Function
    """)
    return


@app.cell
def _(client, model):
    system_prompt = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    """

    def chat(messages, system=None):
        params = {
            "model": model,
            "max_tokens": 1000,
            "messages": messages,
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)
        return message.content[0].text

    return (chat,)


@app.cell
def _(chat, messages):
    # Sin prompt del sistema
    answer = chat(messages)

    # Con prompt del sistema
    system = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    """

    answer = chat(messages, system=system)
    return


if __name__ == "__main__":
    app.run()
