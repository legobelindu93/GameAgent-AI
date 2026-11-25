"""Reusable upstream 3D-rendered grid-world research environment (not a commercial game)."""
def train(steps, output):
    from pathlib import Path
    import gymnasium as gym
    import minigrid
    from minigrid.wrappers import ImgObsWrapper
    from stable_baselines3 import PPO
    from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
    from torch import nn
    class GridFeatures(BaseFeaturesExtractor):
        def __init__(self, observation_space, features_dim=64):
            super().__init__(observation_space, features_dim)
            size=1
            for dim in observation_space.shape:
                size*=dim
            self.net=nn.Sequential(nn.Flatten(),nn.Linear(size,features_dim),nn.ReLU())
        def forward(self, obs):
            return self.net(obs.float())
    if steps<1:
        raise ValueError("steps must be positive")
    env=ImgObsWrapper(gym.make("MiniGrid-Empty-8x8-v0"))
    try:
        model=PPO("MlpPolicy",env,policy_kwargs={"features_extractor_class":GridFeatures,"normalize_images":False},device="cpu",seed=42)
        model.learn(total_timesteps=steps)
        Path(output).parent.mkdir(parents=True,exist_ok=True)
        model.save(output)
    finally:
        env.close()
