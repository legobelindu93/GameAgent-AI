"""Small nearest-neighbor behavioral cloning baseline for simulated demonstrations."""
from .engine import Action
from .planner import legal

class Imitation:
    def __init__(self):
        self.examples = []

    def teach(self, state, action):
        if action not in legal(state):
            raise ValueError("Illegal demonstration")
        self.examples.append((state, action))

    def predict(self, state):
        actions = legal(state)
        examples = [(s,a) for s,a in self.examples if a in actions]
        if not examples:
            raise ValueError("No applicable demonstrations")
        def distance(example):
            s,_ = example
            return abs(s.hp-state.hp)/100 + abs(s.enemy-state.enemy)/100 + abs(s.potions-state.potions)/2
        return min(examples, key=distance)[1]
