import random
from typing import List, Optional, Tuple, Dict, Any
from ..models import Schedule, StudyBlock, Task, Subject, StudentProfile
from ..fuzzy import fatigue_risk


class GAConfig:
    def __init__(self, population_size=50, crossover_p=0.8, mutation_p=0.1, generations=50, seed: Optional[int] = None,
                 w_energy: float = 1.0, w_fatigue: float = 2.0, w_deadline: float = 0.5, w_break_penalty: float = 50.0):
        self.population_size = population_size
        self.crossover_p = crossover_p
        self.mutation_p = mutation_p
        self.generations = generations
        self.seed = seed
        self.w_energy = w_energy
        self.w_fatigue = w_fatigue
        self.w_deadline = w_deadline
        self.w_break_penalty = w_break_penalty


def build_initial_population(tasks: List[Task], subjects: List[Subject], profile: StudentProfile, days: int, slots_per_day: int, seed: Optional[int] = None, population_size: int = 50, locks: Optional[List[Dict[str, Any]]] = None) -> List[Schedule]:
    if seed is not None:
        random.seed(seed)
    population: List[Schedule] = []
    def is_break_lock(lk: Dict[str, Any]) -> bool:
        t = lk.get('type')
        if t == 'break':
            return True
        return lk.get('task_id') is None and lk.get('subject_id') is None
    for _ in range(population_size):
        grid = [[None for _ in range(slots_per_day)] for _ in range(days)]
        # apply locks first
        if locks:
            for lk in locks:
                d = int(lk.get('day', lk.get('day_index', 0)))
                s = int(lk.get('slot', lk.get('slot_index', 0)))
                if 0 <= d < days and 0 <= s < slots_per_day and not is_blocked(profile, d, s):
                    if is_break_lock(lk):
                        grid[d][s] = None
                    else:
                        grid[d][s] = StudyBlock(task_id=lk.get('task_id'), subject_id=lk.get('subject_id'), duration_slots=1, difficulty=int(lk.get('difficulty', 1)), energy_need=1)
        # simple placement honoring blocked times
        for t in tasks:
            remaining = max(1, (t.duration_minutes + 59) // 60)
            placed = False
            for d in range(days):
                for s in range(slots_per_day):
                    if is_blocked(profile, d, s) or grid[d][s] is not None:
                        continue
                    grid[d][s] = StudyBlock(task_id=t.id, subject_id=t.subject_id, duration_slots=1, difficulty=t.difficulty, energy_need=1)
                    remaining -= 1
                    if remaining == 0:
                        placed = True
                        break
                if placed:
                    break
        population.append(Schedule(days=days, slots_per_day=slots_per_day, grid=grid))
    return population


def is_blocked(profile: StudentProfile, day: int, slot: int) -> bool:
    blocked_list = profile.blocked
    for b in blocked_list:
        try:
            if isinstance(b, dict):
                di = b.get('day_index')
                start = b.get('start_slot')
                end = b.get('end_slot')
            else:
                di = b.day_index
                start = b.start_slot
                end = b.end_slot
            if di is not None and start is not None and end is not None:
                if di == day and start <= slot < end:
                    return True
        except Exception:
            continue
    return False


def fitness(schedule: Schedule, subjects: List[Subject], profile: StudentProfile, config: GAConfig | None = None) -> float:
    hard_penalty = 0
    soft_score = 0
    # check blocked times
    for d in range(schedule.days):
        for s in range(schedule.slots_per_day):
            if is_blocked(profile, d, s) and schedule.grid[d][s] is not None:
                hard_penalty += 100
    # mandatory breaks every 2 consecutive study slots
    for d in range(schedule.days):
        consecutive = 0
        for s in range(schedule.slots_per_day):
            if schedule.grid[d][s] is not None:
                consecutive += 1
                if consecutive > 2:
                    hard_penalty += (config.w_break_penalty if config else 50)
            else:
                consecutive = 0
    # soft: align difficulty with energy
    subj_map = {sub.id: sub for sub in subjects}
    for d in range(schedule.days):
        for s in range(schedule.slots_per_day):
            block = schedule.grid[d][s]
            if block and block.subject_id in subj_map:
                idx = d * schedule.slots_per_day + s
                energy = profile.energy_curve[idx] if 0 <= idx < len(profile.energy_curve) else 3
                demand = subj_map[block.subject_id].focus_demand
                soft_score += (config.w_energy if config else 1.0) * max(0, energy - demand)
                # fuzzy fatigue penalty
                soft_score -= (config.w_fatigue if config else 2.0) * fatigue_risk(s, subj_map[block.subject_id].difficulty)
                # deadline proximity bonus (sooner deadlines prefer earlier slots)
                # find the task match via task_id in block by scanning tasks is skipped; approximate via difficulty if deadline_days available
    # deadline scoring by scanning blocks with task_id and synthetic earlier-day weight
    for d in range(schedule.days):
        for s in range(schedule.slots_per_day):
            blk = schedule.grid[d][s]
            if blk and blk.task_id:
                # earlier placement gets a small bonus proportional to config.w_deadline
                soft_score += (config.w_deadline if config else 0.5) * (schedule.days - d)
    return soft_score - hard_penalty


def tournament_select(pop: List[Schedule], scores: List[float], k=3) -> Schedule:
    choices = random.sample(list(zip(pop, scores)), k)
    choices.sort(key=lambda x: x[1], reverse=True)
    return choices[0][0]


def crossover(a: Schedule, b: Schedule) -> Tuple[Schedule, Schedule]:
    point = random.randint(1, a.days - 1)
    grid1 = [row[:] for row in a.grid]
    grid2 = [row[:] for row in b.grid]
    for d in range(point, a.days):
        grid1[d], grid2[d] = grid2[d], grid1[d]
    return Schedule(days=a.days, slots_per_day=a.slots_per_day, grid=grid1), Schedule(days=b.days, slots_per_day=b.slots_per_day, grid=grid2)


def mutate(ind: Schedule, profile: StudentProfile, locks: Optional[List[Dict[str, Any]]] = None):
    d1 = random.randrange(ind.days)
    s1 = random.randrange(ind.slots_per_day)
    d2 = random.randrange(ind.days)
    s2 = random.randrange(ind.slots_per_day)
    if is_blocked(profile, d2, s2):
        return
    if locks:
        def locked_at(d, s):
            for lk in locks:
                ld = int(lk.get('day', lk.get('day_index', 0)))
                ls = int(lk.get('slot', lk.get('slot_index', 0)))
                if ld == d and ls == s:
                    return True
            return False
        if locked_at(d1, s1) or locked_at(d2, s2):
            return
    ind.grid[d1][s1], ind.grid[d2][s2] = ind.grid[d2][s2], ind.grid[d1][s1]


def evolve(tasks: List[Task], subjects: List[Subject], profile: StudentProfile, days: int, slots_per_day: int, config: GAConfig) -> Schedule:
    if config.seed is not None:
        random.seed(config.seed)
    population = build_initial_population(tasks, subjects, profile, days, slots_per_day, seed=config.seed, population_size=config.population_size)
    scores = [fitness(ind, subjects, profile, config) for ind in population]
    for _ in range(config.generations):
        new_pop: List[Schedule] = []
        # elitism
        elites = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)[:2]
        new_pop.extend([e[0] for e in elites])
        while len(new_pop) < config.population_size:
            p1 = tournament_select(population, scores)
            p2 = tournament_select(population, scores)
            c1, c2 = p1, p2
            if random.random() < config.crossover_p:
                c1, c2 = crossover(p1, p2)
            if random.random() < config.mutation_p:
                mutate(c1, profile)
            if random.random() < config.mutation_p:
                mutate(c2, profile)
            new_pop.extend([c1, c2])
            if len(new_pop) >= config.population_size:
                break
        population = new_pop[:config.population_size]
        scores = [fitness(ind, subjects, profile, config) for ind in population]
    best = max(zip(population, scores), key=lambda x: x[1])[0]
    best = repair(best, tasks, profile)
    return best


def evolve_history(tasks: List[Task], subjects: List[Subject], profile: StudentProfile, days: int, slots_per_day: int, config: GAConfig, locks: Optional[List[Dict[str, Any]]] = None) -> Tuple[Schedule, List[float]]:
    if config.seed is not None:
        random.seed(config.seed)
    population = build_initial_population(tasks, subjects, profile, days, slots_per_day, seed=config.seed, population_size=config.population_size, locks=locks)
    scores = [fitness(ind, subjects, profile, config) for ind in population]
    history: List[float] = [max(scores)]
    for _ in range(config.generations):
        new_pop: List[Schedule] = []
        elites = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)[:2]
        new_pop.extend([e[0] for e in elites])
        while len(new_pop) < config.population_size:
            p1 = tournament_select(population, scores)
            p2 = tournament_select(population, scores)
            c1, c2 = p1, p2
            if random.random() < config.crossover_p:
                c1, c2 = crossover(p1, p2)
            if random.random() < config.mutation_p:
                mutate(c1, profile, locks)
            if random.random() < config.mutation_p:
                mutate(c2, profile, locks)
            # re-apply locks to children
            if locks:
                for lk in locks:
                    d = int(lk.get('day', lk.get('day_index', 0)))
                    s = int(lk.get('slot', lk.get('slot_index', 0)))
                    if 0 <= d < days and 0 <= s < slots_per_day:
                        if lk.get('type') == 'break' or (lk.get('task_id') is None and lk.get('subject_id') is None):
                            c1.grid[d][s] = None
                            c2.grid[d][s] = None
                        else:
                            blk = StudyBlock(task_id=lk.get('task_id'), subject_id=lk.get('subject_id'), duration_slots=1, difficulty=int(lk.get('difficulty', 1)), energy_need=1)
                            c1.grid[d][s] = blk
                            c2.grid[d][s] = blk
            new_pop.extend([c1, c2])
        population = new_pop[:config.population_size]
        scores = [fitness(ind, subjects, profile, config) for ind in population]
        history.append(max(scores))
    best_idx, best_score = max(enumerate(scores), key=lambda x: x[1])
    best = population[best_idx]
    best = repair(best, tasks, profile, locks)
    return best, history


def repair(schedule: Schedule, tasks: List[Task], profile: StudentProfile, locks: Optional[List[Dict[str, Any]]] = None) -> Schedule:
    req: Dict[str, int] = {}
    for t in tasks:
        req[t.id] = max(1, (t.duration_minutes + 59) // 60)
    placed: Dict[str, int] = {tid: 0 for tid in req.keys()}
    for d in range(schedule.days):
        for s in range(schedule.slots_per_day):
            blk = schedule.grid[d][s]
            if blk and blk.task_id in placed:
                placed[blk.task_id] += 1
    def is_locked(d: int, s: int) -> bool:
        if not locks:
            return False
        for lk in locks:
            ld = int(lk.get('day', lk.get('day_index', 0)))
            ls = int(lk.get('slot', lk.get('slot_index', 0)))
            if ld == d and ls == s:
                return True
        return False
    for t in tasks:
        need = req[t.id] - placed.get(t.id, 0)
        while need > 0:
            placed_one = False
            for d in range(schedule.days):
                for s in range(schedule.slots_per_day):
                    if schedule.grid[d][s] is not None:
                        continue
                    if is_blocked(profile, d, s) or is_locked(d, s):
                        continue
                    schedule.grid[d][s] = StudyBlock(task_id=t.id, subject_id=t.subject_id, duration_slots=1, difficulty=t.difficulty, energy_need=1)
                    need -= 1
                    placed_one = True
                    break
                if placed_one:
                    break
            if not placed_one:
                break
    return schedule


def compute_metrics(schedule: Schedule, subjects: List[Subject], profile: StudentProfile, config: GAConfig | None = None) -> Dict[str, Any]:
    subj_map = {sub.id: sub for sub in subjects}
    total_slots = schedule.days * schedule.slots_per_day
    used_slots = 0
    hard_penalty = 0
    soft_score = 0.0
    blocked_conflicts = 0
    per_day: List[Dict[str, Any]] = []
    slots_details: List[List[Dict[str, Any]]] = []
    break_violations_total = 0
    for d in range(schedule.days):
        day_used = 0
        day_soft = 0.0
        day_break_violations = 0
        consecutive = 0
        row_details: List[Dict[str, Any]] = []
        for s in range(schedule.slots_per_day):
            blk = schedule.grid[d][s]
            blocked = is_blocked(profile, d, s)
            if blocked and blk is not None:
                hard_penalty += 100
                blocked_conflicts += 1
            if blk is not None:
                used_slots += 1
                day_used += 1
                consecutive += 1
                if consecutive > 2:
                    day_break_violations += 1
                    break_violations_total += 1
                    hard_penalty += (config.w_break_penalty if config else 50)
                sid = blk.subject_id
                demand = subj_map[sid].focus_demand if sid in subj_map else 3
                idx = d * schedule.slots_per_day + s
                energy = profile.energy_curve[idx] if 0 <= idx < len(profile.energy_curve) else 3
                energy_contrib = (config.w_energy if config else 1.0) * max(0, energy - demand)
                fatigue_pen = (config.w_fatigue if config else 2.0) * fatigue_risk(s, subj_map[sid].difficulty if sid in subj_map else 3)
                deadline_bonus = (config.w_deadline if config else 0.5) * (schedule.days - d) if blk.task_id else 0.0
                day_soft += energy_contrib - fatigue_pen + deadline_bonus
                soft_score += energy_contrib - fatigue_pen + deadline_bonus
                row_details.append({
                    "day": d,
                    "slot": s,
                    "subject_id": blk.subject_id,
                    "task_id": blk.task_id,
                    "energy": energy,
                    "demand": demand,
                    "fatigue": fatigue_pen,
                    "energy_contrib": energy_contrib,
                    "deadline_bonus": deadline_bonus,
                    "blocked": blocked,
                    "break_violation": consecutive > 2,
                })
            else:
                consecutive = 0
                row_details.append({
                    "day": d,
                    "slot": s,
                    "subject_id": None,
                    "task_id": None,
                    "energy": None,
                    "demand": None,
                    "fatigue": None,
                    "energy_contrib": 0.0,
                    "deadline_bonus": 0.0,
                    "blocked": blocked,
                    "break_violation": False,
                })
        per_day.append({"day": d, "used_slots": day_used, "soft": day_soft, "break_violations": day_break_violations})
        slots_details.append(row_details)
    subj_stats: Dict[str, Dict[str, Any]] = {}
    for d in range(schedule.days):
        for s in range(schedule.slots_per_day):
            blk = schedule.grid[d][s]
            if blk and blk.subject_id:
                stats = subj_stats.setdefault(blk.subject_id, {"subject_id": blk.subject_id, "slots": 0, "difficulty": subj_map.get(blk.subject_id).difficulty if blk.subject_id in subj_map else None, "focus_demand": subj_map.get(blk.subject_id).focus_demand if blk.subject_id in subj_map else None})
                stats["slots"] += 1
    subjects_metrics = list(subj_stats.values())
    energy_segment = []
    for i in range(total_slots):
        energy_segment.append(profile.energy_curve[i] if i < len(profile.energy_curve) else None)
    overall = {
        "score": soft_score - hard_penalty,
        "soft": soft_score,
        "hard": hard_penalty,
        "utilization": used_slots / float(total_slots or 1),
        "blocked_conflicts": blocked_conflicts,
        "break_violations": break_violations_total,
    }
    return {"overall": overall, "per_day": per_day, "subjects": subjects_metrics, "slots": slots_details, "energy_curve": energy_segment}