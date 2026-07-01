# India RUNS Hackathon - Presentation Deck Content

*Copy and paste the text below into your PowerPoint or Canva template. Use a sleek, dark-mode technical theme to match the project's aesthetics.*

---

## Slide 1: Title Slide
**Headline:** Beyond Keywords: A 3-Layer Hybrid AI Candidate Ranking Engine
**Sub-headline:** India RUNS Hackathon - Track 1: The Data & AI Challenge
**Name:** [Your Name / Team Name]
**Visual Idea:** A sleek tech background or a visual of a funnel filtering data points into top talent.

---

## Slide 2: The Problem with Traditional Recruiting
**Headline:** Why Keywords Are Failing Us
**Bullet Points:**
- **The Illusion of Fit:** A "Marketing Manager" who lists *Machine Learning*, *Python*, and *LLMs* easily slips past naive ATS keyword filters, wasting recruiter time.
- **Context is Ignored:** Traditional systems don't distinguish between a 2-week tutorial project and 3 years of shipping models to production.
- **The Availability Gap:** Perfect technical profiles are useless if the candidate hasn’t logged in for 6 months or never responds to recruiters.

---

## Slide 3: Our Solution Philosophy
**Headline:** Ranking Candidates Like a Technical Recruiter
**Bullet Points:**
- **Understand Context:** Use Semantic Search (Vector Embeddings) to map the *meaning* of a candidate's experience against the Job Description.
- **Enforce Strict Rules:** Apply deterministic heuristics to penalize non-engineering titles and purely consulting backgrounds, prioritizing product-company experience.
- **Measure Intent:** Factor in behavioral availability—recent activity, response rates, and GitHub presence—to ensure the candidate is actually hirable.

---

## Slide 4: The 3-Layer Hybrid Architecture
**Headline:** How The Engine Works
**Visual Idea:** Create a 3-step diagram or pyramid showing the 3 layers.
**Text:**
1. **Layer 1 (40%): Semantic Profile Vectorization**
   - We use `all-MiniLM-L6-v2` and `FAISS` to embed the candidate's entire history and compare it to the Job Description for deep contextual similarity.
2. **Layer 2 (40%): Structured Signal Scoring**
   - An aggressive rule engine that evaluates: Title relevance, verified AI skills, years of experience, and career trajectory (product vs. service firms).
3. **Layer 3 (20%): Behavioral Availability Multiplier**
   - An exponential multiplier based on platform activity. Highly inactive candidates are strictly penalized, pushing them out of the top rankings.

---

## Slide 5: Handling The "Keyword Stuffer" (Edge Case 1)
**Headline:** Defeating The Illusion
**Bullet Points:**
- **The Trap:** The dataset contains a "Marketing Manager" who lists every AI skill imaginable. 
- **Our Defense:** Layer 2 explicitly flags non-engineering titles (`Marketing`, `Accountant`, `HR`) and drastically reduces their score by assigning a heavy negative weight.
- **The Result:** The candidate drops entirely out of the Top 100, ensuring technical roles are filled by technical talent.

---

## Slide 6: Handling The "Ghost" (Edge Case 2)
**Headline:** Filtering Out Inactive Talent
**Bullet Points:**
- **The Trap:** A phenomenal "Lead ML Engineer" who hasn’t logged in since January 2023.
- **Our Defense:** Layer 3 calculates an exponential decay multiplier based on `last_active_date` and `recruiter_response_rate`.
- **The Result:** Despite a near-perfect semantic match, their multiplier (`~0.10`) pulls them completely out of the Top 10 rankings, saving recruiters from chasing ghosts.

---

## Slide 7: Built for Scale & Speed
**Headline:** High Performance & Fully Offline
**Bullet Points:**
- **100% Offline Capability:** Sentence-transformer models are downloaded and cached locally prior to execution, requiring zero network calls (No Gemini/OpenAI API dependency).
- **Memory Efficient:** Processes the 100,000 JSONL records iteratively in batches of 1,000, ensuring maximum performance on standard 16GB CPU setups.
- **Execution Time:** The entire end-to-end embedding, scoring, and ranking process completes in under 5 minutes.

---

## Slide 8: The Output
**Headline:** Clean, Actionable, Validated Results
**Bullet Points:**
- **The Format:** A strict CSV output featuring exactly 100 correctly ranked candidates.
- **AI Reasoning Strings:** Each row contains a concise, human-readable justification (e.g., *"Senior AI Engineer with 7.0 yrs; 5 AI core skills; response rate 0.95"*).
- **Validation:** 100% compliant with the official Hackathon `validate_submission.py` requirements.

---

## Slide 9: Conclusion
**Headline:** Smarter AI. Better Hiring.
**Bullet Points:**
- **Github Repo:** `github.com/Himasri2706/india-runs-ranker`
- **Dashboard Demo:** We built a custom Streamlit UI to visualize the rankings dynamically.
- **Thank You!**

*If possible, include a screenshot of the sleek Glassmorphic Streamlit UI dashboard on this final slide!*
