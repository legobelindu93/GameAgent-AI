# Validation
Run base tests: uv run python -m unittest discover -s tests
Run optional environment check: uv sync --extra learning; uv run python -m unittest discover -s tests
Benchmark: uv run python -m gameagent.benchmark
Diagnostic: uv run python -m gameagent.check_environment

Sources consulted:
- https://maafw.com/en/docs/3.1-PipelineProtocol/ (recognition pipeline design inspiration; not protocol-compatible)
- https://stable-baselines3.readthedocs.io/en/v2.5.0/guide/custom_env.html (environment checker)
- https://rapidai.github.io/RapidOCRDocs/main/en/install_usage/rapidocr/usage/ (OCR API)
No third-party game code imported. Scenarios are synthetic examples, not validated game rules. No live input backend. Optional dependencies and GPU acceleration require local verification.
