import streamlit as st
import pandas as pd
from src.data_streamer import load_and_stream_dataset
from src.utils import normalize_column
from src.scoring import calculate_optimized_master_score
from src.stage3_schema import generate_submission_schema

st.set_page_config(page_title="AI Matcher Engine", layout="wide")
st.title("Automated Talent Intelligence Pipeline")

uploaded_file = st.file_uploader("Upload Raw Candidate Dataset", type=["csv", "json", "jsonl"])
target_count = st.number_input("Number of top candidates to select:", min_value=1, max_value=5000, value=100)

if "last_uploaded_name" not in st.session_state or (uploaded_file and st.session_state.last_uploaded_name != uploaded_file.name):
    if uploaded_file: 
        st.session_state.last_uploaded_name = uploaded_file.name
    st.session_state.df_submission = None

if uploaded_file is not None:
    if st.button("Execute Matcher Pipeline"):
        with st.spinner("Streaming data streams and executing multi-stage filters..."):
            try:
                # 1. Modular Data Streaming Ingestion
                df_raw = load_and_stream_dataset(uploaded_file, uploaded_file.name)
                
                # 2. Vectorized Column Base Normalization
                df_raw['profile'] = normalize_column(df_raw['profile'], dict)
                df_raw['career_history'] = normalize_column(df_raw['career_history'], list)
                df_raw['skills'] = normalize_column(df_raw['skills'], list)
                df_raw['redrob_signals'] = normalize_column(df_raw['redrob_signals'], dict)

                # 3. Progressive Score Matrix Evaluation
                df_raw['final_weighted_score'] = df_raw.apply(calculate_optimized_master_score, axis=1)
                df_filtered = df_raw[df_raw['final_weighted_score'] > 0].copy()
                
                if df_filtered.empty:
                    st.warning("All records filtered out based on hard logistical gates.")
                else:
                    df_top = df_filtered.nlargest(target_count, 'final_weighted_score').copy()
                    df_top = df_top.sort_values(by='final_weighted_score', ascending=False).reset_index(drop=True)
                    
                    # 4. Modular Schema Translation Formatting
                    st.session_state.df_submission = generate_submission_schema(df_top)
            except Exception as e:
                st.error(f"Pipeline Runtime Error: {str(e)}")

    if st.session_state.df_submission is not None:
        st.success(f"Pipeline complete. Formatted top {len(st.session_state.df_submission)} candidates.")
        st.dataframe(st.session_state.df_submission, use_container_width=True)
        
        csv_output = st.session_state.df_submission.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Format-Compliant CSV",
            data=csv_output,
            file_name="final_submission.csv",
            mime="text/csv"
        )