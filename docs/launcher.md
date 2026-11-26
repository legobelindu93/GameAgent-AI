# Game launcher — v0.15

Launch `uv run python -m gameagent` with modern-ui installed. Choose a profile and open its Qt console, or run `uv run python -m gameagent.qt_console --game brown_dust_2`. The console has Application, Installation, Interface native and Diagnostic tabs.

Release discovery and explicit download use GitHub; size and any provided SHA-256 digest are checked. Extraction/installation is manual. Register an installed executable or provision a reviewed source environment. Local WebUI opens via pywebview. Native embedding is experimental and limited to the exact launched process PID. The classic launcher is available via --classic. See [guide](user-guide.md) and [native host](native-host.md).
