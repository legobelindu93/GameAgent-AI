import importlib.util
import unittest

@unittest.skipUnless(importlib.util.find_spec("stable_baselines3") and importlib.util.find_spec("gymnasium"),"Optional learning dependencies absent")
class EnvironmentTests(unittest.TestCase):
    def test_contract(self):
        from stable_baselines3.common.env_checker import check_env
        from gameagent.gym_env import CombatEnv
        env=CombatEnv()
        try:
            check_env(env)
        finally:
            env.close()
