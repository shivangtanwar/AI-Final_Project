from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from ..ga.engine import evolve, GAConfig, evolve_history, compute_metrics
from .crud import get_store


class OptimizeRequest(dict):
    pass


router = APIRouter()


@router.post("/optimize")
def optimize(req: dict = Body(...)):
    subjects, tasks, profile = get_store()
    if profile is None:
        raise HTTPException(status_code=400, detail="profile not set")
    days = int(req.get('days', 7))
    slots_per_day = int(req.get('slots_per_day', 8))
    generations = int(req.get('generations', 50))
    seed = req.get('seed', 42)
    config = GAConfig(population_size=50, generations=generations, seed=seed,
                      w_energy=float(req.get('w_energy', 1.0)),
                      w_fatigue=float(req.get('w_fatigue', 2.0)),
                      w_deadline=float(req.get('w_deadline', 0.5)),
                      w_break_penalty=float(req.get('w_break_penalty', 50.0)))
    history_mode = bool(req.get('history', False))
    locks = req.get('locks')
    if history_mode:
        schedule, hist = evolve_history(list(tasks.values()), list(subjects.values()), profile, days, slots_per_day, config, locks)
    else:
        schedule = evolve(list(tasks.values()), list(subjects.values()), profile, days, slots_per_day, config)
        hist = None
    # serialize dataclass schedule
    grid = []
    for d in range(schedule.days):
        row = []
        for s in range(schedule.slots_per_day):
            blk = schedule.grid[d][s]
            row.append(None if blk is None else blk.__dict__)
        grid.append(row)
    metrics = compute_metrics(schedule, list(subjects.values()), profile, config)
    return {"days": schedule.days, "slots_per_day": schedule.slots_per_day, "grid": grid, "history": hist, "metrics": metrics}