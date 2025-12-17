
import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import nest_asyncio

nest_asyncio.apply()
load_dotenv()

# Configure Settings (must match ingest.py)
Settings.llm = GoogleGenAI(model="gemini-3-flash-preview")
Settings.embed_model = GoogleGenAIEmbedding(model_name="models/text-embedding-004")

STORAGE_DIR = "./storage"

def inspect():
    if not os.path.exists(STORAGE_DIR):
        print("Storage not found.")
        return

    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    response = query_engine.query("What is the exact title of this document and what are the main chapter headings? Provide a brief 1-sentence summary.")
    print(response)

if __name__ == "__main__":
    inspect()
