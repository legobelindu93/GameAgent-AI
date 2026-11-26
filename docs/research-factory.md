# Research Factory
Run python -m gameagent.research_center_ui or python -m gameagent.research_center GAME --help.
No additional Python packages or GPU are required for pack import or metadata search.
- sources: registered discovery links, not permission to scrape.
- cycle: up to three topic searches prioritized by FTS hit count, a weak coverage proxy, not a proof of expertise. Without keys returns registered links only.
- Set YOUTUBE_API_KEY for official public metadata search, BRAVE_SEARCH_API_KEY for web discovery. Keys stay in environment. Provider limits and charges may apply.
- Import authorized transcripts with notes FILE --source HTTPS --patch VERSION --authorized. Local video transcription remains in gameagent.research. No unauthorized captions or video download. The YouTube API requires permissions for caption download: https://developers.google.com/youtube/data/reference/rest/v3/captions/download
- Remote compilation is optional: set OPENAI_API_KEY and GAMEAGENT_REMOTE_MODEL, then compile FILE OUTPUT --version 1.0.0 --source HTTPS --patch VERSION --authorized. Sends explicitly selected excerpt to API; possible charges. Produces candidate-only pack.
- Human review: export records array from pack JSON, verify sources, edit review to approved only where supported, build RECORDS OUTPUT --version 1.0.1, verify OUTPUT, install OUTPUT --trusted. SHA-256 is integrity only, not a digital signature. Review is an explicit trust decision. Candidate entries never enter advisor index via pack installer. Imports are additive; historical entries are not automatically deleted.
- seed installs reviewed, limited BD2 pack. All six games now have limited reviewed starter notes, not complete databases.
- account FILE --confirmed imports normalized JSON (see knowledge_packs/example_account.json). No direct game export compatibility claimed.
- conflicts FILE compares identical topic/patch labels; no semantic conflict resolution.
- Discovery is metadata only; remote compiler cannot browse or watch videos. No ongoing scheduled updates until explicitly configured. No automated game inputs. Network and Windows integration tests remain pending.

## Cloud video and web study
- Install the optional cloud-study extra, configure GEMINI_API_KEY and GAMEAGENT_VIDEO_MODEL (model supporting YouTube video input). See https://ai.google.dev/gemini-api/docs/video-understanding#youtube . One authorized public video per request. No local video download. The service is subject to its own rights, quotas, model availability and pricing; no live call was made in development.
- video-url URL OUTPUT --patch VERSION --authorized produces candidate lessons with timestamp ranges. Time ranges must be verified by a human.
- Set OPENAI_API_KEY and GAMEAGENT_WEB_MODEL (Responses web-search compatible). web-study TOPIC OUTPUT --authorized saves a cited candidate research dossier; it does not automatically approve claims. Review cited sources individually before converting them to a pack.
- review PACK OUTPUT --ids ID1 ID2 --version 1.0.1 marks explicitly reviewed records as approved. Only run after verifying each source. Then install OUTPUT --trusted.
- patch-check compares announcement search result URLs; this is not detection of authoritative patch numbers or deadlines.
- benchmark checks seed retrieval@5 for one game, not strategy quality.
