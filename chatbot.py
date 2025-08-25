import textwrap
from ollama import Client
import os


def build_prompt(question: str, books) -> str:
    context = "\n\n".join(
        " # " + book[1].get("title") + "\n" + book[0] for book in books
    )
    return textwrap.dedent(
        f"""
    You are a librarian, and will answer the 'Question' only by using information
     contained within 'Books you know about'. It's okay to mention just one book in
     your answer. Be concise, do not include useless information.

    # Books you know about
    {context}

    # Question
    {question}
    """
    ).strip()


def generate_answer_stream(prompt: str):
    chat_model = os.getenv("CHAT_MODEL")
    ollama = Client()
    for chunk in ollama.generate(model=chat_model, prompt=prompt, stream=True):
        yield chunk["response"]
