import os
from dotenv import load_dotenv
import nest_asyncio
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

# Apply nest_asyncio
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Check for API keys
if not os.getenv("LLAMA_CLOUD_API_KEY"):
    raise ValueError("LLAMA_CLOUD_API_KEY not found in .env")
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Configure Settings
Settings.llm = GoogleGenAI(model="gemini-3-flash-preview")
Settings.embed_model = GoogleGenAIEmbedding(model_name="models/text-embedding-004")

DATA_DIR = "./data"
STORAGE_DIR = "./storage"

def ingest_documents():
    # Check if storage already exists
    if os.path.exists(STORAGE_DIR):
        print(f"Storage directory '{STORAGE_DIR}' already exists. Skipping ingestion.")
        return

    print("Storage directory not found. Starting ingestion...")

    # Check for PDFs in data directory
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created '{DATA_DIR}'. Please put your PDF files there.")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
    if not files:
        print(f"No PDF files found in '{DATA_DIR}'. Please add a PDF file.")
        return

    print(f"Found {len(files)} PDF(s): {files}")

    # Initialize LlamaParse
    parser = LlamaParse(
        result_type="markdown",
        premium_mode=True,  # Set to True for better table/image extraction
        verbose=True,
        language="en"
    )

    # Use SimpleDirectoryReader with LlamaParse
    file_extractor = {".pdf": parser}
    reader = SimpleDirectoryReader(DATA_DIR, file_extractor=file_extractor)
    documents = reader.load_data()

    print(f"Loaded {len(documents)} document chunks/pages.")

    # Inspect and fix metadata to ensure page_label is present
    print("Checking metadata for page labels...")
    for i, doc in enumerate(documents):
        # LlamaParse puts page number in metadata, try different field names
        if 'page_label' not in doc.metadata:
            # Try alternative metadata fields from LlamaParse
            if 'page' in doc.metadata:
                doc.metadata['page_label'] = str(doc.metadata['page'])
            elif 'page_number' in doc.metadata:
                doc.metadata['page_label'] = str(doc.metadata['page_number'])
            else:
                # Fallback: use document index as page number (starts at 1)
                doc.metadata['page_label'] = str(i + 1)
        
        # Debug: print first few metadata samples
        if i < 3:
            print(f"Document {i} metadata: {doc.metadata}")
    
    # Create Index
    print("Creating VectorStoreIndex...")
    index = VectorStoreIndex.from_documents(documents)

    # Persist Storage
    print(f"Persisting index to '{STORAGE_DIR}'...")
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_documents()
