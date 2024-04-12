# query.py
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "search-ci"
NAMESPACE = os.getenv("COMMIT_ID")

def generate_embedding(question):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(question)

    return embedding.tolist()

def search_query(question):
    try:
        embedding = generate_embedding(question)
        pc = Pinecone(api_key=API_KEY)
        index = pc.Index(INDEX_NAME)

        result = index.query(
            namespace=NAMESPACE,
            vector=embedding,
            top_k=1,
            include_metadata=True
        )
        answer = result.matches[0].metadata["answer"]
        score = result.matches[0].score
        print(f"Question: {question} \nAnswer: {answer} \nSimilarity score: {score}")

        # if result.matches[0].score < 0.5:
        #     return "Sorry, I do not have an answer to that question."

        return answer
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e