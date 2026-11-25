"""Run PPO against the synthetic simulator, never a commercial client."""
import argparse
from pathlib import Path

def main():
    from stable_baselines3 import PPO
    from .gym_env import CombatEnv
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--output", default="data/simulator/ppo")
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("steps must be positive")
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    env = CombatEnv()
    try:
        model = PPO("MlpPolicy", env, seed=42, device="cpu", verbose=1)
        model.learn(total_timesteps=args.steps)
        model.save(args.output)
    finally:
        env.close()

if __name__ == "__main__":
    main()
