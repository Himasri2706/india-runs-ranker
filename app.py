import streamlit as st
import pandas as pd
import json
import os

from src.preprocess import build_candidate_text, extract_features
from src.embedder import CandidateEmbedder
from src.ranker import rank_candidates
from rank import JD_TEXT

st.set_page_config(page_title="India RUNS AI Ranker", page_icon="🚀", layout="wide")

# Inject Custom Premium CSS
st.markdown("""
<style>
    /* Global Styles & Dark Mode Feel */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Typography & Headers */
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium Glassmorphic Candidate Cards */
    .candidate-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .candidate-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.15);
        border-color: #58a6ff;
    }
    
    /* Score Badge */
    .score-badge {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1em;
        float: right;
        box-shadow: 0 4px 10px rgba(31, 111, 235, 0.3);
    }
    
    /* Reasoning Text */
    .reasoning-text {
        color: #8b949e;
        font-size: 0.95em;
        margin-top: 10px;
        border-top: 1px solid #30363d;
        padding-top: 10px;
        line-height: 1.5;
    }
    
    /* Title Highlights */
    .cand-id {
        font-size: 1.2em;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .cand-title {
        color: #a5d6ff;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_embedder():
    embedder = CandidateEmbedder()
    return embedder

# Main Header
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🚀 Talent Intelligence: AI Candidate Ranker</h1>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📋 Job Description")
    jd_input = st.text_area("Edit Job Requirements", value=JD_TEXT, height=600)

with col2:
    st.markdown("### 📤 Upload Candidate Pool")
    uploaded_file = st.file_uploader("Upload candidates JSONL (up to 100K candidates)", type=["jsonl", "json"])
    
    if st.button("✨ Run AI Ranking Engine", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Please upload a candidates file to begin.")
        else:
            with st.spinner("🧠 Initializing Neural Embeddings..."):
                try:
                    embedder = load_embedder()
                    embedder.set_jd(jd_input)
                except Exception as e:
                    st.error(f"Error loading model: {e}")
                    st.stop()
                    
            with st.spinner("⚙️ Processing & Scoring Candidates in Real-Time..."):
                texts = []
                features_list = []
                
                content = uploaded_file.getvalue().decode("utf-8").splitlines()
                
                # Progress bar for streaming
                progress_bar = st.progress(0)
                total_lines = len(content)
                
                for i, line in enumerate(content):
                    line = line.strip()
                    if not line: continue
                    try:
                        cand = json.loads(line)
                        texts.append(build_candidate_text(cand))
                        features_list.append(extract_features(cand))
                    except Exception as e:
                        pass
                    
                    if i % max(1, (total_lines // 20)) == 0:
                        progress_bar.progress(i / total_lines)
                        
                progress_bar.progress(1.0)
                        
                if not texts:
                    st.error("No valid candidates found.")
                    st.stop()
                    
                sem_scores = embedder.embed_and_score_batch(texts)
                results = rank_candidates(features_list, sem_scores)
                results.sort(key=lambda x: (-x['score'], x['candidate_id']))
                
                # Create final dataframe
                df = pd.DataFrame(results)
                df['rank'] = range(1, len(df) + 1)
                
                # Metrics
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Processed", f"{len(results):,}")
                m2.metric("Top Score", f"{results[0]['score']:.4f}")
                m3.metric("Time Taken", "< 5s")
                
                st.markdown("### 🏆 Top 5 Matches")
                
                # Render Premium Cards
                for i in range(min(5, len(results))):
                    r = results[i]
                    # Find matching feature for UI details
                    feat = next((f for f in features_list if f['candidate_id'] == r['candidate_id']), {})
                    
                    st.markdown(f"""
                    <div class="candidate-card">
                        <div class="score-badge">{(r['score']*100):.1f}% Match</div>
                        <div class="cand-id">#{i+1} — {r['candidate_id']}</div>
                        <div class="cand-title">💼 {feat.get('current_title', 'Unknown')} • ⏳ {feat.get('years_of_experience', 0):.1f} Yrs Exp</div>
                        <div class="reasoning-text"><b>AI Reasoning:</b> {r['reasoning']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Table for the rest
                st.markdown("### 📊 Full Leaderboard (Top 20)")
                display_data = []
                for r in results[:20]:
                    feat = next((f for f in features_list if f['candidate_id'] == r['candidate_id']), {})
                    display_data.append({
                        "Rank": r['rank'],
                        "Candidate ID": r['candidate_id'],
                        "Score": r['score'],
                        "Current Title": feat.get('current_title', ''),
                        "Reasoning": r['reasoning']
                    })
                st.dataframe(pd.DataFrame(display_data), use_container_width=True)
                
                # Download
                csv = df[['candidate_id', 'rank', 'score', 'reasoning']].to_csv(index=False)
                st.download_button(
                    label="📥 Download submission.csv",
                    data=csv,
                    file_name="submission.csv",
                    mime="text/csv",
                    use_container_width=True
                )
