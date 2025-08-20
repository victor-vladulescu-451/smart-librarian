import chromadb
import uuid

client = chromadb.PersistentClient(path="./chroma_data")

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


results = collection.query(
    query_texts=[
        "censorship",
        "justice",
    ],
    n_results=1,
)

print(results)
