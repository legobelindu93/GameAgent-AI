# GameAgent AI 0.2.0
Windows-first research studio with six isolated game profiles. All combat currently uses a synthetic simulator, not actual game mechanics.

## Run
```powershell
uv sync
uv run python -m gameagent
uv run python -m unittest discover -s tests
```
Optional offline image recognition:
```powershell
uv sync --extra vision
uv run python -m gameagent
```
Optional synthetic PPO training:
```powershell
uv sync --extra learning
uv run python -m gameagent.train --steps 10000
```
The launcher supports finite-horizon planning, three scoring styles, manual simulated demonstrations, nearest-neighbor imitation, per-profile SQLite history, automatic simulation and stop. No trained commercial-game model or live game inputs. See docs/upstream-review.md for preliminary source review.
