import streamlit as st
import os
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

# Streamlit Config
st.set_page_config(
    page_title="Qatar Economic Analyst | Multi-Modal RAG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - Simple, clean background */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Sidebar - Professional and simple */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Header styling - Simple and clear */
    .main-header {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        padding: 20px 0;
    }
    
    .sub-header {
        color: #5a6c7d;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Message bubbles - Clean and readable */
    .stChatMessage {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #3498db;
    }
    
    /* Info boxes - Soft and visible */
    .stInfo {
        background-color: #e3f2fd;
        color: #1565c0;
        border-left: 4px solid #2196f3;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Buttons - Simple and effective */
    .stButton > button {
        background: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: background 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #2980b9;
    }
    
    /* Input field - Clean borders */
    .stChatInputContainer input {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 12px;
    }
    
    .stChatInputContainer input:focus {
        border-color: #3498db;
        outline: none;
    }
    
    /* Expander - Subtle styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Metric cards - Clean appearance */
    [data-testid="metric-container"] {
        background: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        border: 1px solid #e9ecef;
    }
    
    /* Divider line */
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #3498db, transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Global Settings
Settings.llm = GoogleGenAI(
    model="gemini-3-flash-preview",
    system_prompt="You are an expert Financial Analyst with deep knowledge in corporate finance, accounting, and investment analysis. Your goal is to provide accurate, insightful answers based ONLY on the provided context. You MUST cite your sources including page numbers for every claim you make. If you are unsure, state that you don't know."
)
Settings.embed_model = GoogleGenAIEmbedding(model_name="models/text-embedding-004")

STORAGE_DIR = "./storage"

@st.cache_resource
def load_query_engine():
    if not os.path.exists(STORAGE_DIR):
        st.error(f"⚠️ Storage directory '{STORAGE_DIR}' not found. Please run `ingest.py` first.")
        return None
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = load_index_from_storage(storage_context)
        return index.as_query_engine(similarity_top_k=5)
    except Exception as e:
        st.error(f"❌ Error loading index: {e}")
        return None

# Sidebar
with st.sidebar:
    st.markdown("### 🇶🇦 Qatar Economic Analyst")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    **Multi-Modal Analysis Platform**
    
    This system analyzes Qatar economic documents using:
    
    • **LlamaParse** - Advanced PDF parsing  
    • **Gemini 3 Flash** - AI-powered analysis  
    • **Vector Search** - Semantic retrieval  
    • **Multi-Modal** - Text, tables & charts
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Example Questions")
    st.markdown("""
    • "Summarize Qatar's economic highlights"
    
    • "What is the GDP growth rate?"
    
    • "Analyze revenue streams and sectors"
    
    • "What are the key financial risks?"
    
    • "What's the economic outlook?"
    
    • "Compare year-over-year performance"
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 10px;'>
    <p style='font-size: 0.9em; margin: 0;'>Qatar Economic Intelligence</p>
    <p style='font-size: 0.75em; opacity: 0.8; margin: 5px 0 0 0;'>Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
st.markdown("<h1 class='main-header'>📊 Multi-Modal RAG: Qatar Economic Analyst</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Powered by LlamaParse & Gemini 3 Flash Preview | Analyzes Text, Tables, and Charts</p>", unsafe_allow_html=True)
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Load query engine
query_engine = load_query_engine()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message if no chat history
if len(st.session_state.messages) == 0 and query_engine:
    with st.chat_message("assistant"):
        st.markdown("""
        ### 👋 Welcome to Qatar Economic Analyst!
        
        I'm your AI-powered assistant for analyzing Qatar's economic and financial documents.
        
        **What I can do:**
        - ✅ Extract data from text, tables, and charts
        - ✅ Provide page-level citations for accuracy
        - ✅ Analyze economic trends and metrics
        - ✅ Answer questions about Qatar's financial landscape
        
        **Try asking me about:**
        - Economic performance indicators
        - Revenue analysis and growth trends  
        - Risk assessments and outlook
        - Sector-specific data from tables
        
        **Type your question below to begin!** 👇
        """)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "pages" in message:
            st.info(f"📄 Sources: Pages {message['pages']}")

# Chat Input
if prompt := st.chat_input("Ask about Qatar's economic data..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if query_engine:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Qatar economic data..."):
                try:
                    response = query_engine.query(prompt)
                    
                    # Display Answer
                    st.markdown(response.response)
                    
                    # Citation Logic
                    unique_pages = set()
                    for node in response.source_nodes:
                        page = node.node.metadata.get("page_label", "Unknown")
                        unique_pages.add(page)
                    
                    sorted_pages = sorted(list(unique_pages), key=lambda x: int(x) if x.isdigit() else float('inf'))
                    pages_str = ", ".join(sorted_pages)
                    
                    st.info(f"� **Sources:** Pages {pages_str}")
                    
                    # Optional: Expandable source details
                    with st.expander("� View Source Details"):
                        for i, node in enumerate(response.source_nodes):
                            page = node.node.metadata.get("page_label", "Unknown")
                            score = f"{node.score:.4f}" if node.score else "N/A"
                            
                            st.markdown(f"**Source {i+1}**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Page", page)
                            with col2:
                                st.metric("Relevance", score)
                            
                            st.markdown("**Content Preview:**")
                            st.code(node.node.get_content()[:400] + "...", language="text")
                            
                            if i < len(response.source_nodes) - 1:
                                st.markdown("---")

                    # Append assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response.response,
                        "pages": pages_str
                    })
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
                    st.info("💡 Try rephrasing your question or check if the document contains the information.")
    else:
        st.warning("⚠️ Please run `python ingest.py` first to index your documents.")
