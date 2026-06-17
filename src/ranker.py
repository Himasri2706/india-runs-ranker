from .structured_scorer import compute_structured_score
from .behavioral_scorer import compute_behavioral_score

def rank_candidates(candidates_features, semantic_scores):
    """
    Computes final scores and generates reasoning strings.
    candidates_features: list of dicts from preprocess.extract_features
    semantic_scores: list of floats from FAISS similarity
    """
    results = []
    
    for feat, sem_score in zip(candidates_features, semantic_scores):
        is_all_negative = [False]
        struct_score = compute_structured_score(feat, is_all_negative)
        behav_score = compute_behavioral_score(feat)
        
        # The prompt stated Layer 3 is a MULTIPLIER, despite the formula in the prompt being additive.
        # We will calculate the additive score but apply a heavy penalty if availability is very low,
        # ensuring they drop out of the top 10.
        base_score = (sem_score * 0.40) + (struct_score * 0.40) + (behav_score * 0.20)
        
        # Apply availability as an exponential multiplier to severely punish inactive candidates
        final_score = base_score * (behav_score ** 2)
            
        # Hard cap for explicitly bad candidates
        if is_all_negative[0]:
            final_score *= 0.1
            
        # Build reasoning string
        title = feat.get('current_title', 'Unknown Title')
        yoe = feat.get('years_of_experience', 0.0)
        n_ai = feat.get('n_ai_skills', 0)
        
        raw_sigs = feat.get('raw_data', {}).get('redrob_signals', {})
        resp_rate = float(raw_sigs.get('recruiter_response_rate', 0.0))
        
        reasoning = f"{title} with {yoe:.1f} yrs; {n_ai} AI core skills; response rate {resp_rate:.2f}."
        
        results.append({
            "candidate_id": feat["candidate_id"],
            "score": round(final_score, 4),
            "reasoning": reasoning
        })
        
    return results
