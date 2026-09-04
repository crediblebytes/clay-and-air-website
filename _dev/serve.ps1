# Regenerate, check, and serve the site locally.
#   .\_dev\serve.ps1
# Then open http://localhost:8000  (Ctrl+C to stop)
#
# Serve rather than opening the .html directly: over file:// the YouTube
# embeds fail with a configuration error.

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python _dev\generate.py
python _dev\qa2.py

Write-Host ""
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

python -m http.server 8000
