# Obsidian Studio

The optional Qt shell is a new library and navigation layer, not a replacement for the mature native host. It opens the complete original per-game panel with the chosen profile. All old entry points remain available; their common Tk theme is refreshed. Research Factory groups all 19 existing commands into four tabs. The existing original-app host is intentionally unchanged.

Artwork: six deterministic original procedural illustrations generated with Pillow, cached in memory. To use authorized publisher or personal artwork, supply assets/games/<game>/banner.png (or jpg/webp). No network request or publisher asset included. Restart the app after changing art.

Install: uv sync --extra modern-ui --extra native-ui --extra vision --extra ocr
Launch: uv run python -m gameagent
Classic: uv run python -m gameagent --classic
Add other extras (cloud-study, video, learning, navigation) as required by the existing features.

The Figma design reference is https://www.figma.com/design/jf3AoEy1IWJ4Ofq4DG4Uea?node-id=6-92 . Qt uses Segoe UI as a system font rather than bundling Inter. The current implementation is a Qt Widgets progressive migration, not QML, and the auxiliary windows remain Tkinter.
