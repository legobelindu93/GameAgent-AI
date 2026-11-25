# Navigation research
Reuse https://github.com/brean/python-pathfinding (MIT) via Grid and AStarFinder; no vendored code. Reuse https://github.com/Farama-Foundation/Minigrid via Gymnasium and Stable Baselines3. The three maps are invented grids, not actual game maps. MiniGrid is a grid-world, not a 3D open-world simulator.
Run uv sync --all-extras, then uv run python -m gameagent.lab route genshin_impact or uv run python -m gameagent.lab train-navigation --steps 10000.
Offline OCR: uv run python -m gameagent.lab inspect nikke screenshot.png.
Tauri sidecar reference: https://v2.tauri.app/develop/sidecar/ — implementation deferred. MaaFramework custom recognition reference: https://github.com/MaaXYZ/MaaFramework/blob/main/source/binding/Python/maa/custom_recognition.py — no direct integration yet.
CI runs base and pathfinding tests; optional OCR and training need independent validation.
