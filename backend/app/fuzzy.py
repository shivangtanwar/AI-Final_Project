def fatigue_risk(time_of_day: int, subject_difficulty: int) -> float:
    late = max(0.0, (time_of_day - 4) / 2.0)  # slots 5+ considered late
    hard = max(0.0, (subject_difficulty - 3) / 2.0)
    risk = min(1.0, late * hard)
    return risk