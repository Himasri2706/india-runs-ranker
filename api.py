import json
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.preprocess import build_candidate_text, extract_features
from src.embedder import CandidateEmbedder
from src.ranker import rank_candidates
from src.structured_scorer import check_core_ai_skills

app = FastAPI(title="India RUNS AI Ranker API")

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
embedder = None

@app.on_event("startup")
def startup_event():
    global embedder
    print("Loading AI Model...")
    embedder = CandidateEmbedder()
    print("AI Model loaded.")

@app.post("/api/rank")
async def api_rank(
    job_description: str = Form(...),
    candidates_file: UploadFile = File(...)
):
    global embedder
    if not embedder:
        raise HTTPException(status_code=500, detail="Model not loaded yet.")

    try:
        content = await candidates_file.read()
        lines = content.decode("utf-8", errors="replace").splitlines()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    texts = []
    features_list = []
    
    embedder.set_jd(job_description)

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            cand = json.loads(line)
            texts.append(build_candidate_text(cand))
            features_list.append(extract_features(cand))
        except Exception:
            pass
            
    if not texts:
        raise HTTPException(status_code=400, detail="No valid JSON lines found in the uploaded file.")

    # Run AI engine
    sem_scores = embedder.embed_and_score_batch(texts)
    results = rank_candidates(features_list, sem_scores)
    
    # Sort and rank
    results.sort(key=lambda x: (-x['score'], x['candidate_id']))
    
    final_output = []
    for i, r in enumerate(results[:100]): # Return top 100
        feat = next((f for f in features_list if f['candidate_id'] == r['candidate_id']), {})
        raw_sigs = feat.get('raw_data', {}).get('redrob_signals', {})
        
        # XAI Extraction: get exact matched keywords
        raw_text = build_candidate_text(feat.get('raw_data', {}))
        matched_keywords = list(set(check_core_ai_skills(raw_text)))
        
        final_output.append({
            "rank": i + 1,
            "candidate_id": r['candidate_id'],
            "score": r['score'],
            "reasoning": r['reasoning'],
            "title": feat.get('current_title', 'Unknown'),
            "experience": feat.get('years_of_experience', 0),
            "response_rate": float(raw_sigs.get('recruiter_response_rate', 0)),
            "github_score": raw_sigs.get('github_activity_score', 0),
            "ai_skills": feat.get('n_ai_skills', 0),
            "extracted_keywords": matched_keywords
        })

    return {"status": "success", "results": final_output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
