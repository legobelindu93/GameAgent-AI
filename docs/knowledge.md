# Knowledge engine
Separate SQLite FTS5 evidence indexes per game. Import only authorized local notes, openly licensed data under applicable terms, or transcripts you may use. Source and game patch are mandatory. This is lexical retrieval, not model fine-tuning. Optional advisor calls a locally installed Ollama model; no automatic actions. No mass download of YouTube videos or captions. Official YouTube caption downloads require authorization: https://developers.google.com/youtube/data/reference/rest/v3/captions/download .
Example:
uv run python -m gameagent.study genshin_impact import guide.md --title "My notes" --source "https://keqingmains.com/" --patch 7.2 --authorized
uv run python -m gameagent.study genshin_impact search "rotation" --patch 7.2
Sources manifests are discovery candidates, not imported datasets. Video-based action learning needs permitted footage and aligned action labels, plus validation in an authorized environment.
