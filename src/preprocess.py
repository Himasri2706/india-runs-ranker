def build_candidate_text(candidate):
    """
    Builds the text representation for a candidate.
    Concatenates: headline, summary, current_title, all career_history descriptions, and all skill names.
    """
    profile = candidate.get('profile', {})
    parts = []
    
    parts.append(profile.get('headline', ''))
    parts.append(profile.get('summary', ''))
    parts.append(profile.get('current_title', ''))
    
    for job in candidate.get('career_history', []):
        if job.get('description'):
            parts.append(job['description'])
            
    for skill in candidate.get('skills', []):
        if skill.get('name'):
            parts.append(skill['name'])
            
    # Remove empty strings and join with spaces
    text = " ".join([p.strip() for p in parts if p and p.strip()])
    return text

def extract_features(candidate):
    """
    Extracts structured features needed by Layer 2 and Layer 3 scorers.
    """
    profile = candidate.get('profile', {})
    
    AI_CORE_SKILLS = {"embeddings", "vector search", "faiss", "sentence-transformers",
                      "information retrieval", "ranking systems", "recommendation", "nlp", "llm", "rag",
                      "fine-tuning", "pytorch", "python", "machine learning", "deep learning", "transformers",
                      "bert", "elasticsearch", "pinecone", "qdrant", "weaviate", "milvus", "evaluation",
                      "ndcg", "a/b testing", "search", "retrieval", "reranking"}
    
    n_ai_skills = 0
    for skill in candidate.get('skills', []):
        name = skill.get('name', '').lower()
        if name in AI_CORE_SKILLS:
            n_ai_skills += 1
            
    return {
        "candidate_id": candidate.get('candidate_id'),
        "current_title": profile.get('current_title', 'Unknown Title'),
        "years_of_experience": profile.get('years_of_experience', 0.0),
        "n_ai_skills": n_ai_skills,
        "raw_data": candidate # Keep raw data for scorers
    }
