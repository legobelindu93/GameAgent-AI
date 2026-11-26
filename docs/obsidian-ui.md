# Obsidian Studio — v0.15

All eight workspaces have PySide6 Qt Widgets implementations. The library starts each workspace as a separate Python process. The console retains the original Windows host through a QWidget adapter; the classic Tkinter panels remain available. The shared Qt Workbench provides grouped controls, banner, splitter, output, clipboard copy and a single-worker executor.

```powershell
uv sync --extra modern-ui --extra native-ui --extra vision --extra ocr
uv run python -m gameagent
uv run python -m gameagent --classic
```

Artwork is generated offline; authorized local banner files take precedence. See [artwork](../assets/games/README.md). The design [Figma reference](https://www.figma.com/design/jf3AoEy1IWJ4Ofq4DG4Uea) uses Inter, whereas Qt uses Segoe UI. The UI is not QML or a pixel-perfect port. CI validates construction and selected behavior offscreen, not visual layout or live hosting.

See [user guide](user-guide.md) and [technical reference](technical-reference.md).
