# AI-Based Personal Study Planner — Project Report

## Introduction
This project builds an end‑to‑end AI system that helps students generate effective, personalized study schedules. It combines Genetic Algorithms for global search, fuzzy logic for human‑centric fatigue modeling, and interactive controls (locks, breaks, drag‑and‑drop) to refine solutions. A FastAPI backend provides optimization endpoints and metrics, while a responsive frontend visualizes schedules, fitness, and score explanations.

## 1.1. Problem Statement
Students often struggle to plan study time across multiple subjects with varying difficulties, deadlines, and personal energy constraints. Manual planning rarely accounts for blocked times and rest needs, causing fatigue, missed deadlines, and suboptimal learning outcomes. We need a planner that automatically creates balanced schedules, respects constraints, and adapts to user feedback.

## 1.2. Objective
Design and implement an AI planner that:
- Produces a feasible multi‑day schedule across `days × slots`.
- Respects hard constraints (blocked times, mandatory breaks).
- Optimizes soft objectives (energy alignment, reduced fatigue, deadline proximity).
- Provides explainability (fitness history, metrics, soft vs. hard breakdown).
- Supports interactive adjustments (locks, breaks, drag‑and‑drop) that re‑optimize.

## 1.3. Motivation
A personalized planner reduces decision fatigue and improves focus by aligning study blocks to times of high energy and enforcing sustainable breaks. For academic courses with diverse workloads and deadlines, optimization frees time, improves consistency, and supports better outcomes.

## 1.4. Significance
- Personalization: Integrates an energy curve per student to schedule higher‑demand tasks at peak times.
- Robustness: Uses GA to search globally over factored schedule states and recover from local minima via mutation/crossover.
- Usability: Provides metrics, visual explanations, and interactive controls that make AI decisions transparent and easy to refine.

## 1.5. Challenges
- Balancing constraints: Combining hard constraints (blocked times, breaks) with soft preferences (energy, deadlines) without violating feasibility.
- Representation: Modeling the schedule as a factored state vector over `(day, slot)`, supporting locks and break toggles.
- Convergence and diversity: Maintaining GA diversity while converging to high‑quality schedules; avoiding empty grids via repair steps.
- Explainability: Summarizing fitness into understandable KPIs and soft/hard decompositions tied to the visible schedule.
- Persistence: Preserving user inputs and the latest schedule across refreshes with lightweight caching.

## 1.6. Novelty Proposed
- Hybrid GA with interactive constraints:
  - Content locks pin blocks; break locks reserve empty slots; drag‑and‑drop repositions tasks and triggers re‑optimization.
  - A repair step fills remaining slots while respecting locks and blocked times.
- Human‑centric scoring:
  - Fuzzy fatigue combines slot lateness with subject difficulty.
  - Energy alignment and deadline proximity contribute to soft score; break violations and blocked conflicts accumulate hard penalties.
- Analytics and explainability:
  - Fitness history with convergence signal, KPI cards, subject badges, per‑day table.
  - A score explanation card reconciling soft and hard components to the reported score.
- Practical UX:
  - Responsive, scrollable timeline grid; local caching of subjects/tasks/profile/controls/schedule; fast re‑runs with updated locks/breaks.