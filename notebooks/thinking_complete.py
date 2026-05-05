import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    # Cargar variables de entorno y crear cliente
    from dotenv import load_dotenv
    from anthropic import Anthropic

    load_dotenv()

    client = Anthropic()
    model = "claude-sonnet-4-5"
    return client, model


@app.cell
def _(client, model):
    # Funciones auxiliares
    from anthropic.types import Message

    # Magic string to trigger redacted thinking
    thinking_test_str = "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"


    def add_user_message(messages, message):
        user_message = {
            "role": "user",
            "content": message.content if isinstance(message, Message) else message,
        }
        messages.append(user_message)


    def add_assistant_message(messages, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content if isinstance(message, Message) else message,
        }
        messages.append(assistant_message)


    def chat(
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):
        params = {
            "model": model,
            "max_tokens": 4000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = client.messages.create(**params)
        return message


    def text_from_message(message):
        return "\n".join([block.text for block in message.content if block.type == "text"])

    return add_user_message, chat, thinking_test_str


@app.cell
def _(add_user_message, chat, thinking_test_str):
    messages = []

    add_user_message(messages, thinking_test_str)

    chat(messages, thinking=True)
    return


if __name__ == "__main__":
    app.run()
