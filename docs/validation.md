# Validation — v0.15

## Automated

```powershell
uv sync --extra modern-ui --extra navigation
uv run python -m unittest discover -s tests -v
uv run python -m gameagent.benchmark
$env:QT_QPA_PLATFORM = "offscreen"
uv run python -m unittest tests.test_obsidian_ui tests.test_qt_workbenches tests.test_qt_remaining -v
Remove-Item Env:QT_QPA_PLATFORM
```

CI installs pathfinding, Pillow and PySide6 on Python 3.12, Windows/Ubuntu. The v0.15 candidate passed both matrices ([run](https://github.com/legobelindu93/GameAgent-AI/actions/runs/45852548517)); the prior candidate exposed a deleted Qt layout on Windows, fixed in 149f4b9. Test cases construct windows, count actions, switch profiles, filter sources, exercise synthetic simulation and check artwork; they do not prove every button workflow or visual correctness. Optional dependency tests may skip unavailable features.

## Manual acceptance checklist

- [ ] Launch library; inspect all six covers at 100%, 125%, 150% display scaling and resize.
- [ ] Open each of eight Qt panels and exercise the classic fallback.
- [ ] Verify profile changes, selected paths, release discovery and confirmed downloads.
- [ ] Register an authorized installed upstream application; open it externally.
- [ ] On Windows, attach a compatible window from the launched PID, resize, detach, switch profile and close safely. Use a harmless test window first. Verify external fallback.
- [ ] Install the six packs; query evidence; validate candidate/approved separation and invalid hash rejection.
- [ ] Import a sample account; exercise BD2 planner and synthetic team example.
- [ ] OCR a permitted local screenshot; verify confirmation before snapshot.
- [ ] Inspect local sources; check filter and text preview.
- [ ] Exercise synthetic simulation, reset, imitation and saved memory.
- [ ] With optional dependencies/credentials, separately validate local Ollama, media transcription and authorized remote calls; verify errors and costs.
- [ ] Confirm no secrets in screenshots/logs and no unapproved network or game actions.

Record OS, version/commit, extras, panel, observed outcome and reproduction steps. Manual results are not pre-filled. Benchmark measures synthetic/retrieval behavior, not gameplay expertise.
