# 🇶🇦 Multi-Modal RAG: Qatar Economic Analyst

An AI-powered financial analysis chatbot specialized in analyzing Qatar's economic documents using **multi-modal capabilities** (text, tables, and charts).

## 🎯 Overview

This project implements an intelligent QA system that combines:
- **LlamaParse** for advanced PDF parsing with table/chart extraction
- **LlamaIndex** for semantic search and retrieval
- **Gemini 3 Flash Preview** for fast, accurate AI analysis
- **Vector embeddings** for precise document retrieval
- **Streamlit** for a modern, interactive UI

## 🚀 Quick Start

### 1. Setup Environment
Install all dependencies:
```bash
pip install -r requirements.txt
```

API Keys are pre-filled in `.env` file.

### 2. Add Your Data
**IMPORTANT**: Place your financial PDF file(s) into the `data/` directory.
- The script looks for `.pdf` files in `data/`
- Supports multi-modal content: text, tables, and charts

### 3. Ingestion (Index Creation)
Run the ingestion script to parse PDFs and create the vector index:
```bash
python ingest.py
```
This will:
- Parse PDFs using LlamaParse in premium mode
- Extract text, tables, and chart data
- Create embeddings using Gemini
- Store everything in `storage/` directory

### 4. Run the Application
Start the Qatar Economic Analyst chatbot:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`

### 5. Evaluation & Benchmarking
Run the benchmark suite to test performance:
```bash
python evaluate.py
```
Results will be saved to `benchmark_results.csv`

## 🏗️ Project Structure
```
📦 RAG agent/
├── 📄 app.py                    # Streamlit QA application (Qatar theme)
├── 📄 ingest.py                 # PDF parsing and indexing
├── 📄 evaluate.py               # Performance benchmarking
├── 📄 inspect_doc.py            # Document inspection utility
├── 📄 TECHNICAL_REPORT.md       # Architecture documentation
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # API keys (pre-configured)
├── 📂 data/                     # Input PDF files
├── 📂 storage/                  # Vector index (auto-generated)
└── 📂 benchmark_results.csv     # Evaluation results
```

## 🔑 Key Features
- ✅ **Multi-Modal Analysis**: Extracts data from text, tables, and charts
- ✅ **Page-Level Citations**: Every answer includes source page numbers
- ✅ **Qatar Economic Focus**: Specialized prompts for economic analysis
- ✅ **Modern UI**: Beautiful gradient design with glassmorphism
- ✅ **Fast Performance**: Using Gemini 3 Flash Preview for speed
- ✅ **Accurate Retrieval**: Vector search with semantic understanding

## 🛠️ Technology Stack
| Component | Technology |
|-----------|-----------|
| **LLM** | Gemini 3 Flash Preview |
| **Embeddings** | Gemini text-embedding-004 |
| **PDF Parser** | LlamaParse (Premium Mode) |
| **Vector Store** | LlamaIndex VectorStoreIndex |
| **UI Framework** | Streamlit |
| **Language** | Python 3.11+ |

## 📊 Model Information
- **Primary LLM**: `gemini-3-flash-preview`  
  Fast, efficient model optimized for RAG applications
- **Embedding Model**: `models/text-embedding-004`  
  Latest Gemini embedding model for semantic search

## 🎨 UI Features
The Qatar Economic Analyst features a premium UI with:
- Qatar-inspired color scheme (maroon & gold)
- Glassmorphism effects
- Smooth animations
- Responsive design
- Dark gradient backgrounds
- Professional typography

---

**🇶🇦 Built for Qatar Economic Intelligence | Powered by AI**
