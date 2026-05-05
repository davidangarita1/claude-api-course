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
    model = "claude-sonnet-4-0"

    messages = []
    return client, messages, mo, model


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Building Helper Functions
    """)
    return


@app.cell
def _(client, model):
    def add_user_message(messages, text):
        user_message = {"role": "user", "content": text}
        messages.append(user_message)


    def add_assistant_message(messages, text):
        assistant_message = {"role": "assistant", "content": text}
        messages.append(assistant_message)

    def chat(messages):
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=messages,
        )
        return message.content[0].text

    return add_assistant_message, add_user_message, chat


@app.cell
def _(mo):
    mo.md("""
    Putting It All Together
    """)
    return


@app.cell
def _(add_assistant_message, add_user_message, chat, messages):
    # Add the initial user question
    add_user_message(messages, "Define quantum computing in one sentence")

    # Get Claude's response
    answer = chat(messages)

    # Add Claude's response to the conversation history
    add_assistant_message(messages, answer)

    # Add a follow-up question
    add_user_message(messages, "Write another sentence")

    # Get the follow-up response with full context
    final_answer = chat(messages)
    return


if __name__ == "__main__":
    app.run()
