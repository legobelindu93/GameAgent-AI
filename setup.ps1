$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
uv sync
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run python -m unittest discover -s tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run python -m gameagent
