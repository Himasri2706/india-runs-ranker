from datetime import datetime

def compute_behavioral_score(candidate):
    """
    Computes the Layer 3 behavioral availability multiplier.
    Returns: float (0-1)
    """
    raw = candidate.get('raw_data', {})
    signals = raw.get('redrob_signals', {})
    
    # 1. Activity Score
    last_active = signals.get('last_active_date', '2023-01-01')
    try:
        last_active_date = datetime.strptime(last_active, '%Y-%m-%d')
        # Hardcoding "today" to a reasonable date for the hackathon context
        # Or relative to the dataset max date. We'll use 2024-05-01 as "today" or use current.
        today = datetime.now()
        days_since_active = (today - last_active_date).days
    except:
        days_since_active = 200
        
    if days_since_active <= 14: activity_score = 1.0
    elif days_since_active <= 30: activity_score = 0.85
    elif days_since_active <= 60: activity_score = 0.70
    elif days_since_active <= 90: activity_score = 0.50
    elif days_since_active <= 180: activity_score = 0.30
    else: activity_score = 0.10
    
    # 2. Open to Work Bonus
    open_bonus = 0.15 if signals.get('open_to_work_flag', False) else 0.0
    
    # 3. Response Score
    response_score = float(signals.get('recruiter_response_rate', 0.0))
    avg_resp_hrs = float(signals.get('avg_response_time_hours', 100.0))
    if avg_resp_hrs > 72:
        response_score *= 0.7
    elif avg_resp_hrs > 24:
        response_score *= 0.85
        
    # 4. Interview Score
    interview_score = float(signals.get('interview_completion_rate', 0.0))
    
    # 5. GitHub Score
    gh_score_raw = signals.get('github_activity_score', -1)
    if gh_score_raw >= 0:
        github_score = gh_score_raw / 100.0
    else:
        github_score = 0.3
        
    # 6. Profile Score
    profile_score = float(signals.get('profile_completeness_score', 50)) / 100.0
    
    availability_score = (
        activity_score * 0.35 +
        response_score * 0.25 +
        interview_score * 0.15 +
        profile_score * 0.10 +
        github_score * 0.10 +
        min(1.0, open_bonus + 0.85) * 0.05
    )
    
    # Ensure between 0 and 1
    return max(0.0, min(1.0, availability_score))
