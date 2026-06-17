import streamlit as st
import pandas as pd
import json
import os

from src.preprocess import build_candidate_text, extract_features
from src.embedder import CandidateEmbedder
from src.ranker import rank_candidates
from rank import JD_TEXT

st.set_page_config(page_title="India RUNS AI Ranker", layout="wide")

@st.cache_resource
def load_embedder():
    embedder = CandidateEmbedder()
    return embedder

st.title("🏆 India RUNS Hackathon - AI Candidate Ranker")
st.markdown("Upload your `candidates.jsonl` file and we will rank them against the Job Description.")

# Sidebar
st.sidebar.header("Job Description")
jd_input = st.sidebar.text_area("Paste JD Here", value=JD_TEXT, height=500)

# Main Area
uploaded_file = st.file_uploader("Upload candidates JSONL", type=["jsonl", "json"])

if st.button("Rank Candidates", type="primary"):
    if uploaded_file is None:
        st.error("Please upload a candidates file.")
    else:
        with st.spinner("Initializing Model & Embedding JD..."):
            try:
                embedder = load_embedder()
                embedder.set_jd(jd_input)
            except Exception as e:
                st.error(f"Error loading model: {e}")
                st.stop()
                
        with st.spinner("Processing & Scoring Candidates..."):
            texts = []
            features_list = []
            
            # Read uploaded file
            content = uploaded_file.getvalue().decode("utf-8").splitlines()
            for line in content:
                line = line.strip()
                if not line: continue
                try:
                    cand = json.loads(line)
                    texts.append(build_candidate_text(cand))
                    features_list.append(extract_features(cand))
                except Exception as e:
                    pass
                    
            if not texts:
                st.error("No valid candidates found.")
                st.stop()
                
            # Embed and score
            sem_scores = embedder.embed_and_score_batch(texts)
            results = rank_candidates(features_list, sem_scores)
            
            # Sort
            results.sort(key=lambda x: (-x['score'], x['candidate_id']))
            
            # Display
            df = pd.DataFrame(results)
            df['rank'] = range(1, len(df) + 1)
            
            # Join with title/experience for display
            display_data = []
            for r, feat in zip(results, sorted(features_list, key=lambda f: [x for x in results if x['candidate_id'] == f['candidate_id']][0]['score'], reverse=True)):
                display_data.append({
                    "Rank": r['rank'],
                    "Candidate ID": r['candidate_id'],
                    "Score": r['score'],
                    "Current Title": feat.get('current_title', ''),
                    "Years Exp": feat.get('years_of_experience', 0),
                    "Reasoning": r['reasoning']
                })
                
            display_df = pd.DataFrame(display_data).head(20)
            
            st.success(f"Successfully ranked {len(results)} candidates!")
            
            st.subheader("Top 20 Candidates")
            st.dataframe(display_df, use_container_width=True)
            
            st.subheader("Score Distribution (Top 20)")
            st.bar_chart(display_df.set_index('Candidate ID')['Score'])
            
            # Download button
            csv = df[['candidate_id', 'rank', 'score', 'reasoning']].to_csv(index=False)
            st.download_button(
                label="Download submission.csv",
                data=csv,
                file_name="submission.csv",
                mime="text/csv",
            )
