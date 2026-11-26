# GameAgent AI

![Version](https://img.shields.io/badge/version-0.14.0-7658e8)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB)
![Windows](https://img.shields.io/badge/platform-Windows-0078D4)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

**A modular desktop research studio for game strategy, local AI, computer vision and upstream application integration.**

Six isolated game profiles, a unified launcher, native interface hosting, and a dedicated Brown Dust 2 F2P expert laboratory.

> [!IMPORTANT]
> GameAgent is a research prototype, not a fully autonomous player. The original third-party applications retain their own features. The strategy and simulation modules do not execute live game actions. Use third-party applications only in environments where their use is authorized.

## Supported games

| Game | Upstream project | Integration |
| --- | --- | --- |
| NIKKE | [NIKKEAutoScript](https://github.com/megumiss/NIKKEAutoScript) | Python / local WebUI |
| Brown Dust 2 | [MFABD2](https://github.com/sunyink/MFABD2) | Native UI, read-only task inventory, expert lab |
| Genshin Impact | [BetterGI](https://github.com/babalae/better-genshin-impact) | .NET / WPF |
| Wuthering Waves | [OK-WW](https://github.com/ok-oldking/ok-wuthering-waves) | Python / Qt |
| Neverness to Everness | [OK-NTE](https://github.com/BnanZ0/ok-nte) | Python / Qt |
| Honkai: Star Rail | [StarRailCopilot](https://github.com/LmeSzinc/StarRailCopilot) | Python / local WebUI |

## Features

- Game-specific dashboard, Segoe UI, status cards and configurable artwork.
- GitHub release discovery and download, with size and published digest checks.
- Isolated Python environments and partial Windows runtime provisioning.
- Native executable registration, local WebUI display and experimental Win32 window hosting.
- Read-only source inventory, diagnostics and logs.
- SQLite FTS5 knowledge index, structured catalog, optional local Ollama advisor.
- Offline OCR, authorized video transcription, synthetic combat and navigation experiments.

## Installation

Requirements: Windows 10/11, Git, Python 3.12+, [uv](https://docs.astral.sh/uv/). Optional: [Ollama](https://ollama.com/). Upstream applications require their own installation and may need different Python versions.

```powershell
git clone https://github.com/legobelindu93/GameAgent-AI.git
cd GameAgent-AI
uv sync --all-extras
uv run python -m gameagent
```

Update an existing installation:

```powershell
git pull origin main
uv sync --all-extras
uv run python -m gameagent
```

Select a game, consult its Installation tab and original release instructions, register the installed executable, then open the original interface. The Interface originale tab can experimentally host compatible Windows windows. Local WebUIs require a running server. Complete automatic installation and direct task API integration are not implemented.

## Brown Dust 2 Expert Lab

```powershell
uv run python -m gameagent.bd2_expert_ui
uv run python -m gameagent.bd2_lab_ui
```

Optional local model:

```powershell
ollama pull qwen2.5:3b
```

The offline F2P planner works without Ollama. For the tactical optimizer, load `games/brown_dust_2/example_team.json` in the lab; its statistics are synthetic.

| System | Current status |
| --- | --- |
| F2P progression planner | Heuristic prototype |
| Knowledge base | Eight initial notes, patch-aware retrieval |
| Character catalog | Partial seed of 65 names; normalized JSON import |
| Costume and skill statistics | Incomplete |
| Damage calculator | Simplified one-turn expected damage |
| Team optimizer | SP-constrained permutations; up to 10 skills, 5 characters |
| Screenshot OCR | Explicit local image selection |
| Account memory | Confirmed resource values |
| Video study | Local Whisper transcription and indexing, not model training |
| News | RSS metadata implementation; endpoint unvalidated |
| MFABD2 | Read-only local log discovery; no verified task API |
| Autonomous gameplay | Not implemented |

Manual integration observation: MFABD2 was launched and embedded, the PC game window was detected and its capture displayed. This does not validate every upstream application or task. Expert lab tests remain pending.

## Architecture

```text
GameAgent-AI/
├── gameagent/
│   ├── launcher_ui.py       # Unified library
│   ├── bridges.py           # Original UI launch
│   ├── dependencies.py      # Partial provisioning
│   ├── installations.py     # Release downloads
│   ├── window_host.py       # Win32 hosting
│   ├── task_catalog.py      # Read-only inventory
│   ├── knowledge.py        # Evidence index
│   ├── catalog.py          # Structured data
│   ├── advisor.py          # Local AI advisor
│   ├── bd2_expert.py       # F2P planning
│   ├── bd2_tactics.py      # Tactical analysis
│   ├── bd2_observe.py      # OCR and diagnostics
│   ├── bd2_data.py         # Catalog and snapshots
│   ├── bd2_news.py         # News metadata
│   └── bd2_lab_ui.py       # Expert lab
├── games/                  # Profiles and data
├── assets/games/            # Optional local artwork
├── data/                    # Local environments and data
├── docs/
└── tests/
```

## Development and tests

```powershell
uv run python -m unittest discover -s tests -v
uv run python -m gameagent.benchmark
uv run python -m gameagent.lab route genshin_impact
uv run python -m gameagent.lab inspect nikke screenshot.png
uv run python -m gameagent.train --steps 10000
uv run python -m gameagent.lab train-navigation --steps 10000
```

Training and navigation environments are synthetic. No trained game-specific model is included. Test commands are supplied for local validation; passing results are not asserted.

## Research & Knowledge Factory (v0.12.0)

```powershell
uv run python -m gameagent.research_center_ui
uv run python -m gameagent.research_center brown_dust_2 bootstrap
uv run python -m gameagent.research_center brown_dust_2 cycle
uv run python -m gameagent.research_center brown_dust_2 offline "progression F2P"
uv run python -m gameagent.research_center brown_dust_2 bundle data/packs
```

Six source registries, 40 curated starter notes across six games, offline SHA-256 pack validation, candidate/approved separation, authorized transcript imports, optional YouTube/Brave discovery optional remote document compilation, cited web dossiers and public YouTube video study through Gemini. No GPU required for pack import, evidence retrieval, discovery or remote analysis. The bounded batch workflow prioritizes knowledge gaps and caches candidate results. Cloud calls require explicit opt-in and separate keys. For a lightweight setup use `uv sync` rather than `--all-extras`; add `--extra cloud-study` only for remote video analysis. External providers need credentials and may incur costs; no automatic video downloading or model training. See [research factory documentation](docs/research-factory.md).

## Roadmap

- Complete versioned costume, character and equipment data.
- Validate damage formulas and multi-turn tactical evaluation.
- Improve screenshot interpretation and confirmed account-state extraction.
- Validate news sources and event calendars.
- Improve read-only diagnostics, Windows compatibility and strategy benchmarks.
- Extend the expert approach to other profiles.

## Documentation

- [BD2 expert advisor](docs/bd2-expert.md)
- [BD2 expert lab](docs/bd2-lab.md)
- [Upstream bridges](docs/upstream-bridges.md)
- [Native window hosting](docs/native-host.md)
- [Launcher](docs/launcher.md)
- [Visual customization](docs/visual-refresh.md)
- [Synthetic navigation](docs/navigation.md)

## Credits

GameAgent is independent of publishers and upstream projects. Credit and licensing remain with the original authors. Consult their licenses before redistribution. No official game artwork or upstream release binaries are bundled. Community guides are version-sensitive. The advisor does not make purchases or send game inputs.

## Obsidian Studio (v0.13.0)

Install the optional modern library with `uv sync --extra modern-ui --extra native-ui --extra vision --extra ocr`, then launch `uv run python -m gameagent`. Original full panels remain accessible from the library and via `uv run python -m gameagent.launcher_ui`. Original offline procedural landscape illustrations are supplied at runtime; user-provided artwork at `assets/games/<game>/banner.png` takes precedence. No publisher artwork is redistributed. The Qt shell is a progressive migration, not a full Qt port of every panel.

### Qt workbenches (v0.14.0)

Research Factory (19 actions), Knowledge Center (3), F2P Expert (3), and Tactical Lab (7) now open in modern Qt windows with shared artwork, grouped commands, split results, and background processing. Classic modules remain available. Native hosting, source explorer and simulation still use the original Tk panels.
