import pytest
from src.structured_scorer import extract_experience, check_core_ai_skills
from src.behavioral_scorer import compute_behavioral_score

def test_extract_experience():
    # Test valid extraction
    assert extract_experience("Senior AI Engineer with 5 years of experience") == 5.0
    
    # Test fallback
    assert extract_experience("Just graduated") == 0.0

def test_core_ai_skills():
    # Test exact keyword matching for AI skills
    text = "Proficient in Python, PyTorch, and deploying LLMs."
    skills = check_core_ai_skills(text)
    
    assert "pytorch" in skills
    assert "llm" in skills
    assert len(skills) >= 2

def test_response_rate_penalty():
    # Test that a 0% response rate severely penalizes the score
    cand = {'raw_data': {'redrob_signals': {'recruiter_response_rate': 0.0, 'last_active_date': '2023-01-01'}}}
    score = compute_behavioral_score(cand)
    assert score < 0.5  # Massive penalty

def test_perfect_response_rate():
    # Test that a 100% response rate maintains the score
    cand = {'raw_data': {'redrob_signals': {'recruiter_response_rate': 100.0, 'last_active_date': '2024-05-01'}}}
    score = compute_behavioral_score(cand)
    assert score > 0.5
