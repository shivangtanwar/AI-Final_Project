from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Subject:
    id: str
    name: str
    difficulty: int
    focus_demand: int


@dataclass
class Task:
    id: str
    title: str
    subject_id: str
    duration_minutes: int
    deadline: Optional[str] = None
    deadline_days: Optional[int] = None
    difficulty: int = 1


@dataclass
class BlockedTime:
    day_index: int
    start_slot: int
    end_slot: int


@dataclass
class StudentProfile:
    id: str
    energy_curve: List[int]
    blocked: List[BlockedTime] = field(default_factory=list)


@dataclass
class StudyBlock:
    task_id: Optional[str] = None
    subject_id: Optional[str] = None
    duration_slots: int = 1
    difficulty: int = 1
    energy_need: int = 1


@dataclass
class Schedule:
    days: int
    slots_per_day: int
    grid: List[List[Optional[StudyBlock]]]
