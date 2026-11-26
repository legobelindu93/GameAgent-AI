# GameAgent AI — Obsidian Studio

[![Version](https://img.shields.io/badge/version-0.15.0-8bb94b)](pyproject.toml)
[![Tests](https://github.com/legobelindu93/GameAgent-AI/actions/workflows/tests.yml/badge.svg)](https://github.com/legobelindu93/GameAgent-AI/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB)
![Platform](https://img.shields.io/badge/desktop-Windows-0078D4)

**A modular desktop research studio for game strategy, evidence retrieval, computer vision and third-party interface integration.**

GameAgent brings six isolated game profiles into a unified PySide6/Qt Widgets workspace, with offline knowledge packs, optional cloud research and a dedicated Brown Dust 2 F2P laboratory.

> [!IMPORTANT]
> This is a research prototype, not an autonomous game-playing agent. It does not send game inputs, bypass anti-cheat, make purchases or train a game-specific neural policy. Original upstream applications remain independent and must be used only where authorized.

## Quick start

Requirements: Windows 10/11, Git, Python 3.12+, [uv](https://docs.astral.sh/uv/). Open PowerShell in a simple local folder.

```powershell
git clone https://github.com/legobelindu93/GameAgent-AI.git
cd GameAgent-AI
uv sync --extra modern-ui --extra native-ui --extra vision --extra ocr
uv run python -m gameagent
```

For an existing installation, run `git pull origin main` from the repository, then repeat the sync and launch commands. Local data under `data/` is not replaced by a normal pull. Back it up before maintenance. The lightweight installation requires no API key or dedicated GPU. Optional extras are documented in the [user guide](docs/user-guide.md). Do not use all extras unless you need them.

Classic fallback: `uv run python -m gameagent --classic`.

## Game library

| Profile | Upstream project | Interface path |
|---|---|---|
| NIKKE | [NIKKEAutoScript](https://github.com/megumiss/NIKKEAutoScript) | Python / local WebUI |
| Brown Dust 2 | [MFABD2](https://github.com/sunyink/MFABD2) | Installed native executable; experimental hosting |
| Genshin Impact | [BetterGI](https://github.com/babalae/better-genshin-impact) | Installed native executable |
| Wuthering Waves | [OK-Wuthering-Waves](https://github.com/ok-oldking/ok-wuthering-waves) | Python / original interface |
| Neverness to Everness | [OK-NTE](https://github.com/BnanZ0/ok-nte) | Python / original interface |
| Honkai: Star Rail | [StarRailCopilot](https://github.com/LmeSzinc/StarRailCopilot) | Python / local WebUI |

Each upstream project requires its own compatible installation. GameAgent can discover release assets, download an explicitly selected file without executing it, register an installed executable and launch the original interface. It does not bundle upstream code or provide a universal task API.

## Obsidian Studio

| Workspace | Main capabilities |
|---|---|
| Library | Six illustrated profiles and navigation |
| Game console | Releases, dependencies, executable registration, WebUI, diagnostics and experimental native host |
| Research Factory | 19 grouped operations: discovery, study, packs, account and analysis |
| Knowledge Center | Guide retrieval, catalog search, optional local Ollama advisor |
| F2P Expert | Manual account context and heuristic progression plan |
| Tactical Lab | OCR, catalog import, simplified team optimization, authorized video study, RSS and log diagnostics |
| Source Explorer | Read-only inventory, search and file preview |
| Simulation | Synthetic combat, planning, demonstrations, SQLite memory and offline image matching |

All eight workspaces have Qt Widgets implementations. Original Tkinter modules remain available. Figma: [Obsidian UI design](https://www.figma.com/design/jf3AoEy1IWJ4Ofq4DG4Uea). The application uses original procedural artwork, not official game art; permitted local artwork can override it ([instructions](assets/games/README.md)). Figma is a design reference, not a pixel-perfect rendering of the app.

## Offline knowledge

```powershell
uv run python -m gameagent.research_center brown_dust_2 bootstrap
uv run python -m gameagent.research_center brown_dust_2 offline "progression F2P"
uv run python -m gameagent.qt_research
```

Bootstrap installs the six starter packs (40 initial records: 20 BD2 and four per other game). These are limited, manually prepared references, not an independently verified complete game database. Review sources and patch applicability. Offline advice retrieves evidence rather than computing an optimal game policy. Optional remote research produces candidate records requiring human review. See [Research Factory](docs/research-factory.md).

## Documentation

| Document | Purpose |
|---|---|
| [Documentation index](docs/README.md) | All guides and reference pages |
| [User guide (FR)](docs/user-guide.md) | Installation, every workspace, troubleshooting |
| [Technical reference (FR)](docs/technical-reference.md) | Architecture, modules, schemas, API boundaries, testing |
| [Architecture](docs/architecture.md) | Component map and flows |
| [Validation](docs/validation.md) | Automated tests and manual acceptance |
| [Release notes](CHANGELOG.md) | Version history and remaining limitations |

## Development

```powershell
uv run python -m unittest discover -s tests -v
uv sync --extra modern-ui --extra navigation
uv run python -m unittest discover -s tests -v
uv run python -m gameagent.benchmark
```

GitHub Actions passed on Windows and Ubuntu for the v0.15 merge candidate ([run 45852548517](https://github.com/legobelindu93/GameAgent-AI/actions/runs/45852548517)). CI uses offscreen Qt tests; it does not validate live commercial games, external APIs, actual native window embedding or visual polish. Optional training remains synthetic.

## Roadmap and credits

Priorities: manual Windows acceptance, better visual assets, independently verified patch-aware data, richer tactical models, improved diagnostics and expert coverage for other profiles. No autonomous gameplay is implemented.

GameAgent is independent of the publishers and upstream authors listed above. Their code, artwork and licenses remain theirs; verify permissions before use or redistribution. No upstream release binaries or official game art are bundled. A complete license/security review of third-party integrations remains outstanding.
