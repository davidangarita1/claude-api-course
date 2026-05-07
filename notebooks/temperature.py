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
    Implementing Temperature in Code
    """)
    return


@app.cell
def _(client, model):
    def chat(messages, system=None, temperature=1.0):
        params = {
            "model": model,
            "max_tokens": 1000,
            "messages": messages,
            "temperature": temperature
        }
    
        if system:
            params["system"] = system
    
        message = client.messages.create(**params)
        return message.content[0].text

    return (chat,)


@app.cell
def _(chat, messages):
    # Temperatura baja - más predecible
    answer = chat(messages, temperature=0.0)

    # Temperatura alta - más creativo  
    answer = chat(messages, temperature=1.0)
    return


if __name__ == "__main__":
    app.run()
