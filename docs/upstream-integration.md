# Game-specific source integration
Six public upstream repositories now have separate manifests and a source acquisition/inventory tool. Clone is explicitly no-checkout; no upstream code is executed or redistributed. This is source acquisition infrastructure, not a working gameplay adapter. Review each exact revision, dependencies, licenses and game permissions before extracting reusable offline perception components.
```powershell
uv run python -m gameagent.upstream acquire nikke
uv run python -m gameagent.upstream inventory nikke
```
Repeat with brown_dust_2, genshin_impact, wuthering_waves, neverness_to_everness, honkai_star_rail. Local clones live under ignored data/upstream. No live execution or anti-cheat evasion support.
