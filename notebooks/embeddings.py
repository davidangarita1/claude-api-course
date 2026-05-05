import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    # Instalar la librería VoyageAI
    # El comando '%pip install voyageai' es soportado automáticamente en marimo
    return


@app.cell
def _():
    # Configuración del cliente
    from dotenv import load_dotenv
    import voyageai

    load_dotenv()

    client = voyageai.Client()
    return (client,)


@app.cell
def _():
    # Dividir por sección
    import re


    def chunk_by_section(document_text):
        pattern = r"\n## "
        return re.split(pattern, document_text)

    return (chunk_by_section,)


@app.cell
def _(client):
    # Generación de embeddings
    def generate_embedding(text, model="voyage-3-large", input_type="query"):
        result = client.embed([text], model=model, input_type=input_type)

        return result.embeddings[0]

    return (generate_embedding,)


@app.cell
def _(chunk_by_section, generate_embedding):
    with open("./report.md", "r") as f:
        text = f.read()

    chunks = chunk_by_section(text)

    generate_embedding(chunks[0])
    return


if __name__ == "__main__":
    app.run()
