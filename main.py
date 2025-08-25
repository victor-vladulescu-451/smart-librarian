<<<<<<< HEAD
import chromadb
import uuid

client = chromadb.PersistentClient(path="data/chroma_data")

collection_name = "books"

try:
    collection = client.get_collection(name=collection_name)
except Exception as e:
    collection = None

if collection is None:
    print("Creating new collection 'books'...\n\n")
    collection = client.create_collection(name=collection_name)
    books_store: dict[str, str] = {}

    with open("book_summaries.txt", "r", encoding="utf-8") as file:
        file_contents = file.read().strip()
        books = file_contents.split("\n\n")
        for book in books:
            title, summary = book.split("\n", 1)
            title = title.replace("#", "").strip()
            summary = summary.replace("\n", " ").strip()
            books_store[title.strip()] = summary.strip()

    collection.add(
        ids=[str(uuid.uuid4()) for _ in books_store],
        documents=list(books_store.values()),
        metadatas=[{"title": title} for title in books_store.keys()],
    )
=======
from dotenv import load_dotenv
import chroma
import chatbot
>>>>>>> 97941b2aa315bae08abbae081e5893b92786af60


if __name__ == "__main__":

<<<<<<< HEAD
print(results)
=======
    load_dotenv()

    print("Question: ")
    question = input()

    books = chroma.get_collection()
    chunks = chroma.query_chunks(books, question, k=3)
    prompt = chatbot.build_prompt(question, chunks)

    print("\nAnswer:\n", end="", flush=True)
    for chunk in chatbot.generate_answer_stream(prompt):
        print(chunk, end="", flush=True)
    print()
>>>>>>> 97941b2aa315bae08abbae081e5893b92786af60
