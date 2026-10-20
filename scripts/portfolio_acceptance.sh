#!/usr/bin/env bash
set -euo pipefail

echo "== StartupCoach portfolio acceptance =="

# Quality-gate the maintained application, not only demo fixtures.
ruff check \
  app.py workflow_manager.py tools_manager.py calculators.py token_tracker.py \
  chat_manager.py translations.py demo_mode.py tests
ruff format --check \
  app.py workflow_manager.py tools_manager.py calculators.py token_tracker.py \
  chat_manager.py translations.py demo_mode.py tests

python -m pytest -q tests
python -m py_compile app.py demo_mode.py

# Real maintained modules must import without making a live provider call.
python -c "import workflow_manager, chat_manager, tools_manager, calculators, token_tracker, translations; print('maintained modules imported')"

# Demo bootstrap must need no API key.
DEMO_MODE=1 python -c "import demo_mode; assert len(demo_mode.DEMO_SCENARIOS) >= 3"

python - <<'PY'
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
assert "Turing College" in readme, "README must state the project's Turing College context"
assert "A powerful AI-powered" not in readme, "Replace generic portfolio-marketing opening"
assert "Python 3.11" in readme or "Python-3.11" in readme, "README must match the supported runtime"
PY

echo "StartupCoach acceptance passed."
