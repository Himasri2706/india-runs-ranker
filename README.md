# India RUNS Hackathon - AI Candidate Ranking System

## Problem Statement
The objective is to build a high-performance offline AI candidate ranking system capable of parsing 100,000 candidate profiles against a specified AI Engineer Job Description (JD). The system must run entirely offline, fit within a 16GB CPU constraint, complete within 5 minutes, and effectively filter out keyword-stuffing candidates, non-technical candidates, and candidates lacking behavioral availability.

## Approach
Our solution employs a **3-Layer Hybrid Scoring System**:
1. **Semantic Profile Score (40%)**: We use `all-MiniLM-L6-v2` via `sentence-transformers` coupled with `FAISS` to execute fast vector similarity search between the JD and a synthesized textual representation of the candidate.
2. **Structured Signal Score (40%)**: A rule-based engine scores title relevance, experience duration, skill verification, career trajectory, and location constraints. This layer is crucial for explicitly penalizing non-engineering roles and service-company dominance, while boosting actual product-company AI experience.
3. **Behavioral Availability Multiplier (20%)**: A multiplier based on the candidate's recency of platform activity, response rates, and GitHub activity. A technically perfect candidate who hasn't logged in for 6 months will be severely down-weighted.

## Why NOT Keyword Matching
Keyword matching is easily gamed and lacks semantic understanding of a candidate's actual responsibilities. A "Marketing Manager" could list "Machine Learning" and "Python" to artificially inflate their score, despite having zero engineering capabilities. Our structured signal layer explicitly down-weights non-engineering titles and cross-references skills with verified assessments, while our semantic layer matches the *context* of the experience against the JD, effectively neutralizing keyword stuffers.

## Architecture Diagram
```
[ Candidates JSONL ] ---> (Streaming Reader, batch size 1000)
                             |
                             v
[ Preprocessor ] -------> (Text Representation & Feature Dictionary)
                             |
                             v
+-------------------------------------------------------------+
| Layer 1: FAISS Vector Embedding & Cosine Similarity         |
| Layer 2: Rule-Based Structured Scoring                      |
| Layer 3: Behavioral Availability Multiplier                 |
+-------------------------------------------------------------+
                             |
                             v
[ Ranker ] -------------> (Score Aggregation & Sorting)
                             |
                             v
[ output/submission.csv ]
```

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Pre-download the model to the local cache (requires internet, run once):
   ```bash
   python download_model.py
   ```
3. Run the ranking system (fully offline):
   ```bash
   python rank.py --candidates path/to/candidates.jsonl --out output/submission.csv
   ```
4. Validate the output:
   ```bash
   python validate_submission.py output/submission.csv
   ```

## Reproduce Command
```bash
python rank.py --candidates ./candidates.jsonl --out ./output/submission.csv
```

## Scoring Breakdown
- **Semantic Score**: 40%
- **Structured Score**: 40% (Title 30%, Experience 20%, Skills 25%, Career Trajectory 15%, Location 10%)
- **Behavioral Multiplier**: 20% (Combines Recency, Response Rate, Profile Completeness, GitHub Score, Open-to-work)

## Results
(To be updated after running on final dataset)
