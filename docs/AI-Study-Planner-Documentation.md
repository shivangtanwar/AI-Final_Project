# AI-Based Personal Study Planner (Genetic Algorithm)

## Project Overview
- Goal: Generate balanced study schedules optimized for energy, deadlines, fatigue, mandatory breaks, and user constraints.
- Stack: FastAPI backend (`backend/app`), HTML/JS frontend (`backend/frontend`), unit tests (`backend/tests`).
- Core Engine: Genetic Algorithm (GA) evolves schedules with fitness combining hard constraints and soft preferences.

## Architecture
- Backend
  - GA engine: `backend/app/ga/engine.py` (config, population, fitness, selection, crossover, mutation, repair, metrics)
  - Routers: `backend/app/routers/{crud.py, optimize.py}`
  - Models: `backend/app/models.py`
  - Fuzzy logic: `backend/app/fuzzy.py`
  - App entry: `backend/app/main.py`
- Frontend: `backend/frontend/index.html` renders the schedule grid, controls, locks, fitness chart, metrics, and explanations.
- Dev script: `backend/scripts/dev_server.sh` installs deps and runs Uvicorn on `0.0.0.0:8000`.

## Data Model
- `Subject` and `Task`: Study metadata; tasks include `duration_minutes` and `difficulty` (models.py:14–22).
- `BlockedTime`: Hard constraints for unavailable slots (models.py:25–29).
- `StudentProfile`: Energy curve and blocked times (models.py:31–36).
- `StudyBlock`: Scheduled unit with `task_id`, `subject_id`, `duration_slots` (models.py:39–45).
- `Schedule`: Grid of `StudyBlock|None` with `days` and `slots_per_day` (models.py:47–51).

## API
- CRUD: Add/list subjects and tasks; set/get profile; in-memory store (routers/crud.py:13–69).
- Optimize: Compute schedule and return grid, fitness history, and metrics (routers/optimize.py:14–43).

## Genetic Algorithm (GA)
- Config: `GAConfig` sets `population_size`, `generations`, `crossover_p`, `mutation_p`, and weight sliders (engine.py:7–18).
- Initialization: `build_initial_population` honors blocked times and user locks (including explicit break locks) (engine.py:21–50).
- Fitness: `fitness` penalizes hard violations and scores alignment with energy, fatigue, and deadline proximity (engine.py:73–112).
- Evolution: Tournament selection, single boundary crossover by day, mutation via swaps, plus elitism (engine.py:115–176).
- Locks & Repair: `evolve_history` and `repair` re-apply locks and fill gaps while respecting constraints (engine.py:180–216, 219–256).
- Metrics: `compute_metrics` provides overall and per-slot/day stats used by frontend analysis (engine.py:219–256 and below).

## Constraints & Preferences
- Hard constraints
  - Blocked times: Scheduling into blocked slots incurs 100 penalty (engine.py:77–81).
  - Mandatory breaks: More than 2 consecutive study slots incurs break penalty weighted by `w_break_penalty` (engine.py:82–91).
- Soft preferences
  - Energy alignment: Reward when slot energy meets/exceeds subject demand (engine.py:97–101).
  - Fatigue risk: Fuzzy penalty based on slot index and subject difficulty (engine.py:101–102; fuzzy.py:1–5).
  - Deadline proximity: Small bonus for earlier placement of tasks (engine.py:109–112).

## Frontend UX Highlights
- Responsive grid with meta labels per-slot (energy/demand/fatigue) and lock visualization (frontend/index.html:140–167).
- Fitness chart and convergence indicator (frontend/index.html:360–386).
- Metrics panel with KPI cards, subject badges, per-day table, and explanation card reconciling soft/hard totals with final score (frontend/index.html:389–446).
- Drag-and-drop to pin tasks and auto-create break at source (frontend/index.html:176–203).
- Double-click to toggle break locks (frontend/index.html:345–359).
- Locks toolbar with Lock/Unlock/Clear (frontend/index.html:71–76, 319–343).
- Local caching: Restores subjects, tasks, profile, controls, locks, and last schedule (frontend/index.html:102–139, 446–452).

## Deployment & Dev
- Start dev server: `bash backend/scripts/dev_server.sh`
- Access: `http://<server>:8000/`
- Tests: `pytest -q` (backend/tests/test_ga.py validates blocked slots in schedule)

## AI Components Slide (Mandatory)

- State Space Search
  - Used: Yes, as population-based search via Genetic Algorithm, not classical BFS/DFS.
  - Atomic vs Factored: Factored. A state is a schedule grid vectorized by `(day, slot)` cells; each cell can be `None` or `StudyBlock`.
  - BFS/DFS/Greedy/A*: Not used. GA performs heuristic selection, crossover, and mutation over the factored state population.

- Constraint Satisfaction Problem (CSP)
  - Usage: Partial. We enforce constraints (blocked times, mandatory breaks) and preferences in fitness; this is akin to soft CSP.
  - Factored states: Yes. The state vector `(days × slots)` supports CSP formulation; current implementation uses GA rather than a CSP solver.

- Knowledge Base (KB)
  - Used: No formal KB. We modeled domain via dataclasses and heuristic fitness instead of symbolic KB.
  - Reason: The problem is numeric/heuristic; GA plus dataclasses is sufficient. A KB would add complexity without clear gain for schedule optimization.

- Applied ML / LLM / Computer Vision / RAG
  - Status: Not used. No supervised learning, LLM prompts, or vision tasks are required for schedule optimization here.
  - Future: A small RAG/LLM module could propose initial energy curves or study recommendations.

- Genetic Algorithm
  - Used: Yes. Population initialized from tasks; schedule state evolves via tournament selection, single-point crossover by day boundary, and mutation swaps.
  - References: `GAConfig` (engine.py:7–18), `evolve` (engine.py:150–177), `crossover` (engine.py:121–127), `mutate` (engine.py:130–147).

- Fuzzy Logic
  - Used: Yes. `fatigue_risk` provides a fuzzy penalty combining slot lateness and subject difficulty (fuzzy.py:1–5).

- AI Philosophy Linkage
  - Approach: Heuristic search over factored states, balancing hard constraints (satisfiability) with soft human-centric preferences (energy, fatigue, deadlines).
  - Trade-offs: GA provides robust global search and human-friendly tunability but no formal guarantee of optimality; constraints are encoded in fitness rather than hard pruning.

## Learnings & Improvements
- Learnings
  - Factored schedule states work well with GA’s crossover/mutation while enabling lock and break constraints.
  - A small fuzzy component improves human-aligned outcomes without complex modeling.
  - Visual analytics (metrics and score breakdown) substantially improves trust and usability.
- Improvements
  - Add a CSP repair phase that prunes break violations deterministically after GA operations.
  - Adopt SQLite persistence for subjects/tasks/profile/schedules to survive server restarts.
  - Introduce subject-level fairness objective to balance slots across days.
  - Optional: LLM-based recommendations (study plan hints) and adaptive energy curve estimation.

## File References
- GA config/engine: `backend/app/ga/engine.py:7–18`, `backend/app/ga/engine.py:73–112`, `backend/app/ga/engine.py:150–177`, `backend/app/ga/engine.py:180–216`, `backend/app/ga/engine.py:219–256`
- Models: `backend/app/models.py:14–22`, `backend/app/models.py:25–36`, `backend/app/models.py:39–51`
- Routers: `backend/app/routers/crud.py:13–69`, `backend/app/routers/optimize.py:14–43`
- Fuzzy logic: `backend/app/fuzzy.py:1–5`
- Frontend: `backend/frontend/index.html:140–203`, `backend/frontend/index.html:360–446`