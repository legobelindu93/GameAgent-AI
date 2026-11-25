"""Optional Gymnasium adapter for training in the synthetic environment."""
import gymnasium as gym
import numpy as np
from .engine import Action, State, step
from .planner import legal

class CombatEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(0, 100, shape=(3,), dtype=np.float32)
        self.state = State()

    def observation(self):
        return np.array([self.state.hp,self.state.enemy,self.state.potions],dtype=np.float32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = State()
        return self.observation(), {}

    def step(self, action):
        previous = self.state
        a = tuple(Action)[int(action)]
        if a not in legal(previous):
            self.state = step(previous, Action.DEFEND)
            penalty = -5
        else:
            self.state = step(previous,a)
            penalty = 0
        s = self.state
        ended = s.hp <= 0 or s.enemy <= 0
        reward = (previous.enemy-s.enemy)/10 + (s.hp-previous.hp)/20 + penalty
        reward += 20 if s.enemy <= 0 else -20 if s.hp <= 0 else 0
        return self.observation(), float(reward), ended, s.turn >= 30 and not ended, {}
