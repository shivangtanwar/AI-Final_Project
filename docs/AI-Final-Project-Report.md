# AI-Based Personal Study Planner using Genetic Algorithm — Final Project Report

## Candidate’s Declaration
I hereby declare that “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by me for academic purposes. All sources of information have been acknowledged, and no part of this work has been submitted previously for any degree or diploma.

## Supervisor’s Declaration
I certify that this project report entitled “AI-Based Personal Study Planner using Genetic Algorithm” is an original work carried out by the candidate under my guidance. The project adheres to academic integrity and fulfills the requirements of the course.

## Acknowledgement
I express gratitude to my supervisor and faculty for guidance and feedback. Thanks to peers for user-testing the interface and to open-source contributors whose libraries and references informed this work. Special acknowledgement to the academic ecosystem fostering responsible AI for education and to communities advancing accessible AI practices.

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

## Abstract
This project designs and implements an AI-based personal study planner that produces feasible, high-quality schedules for students across multiple days and time slots. The system uses a Genetic Algorithm (GA) to search a factored schedule state-space, a fuzzy fatigue model to incorporate human-centric uncertainty, and configurable constraints such as blocked times and mandatory breaks. The FastAPI backend exposes optimization endpoints and metrics; a responsive frontend visualizes the schedule, fitness history, and score decomposition. Interactivity (locks, break toggling, drag-and-drop) lets human users guide optimization, ensuring “AI for Human Insight and Capability Enhancement.” Results show robust scheduling aligned to energy curves, reduced fatigue, and clear explainability.

## Introduction with Literature Review
Intelligent scheduling is a classic AI problem involving search, optimization, and constraint handling. Early work on state-space search introduced systematic strategies (BFS/DFS/Greedy/A*) for discrete, well-structured problems with admissible heuristics. Constraint Satisfaction Problems (CSPs) cast scheduling as variable–domain–constraint frameworks supporting backtracking and propagation. Metaheuristics—particularly Genetic Algorithms—are effective when the state space is large, objective factors interact nonlinearly, and global exploration is required. Fuzzy logic contributes to human-aligned scoring by modeling uncertainty (e.g., fatigue rising later in the day, amplified by subject difficulty). In education technology, aligning study workloads with energy cycles and enforcing rest periods aligns with cognitive load theory, demonstrating how AI can amplify human capability. 

In this work, GA (population-based search) is paired with soft CSP-like fitness design and fuzzy penalties, aligning algorithmic efficiency with human-centered preferences. The architecture adapts modern web stacks (FastAPI + HTML/JS) to provide explainability through metrics and per-slot insights. This balance of search, constraints, and human-in-the-loop controls situates the planner within the broader literature on hybrid AI systems for decision support in education.

## Problem Statement
Students must allocate study time across subjects with varying difficulty and deadlines while respecting personal energy levels and non-study commitments (blocked times). Manual planning tends to ignore rest needs and misalign demanding tasks with low-energy periods, leading to fatigue, missed deadlines, and suboptimal performance. We seek an AI planner that:
- Generates a feasible multi-day schedule that respects blocked times and mandatory breaks.
- Optimizes alignment with energy curves, reduces fatigue, and nudges deadlines earlier.
- Provides explanations and interactive control for human oversight.

Relevance to AI: The problem involves state-space exploration, constraint handling, heuristic scoring, and iterative improvement—core AI paradigms. GA with fuzzy logic provides a robust combination for uncertain human preferences and large search spaces. 

Real-world importance: Study planning affects academic outcomes, stress management, and sustainability of effort. An AI that offloads planning while preserving human control supports better learning and well-being. 

Clarity and feasibility: We define states, operators, objective, and constraints; we implement an end-to-end system with measurable outputs (fitness, metrics), user controls, and verified behaviors.

## Methodology
- Represent schedule states as a factored grid of `days × slots_per_day`, where each cell holds a `StudyBlock` (task + subject) or `None`.
- Initialize a population honoring blocked times and user-specified locks/breaks.
- Evaluate fitness combining:
  - Hard penalties: blocked time violations (100 per violation) and break violations (weighted by `w_break_penalty`).
  - Soft components: energy alignment with subject demand; fuzzy fatigue risk; small bonus for earlier task placement relative to deadlines.
- Evolve population via tournament selection (k=3), single-point crossover at day boundaries, mutation swaps, and elitism.
- Apply a repair step to fill remaining slots respecting constraints and locks.
- Compute metrics for explainability (overall KPIs, per-day summaries, per-slot contributions).
- Provide a frontend for visualization and interactivity (locks, breaks, drag-and-drop), with local caching for persistence.

Conceptual data-flow diagram (textual):
1) Inputs (subjects, tasks, profile) → stored via CRUD → 2) Optimize (GA config, locks) → 3) GA evolve → 4) Schedule + history + metrics → 5) Frontend visualization (grid, chart, metrics) → 6) User refinements (locks, breaks, drag-and-drop) → 7) Re-optimize.

## State Space Search
- States: A schedule represented as a grid over `(day, slot)` cells; each cell is `None` or a `StudyBlock(task_id, subject_id, ...)`.
- Initial State: Generated via `build_initial_population`, respecting blocked times and user locks; tasks are placed greedily where possible.
- Goal State: A high-scoring, feasible schedule maximizing `soft − hard` fitness.
- Operators / Actions: 
  - Crossover: exchange trailing day segments between two states.
  - Mutation: swap two randomly chosen cells if not blocked/locked.
  - Repair: fill remaining empty cells with remaining task units.
- Search Strategy: Genetic Algorithm with tournament selection, single-point crossover, mutation, and elitism.
- Suitability: GA balances global exploration and local refinement in large, mixed-objective spaces. A* is less natural due to composite heuristics without admissibility; GA is practical and tunable for human-centric scheduling.

## Knowledge Representation
- Technique: Typed semantic data structures via Python dataclasses rather than a formal symbolic KB. Domain entities—`Subject`, `Task`, `BlockedTime`, `StudentProfile`, `StudyBlock`, `Schedule`—encapsulate structure and attributes.
- Fit: Numeric attributes (duration, difficulty, energy, slots) map naturally to records and integrate seamlessly with serialization and endpoints. The numeric/heuristic nature of the fitness obviated a formal rule-based KB.
- Implementation: Dataclasses in `backend/app/models.py` are consumed by GA, routers, and frontend, enabling consistent IO across system components.

## Intelligent System Design
- Architecture: 
  - Backend (FastAPI) exposes CRUD and optimize endpoints; GA engine performs schedule evolution; metrics increase transparency.
  - Frontend (HTML/JS) renders grid, chart, metrics, and explanations; supports locks/breaks/drag-and-drop; persists state client-side.
- Components: GAConfig, evolve, fitness, build_initial_population, crossover, mutate, repair, compute_metrics; routers for CRUD/optimize; UI for visualization and control.
- Data flow: As described in Methodology; iterative human-in-the-loop optimization.
- Innovative Aspects: Interactive constraints (content locks, break locks, drag-and-drop repositions) tightly integrated with GA; fuzzy fatigue risk; explanation card reconciling soft/hard totals with final score.

## Constraint Satisfaction Problem (or Fuzzy Logic Application)
- Chosen: Fuzzy Logic Application (primary), soft CSP-like penalties (secondary).
- Fuzzy Logic:
  - Fuzzy sets/proxy: Risk increases with slot lateness and subject difficulty; bounded in [0,1].
  - Rules/inference: Penalize schedules with higher fuzzy risk scaled by `w_fatigue`.
  - Uncertainty handling: Captures human fatigue uncertainty; complements energy alignment.
- CSP Viewpoint:
  - Variables: Each `(day, slot)` cell.
  - Domains: `None` or assignment of a task unit.
  - Constraints: Blocked times (hard), break limits (hard), locks (hard), energy/demand matching (soft).
  - Solving: Implemented via GA fitness rather than pure CSP solver for flexibility and tunability.

## Additional AI Techniques
- Genetic Algorithm: Primary technique; population-based search with crossover, mutation, selection, and elitism; combined with a repair step.
- Not used: Neural networks, NLP, RL, LLM/CV/RAG in core implementation. Future optional: LLM/RAG to suggest energy curves or study strategies.

## Clear Distinction between AI and Non-AI Components
- AI Components: GA evolve (`evolve`, `crossover`, `mutate`), fitness with fuzzy risk, repair step, metrics computation, human-in-the-loop constraints integrated in optimization.
- Non-AI Components: FastAPI routing and serialization, static frontend rendering and interaction handlers, local caching, dev server scripts.

## Analysis & Discussion of Results
- Metrics & Explainability: KPIs (score, soft, hard, utilization, conflicts, breaks), subject badges, per-day table; explanation card shows Soft and Hard totals and reconciles final score.
- Observations: 
  - Schedules tend to place high-demand tasks at high-energy slots; fuzzy fatigue discourages late hard tasks.
  - Drag-and-drop plus locks/breaks immediately re-orients the schedule, demonstrating robust human-in-the-loop control.
  - Repair step improves schedule completeness; metrics foster trust.
- Limitations:
  - GA optimizes heuristically without optimality guarantees; performance depends on configuration.
  - Deadline handling is heuristic; richer deadline modeling (e.g., task urgency profiles) could improve ordering.
  - In-memory persistence requires local caching or a database for durability.

## Conclusion
The system demonstrates how GA and fuzzy logic can produce practical, explainable study schedules that respect human constraints and preferences. The factored schedule state-space supports meaningful crossover/mutation, while fitness components reflect energy, fatigue, and deadlines. Interactivity ensures “AI for Human Insight and Capability Enhancement,” placing humans in control of final plans. Future work will integrate stronger CSP repair, database persistence, subject-level fairness objectives, and optional LLM recommendations.

## References (APA style)
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338–353.
- Dechter, R. (2003). *Constraint Processing*. Morgan Kaufmann.
- Kramer, O. (2017). *Genetic Algorithm Essentials*. Springer.

---

## PROJECT REQUIREMENT DETAILS (Coverage Summary)

### 1. Problem Statement (3 marks)
- Defined clearly with AI relevance and real-world importance; feasibility explained.

### 2. State Space Search (3 marks)
- States, initial/goal states, operators/actions, strategy (GA), and suitability justification included.

### 3. Knowledge Representation (3 marks)
- Dataclass-based semantic structures; rationale and implementation described.

### 4. Intelligent System Design (3 marks)
- Architecture, components, data flow (conceptual), innovative aspects covered.

### 5. CSP or Fuzzy Logic (3 marks)
- Fuzzy logic chosen; sets/rules/inference/uncertainty handling explained; soft CSP penalties noted.

### 6. Other AI Techniques (2 marks)
- GA integrated; other techniques noted as not applicable in core but possible future work.

### Bonus Points
- Originality: Hybrid GA + interactive locks/breaks; explanation card linking metrics to outcome.
- Ethical considerations: Transparency (metrics/explanations), human oversight/control; notes on fairness.

### Important Notes
- Clear AI vs non-AI distinction provided.
- Methodology steps not applicable (NN, RL, NLP) explicitly noted.
- “AI for Human Insight and Capability Enhancement” emphasized; benefits to learners explained.
- Domain relevance: Education; applicable patterns extend to healthcare, finance, creative workflows, social systems, and games with scheduled activities.