from ..models import Subject, Task, StudentProfile, BlockedTime

def demo():
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