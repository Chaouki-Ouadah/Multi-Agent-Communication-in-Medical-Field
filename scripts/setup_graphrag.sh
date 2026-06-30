#!/usr/bin/env bash
# Card 10b — set up the ISOLATED Microsoft GraphRAG venv + workspace (SRQ2 config B, half 2).
# GraphRAG pins numpy~=2.1 and is kept OUT of the medargue env; it runs only here and is invoked by
# subprocess from src/knowledge/graph_rag.py. Run from the repo root. Ollama must be running.
set -euo pipefail

VENV=".venv-graphrag"
WS=".graphrag"
CORPUS="${1:-data/graphrag_corpus/sample}"

# 1. Isolated venv + GraphRAG (Windows note: if Defender blocks venv creation with WinError 225,
#    add a Defender exclusion for $VENV first — see docs/graphrag-neo4j-setup.md).
if [ ! -x "$VENV/Scripts/python.exe" ] && [ ! -x "$VENV/bin/python" ]; then
  python -m venv "$VENV"
fi
PY="$VENV/Scripts/python.exe"; [ -x "$PY" ] || PY="$VENV/bin/python"
"$PY" -m pip install --upgrade pip >/dev/null
"$PY" -m pip install -r requirements-graphrag.txt

# 2. Init workspace + load the corpus
"$PY" -m graphrag init --root "$WS" || true
mkdir -p "$WS/input"
cp "$CORPUS"/*.txt "$WS/input/" 2>/dev/null || true

# 3. Point settings.yaml at local Ollama (OpenAI-compatible) — see docs for the exact block.
echo "Next: edit $WS/settings.yaml to use Ollama (http://localhost:11434/v1), then:"
echo "  $PY -m graphrag index --root $WS"
echo "  $PY -m graphrag query --root $WS --method local --query 'differential for bilateral opacities with elevated BNP'"
