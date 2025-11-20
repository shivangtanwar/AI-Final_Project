from typing import Dict, List
import re
from fastapi import APIRouter, HTTPException
from ..models import Subject, Task, StudentProfile, BlockedTime


router = APIRouter()

_subjects: Dict[str, Subject] = {}
_tasks: Dict[str, Task] = {}
_profile: StudentProfile | None = None


@router.post("/subjects")
def create_subject(s: dict):
    s_obj = Subject(**s)
    _subjects[s_obj.id] = s_obj
    return s_obj.__dict__


@router.get("/subjects")
def list_subjects():
    return [v.__dict__ for v in _subjects.values()]


@router.post("/tasks")
def create_task(t: dict):
    def gen_id(title: str) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", title.strip().lower())
        base = base.strip("-") or "task"
        cand = base
        i = 2
        while cand in _tasks:
            cand = f"{base}-{i}"
            i += 1
        return cand
    payload = {k: v for k, v in t.items() if k in {"title","subject_id","duration_minutes","deadline","difficulty"}}
    tid = t.get("id") or gen_id(payload.get("title", ""))
    payload["id"] = tid
    t_obj = Task(**payload)
    if t_obj.subject_id not in _subjects:
        raise HTTPException(status_code=400, detail="subject_id not found")
    _tasks[t_obj.id] = t_obj
    return t_obj.__dict__


@router.get("/tasks")
def list_tasks():
    return [v.__dict__ for v in _tasks.values()]


@router.post("/profile")
def set_profile(p: dict):
    global _profile
    blocked = [BlockedTime(**b) for b in p.get("blocked", [])]
    _profile = StudentProfile(id=p.get("id"), energy_curve=p.get("energy_curve", []), blocked=blocked)
    return {
        "id": _profile.id,
        "energy_curve": _profile.energy_curve,
        "blocked": [
            {"day_index": b.day_index, "start_slot": b.start_slot, "end_slot": b.end_slot} for b in _profile.blocked
        ],
    }


@router.get("/profile")
def get_profile():
    if _profile is None:
        raise HTTPException(status_code=404, detail="profile not set")
    return {
        "id": _profile.id,
        "energy_curve": _profile.energy_curve,
        "blocked": [
            {"day_index": b.day_index, "start_slot": b.start_slot, "end_slot": b.end_slot} for b in _profile.blocked
        ],
    }


def get_store():
    return _subjects, _tasks, _profile