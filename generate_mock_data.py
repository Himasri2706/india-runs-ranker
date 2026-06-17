import json
import random

def generate_mock_data():
    candidates = []
    
    # 1. Real ML Engineer (Should be #1)
    cand_ml = {
        "candidate_id": "CAND_0000001",
        "profile": {
            "headline": "Senior AI Engineer at TechProduct",
            "summary": "Experienced ML Engineer building scalable ranking systems and RAG architectures.",
            "current_title": "Senior AI Engineer",
            "current_company": "TechProduct Corp",
            "current_company_size": "501-1000",
            "current_industry": "Software",
            "years_of_experience": 7.0,
            "location": "Pune",
            "country": "India"
        },
        "career_history": [
            {
                "company": "TechProduct Corp",
                "title": "Senior AI Engineer",
                "start_date": "2021-01-01",
                "end_date": "Present",
                "duration_months": 36,
                "is_current": True,
                "industry": "Software",
                "company_size": "501-1000",
                "description": "Built vector search systems using sentence-transformers, FAISS, and Pinecone for product recommendations. Deployed LLMs for text retrieval."
            }
        ],
        "skills": [
            {"name": "Python", "proficiency": "expert", "endorsements": 45, "duration_months": 72},
            {"name": "Sentence-Transformers", "proficiency": "advanced", "endorsements": 20, "duration_months": 36},
            {"name": "FAISS", "proficiency": "expert", "endorsements": 30, "duration_months": 36},
            {"name": "Ranking Systems", "proficiency": "advanced", "endorsements": 25, "duration_months": 40},
            {"name": "Information Retrieval", "proficiency": "advanced", "endorsements": 25, "duration_months": 40}
        ],
        "redrob_signals": {
            "profile_completeness_score": 100,
            "last_active_date": "2024-05-01",  # Recent
            "open_to_work_flag": True,
            "recruiter_response_rate": 0.95,
            "avg_response_time_hours": 12.0,
            "notice_period_days": 30,
            "willing_to_relocate": True,
            "github_activity_score": 85,
            "interview_completion_rate": 1.0,
            "skill_assessment_scores": {"FAISS": 95, "Python": 98}
        }
    }
    candidates.append(cand_ml)

    # 2. Marketing Manager Keyword Stuffer
    cand_mkt = {
        "candidate_id": "CAND_0000002",
        "profile": {
            "headline": "Marketing Manager leveraging AI",
            "summary": "I use machine learning, python, sentence-transformers, LLM, deep learning to optimize our marketing campaigns.",
            "current_title": "Marketing Manager",
            "current_company": "Adverts Co",
            "current_company_size": "51-200",
            "current_industry": "Marketing",
            "years_of_experience": 8.0,
            "location": "Noida",
            "country": "India"
        },
        "career_history": [
            {
                "company": "Adverts Co",
                "title": "Marketing Manager",
                "start_date": "2016-01-01",
                "end_date": "Present",
                "duration_months": 96,
                "is_current": True,
                "industry": "Marketing",
                "company_size": "51-200",
                "description": "Used AI, machine learning, deep learning, NLP, sentence-transformers to target ads."
            }
        ],
        "skills": [
            {"name": "Marketing", "proficiency": "expert", "endorsements": 50, "duration_months": 96},
            {"name": "Machine Learning", "proficiency": "beginner", "endorsements": 1, "duration_months": 6},
            {"name": "Python", "proficiency": "beginner", "endorsements": 2, "duration_months": 6}
        ],
        "redrob_signals": {
            "profile_completeness_score": 100,
            "last_active_date": "2024-05-01",
            "open_to_work_flag": True,
            "recruiter_response_rate": 0.90,
            "avg_response_time_hours": 24.0,
            "notice_period_days": 30,
            "willing_to_relocate": True,
            "github_activity_score": -1,
            "interview_completion_rate": 0.8
        }
    }
    candidates.append(cand_mkt)

    # 3. Pure Consulting Profile
    cand_consult = {
        "candidate_id": "CAND_0000003",
        "profile": {
            "headline": "Data Scientist at TCS",
            "summary": "Data Scientist with experience in building ML models for various clients.",
            "current_title": "Data Scientist",
            "current_company": "TCS",
            "current_company_size": "10001+",
            "current_industry": "IT Services",
            "years_of_experience": 6.0,
            "location": "Bangalore",
            "country": "India"
        },
        "career_history": [
            {
                "company": "TCS",
                "title": "Data Scientist",
                "start_date": "2018-01-01",
                "end_date": "Present",
                "duration_months": 72,
                "is_current": True,
                "industry": "IT Services",
                "company_size": "10001+",
                "description": "Developed NLP models for client projects."
            }
        ],
        "skills": [
            {"name": "Python", "proficiency": "advanced", "endorsements": 30, "duration_months": 60},
            {"name": "NLP", "proficiency": "advanced", "endorsements": 25, "duration_months": 48}
        ],
        "redrob_signals": {
            "profile_completeness_score": 90,
            "last_active_date": "2024-05-01",
            "open_to_work_flag": True,
            "recruiter_response_rate": 0.85,
            "avg_response_time_hours": 48.0,
            "notice_period_days": 90,
            "willing_to_relocate": False,
            "github_activity_score": 40,
            "interview_completion_rate": 0.9
        }
    }
    candidates.append(cand_consult)

    # 4. Inactive Candidate (otherwise perfect)
    cand_inactive = {
        "candidate_id": "CAND_0000004",
        "profile": {
            "headline": "Lead ML Engineer",
            "summary": "Lead ML Engineer building FAISS vector search and recommendation systems.",
            "current_title": "Lead ML Engineer",
            "current_company": "StartupAI",
            "current_company_size": "51-200",
            "current_industry": "Software",
            "years_of_experience": 8.0,
            "location": "Pune",
            "country": "India"
        },
        "career_history": [
            {
                "company": "StartupAI",
                "title": "Lead ML Engineer",
                "start_date": "2016-01-01",
                "end_date": "Present",
                "duration_months": 96,
                "is_current": True,
                "industry": "Software",
                "company_size": "51-200",
                "description": "Vector search, sentence-transformers, NLP, ranking systems."
            }
        ],
        "skills": [
            {"name": "Python", "proficiency": "expert", "endorsements": 50, "duration_months": 96},
            {"name": "FAISS", "proficiency": "expert", "endorsements": 40, "duration_months": 48}
        ],
        "redrob_signals": {
            "profile_completeness_score": 95,
            "last_active_date": "2023-01-01", # Inactive for over a year
            "open_to_work_flag": False,
            "recruiter_response_rate": 0.10,
            "avg_response_time_hours": 100.0,
            "notice_period_days": 30,
            "willing_to_relocate": True,
            "github_activity_score": 90,
            "interview_completion_rate": 0.5
        }
    }
    candidates.append(cand_inactive)

    # Generate 100 more random mediocre candidates to fill out the 100 requirement for validation
    titles = ["Software Engineer", "Backend Engineer", "Data Analyst", "Frontend Developer"]
    companies = ["Infosys", "Wipro", "TechMahindra", "Accenture", "RandomStartup", "BigCorp"]
    
    for i in range(5, 120):
        cand = {
            "candidate_id": f"CAND_{i:07d}",
            "profile": {
                "headline": f"Engineer {i}",
                "summary": "Standard engineering profile.",
                "current_title": random.choice(titles),
                "current_company": random.choice(companies),
                "current_company_size": "1001-5000",
                "current_industry": "IT",
                "years_of_experience": random.uniform(2.0, 10.0),
                "location": "Hyderabad",
                "country": "India"
            },
            "career_history": [],
            "skills": [
                {"name": "Java", "proficiency": "intermediate", "endorsements": 10, "duration_months": 24}
            ],
            "redrob_signals": {
                "profile_completeness_score": 80,
                "last_active_date": "2024-04-01",
                "open_to_work_flag": True,
                "recruiter_response_rate": 0.7,
                "avg_response_time_hours": 48.0,
                "notice_period_days": 60,
                "willing_to_relocate": False,
                "github_activity_score": 50,
                "interview_completion_rate": 0.8
            }
        }
        candidates.append(cand)
        
    # Write to JSONL
    with open('candidates.jsonl', 'w', encoding='utf-8') as f:
        for c in candidates:
            f.write(json.dumps(c) + '\n')
            
    print(f"Generated {len(candidates)} mock candidates in candidates.jsonl")

if __name__ == "__main__":
    generate_mock_data()
