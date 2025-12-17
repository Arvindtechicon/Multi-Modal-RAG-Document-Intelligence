import os
import time
import pandas as pd
from dotenv import load_dotenv
import nest_asyncio
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

# Apply nest_asyncio
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Global Settings (ensure they match ingest.py)
Settings.llm = GoogleGenAI(
    model="gemini-3-flash-preview",
    system_prompt="You are an expert Financial Analyst. Provide accurate answers based ONLY on the provided context."
)
Settings.embed_model = GoogleGenAIEmbedding(model_name="models/text-embedding-004")

STORAGE_DIR = "./storage"
RESULTS_FILE = "benchmark_results.csv"

# Complex Queries to Benchmark
QUERIES = [
    "Summarize the key financial highlights from the document.",
    "What are the risk factors mentioned? details please.",
    "Analyze the revenue growth trends if available in the tables.",
    "What is the outlook for the next fiscal year?",
    "Compare the operating expenses between the current and previous periods."
]

def run_evaluation():
    if not os.path.exists(STORAGE_DIR):
        print(f"Storage directory '{STORAGE_DIR}' not found. Please run ingest.py first.")
        return

    print("Loading Index...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    results = []

    print("Starting Benchmark...")
    for query in QUERIES:
        print(f"Running query: {query}")
        start_time = time.time()
        
        try:
            response = query_engine.query(query)
            end_time = time.time()
            latency = end_time - start_time
            answer = response.response
            
            # Extract page citations if possible
            pages = set()
            for node in response.source_nodes:
                pages.add(node.node.metadata.get("page_label", "Unknown"))
            pages_str = ", ".join(pages)

            results.append({
                "Query": query,
                "Latency (s)": round(latency, 2),
                "Pages Cited": pages_str,
                "Answer Preview": answer[:100] + "..." if len(answer) > 100 else answer
            })
            print(f"Completed in {latency:.2f}s")
            
        except Exception as e:
            print(f"Error querying '{query}': {e}")
            results.append({
                "Query": query,
                "Latency (s)": -1,
                "Pages Cited": "Error",
                "Answer Preview": str(e)
            })

    # Save Results
    df = pd.DataFrame(results)
    df.to_csv(RESULTS_FILE, index=False)
    print(f"\nBenchmark complete. Results saved to {RESULTS_FILE}")
    print(df)

if __name__ == "__main__":
    run_evaluation()
