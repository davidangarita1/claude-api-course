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
def _(mo):
    mo.md("""
    ## Simplified Text Streaming

    Rather than manually parsing events, you can use the SDK's simplified streaming interface that extracts just the text content:
    """)
    return


@app.cell
def _(client, messages, model):
    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            # Send each chunk to your client
            pass
    
        # Get the complete message for database storage
        final_message = stream.get_final_message()
    return


if __name__ == "__main__":
    app.run()
