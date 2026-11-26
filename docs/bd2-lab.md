# BD2 expert lab
Launch Expert Brown Dust 2 > Laboratoire expert, or uv run python -m gameagent.qt_lab.
Character seed: 65 manually prepared names referencing https://browndust2-db.souseha.com/en/characters (independent verification outstanding); partial index, no invented stats. Import normalized authorized catalog JSON using existing Catalog format.
Tactics: select games/brown_dust_2/example_team.json (synthetic). Estimate expected ordinary physical/magic damage per hit with chain progression, input buffs and resistance. Based on https://botan14xd.github.io/BD2-Overview/game-mechanics/battle-system/ and https://dotgg.gg/brown-dust-2/beginners-guide-frequently-asked-questions/. Omits fixed damage, conditional buffs, pressure, grids, cooldowns, multi-round effects, rounding, targets, and verified skill values. Exact permutation search only within this reduced model, <=10 skills.
OCR: user-selected screenshots only; explicit resource labels, confidence filter, confirmation before saving. No automatic account scan or roster identification. Videos: local authorized media, Whisper transcript indexed for retrieval, no model training or visual learning. News: unverified RSS endpoint, headline synchronization only; event dates not inferred. MFABD2: read-only local log discovery, exact upstream log locations and protocol not verified; no direct task execution API. Base CI passed for v0.15; live OCR, RSS and Windows integrations require separate validation.


Current version: 0.15. See the [user guide](user-guide.md) and [technical reference](technical-reference.md).
