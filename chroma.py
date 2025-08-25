import chromadb
import uuid
import os


def get_collection() -> chromadb.Collection:

    collection_name = "books"
    collection = None

    persist_directory = os.environ.get("CHROMA_DIR")
    client = chromadb.PersistentClient(path=persist_directory)

    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        collection = None

    if collection is not None:
        return collection

    print("Creating new collection '" + collection_name + "'...\n\n")
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

    return collection


def query_chunks(col: chromadb.Collection, query: str, k: int):
    res = col.query(n_results=k, query_texts=query)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    return list(zip(docs, metas))
