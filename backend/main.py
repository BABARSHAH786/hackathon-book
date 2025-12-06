# neeechay code comment hai
# new
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# RAG Libraries
from google import genai
from google.genai.errors import APIError
from qdrant_client import QdrantClient

# --------------------------- LOAD ENV ---------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "ragchatbot")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# --------------------------- FASTAPI ---------------------------
app = FastAPI(title="Physical AI RAG Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- INIT GEMINI + QDRANT ----------------------
try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✅ RAG Initialized. Collection: {QDRANT_COLLECTION_NAME}")

except Exception as e:
    gemini_client = None
    qdrant_client = None
    print("🛑 Initialization Error:", e)

# ---------------------- API MODELS ----------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# ---------------------- UNIVERSAL EMBEDDING FIX ----------------------
def get_embedding_safe(query: str):
    """
    Works on ALL Google Gemini SDK versions:
    - OLD: embed_content(contents=[...]) + .embedding
    - MID: embed_content(contents=[...]) + .embeddings
    - NEW: embed_content(content=...) + .embeddings
    """

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


# ---------------------- RAG PIPELINE ----------------------
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


# ---------------------- ENDPOINT ----------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    answer = perform_rag_query(request.message)
    return ChatResponse(response=answer)


# ---------------------- START SERVER ----------------------
if __name__ == "__main__":
    print(f"🔥 Server running at http://{HOST}:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)







# old
# import os
# import uvicorn
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Dict

# # --- RAG Libraries ---
# from google import genai
# from google.genai.errors import APIError
# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct, Distance, VectorParams, SearchParams

# # --- 1. ENVIRONMENT & CONFIGURATION LOADING ---

# # Load environment variables from .env file
# load_dotenv()

# # API Keys and URLs from your .env (Using variable NAMES, not values)
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# # Ensure the collection name matches what you used during indexing
# QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "ragchatbot") 
# HOST = os.getenv("HOST", "0.0.0.0")
# PORT = int(os.getenv("PORT", 8000))

# # CORS settings for frontend communication (Ensure 3000/5173 is included)
# ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(',')

# # --- 2. FASTAPI APP INITIALIZATION ---

# app = FastAPI(
#     title="Physical AI RAG Chatbot Backend",
#     version="1.0",
# )

# # Apply CORS Middleware (Must be done first)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- 3. RAG/GEMINI INITIALIZATION ---

# # Clients ko globally define karein
# gemini_client = None
# qdrant_client = None

# try:
#     if not GEMINI_API_KEY or not QDRANT_URL or not QDRANT_API_KEY:
#         raise ValueError("One or more required RAG keys (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY) are missing in .env")

#     # Initialize Gemini Client
#     gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    
#     # Initialize Qdrant Client
#     qdrant_client = QdrantClient(
#         url=QDRANT_URL, 
#         api_key=QDRANT_API_KEY
#     )
#     print(f"✅ RAG Clients Initialized. Collection: {QDRANT_COLLECTION_NAME}")

# except ValueError as e:
#     print(f"🛑 Initialization Error: {e}")
    
# except Exception as e:
#     print(f"🛑 Critical RAG Initialization Error: {e}")

# # --- 4. DATA MODEL ---

# class ChatRequest(BaseModel):
#     message: str

# class ChatResponse(BaseModel):
#     response: str

# # --- 5. RAG FUNCTION (FULL IMPLEMENTATION with FIX) ---

# def perform_rag_query(query: str) -> str:
#     """
#     Full RAG logic: Query -> Embed -> Retrieve (Qdrant) -> Generate (Gemini).
#     """
#     if not gemini_client or not qdrant_client:
#         return "ERROR: RAG clients are not initialized. Check server console for .env errors."
        
#     try:
#         # 1. Embed the user query (FIX: Use 'contents' instead of 'content' and pass as a list)
#         embedding_result = gemini_client.models.embed_content(
#             model='models/text-embedding-004', # Ya koi aur suitable embedding model
#             contents=[query] # <-- FIX APPLIED
#         )
#         # Embedding output list mein aata hai, isliye pehla element nikalen
#         query_vector = embedding_result['embedding'][0] 

#         # 2. Search Qdrant for relevant documents
#         search_result = qdrant_client.search(
#             collection_name=QDRANT_COLLECTION_NAME,
#             query_vector=query_vector,
#             limit=3,  # Top 3 results nikalen
#             with_payload=True 
#         )
        
#         # Aggregate the retrieved context
#         context_parts = [point.payload.get('text', '') for point in search_result if point.payload.get('text')]
#         context = "\n\n---\n\n".join(context_parts)
        
#         if not context:
#             return "Sorry, I couldn't find any relevant course material in the knowledge base. Please try a different question."

#         # 3. Construct the prompt for the LLM
#         prompt = (
#             f"You are a helpful assistant for a Physical AI and Humanoid Robotics course. "
#             f"Use the following course context to answer the user's question accurately and concisely. "
#             f"If the context does not contain the answer, state clearly: 'I cannot answer that question based on the course materials provided.'\n\n"
#             f"CONTEXT:\n{context}\n\n"
#             f"USER QUESTION: {query}"
#         )

#         # 4. Call the Gemini API to generate the response
#         response = gemini_client.models.generate_content(
#             model='gemini-2.5-flash', # Fastest model for chat
#             contents=prompt
#         )
#         return response.text
    
#     except APIError as e:
#         print(f"Gemini API Error: {e}")
#         # Agar error API call se aata hai, toh yeh message aayega.
#         return "LLM Service Error: Could not get a response from Gemini API. Check your API key or quota."
        
#     except Exception as e:
#         print(f"RAG Processing Error: {e}")
#         # Dusre kisi bhi error ke liye yeh message aayega.
#         return f"An internal RAG error occurred during processing: {str(e)}"

# # --- 6. API ENDPOINT ---

# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
#     """
#     Handles incoming chat messages and returns an RAG-generated response.
#     """
#     try:
#         # Get the RAG response
#         rag_answer = perform_rag_query(request.message)
        
#         return ChatResponse(response=rag_answer)
        
#     except HTTPException:
#         # Re-raise explicit HTTP errors
#         raise 
        
#     except Exception as e:
#         print(f"Internal Endpoint Error: {e}")
#         # Return a controlled error message to the frontend
#         return ChatResponse(response="An unexpected server error occurred on the endpoint.")


# # --- 7. SERVER RUNNER ---

# if __name__ == "__main__":
#     print(f"Starting server at http://{HOST}:{PORT}")
#     print(f"Allowed Frontend Origins: {ALLOWED_ORIGINS}")
    
#     # Run the Uvicorn server
#     uvicorn.run(
#         "main:app", 
#         host=HOST, 
#         port=PORT, 
#         reload=True # Use reload=True for development
#     )