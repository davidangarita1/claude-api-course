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


@app.cell
def _(client, model):
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
def _(mo):
    mo.md("""
    Assistant Message Prefilling + Stop Sequences
    """)
    return


@app.cell
def _(add_assistant_message, add_user_message, chat, messages):
    add_user_message(messages, "Generate a very short event bridge rule as json")
    add_assistant_message(messages, "```json")

    text = chat(messages, stop_sequences=["```"])
    return


if __name__ == "__main__":
    app.run()
