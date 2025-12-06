
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from google import genai
from google.genai.errors import APIError

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "ragchatbot")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

qdrant_client = None
gemini_client = None

try:
    if not QDRANT_URL or not QDRANT_API_KEY or not GEMINI_API_KEY:
        raise ValueError("Missing one or more RAG environment variables (QDRANT_URL, QDRANT_API_KEY, GEMINI_API_KEY).")

    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    print(f"✅ Qdrant and Gemini clients initialized. Collection: {QDRANT_COLLECTION_NAME}")

except ValueError as e:
    print(f"🛑 RAG Initialization Error: {e}")
except Exception as e:
    print(f"🛑 Critical RAG Initialization Error: {e}")

def get_embedding_safe(query: str):
    """
    Works on ALL Google Gemini SDK versions:
    - OLD: embed_content(contents=[...]) + .embedding
    - MID: embed_content(contents=[...]) + .embeddings
    - NEW: embed_content(content=...) + .embeddings
    """
    if gemini_client is None:
        raise ValueError("Gemini client not initialized.")

    # 1️⃣ Try NEW API
    try:
        res = gemini_client.models.embed_content(
            model="models/text-embedding-004",
            content=query
        )
        return res.embeddings[0].values

    except TypeError:
        # The SDK does NOT support "content=" → use OLD API
        res = gemini_client.models.embed_content(
            model="models/text-embedding-004",
            contents=[query]
        )

        # OLD:
        if hasattr(res, "embedding"):
            return res.embedding[0]

        # MID:
        if hasattr(res, "embeddings"):
            return res.embeddings[0].values

        raise ValueError("❌ No valid embedding attribute found.")

def perform_rag_query(query: str) -> str:
    if gemini_client is None or qdrant_client is None:
        return "❌ RAG is not initialized. Check your .env settings."

    try:
        # 1️⃣ Get vector
        query_vector = get_embedding_safe(query)

        # 2️⃣ Qdrant search
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=3,
            with_payload=True,
        )

        # Extract context
        chunks = [
            point.payload.get("text", "")
            for point in search_result
            if point.payload and point.payload.get("text")
        ]

        if not chunks:
            return "No relevant course material found."

        context = "\n\n---\n\n".join(chunks)

        # 3️⃣ Prompt
        prompt = f"""
You are a helpful assistant for a Physical AI & Humanoid Robotics course.

Use only the following CONTEXT to answer.
If answer is not available, say:
"I cannot answer that based on the available course materials."

CONTEXT:
{context}

USER QUESTION:
{query}
"""

        # 4️⃣ LLM Response
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("RAG Error:", e)
        return f"Internal RAG error: {str(e)}"
