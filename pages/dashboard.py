import streamlit as st
import pandas as pd
import os
from pathlib import Path

st.set_page_config(page_title="Evaluation Dashboard", page_icon="📊", layout="wide")

st.title("📊 Evaluation Dashboard")
st.markdown("Performance metrics and benchmarking results for the Qatar Economic Analyst system.")

st.markdown("---")

# Path to benchmark results - FIXED FOR v2.0
RESULTS_FILE = "benchmark_results.csv"

# Check if results file exists
if not os.path.exists(RESULTS_FILE):
    st.warning("⚠️ No evaluation results found. Please run `python evaluate.py` first to generate benchmark data.")
    st.info("💡 This will create the `benchmark_results.csv` file with performance metrics.")
    st.stop()

# Load benchmark results
try:
    df = pd.read_csv(RESULTS_FILE)
    
    # Display key metrics
    st.header("🎯 Key Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    avg_latency = df[df["Latency (s)"] > 0]["Latency (s)"].mean()
    successful_queries = len(df[df["Latency (s)"] > 0])
    total_queries = len(df)
    success_rate = (successful_queries / total_queries) * 100 if total_queries > 0 else 0
    
    with col1:
        st.metric(
            label="Average Latency",
            value=f"{avg_latency:.2f}s",
            delta=None,
            help="Average query response time"
        )
    
    with col2:
        st.metric(
            label="Success Rate",
            value=f"{success_rate:.0f}%",
            delta=None,
            help="Percentage of successful queries"
        )
    
    with col3:
        st.metric(
            label="Total Queries",
            value=total_queries,
            delta=None,
            help="Number of benchmark queries"
        )
    
    with col4:
        st.metric(
            label="Failed Queries",
            value=total_queries - successful_queries,
            delta=None,
            help="Number of failed queries"
        )
    
    st.markdown("---")
    
    # Latency Chart
    st.header("📈 Query Performance Analysis")
    
    # Filter successful queries for chart
    chart_df = df[df["Latency (s)"] > 0].copy()
    
    if not chart_df.empty:
        # Create bar chart
        st.bar_chart(
            chart_df.set_index("Query")["Latency (s)"],
            use_container_width=True
        )
        
        st.caption("📊 Latency in seconds for each benchmark query")
    else:
        st.warning("No successful queries to display in chart.")
    
    st.markdown("---")
    
    # Detailed Results Table
    st.header("📋 Detailed Results")
    
    # Display full dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name="benchmark_results.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Performance Insights
    st.header("💡 Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Strengths")
        if success_rate >= 80:
            st.success(f"High success rate ({success_rate:.0f}%)")
        if avg_latency < 10:
            st.success(f"Fast response times ({avg_latency:.2f}s average)")
        
        # Check for page citations
        if "Pages Cited" in df.columns:
            has_citations = df["Pages Cited"].notna().sum()
            if has_citations > 0:
                st.success(f"Page citations working ({has_citations} queries with sources)")
    
    with col2:
        st.subheader("⚠️ Areas for Improvement")
        if success_rate < 80:
            st.warning(f"Success rate could be improved ({success_rate:.0f}%)")
        if avg_latency > 10:
            st.warning(f"Average latency is high ({avg_latency:.2f}s)")
        
        failed_count = total_queries - successful_queries
        if failed_count > 0:
            st.warning(f"{failed_count} queries failed - check error logs")

except Exception as e:
    st.error(f"❌ Error loading benchmark results: {e}")
    st.info("Please ensure the `benchmark_results.csv` file is properly formatted.")
