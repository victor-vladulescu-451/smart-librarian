from dotenv import load_dotenv
import chroma
import chatbot


if __name__ == "__main__":

    load_dotenv()

    question = "Recommend a book about dystopian worlds."

    books = chroma.get_collection()
    chunks = chroma.query_chunks(books, question, k=3)
    prompt = chatbot.build_prompt(question, chunks)
    answer = chatbot.generate_answer(prompt)

    print("\nQ:", question)
    print("\nAnswer:\n", answer)
