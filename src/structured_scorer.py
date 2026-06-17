import math

def compute_structured_score(candidate, is_all_negative_titles=[False]):
    """
    Computes the Layer 2 rule-based structured score.
    Returns:
        structured_score (float, 0-1)
        is_all_negative (bool) indicating if the candidate should be heavily penalized
    """
    raw = candidate.get('raw_data', {})
    profile = raw.get('profile', {})
    career = raw.get('career_history', [])
    skills = raw.get('skills', [])
    signals = raw.get('redrob_signals', {})
    
    # A. Title & Role Fit Score (30%)
    POSITIVE_TITLES = ["ai engineer", "ml engineer", "machine learning", "data scientist",
                       "nlp engineer", "search engineer", "recommendation", "ranking", "retrieval", "applied ml",
                       "senior engineer", "staff engineer", "founding engineer"]
    NEGATIVE_TITLES = ["marketing", "accountant", "hr manager", "graphic designer",
                       "civil engineer", "mechanical engineer", "sales", "customer support", "content writer",
                       "operations manager", "business analyst", "project manager"]
    
    def score_title(title):
        t = str(title).lower()
        if any(pt in t for pt in POSITIVE_TITLES): return 1.0
        if any(nt in t for nt in NEGATIVE_TITLES): return -0.5
        return 0.0

    title_score = 0.0
    total_weight = 0.0
    all_negative = True
    has_roles = False
    
    current_title = profile.get('current_title', '')
    if current_title:
        has_roles = True
        s = score_title(current_title)
        if s > -0.5: all_negative = False
        title_score += s * 24.0 # current role weighted 2 years
        total_weight += 24.0
        
    for role in career:
        has_roles = True
        dur = max(1.0, float(role.get('duration_months', 12.0)))
        s = score_title(role.get('title', ''))
        if s > -0.5: all_negative = False
        title_score += s * dur
        total_weight += dur
        
    if total_weight > 0:
        title_score = title_score / total_weight
    else:
        title_score = 0.0
        
    # Map title_score from [-0.5, 1.0] to [0, 1] roughly
    title_score_norm = max(0.0, min(1.0, (title_score + 0.5) / 1.5))
    if not has_roles:
        all_negative = False
        
    is_all_negative_titles[0] = all_negative

    # B. Experience Fit Score (20%)
    yoe = profile.get('years_of_experience', 0.0)
    if 5 <= yoe <= 9: exp_score = 1.0
    elif 4 <= yoe <= 10: exp_score = 0.8
    elif 3 <= yoe <= 12: exp_score = 0.6
    else: exp_score = 0.3
    
    # C. Skills Quality Score (25%)
    AI_CORE_SKILLS = ["embeddings", "vector search", "faiss", "sentence-transformers",
                      "information retrieval", "ranking systems", "recommendation", "nlp", "llm", "rag",
                      "fine-tuning", "pytorch", "python", "machine learning", "deep learning", "transformers",
                      "bert", "elasticsearch", "pinecone", "qdrant", "weaviate", "milvus", "evaluation",
                      "ndcg", "a/b testing", "search", "retrieval", "reranking"]
    
    skill_score_sum = 0.0
    assessed_skills = signals.get('skill_assessment_scores', {})
    
    for skill in skills:
        name = skill.get('name', '').lower()
        if any(core in name for core in AI_CORE_SKILLS):
            # Check assessment
            matched_assess = None
            for askill, ascore in assessed_skills.items():
                if askill.lower() == name:
                    matched_assess = ascore
                    break
            
            if matched_assess is not None:
                skill_score_sum += matched_assess / 100.0
            else:
                prof = skill.get('proficiency', 'beginner').lower()
                base = {"beginner": 0.3, "intermediate": 0.6, "advanced": 0.85, "expert": 1.0}.get(prof, 0.3)
                endors = min(20, skill.get('endorsements', 0))
                dur = min(36, skill.get('duration_months', 0))
                trust = min(1.0, (endors / 20.0) * 0.5 + (dur / 36.0) * 0.5)
                skill_score_sum += base * trust
                
    skills_score = min(1.0, skill_score_sum / max(1.0, min(5.0, len(skills))))
    if skill_score_sum > 0:
        # If they have at least some good verified skills, boost the score
        skills_score = min(1.0, skill_score_sum / 3.0) 

    # D. Career Trajectory Score (15%)
    traj_score = 0.0
    IT_SERVICES = ["it services", "consulting", "outsourcing", "bpo"]
    SERVICE_FIRMS = ["tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini", "hcl", "tech mahindra"]
    
    has_product = False
    has_long_tenure = False
    all_service = True
    
    current_company = str(profile.get('current_company', '')).lower()
    current_industry = str(profile.get('current_industry', '')).lower()
    
    if current_company and not any(sf in current_company for sf in SERVICE_FIRMS) and not any(it in current_industry for it in IT_SERVICES):
        traj_score += 0.3
        
    for role in career:
        comp = str(role.get('company', '')).lower()
        ind = str(role.get('industry', '')).lower()
        size = str(role.get('company_size', ''))
        dur = float(role.get('duration_months', 0))
        
        if size in ["51-200", "201-500", "501-1000"] or (ind and not any(it in ind for it in IT_SERVICES)):
            has_product = True
        
        if dur >= 24:
            has_long_tenure = True
            
        if not any(sf in comp for sf in SERVICE_FIRMS):
            all_service = False
            
    if has_product: traj_score += 0.4
    if has_long_tenure: traj_score += 0.3
    
    traj_score = min(1.0, traj_score)
    if all_service and has_roles:
        traj_score *= 0.5
        
    # E. Location & Logistics Score (10%)
    loc_score = 0.0
    country = str(profile.get('country', '')).lower()
    loc = str(profile.get('location', '')).lower()
    
    if country in ["india", "in"]:
        if any(c in loc for c in ["pune", "noida", "delhi", "ncr", "hyderabad", "mumbai", "bangalore"]):
            loc_score = 1.0
        else:
            loc_score = 0.7
            
    if signals.get('willing_to_relocate', False):
        loc_score = min(1.0, loc_score + 0.2)
        
    np_days = int(signals.get('notice_period_days', 90))
    if np_days <= 30:
        loc_score += 0.1
    elif np_days > 90:
        loc_score -= 0.1
        
    loc_score = max(0.0, min(1.0, loc_score))
    
    final_structured = (
        title_score_norm * 0.30 +
        exp_score * 0.20 +
        skills_score * 0.25 +
        traj_score * 0.15 +
        loc_score * 0.10
    )
    
    return final_structured
