"""Explainable finite-horizon planning in the synthetic combat environment."""
from .engine import Action, State, step

def legal(s):
    if s.hp <= 0 or s.enemy <= 0:
        return ()
    return tuple(a for a in Action if a != Action.HEAL or s.potions > 0)

def value(s, style):
    if s.hp <= 0:
        return -1000.0
    if s.enemy <= 0:
        return 500.0 + s.hp + 5*s.potions
    health_weight = {"careful": 2.0, "balanced": 1.0, "aggressive": 0.5}[style]
    return health_weight*s.hp - 2*s.enemy + 8*s.potions

def plan(s: State, style="balanced", depth=4):
    if style not in ("careful", "balanced", "aggressive") or not 1 <= depth <= 6:
        raise ValueError("Invalid planning configuration")
    def search(state, remaining):
        actions = legal(state)
        if not remaining or not actions:
            return value(state, style)
        return max(search(step(state, a), remaining-1) - 0.1 for a in actions)
    scores = {a: search(step(s, a), depth-1) for a in legal(s)}
    if not scores:
        raise ValueError("Terminal state")
    action = max(scores, key=scores.get)
    return action, {a.value: round(v, 2) for a,v in scores.items()}
