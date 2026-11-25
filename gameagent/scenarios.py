"""Distinct synthetic research scenarios; not replicas of commercial games."""
from dataclasses import dataclass
from .engine import State
from .planner import plan
from .engine import step

@dataclass(frozen=True)
class Scenario:
    hp: int
    enemy: int
    potions: int
    style: str

SCENARIOS = {
    "nikke": Scenario(100,100,1,"balanced"),
    "brown_dust_2": Scenario(85,100,2,"careful"),
    "genshin_impact": Scenario(100,75,1,"balanced"),
    "wuthering_waves": Scenario(75,100,1,"aggressive"),
    "neverness_to_everness": Scenario(90,75,0,"balanced"),
    "honkai_star_rail": Scenario(100,100,2,"careful"),
}

def initial(game_id):
    s=SCENARIOS[game_id]
    return State(hp=s.hp,enemy=s.enemy,potions=s.potions)

def evaluate(game_id, max_turns=30):
    if not 1 <= max_turns <= 100:
        raise ValueError("Invalid turn limit")
    s=initial(game_id)
    trace=[]
    while s.hp>0 and s.enemy>0 and s.turn<max_turns:
        a,scores=plan(s,SCENARIOS[game_id].style)
        s=step(s,a)
        trace.append({"turn":s.turn,"action":a.value,"hp":s.hp,"enemy":s.enemy,"scores":scores})
    return {"game":game_id,"won":s.enemy<=0,"turns":s.turn,"hp":s.hp,"trace":trace}
