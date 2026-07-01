# 🚀 India RUNS AI Ranker (Talent Intelligence AI)

> **Hack2Skill x Redrob AI - The Data & AI Challenge**

An enterprise-grade, 100% offline Candidate Ranking Engine built with a **Two-Tower Dense + Sparse Hybrid Search Architecture**.

![Talent AI Architecture](https://img.shields.io/badge/Architecture-Full_Stack-indigo.svg)
![Offline Compliant](https://img.shields.io/badge/Offline_Compliant-100%25-green.svg)
![AI Engine](https://img.shields.io/badge/AI_Engine-Hybrid_Search-fuchsia.svg)

## 🌟 Key Features

### 1. Hybrid Search (Dense + Sparse)
To solve the classic "Vocabulary Mismatch" problem in Vector Search, this engine uses a Two-Tower Retrieval system:
* **70% Dense Scoring (Semantic):** Uses `all-MiniLM-L6-v2` via `sentence-transformers` to deeply understand the semantic meaning of the candidate's career history and the Job Description.
* **30% Sparse Scoring (Lexical):** Uses `TfidfVectorizer` to do exact keyword matching on the fly, ensuring specific requirements (e.g., "PyTorch") aren't missed.

### 2. Multi-Layer Ranking Algorithm
* **Layer 1 (Hybrid Semantic Search):** Scores the candidate against the Job Description.
* **Layer 2 (Structured Feature Extraction):** Evaluates Years of Experience and presence of core AI Skills.
* **Layer 3 (Behavioral Signals):** Analyzes Redrob metrics (Response Rate, GitHub activity) and severely penalizes inactive/unresponsive candidates.

### 3. Ultra-Premium Full-Stack UI
* **Backend:** Blazing fast **FastAPI** REST API.
* **Frontend:** Modern **React + Vite** SPA.
* **Aesthetics:** Stunning glassmorphic design built with **Tailwind CSS v4** and animated with **Framer Motion**.
* **Analytics:** Beautiful data visualizations (Score Distributions, Experience vs. Match Scatter plots) powered by **Recharts**.

## 🎨 UI Showcase
*(Drag and drop a screenshot of the React Dashboard here before submitting!)*
<p align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Replace+with+Screenshot+of+your+beautiful+React+App" alt="Dashboard UI Screenshot" width="800"/>
</p>

### 4. 100% Offline Compliance
Strictly adheres to Hackathon Rules: Zero network API calls to OpenAI/Gemini during execution. The sentence-transformer model is cached locally.

## 🛠️ How to Run Locally

### Prerequisites
* Python 3.10+
* Node.js v20+

### 1. Download AI Models (One-time setup)
Before running, you must download the local AI weights to the `cache/` folder:
```bash
python download_model.py
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 4. Launch Full Stack (Windows)
We have provided a convenient launcher script that starts both the FastAPI backend and the Vite frontend simultaneously:
```bash
start-fullstack.bat
```

Alternatively, run them separately:
* **Backend:** `python api.py` (Runs on port 8000)
* **Frontend:** `cd frontend && npm run dev` (Runs on port 5173)

## 📦 Project Structure
```
├── src/
│   ├── embedder.py          # Hybrid Search Logic (SentenceTransformers + TF-IDF)
│   ├── ranker.py            # The 3-Layer Scoring Equation & Reasoning Engine
│   ├── preprocess.py        # Text & Feature extraction from JSONL
│   ├── structured_scorer.py # Layer 2 Scoring
│   └── behavioral_scorer.py # Layer 3 Scoring
├── frontend/                # React + Vite Web Application
│   ├── src/App.jsx          # Main UI, Analytics Dashboard, and Leaderboard
│   └── tailwind.config.js
├── api.py                   # FastAPI Server wrapper for the AI Engine
├── rank.py                  # CLI Orchestrator (For strict Hackathon validation)
├── download_model.py        # Caches huggingface models offline
└── start-fullstack.bat      # 1-Click Launchpad
```

## 📋 Hackathon Validation
To validate against the strict Hackathon format (without the UI):
```bash
python rank.py --candidates <path_to_jsonl> --job_description <path_to_txt> --output submission.csv
```
This guarantees the exact required `submission.csv` format for `validate_submission.py`.
