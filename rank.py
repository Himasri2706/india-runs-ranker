import argparse
import json
import pandas as pd
from tqdm import tqdm
import os

from src.preprocess import build_candidate_text, extract_features
from src.embedder import CandidateEmbedder
from src.ranker import rank_candidates

JD_TEXT = """
Role: Senior AI Engineer — Founding Team
Company: Redrob AI (Series A, AI-native talent intelligence platform)
Location: Pune/Noida, India (Hybrid) — relocation candidates from Tier-1 Indian cities welcome
Experience: 5–9 years

MUST HAVE (hard requirements):
- Production experience with embeddings-based retrieval systems (sentence-transformers, BGE, E5, OpenAI embeddings, or similar) deployed to real users — not just tutorials or demos
- Production experience with vector databases or hybrid search infrastructure (Pinecone, Weaviate, Qdrant, Milvus, FAISS, Elasticsearch, OpenSearch, or similar)
- Strong Python (code quality matters)
- Hands-on experience designing evaluation frameworks for ranking systems (NDCG, MRR, MAP, A/B testing, offline-to-online correlation)

PREFERRED (nice to have):
- LLM fine-tuning experience (LoRA, QLoRA, PEFT)
- Learning-to-rank models (XGBoost-based or neural)
- Prior exposure to HR-tech, recruiting tech, or marketplace products
- Background in distributed systems or large-scale inference optimization
- Open-source contributions in the AI/ML space

EXPLICIT DISQUALIFIERS (must rank these candidates LOW regardless of AI keywords):
- Career spent entirely in pure research environments (academic labs, no production deployment)
- "AI experience" that is only recent (<12 months) LangChain/OpenAI tutorial projects
- Entire career at IT services/consulting firms (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, etc.) — if all jobs are at these firms, rank lower
- Primary expertise in computer vision, speech, or robotics without NLP/IR exposure
- Titles that are non-engineering (Marketing Manager, Accountant, HR Manager, Graphic Designer, Civil Engineer, etc.) cannot be top candidates no matter their listed skills

IDEAL CANDIDATE PROFILE:
- 6–8 years total, of which 4–5 are applied ML/AI roles at PRODUCT companies (not services)
- Has shipped at least one end-to-end ranking, search, or recommendation system to real users
- Located in or willing to relocate to Noida/Pune (India preferred)
- Active on the platform (recently logged in, responds to recruiters)
- Notice period under 30 days preferred (can buy out up to 30 days)
"""

def main():
    parser = argparse.ArgumentParser(description="AI Candidate Ranking System")
    parser.add_argument("--candidates", required=True, help="Path to candidates.jsonl")
    parser.add_argument("--out", required=True, help="Path to output submission.csv")
    args = parser.parse_args()

    # Create output dir if not exists
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    print("Initializing offline embedding model...")
    embedder = CandidateEmbedder()
    embedder.set_jd(JD_TEXT)
    
    all_scored_candidates = []
    
    batch_size = 1000
    current_batch_texts = []
    current_batch_features = []
    
    print("Processing candidates stream...")
    with open(args.candidates, 'r', encoding='utf-8', errors='replace') as f:
        for line in tqdm(f, desc="Reading candidates"):
            line = line.strip()
            if not line: continue
            
            try:
                candidate = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            text = build_candidate_text(candidate)
            features = extract_features(candidate)
            
            current_batch_texts.append(text)
            current_batch_features.append(features)
            
            if len(current_batch_texts) >= batch_size:
                # Process batch
                sem_scores = embedder.embed_and_score_batch(current_batch_texts)
                batch_results = rank_candidates(current_batch_features, sem_scores)
                all_scored_candidates.extend(batch_results)
                
                # Reset batch
                current_batch_texts = []
                current_batch_features = []
                
        # Process final batch
        if current_batch_texts:
            sem_scores = embedder.embed_and_score_batch(current_batch_texts)
            batch_results = rank_candidates(current_batch_features, sem_scores)
            all_scored_candidates.extend(batch_results)
            
    print(f"Scored {len(all_scored_candidates)} candidates. Sorting and selecting top 100...")
    
    # Sort by score descending, then by candidate_id ascending for tie-breaks
    all_scored_candidates.sort(key=lambda x: (-x['score'], x['candidate_id']))
    
    top_100 = all_scored_candidates[:100]
    
    # Write CSV
    print(f"Writing output to {args.out}...")
    
    rows = []
    for i, c in enumerate(top_100):
        rows.append({
            "candidate_id": c["candidate_id"],
            "rank": i + 1,
            "score": c["score"],
            "reasoning": c["reasoning"]
        })
        
    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False, encoding='utf-8')
    
    print("Done. Automatically validating submission...")
    os.system(f"python validate_submission.py {args.out}")

if __name__ == "__main__":
    main()
