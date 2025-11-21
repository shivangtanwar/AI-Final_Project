# AI-Based Personal Study Planner using Genetic Algorithm — Comprehensive Project Report

## Candidate’s Declaration
I hereby declare that “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by me for academic purposes. All sources of information have been acknowledged, and no part of this work has been submitted previously for any degree or diploma.

Name: ____________________   Roll No.: ____________________   Date: ____________________   Signature: ____________________

## Supervisor’s Declaration
I certify that this project report entitled “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by the candidate under my guidance. The project adheres to academic integrity and fulfills the requirements of the course.

Name: ____________________   Designation: ____________________   Date: ____________________   Signature: ____________________

## Acknowledgement
I thank my supervisor and faculty for sustained guidance and feedback. I appreciate peers for interface testing and constructive suggestions. I acknowledge open-source communities and libraries that enabled rapid development, and my institution for fostering responsible, human-centered AI in education.

## Table of Contents
- Abstract
- Introduction with Literature Review
- Problem Statement
- Methodology
- State Space Search
- Knowledge Representation
- Intelligent System Design
- Constraint Satisfaction Problem (or Fuzzy Logic Application)
- Additional AI Techniques
- AI vs Non-AI Components
- Analysis & Discussion of Results
- Conclusion
- References (APA)
- Appendices

## Abstract
This project builds an AI planner that generates personalized, feasible study schedules across multiple days and time slots. The core Solver is a Genetic Algorithm (GA) searching a factored schedule state-space; a fuzzy fatigue model accounts for uncertainty in human performance; constraints enforce blocked times and mandatory breaks. A FastAPI backend exposes optimization endpoints and metrics, and a responsive frontend visualizes the schedule, fitness history, and score decomposition. Human-in-the-loop features—locks, break toggles, and drag-and-drop—allow users to steer the optimization. Results demonstrate aligned energy-task allocation, reduced fatigue, and transparent, explainable outcomes.

## Introduction with Literature Review
### Context and Motivation
Students face multi-course workloads, deadlines, and varying energy levels. Manual planning often ignores rest needs and misaligns high-demand tasks with low-energy periods, causing missed targets and fatigue. AI can assist by exploring complex state spaces and balancing constraints with preferences, while keeping human agency central.

### Literature Review (conceptual summary)
- State-space search (BFS/DFS/Greedy/A*) is effective when heuristics are admissible and costs are well-structured, but complex, multi-objective schedules challenge these assumptions.
- CSP frames scheduling as variables, domains, and constraints; strong for hard feasibility, but soft preferences and continuous trade-offs benefit from optimization layers.
- GA is widely used in timetabling and scheduling due to global exploration, diversity maintenance, and tunability (Goldberg, 1989; Kramer, 2017).
- Fuzzy logic (Zadeh, 1965) models uncertainty and graded membership, useful to capture fatigue risk from late hours and task difficulty.
- Educational technology emphasizes cognitive load theory and personalization; explainability and control build trust and improve adherence.

## Problem Statement
### Definition
Create an intelligent study planner that, for a planning horizon of `days × slots`, assigns task units to time slots to maximize learning effectiveness while respecting human constraints.

### AI Relevance
The problem requires state-space search, constraint handling, heuristic scoring, and iterative improvement—core AI paradigms. GA with fuzzy logic handles large search spaces and uncertain human factors effectively.

### Real-World Importance
Better plans improve academic outcomes, reduce stress, and support sustainable study habits. Transparent AI augments human insight and capability rather than replacing judgment.

## Methodology
- Represent schedule states as a factored grid of `days × slots`; each cell holds `None` or a `StudyBlock` (models in `backend/app/models.py:39`–`backend/app/models.py:51`).
- Initialize population honoring blocked times and user locks, including explicit break locks (engine in `backend/app/ga/engine.py:19`–`backend/app/ga/engine.py:50`).
- Evaluate fitness combining:
  - Hard penalties: blocked conflicts (100 each) and break violations (>2 consecutive slots, weighted by `w_break_penalty`) (fitness in `backend/app/ga/engine.py:73`–`backend/app/ga/engine.py:112`).
  - Soft components: energy alignment, fuzzy fatigue risk (`backend/app/fuzzy.py:1`–`backend/app/fuzzy.py:5`), and simple deadline proximity bonus.
- Evolve via tournament selection, day-boundary single-point crossover, mutation swaps, and elitism (evolve in `backend/app/ga/engine.py:150`–`backend/app/ga/engine.py:177`).
- Repair schedules to fill remaining empty slots while respecting constraints and locks (repair in `backend/app/ga/engine.py:219`–`backend/app/ga/engine.py:256`).
- Compute metrics for explainability (overall KPIs, per-day summaries, per-slot contributions) (metrics in `backend/app/ga/engine.py:269`–`backend/app/ga/engine.py:356`).
- Provide UI with locks, break toggles, drag-and-drop; visualize fitness history and score explanation (frontend in `backend/frontend/index.html:360`–`backend/frontend/index.html:471`).

## State Space Search
- **States:** 2D schedule grid; each cell is `None` or `StudyBlock`. Factored representation enables meaningful crossover and mutation.
- **Initial State:** Built respecting blocked times and locks (including break locks).
- **Goal State:** High fitness (`soft − hard`), feasible schedule with human-aligned preferences.
- **Operators:** Crossover swaps trailing day segments; mutation swaps cells; repair fills gaps.
- **Search Strategy:** Genetic Algorithm (tournament selection, single-point crossover, mutation, elitism).
- **Suitability:** GA explores globally and balances diversity with convergence; classical A* is less suitable due to multi-objective soft preferences and lack of admissible heuristics.

## Knowledge Representation
- **Technique:** Typed semantic data structures via Python dataclasses (Subjects, Tasks, BlockedTimes, StudentProfile, StudyBlock, Schedule) (`backend/app/models.py`).
- **Fit:** Numeric, structured attributes (duration, difficulty, energy, slots) map naturally to dataclasses; serialization is straightforward for API/Frontend.
- **Note:** A formal symbolic KB is not required given numeric fitness and direct constraints; however, the dataclass model functions as a pragmatic domain schema.

## Intelligent System Design
- **Architecture:** Frontend (HTML/JS) → Backend (FastAPI) → GA Engine (optimization).
- **Components:** CRUD and optimize routers (`backend/app/routers/crud.py:13`–`backend/app/routers/crud.py:69`, `backend/app/routers/optimize.py:14`–`backend/app/routers/optimize.py:43`), GA engine, fuzzy module, metrics, and responsive UI.
- **Data Flow (textual):** Inputs → Initial population → GA evolution (selection, crossover, mutation) → Fitness evaluation → Best schedule + metrics → Visualization → Human refinements (locks/breaks/drag-and-drop) → Re-optimization.
- **Innovations:** Human-in-the-loop constraints; fuzzy fatigue; repair-augmented evolution; comprehensive metrics; score explanation card.

## Constraint Satisfaction Problem (or Fuzzy Logic Application)
- **Chosen:** Fuzzy Logic Application (primary), soft CSP penalty design (secondary).
- **Fuzzy Logic:** Fatigue risk inferred from time-of-day and subject difficulty; bounded in [0,1]; incorporated as a penalty scaled by `w_fatigue` (`backend/app/fuzzy.py:1`–`backend/app/fuzzy.py:5`).
- **CSP Perspective:** Variables = cells; Domains = task units or `None`; Hard constraints = blocked/locks/break; Soft = energy alignment, fatigue, deadlines; GA fitness encodes these to balance feasibility and preference.

## Additional AI Techniques
- **Genetic Algorithm:** Primary optimization technique; integrates repair and metrics; lock-aware mutation/crossover (`backend/app/ga/engine.py`).
- **Not used in core:** Neural networks, NLP, RL, LLM/CV/RAG; can be future enhancements (e.g., LLM suggestions for energy curves).

## Clear Distinction: AI vs Non-AI Components
- **AI:** GA (evolve, crossover, mutate), fitness with fuzzy risk, repair, metrics, human-in-the-loop constraint handling.
- **Non-AI:** FastAPI routing/serialization, static UI, local caching, dev scripts.

## Analysis & Discussion of Results
- **Metrics & Explainability:** KPI cards (score, soft, hard, utilization, conflicts, breaks), subject badges, per-day table; explanation card reconciles Soft and Hard contributions to the final score (`backend/frontend/index.html:389`–`backend/frontend/index.html:471`).
- **Observations:** Schedules place high-demand tasks in high-energy slots; fuzzy penalizes late difficult tasks; locks/breaks/drag re-orient schedules promptly; repair improves completeness.
- **Limitations:** GA heuristic nature; simplistic deadline bonuses; in-memory persistence; potential subject fairness concerns.

## Conclusion
GA + fuzzy logic yields practical, explainable study schedules aligning with human constraints and preferences. The factored state representation enables meaningful genetic operations. Comprehensive visualization and human-in-the-loop controls embody “AI for Human Insight and Capability Enhancement.” Future work: stronger CSP repair, database persistence, fairness objectives, and optional LLM/RAG assistance.

## References (APA)
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.
- Dechter, R. (2003). *Constraint Processing*. Morgan Kaufmann.
- Kramer, O. (2017). *Genetic Algorithm Essentials*. Springer.
- Amershi, P., et al. (2019). Guidelines for Human-AI Interaction. *CHI*. 
- Sweller, J. (1988). Cognitive load theory. *Cognitive Science*, 12(2), 257–285.

## Appendices
### A. Code References
- GA fitness: `backend/app/ga/engine.py:73`–`backend/app/ga/engine.py:112`
- GA evolve: `backend/app/ga/engine.py:150`–`backend/app/ga/engine.py:177`
- Locks in evolution: `backend/app/ga/engine.py:180`–`backend/app/ga/engine.py:216`
- Repair step: `backend/app/ga/engine.py:219`–`backend/app/ga/engine.py:256`
- Metrics compute: `backend/app/ga/engine.py:269`–`backend/app/ga/engine.py:356`
- Models: `backend/app/models.py:14`–`backend/app/models.py:51`
- Optimize endpoint: `backend/app/routers/optimize.py:14`–`backend/app/routers/optimize.py:43`
- Frontend visualization & metrics: `backend/frontend/index.html:360`–`backend/frontend/index.html:471`

### B. GA Evolution (textual pseudocode)
- Initialize population → Evaluate fitness → Select parents (tournament) → Crossover at day boundary → Mutate by swaps (respect locks/blocked) → Repair gaps → Elitism → Repeat for `generations` → Return best.

### C. Fitness Components (formalized)
- Soft = Σ(max(0, energy − demand)) − Σ(fuzzy_fatigue) + Σ(deadline_bonus)
- Hard = 100 × blocked_conflicts + `w_break_penalty` × break_violations
- Score = Soft − Hard

### D. Example Test Case
- Days = 2; Slots/day = 6; Subjects: Math (d=5), CS (d=3); Tasks: 120m Math, 60m CS; Profile: energy `[3,4,5,4,3,2, 2,3,4,3,2,1]`; Blocked slot `D0,S5` (test in `backend/tests/test_ga.py`).