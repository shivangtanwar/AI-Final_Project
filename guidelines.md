# Project Guidelines: AI-Based Personal Study Planner
**Project Type:** End-Semester AI Project
**Core Algorithm:** Genetic Algorithm (GA)
**Theme:** AI for Human Insight and Capability Enhancement

## 1. Project Philosophy & Objective
**Goal:** Create an intelligent system that optimizes a student's study schedule to enhance learning efficiency, rather than just recording tasks.
**Core Requirement:** The system must demonstrate "Intelligent Behavior" (reasoning, planning, decision making), not just data storage or simple automation.

* **AI Component:** The Genetic Algorithm (GA) acts as the scheduling engine to solve the Constraint Satisfaction Problem (CSP) of time management.
* **Non-AI Component:** The Frontend (UI), Database, and Authentication handle the data flow and visualization.
* **Distinction:** We must strictly separate the "Intelligent Solver" from the "Application Wrapper."

---

## 2. Technical Implementation Roadmap (Marking Criteria)

The following modules are required to meet the academic evaluation standards.

### A. State Space & Representation (Requirement: Factored States)
**Concept:** We must define what a "Schedule" looks like mathematically.
* **State Representation ($S$):** The state must be **factored** (a vector or matrix), not atomic.
    * *Implementation:* A "Chromosome" in the GA.
    * *Structure:* A 2D Grid (Days x Time Slots) or a Vector of Task Objects assigned to Time Slots.
    * *Dimensions ($R^n$):* Variables include Subject ID, Difficulty Level, and Energy Requirement.
* **Action Space:** Moving a task from Slot A to Slot B; Swapping two tasks.

### B. Knowledge Representation (KR)
**Concept:** How the system understands the "Student" and the "Subjects."
* **Ontology/Semantic Data:**
    * **Subject Nodes:** define relationships (e.g., "Calculus" requires high focus).
    * **Student Profile:** define peak energy times (e.g., "User is a night owl").
* **Implementation:** A JSON-based knowledge graph or a structured database schema that stores constraints (e.g., `Math` cannot be scheduled after `Heavy Exercise`).

### C. Constraint Satisfaction Problem (CSP) Integration
**Concept:** The schedule is a CSP where we maximize utility while obeying rules.
* **Variables:** Study Blocks.
* **Domains:** Available time slots (08:00 - 22:00).
* **Constraints (The Fitness Function for GA):**
    * *Hard Constraints (Must satisfy):* No overlapping tasks; No studying during "Blocked" times (e.g., sleep).
    * *Soft Constraints (Maximize score):* High-difficulty subjects during peak energy times; Breaks inserted every 2 hours.

### D. Fuzzy Logic Layer (Optional but Recommended for Marks)
**Concept:** Handling uncertainty in user input.
* **Implementation:** Use Fuzzy Logic to calculate the "Fatigue Factor."
    * *Inputs:* `Time of Day` (Late) AND `Subject Difficulty` (Hard).
    * *Rule:* IF Time is Late AND Subject is Hard THEN Fatigue Risk is High.
    * *Output:* The GA Fitness function penalizes schedules with "High Fatigue Risk."

### E. The Search Strategy: Genetic Algorithm
**Concept:** Finding the optimal schedule in the vast search space.
* **Population:** Generate 50 random schedules.
* **Fitness Function:** `Score = (Constraints Satisfied) + (Preference Match) - (Fatigue Cost)`.
* **Selection:** Tournament selection.
* **Crossover:** Single-point crossover (swapping days between two schedules).
* **Mutation:** Randomly moving a study block to a different slot.

---

## 3. Architecture & Deliverables

### System Architecture
1.  **Perception Layer (Input):** User inputs tasks, deadlines, and "energy preferences."
2.  **State Derivation:** Convert inputs into the Initial Population (Factored State).
3.  **Reasoning Layer (The Brain):**
    * **GA Engine:** Runs the evolution (Selection -> Crossover -> Mutation) for $N$ generations.
    * **Logic Check:** Validates hard constraints.
4.  **Action/Output:** Returns the optimal schedule to the UI.

### AI vs. Non-AI Split (Required for Report)
* **AI Modules:** Genetic Algorithm logic, Fitness function calculation, Fuzzy inference system.
* **Non-AI Modules:** React/Web Frontend, User Login, CRUD operations for adding tasks, Notification system.

### Ethical Considerations
* **Burnout Prevention:** The AI must prioritize mental health (enforce breaks) rather than just maximizing work hours.

---

## 4. Development Checklist for Trae AI

- [ ] **Step 1: Data Structures.** Define the `Task`, `Slot`, and `Schedule` classes (The Genome).
- [ ] **Step 2: Fitness Function.** Write the logic to score a schedule based on the CSP constraints defined above.
- [ ] **Step 3: GA Engine.** Implement the evolution loop (Initialize -> Evaluate -> Select -> Reproduce -> Mutate).
- [ ] **Step 4: Integration.** Connect the Python/Node backend (running the GA) to a simple Frontend interface.
- [ ] **Step 5: Visualization.** Display the schedule clearly, highlighting how the AI optimized it (e.g., "Scheduled Math at 10 AM because your energy is highest").

## 5. Important Dates (Pre-Submission)
* **Target Date:** Before Oct 27-31, 2025.
* **Pre-Submission Deliverable:** Objectives defined, Flowchart of the GA, and Partial Implementation (~40% - Setup of the State Space and basic Fitness Function).

## 6. Frontend Architecture & Design Specifications
**Tech Stack:** React.js (Vite), Tailwind CSS, Recharts (for GA visualization), Framer Motion (for smooth transitions).

### A. Core Philosophy: "The Glass Box"
Unlike a standard calendar that just shows the result, this UI must operate as a "Glass Box"—showing the user *how* the AI is making decisions. [cite_start]This satisfies the requirement to "demonstrate intelligent behavior" [cite: 54] [cite_start]and "enhance human insight"[cite: 48].

### B. Page Flow & Component Breakdown

#### 1. The "Perception" Dashboard (Input Layer)
* [cite_start]**Purpose:** Captures the "Factored State" variables.
* **UI Components:**
    * **Task Input Card:** Fields for *Subject Name*, *Deadline*, *Est. Duration*.
    * **Attribute Sliders (Crucial for AI):** Instead of just time, the user sets:
        * *Difficulty Level (1-10)*
        * *Focus Required (High/Low)*
    * **User Profile Panel:**
        * *Chronotype Selector:* "Are you a Morning Lark or Night Owl?" (Defines energy peak constraints).
        * *Constraint Toggles:* "No studying on Friday nights", "Max 4 hours continuous work".

#### 2. The "Evolution" Loading Screen (State Space Visualization)
* [cite_start]**Purpose:** To visualize the "State Space Search" [cite: 16] and prove the Genetic Algorithm is running real-time.
* **Functionality:**
    * Do **not** use a simple loading spinner.
    * **Live Graph:** Show a line chart updating in real-time: `X-axis: Generation`, `Y-axis: Fitness Score`.
    * **Text Log:** "Generation 1: Clash detected... Generation 15: Optimizing for energy peaks... Generation 50: Solution Converged."

#### 3. The Intelligent Schedule View (Output Layer)
* [cite_start]**Purpose:** Displays the optimal schedule derived from the CSP[cite: 26].
* **UI Components:**
    * **The Calendar Grid:** Time blocks colored by *Subject* or *Energy Demand*.
    * [cite_start]**Break Indicators:** Visually distinct blocks labeled "AI Suggested Break" (to prevent burnout - Ethical Bonus [cite: 40]).
    * **Conflict Resolver:** If the AI couldn't satisfy all hard constraints, highlight the problem area in Red with a tooltip: "Impossible to schedule Calculus here due to overlap."

#### 4. The "Insight & Explainability" Panel (High Marking Value)
* [cite_start]**Purpose:** To satisfy the "Explainable AI" requirement[cite: 116].
* **Functionality:** When a user clicks a scheduled task (e.g., Math at 10 AM), a side panel opens:
    * **"Why this time?"**
    * *Explanation Text:* "Scheduled 'Calculus' at 10:00 AM because your profile indicates 'High Energy' in mornings, and this task is rated 'High Difficulty'."
    * *Alternative:* "Moved 'History' to evening because it requires 'Low Focus'."

#### 5. Feedback Loop (Reinforcement/Adjustment)
* [cite_start]**Purpose:** Allows the system to adapt based on user feedback.
* **UI Actions:**
    * **"Lock & Re-roll":** User can lock one specific task (making it a Hard Constraint) and click "Re-optimize" to run the GA again for the remaining slots.
    * **Rating System:** After a study session, a popup asks: "Was this time actually good for you?" (Data collected for future model tuning).

### C. Visual Design Style
* **Theme:** "Deep Focus." Dark mode options with soft accent colors (Teal for high energy, Indigo for deep work, Amber for breaks).
* **Layout:** Dashboard style. Left sidebar for inputs, Center for Calendar, Right sidebar for "AI Insights."

### D. Trae AI Development Instructions
1.  **Scaffold:** Create `components/InputForm.jsx`, `components/GeneticVisualizer.jsx`, `components/ScheduleGrid.jsx`, `components/InsightPanel.jsx`.
2.  **State Management:** Use a central Store (Context API or Zustand) to hold the `Population` and `BestSchedule` objects.
3.  **Responsiveness:** Ensure the timeline view is scrollable on smaller screens.