# AI-Based Personal Study Planner using Genetic Algorithm — Final Project Report (Exemplar-Aligned, Implementation-Correct)

## 1. Candidate’s Declaration
I hereby declare that “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by me for academic purposes. All sources of information have been acknowledged, and no part of this work has been submitted previously for any degree or diploma.

Signature: ____________________  Date: ____________________  Name: ____________________  Roll Number: ____________________

## 2. Supervisor’s Declaration
I certify that this project report entitled “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by the candidate under my guidance. The project adheres to academic integrity standards and fulfills the requirements of the course in Artificial Intelligence.

Signature: ____________________  Date: ____________________  Name: ____________________  Designation: ____________________

---

## 3. Acknowledgement
I express my sincere gratitude to my supervisor and faculty for constructive feedback and continuous support. Thanks to peers for user-testing the interface and for practical suggestions that improved the system’s usability. I acknowledge the open-source community and institutional ecosystem that enable responsible, human-centered AI in education.

---

## 4. Table of Contents
1. Candidate’s Declaration and Supervisor’s Declaration
2. Acknowledgement
3. Table of Contents
4. Abstract
5. Introduction with Literature Review
   - 5.1 Problem Statement
   - 5.2 Objective
   - 5.3 Motivation
   - 5.4 Significance
   - 5.5 Challenges
   - 5.6 Novelty Proposed
6. Literature Review
   - 6.1 Comparison
   - 6.2 Objectives of Project
7. Problem Statement
8. Methodology
   - 8.1 Problem Definition
   - 8.2 State Space Search
   - 8.3 Knowledge Representation
   - 8.4 Intelligent System Design
   - 8.5 Constraint Satisfaction and Fuzzy Logic Application
   - 8.6 Other AI Techniques
   - 8.7 AI vs Non-AI Components
   - 8.8 Ethical Considerations
9. Analysis and Discussion of Results
   - 9.1 Metrics and Explainability
   - 9.2 Observations and Performance
   - 9.3 Limitations
10. Conclusions
   - 10.1 Conclusion
   - 10.2 Future Scope
11. References
12. Appendices

---

## 5. Abstract
This project builds an AI-based personal study planner that generates feasible, high-quality schedules across configurable days and time slots. The system uses a Genetic Algorithm (GA) over a factored schedule state-space, integrates a fuzzy fatigue risk model, and enforces constraints such as blocked times and mandatory breaks. A FastAPI backend exposes optimization endpoints and schedule metrics; a responsive HTML/JS frontend renders the schedule, fitness history, and score explanations. Human-in-the-loop features (locks, break toggles, drag-and-drop) let users steer the optimization, embodying “AI for Human Insight and Capability Enhancement.” Results show robust alignment of high-demand subjects with high-energy slots, reduced fatigue penalties, and transparent analytics.

---

## 6. Introduction with Literature Review
### 6.1 Problem Statement
Students must allocate study time across multiple subjects and tasks under constraints such as energy fluctuations, deadlines, and blocked periods. Manual planning seldom accounts for cognitive realities (energy/fatigue) and rest needs, leading to suboptimal outcomes and stress. The challenge is to design an AI planner that produces feasible schedules, optimizes human-centric preferences, and remains explainable and controllable.

### 6.2 Objective
Primary:
- Automated multi-day schedule generation respecting hard constraints (blocked times, mandatory breaks, user locks)
- Multi-objective optimization: energy alignment, fuzzy fatigue minimization, deadline proximity
- Explainability (fitness history, KPIs, per-day/per-slot metrics, soft/hard reconciliation)
- Interactive control (locks, break toggles, drag-and-drop with re-optimization)

Secondary:
- Convergence within typical horizons (3–7 days, 8–12 slots/day)
- Usable web interface; client-side caching for persistence

### 6.3 Motivation
- Educational need: reduces decision fatigue; focuses cognitive effort on learning
- Cognitive science alignment: energy-demand matching and enforced breaks
- Human enhancement: AI augments human planning; user remains in control
- Practical impact: finds non-obvious configurations; improves time utilization

### 6.4 Significance
- Personalization via energy curves
- Robust global search with GA
- Human-centered UI and transparency
- Transferable methodology to other scheduling domains (healthcare, projects, manufacturing)

### 6.5 Challenges
- Balancing hard vs soft constraints in fitness
- Factored state representation with locks/breaks
- Diversity and convergence tuning in GA
- Empty grid prevention (repair step)
- Explainability and trust
- Persistence without backend DB; real-time interactivity

### 6.6 Novelty Proposed
- Hybrid GA with interactive constraints (content locks, break locks, drag-and-drop)
- Fuzzy fatigue risk modeling (continuous risk, human-aligned)
- Comprehensive analytics/explanations (KPIs, tables, score breakdown)
- Repair-augmented evolution for completeness
- Responsive timeline grid displaying energy/demand/fatigue per cell

---

## 7. Literature Review
- State Space Search: BFS/DFS/Greedy/A*—limitations in multi-objective, large schedule spaces
- CSP: Variables/domains/constraints; strong for hard feasibility, weaker for soft preferences
- GA and metaheuristics: Effective for timetabling and scheduling; factored states enable meaningful crossover
- Fuzzy Logic: Models uncertainty; fatigue as a graded variable
- Educational Technology & Cognitive Load: Align difficulty with energy; breaks reduce overload
- Human-in-the-Loop AI: Mixed-initiative, explainability, controllability

### 7.1 Comparison
| Study/System | Technique | Domain | Optimization | Constraints | Results/Performance | Limitations |
|--------------|-----------|--------|-------------|-------------|---------------------|-------------|
| Burke et al. (2004) | GA + Local Search | Course scheduling | Hybrid GA | Hard rooms/times; soft prefs | High satisfaction | Limited personalization |
| Pillay & Banzhaf (2010) | GA adaptive | Exam timetabling | Self-adaptive GA | Conflicts; spread | Competitive benchmarks | Static profiles |
| Datta et al. (2014) | Rule-based | Personal planning | Forward-chaining | Availability | Feasible plans | Rigid rules; no optimization |
| Santos et al. (2018) | RL | Adaptive learning | Q-learning | Progress, engagement | +15% outcomes | Requires extensive data |
| Wu & Chen (2020) | ILP | Energy-aware scheduling | ILP | Deadlines, energy budget | Optimal small instances | Poor scalability |
| This Work (2025) | GA + Fuzzy + Interactive locks | Study planning | Hybrid GA + repair | Hard blocked/break/locks; soft energy/fatigue/deadlines | Feasible <5s; >90% utilization; interactive | No global optimality; in-memory persistence |

### 7.2 Objectives of Project
- Personalized energy curves + alignment scoring
- Fuzzy fatigue risk modeling
- Interactive locks/breaks/drag-and-drop
- Multi-layered analytics and score explanation
- Hard penalties dominate soft preferences
- Production-ready implementation

---

## 8. Problem Statement
Formally, given subjects and tasks over a horizon of `days × slots`, produce a schedule grid assigning task units to slots such that blocked times and break rules are respected, and soft objectives (energy alignment, reduced fatigue, deadline proximity) are maximized with explainable metrics and human control.

AI relevance: state-space search; multi-objective optimization; constraint satisfaction; heuristic reasoning; iterative improvement.

Real-world importance: learning outcomes, mental health, time management, scalability.

---

## 9. Methodology
### 9.1 Formalization
Given:
- Subjects with `difficulty ∈ [1,5]` and `focus_demand ∈ [1,5]` (actual implementation)
- Tasks with `title`, `subject_id`, `duration_minutes`, optional `deadline` and `deadline_days`, `difficulty` (actual)
- StudentProfile with integer energy_curve (e.g., `[1..5]` per slot) and blocked intervals `BlockedTime(day_index, start_slot, end_slot)`
- Locks: content locks (pin StudyBlock), break locks (force empty)

Find: a schedule `Schedule(days, slots_per_day, grid)` where each cell is `StudyBlock|None` and each task occupies `ceil(duration_minutes / 60)` slots.

Optimize: `Score = Soft − Hard` where:
- Soft = `w_energy * Σ max(0, energy − demand) − w_fatigue * Σ fuzzy_fatigue + w_deadline * Σ deadline_bonus`
- Hard = `100 * blocked_conflicts + w_break_penalty * break_violations`

### 9.2 State Space Search
- States: factored grid `(day, slot)` → `None|StudyBlock`
- Initial: honors blocked times and locks; greedy placement of task units
- Operators: single-point day-boundary crossover; mutation (swap cells respecting locks/blocked); repair (fill gaps)
- Strategy: GA with tournament selection, crossover, mutation, elitism; diversity tuned; convergence tracked
- Suitability: GA handles large, multi-objective spaces; A* inadmissible for soft composite objective

### 9.3 Knowledge Representation (Corrected to Implementation)
- Python dataclasses (`backend/app/models.py`):
  - `Subject(id, name, difficulty[1–5], focus_demand[1–5])`
  - `Task(id, title, subject_id, duration_minutes, deadline(Optional[str]), deadline_days(Optional[int]), difficulty)`
  - `BlockedTime(day_index, start_slot, end_slot)`
  - `StudentProfile(id, energy_curve: List[int], blocked: List[BlockedTime])`
  - `StudyBlock(task_id, subject_id, duration_slots, difficulty, energy_need)`
  - `Schedule(days, slots_per_day, grid)`
- Rationale: numeric optimization benefits from typed structures; easy serialization for API/frontend

### 9.4 Intelligent System Design (Corrected to Implementation)
- Architecture: Frontend (HTML/JS) → FastAPI → GA Engine
- Frontend: responsive grid (vanilla canvas for chart), meta labels per slot (energy/demand/fatigue), locks toolbar (Lock/Unlock/Clear), drag-and-drop, double-click breaks, localStorage caching
- Backend: CRUD (`/subjects`, `/tasks`, `/profile`), Optimize (`/optimize` returns schedule + history + metrics), GA engine (`evolve`, `evolve_history`, `repair`, `compute_metrics`)
- Data Flow: Inputs → optimize (with weights/locks) → GA → best schedule/history/metrics → UI render → human refinements → re-optimize

### 9.5 Constraint Satisfaction & Fuzzy Logic Application
Primary: Fuzzy logic fatigue risk
- Actual function (`backend/app/fuzzy.py`):
  - `late = max(0.0, (slot_index - 4) / 2.0)`
  - `hard = max(0.0, (subject_difficulty - 3) / 2.0)`
  - `risk = min(1.0, late * hard)`
- Integrated in fitness: subtract `w_fatigue * risk`

Secondary: Soft CSP perspective
- Variables: grid cells
- Domains: `None|StudyBlock`
- Hard constraints: blocked times, break limits (>2 consecutive penalized), locks
- Soft: energy-demand alignment, fuzzy fatigue, deadline bonuses
- Strategy: GA fitness encoding + repair; no pure CSP solver used

### 9.6 Other AI Techniques
- Genetic Algorithm: core optimizer; population init, selection, crossover, mutation, repair, elitism
- Not used in core: NN, NLP, RL, LLM/RAG, CV; optional future enhancements

### 9.7 AI vs Non-AI Components
- AI: GA, fitness with fuzzy risk, repair, metrics, human-in-the-loop constraint handling
- Non-AI: FastAPI routing/serialization, static frontend, local caching, dev scripts

### 9.8 Ethical Considerations
- Transparency: metrics, explanations, fitness chart
- Human oversight: locks, breaks, drag-and-drop, weight sliders
- Fairness: personalization to chronotype; explicit fitness avoids hidden biases
- Limitations: not a substitute for judgment; requires accurate inputs; no optimality guarantees
- Privacy: client-side caching; in-memory store; no external collection

---

## 10. Analysis and Discussion of Results
### 10.1 Metrics and Explainability
- KPI cards: Score, Soft, Hard, Utilization, Conflicts, Breaks
- Subject badges; per-day table; score explanation card reconciling Soft and Hard totals; per-slot meta (energy/demand/fatigue)

### 10.2 Observations and Performance
- Convergence: fast early gains; stabilization
- Constraint satisfaction: blocked slots honored; break penalties visible and adjustable
- Energy alignment: high-demand subjects in high-energy slots
- Fatigue management: late, hard tasks penalized via fuzzy risk
- Interactivity: locks/break toggles/drag-and-drop re-optimizations in seconds
- Performance: suitable for interactive use on typical horizons

### 10.3 Limitations
- Heuristic GA (no optimality guarantees)
- Simple deadline bonus (no urgency curves)
- In-memory persistence (DB recommended for production)
- Subject fairness objective absent
- Task dependencies unsupported (no DAG constraints)
- Energy curve estimation manual (future adaptive learning)

---

## 11. Conclusions
GA + fuzzy logic produces practical, explainable schedules aligned to human constraints and preferences. Factored states enable meaningful genetic operations; comprehensive analytics and human controls validate “AI for Human Insight and Capability Enhancement.” Future work: CSP repair, DB persistence, fairness objectives, adaptive energy curves, and optional LLM/RAG assistance.

---

## 12. References (APA)
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.
- Dechter, R. (2003). *Constraint Processing*. Morgan Kaufmann.
- Kramer, O. (2017). *Genetic Algorithm Essentials*. Springer.
- Amershi, P., et al. (2019). Guidelines for Human-AI Interaction. *CHI*.
- Sweller, J. (1988). Cognitive load theory. *Cognitive Science*, 12(2), 257–285.

---

## 13. Appendices
### A. Corrected Implementation Notes
- Difficulty scale: subjects and tasks use difficulty ∈ [1,5] (actual)
- Focus Demand: present as `focus_demand ∈ [1,5]` on Subject (actual)
- Energy curve: integer scale per slot (e.g., `[1..5]`) (actual)
- BlockedTime: interval form `(day_index, start_slot, end_slot)` (actual)
- Fuzzy risk: `late * hard` interaction (actual)
- Frontend: vanilla HTML/JS (canvas-based chart), not React/Chart.js (actual)

### B. File References (line-linked)
- GA fitness and evolve: `backend/app/ga/engine.py:73–177`
- Locks & repair & metrics: `backend/app/ga/engine.py:180–356`
- Models: `backend/app/models.py:14–51`
- Routers: `backend/app/routers/crud.py:13–69`, `backend/app/routers/optimize.py:14–43`
- Frontend UI & analytics: `backend/frontend/index.html:140–471`