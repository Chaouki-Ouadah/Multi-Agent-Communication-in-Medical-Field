# GraphRAG + Neo4j setup (Card 10b — SRQ2 config B)

Config B = **Neo4j entity-relationship retrieval over PrimeKG** + **Microsoft GraphRAG community
search over a clinical-text corpus**. Both feed config C (hybrid). The core `medargue` env never
imports `graphrag` (it pins `numpy~=2.1`, clashing with our `numpy<2` scispaCy stack) — GraphRAG runs
in an isolated `.venv-graphrag` and is invoked by subprocess.

Credentials are env-only (`.env`, gitignored). Copy `.env.example` → `.env`.

## 1. Neo4j (PrimeKG knowledge graph)

Dev container (Docker Desktop):

```bash
docker run -d --name neo4j-medargue --restart unless-stopped \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/medargue-dev-pw -e NEO4J_PLUGINS='["apoc"]' neo4j:5
```

Set `NEO4J_URI=bolt://localhost:7687`, `NEO4J_USER=neo4j`, `NEO4J_PASSWORD=medargue-dev-pw` in `.env`.

Ingest PrimeKG (open, Harvard/MIT — download `kg.csv` from the Harvard Dataverse,
doi:10.7910/DVN/IXA7BM):

```bash
python scripts/ingest_primekg.py path/to/kg.csv            # full (~8M edges, long)
python scripts/ingest_primekg.py path/to/kg.csv --limit 5000   # subset for dev
```

`Neo4jGraphRetriever` then resolves a query's clinical entities (scispaCy NER) to their PrimeKG
neighbourhood via Cypher.

## 2. Microsoft GraphRAG (isolated venv)

> Windows + Defender: `python -m venv` may fail with `WinError 225` (false-positive on the copied
> python.exe). Fix once, in an **elevated** PowerShell:
> `Add-MpPreference -ExclusionPath "<repo>\.venv-graphrag"` then recreate the venv.

```bash
bash scripts/setup_graphrag.sh            # venv + graphrag + workspace + sample corpus
# or a richer corpus:
python scripts/build_graphrag_corpus.py --out .graphrag/input --per-term 20   # PubMed abstracts
```

Point `.graphrag/settings.yaml` at local Ollama (OpenAI-compatible). Minimal block:

```yaml
models:
  default_chat_model:
    type: openai_chat
    api_base: http://localhost:11434/v1
    api_key: ollama          # dummy; Ollama ignores it
    model: llama3.1:8b
  default_embedding_model:
    type: openai_embedding
    api_base: http://localhost:11434/v1
    api_key: ollama
    model: nomic-embed-text
```

Index + query (in the isolated venv):

```bash
.venv-graphrag/Scripts/python.exe -m graphrag index --root .graphrag
.venv-graphrag/Scripts/python.exe -m graphrag query --root .graphrag \
  --method local --query "differential for bilateral opacities with elevated BNP"
```

`GraphRAGRetriever` shells out to exactly that `graphrag query` and wraps the answer as a
`RetrievedItem` (modality `graph`).

## 3. Use in code

```python
from src.knowledge.neo4j_client import Neo4jClient
from src.knowledge.graph_rag import Neo4jGraphRetriever, GraphRAGRetriever, make_graph_retriever
from src.knowledge.retrieval import build_retriever, RetrievalConfig

graph = make_graph_retriever(
    neo4j_graph=Neo4jGraphRetriever(Neo4jClient()),
    graphrag=GraphRAGRetriever(workspace=".graphrag", venv_python=".venv-graphrag/Scripts/python.exe"),
)
config_b = build_retriever(RetrievalConfig.GRAPH, graph_retriever=graph)
config_c = build_retriever(RetrievalConfig.HYBRID, text_retriever=..., image_retriever=..., graph_retriever=graph)
```

## 4. Tests

- **CI (pure):** `tests/test_kg.py` mocks the driver + subprocess — no server/venv/network.
- **Live (`-m slow`, local):** real PrimeKG-sample ingest+retrieve (needs Neo4j) + real `graphrag
  query` (needs the venv + an indexed workspace). Both skip cleanly when absent.
