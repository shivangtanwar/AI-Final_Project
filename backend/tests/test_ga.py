from backend.app.ga.engine import GAConfig, evolve
from backend.app.models import Subject, Task, StudentProfile, BlockedTime


def seed_data():
    subjects = [
        Subject(id="math", name="Math", difficulty=5, focus_demand=5),
        Subject(id="cs", name="CS", difficulty=3, focus_demand=3),
    ]
    tasks = [
        Task(id="t1", title="Calculus", subject_id="math", duration_minutes=120, deadline=None, difficulty=5),
        Task(id="t2", title="Algorithms", subject_id="cs", duration_minutes=60, deadline=None, difficulty=3),
    ]
    days = 2
    slots = 6
    energy = [3,4,5,4,3,2,  2,3,4,3,2,1]
    profile = StudentProfile(id="u1", energy_curve=energy, blocked=[BlockedTime(day_index=0, start_slot=5, end_slot=6)])
    return subjects, tasks, profile, days, slots


def test_evolve_produces_schedule():
    subjects, tasks, profile, days, slots = seed_data()
    config = GAConfig(population_size=20, generations=10, seed=123)
    sched = evolve(tasks, subjects, profile, days, slots, config)
    assert sched.days == days
    assert sched.slots_per_day == slots
    # ensure no blocks in blocked slot
    assert sched.grid[0][5] is None