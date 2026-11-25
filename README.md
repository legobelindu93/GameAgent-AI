# GameAgent AI 0.4.0
Modular research studio with six isolated profiles. All combat and navigation are synthetic; no commercial game control or trained game-specific models.

## Run
```powershell
uv sync --all-extras
uv run python -m gameagent
uv run python -m unittest discover -s tests -v
uv run python -m gameagent.benchmark
uv run python -m gameagent.lab route genshin_impact
```
Offline recognition: uv run python -m gameagent.lab inspect nikke screenshot.png
Synthetic PPO: uv run python -m gameagent.train --steps 10000
Grid-world PPO: uv run python -m gameagent.lab train-navigation --steps 10000
See docs/navigation.md and docs/upstream-review.md for sources and limits.
