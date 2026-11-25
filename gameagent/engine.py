from dataclasses import dataclass
from enum import Enum

class Action(str, Enum):
    ATTACK = "attack"
    HEAL = "heal"
    DEFEND = "defend"

@dataclass(frozen=True)
class State:
    hp: int = 100
    enemy: int = 100
    potions: int = 2
    turn: int = 0

def choose(s: State) -> tuple[Action, str]:
    if s.hp <= 35 and s.potions:
        return Action.HEAL, "Preserve health"
    if s.hp <= 20 and s.enemy > 25:
        return Action.DEFEND, "Reduce incoming damage"
    return Action.ATTACK, "Advance objective"

def step(s: State, a: Action) -> State:
    if s.hp <= 0 or s.enemy <= 0:
        return s
    hp, enemy, potions = s.hp, s.enemy, s.potions
    if a == Action.HEAL:
        if not potions:
            raise ValueError("No potions")
        hp, potions = min(100, hp + 40), potions - 1
    elif a == Action.ATTACK:
        enemy = max(0, enemy - 25)
    if enemy:
        hp = max(0, hp - (5 if a == Action.DEFEND else 18))
    return State(hp, enemy, potions, s.turn + 1)
