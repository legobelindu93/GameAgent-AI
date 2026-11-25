# Research center
Install optional dependencies with uv sync --extra video --extra vision. Launch uv run python -m gameagent.research_ui. Ollama is optional; the advisor expects a local qwen2.5:3b model by default.
Import permitted normalized JSON: uv run python -m gameagent.research nikke catalog-import characters.json --authorized
Schema: [{"kind":"character","name":"Example","patch":"test","source":"local:example","data":{"role":"support"}}]
Transcribe footage you are authorized to process: uv run python -m gameagent.research nikke transcribe clip.mp4 --source local:clip --patch YOUR_PATCH --authorized
Extract annotation frames: uv run python -m gameagent.research nikke frames clip.mp4 data/frames/example --authorized
Search or ask: uv run python -m gameagent.research nikke ask "Which team?" --patch YOUR_PATCH
Sources for future adapters: https://github.com/theBowja/genshin-db, https://github.com/Mar-7th/StarRailRes, https://github.com/SYSTRAN/faster-whisper. Only faster-whisper is integrated by API; other datasets need license and schema review. No data is bundled. The video pipeline does not infer player inputs. No commercial client automation, live 3D navigation, or anti-cheat bypass. Local validation pending.
