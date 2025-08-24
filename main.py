from dotenv import load_dotenv
import chroma
import chatbot


if __name__ == "__main__":

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
