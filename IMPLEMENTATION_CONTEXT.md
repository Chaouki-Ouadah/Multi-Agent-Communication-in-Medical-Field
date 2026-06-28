# IMPLEMENTATION CONTEXT — Multi-Agent Argumentation Clinical Decision Support

> **This file is the single source of truth for implementing this project in this workspace.**
> Read it fully before writing any code. It is written for an autonomous coding agent (Claude Code)
> with no prior knowledge of the project. Everything needed to start building is here.

---

## 0. TL;DR — What We Are Building Right Now

We are building a **multi-agent argumentation system** for clinical decision support, where 3 LLM
"specialist" agents each see a **different partition** of a patient's clinical features, debate the
likely complications, and a **symbolic argumentation engine** (Dung's AAF) resolves the debate into
an explainable recommendation.

**START HERE → Track 1 (Surrogate Data First):** We do **NOT** have MIMIC access yet (PhysioNet +
CITI credentialing is in progress). So we begin on **fully synthetic / surrogate clinical data** that
mimics the structure of the real datasets. This lets us build, test, and validate the *entire
pipeline end-to-end* with zero data-access risk. When MIMIC/UCI access is granted, we swap the data
loader — nothing else changes.

**Repository:** https://github.com/Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field
**Degree:** MSc AI/Data Science — Heriot-Watt University Dubai
**Student:** Chaouki Ouadah
**Supervisor:** Radu-Casian Mihailescu, Ph.D.

---

## 1. Project Thesis & Research Questions

**Primary RQ:** How can multi-agent argumentation frameworks, augmented by LLMs and RAG, improve the
explainability and trustworthiness of clinical decision support systems?

| ID | Sub-Question | Components |
|----|-------------|-----------|
| SRQ1 | How can Walton's schemes integrate with LLM debate to produce clinical explanations? | Argumentation engine |
| SRQ2 | How do different RAG approaches affect factual grounding of multi-agent reasoning? | Vector vs GraphRAG vs Hybrid |
| SRQ3 | How do information-partitioned agents (history/diagnostics/treatment) affect outcomes? | Agent design |
| SRQ4 | What metrics beyond accuracy (explainability, process, trust) work best? | Evaluation |

**The novel contribution:** First system to combine **KG-RAG + multi-agent argumentation + symbolic
Dung's AAF resolution + information partitioning** with multi-dimensional evaluation (not just accuracy).

---

## 2. The Surrogate-Data-First Strategy (Track 1)

### Why surrogate data
- MIMIC credentialing (PhysioNet + CITI "Data or Specimens Only Research") is pending.
- We must not block implementation on data access.
- Surrogate data lets us prove the pipeline works, write tests, and demo to supervisor.

### What "surrogate data" means here
A `SurrogatePatientGenerator` produces synthetic tabular rows that **structurally match** the primary
target dataset (Myocardial Infarction Complications, UCI #579): ~111 features across 17 clinical
domains, 12 complication targets, realistic missingness, clinically plausible correlations.

### Design rule: dataset-agnostic loader
All data flows through one interface: `BaseDatasetLoader`. We implement `SurrogateLoader` first.
Later, `MIMICLoader` / `UCILoader` implement the same interface → **no pipeline changes** to swap.

```python
class BaseDatasetLoader(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame: ...
    @abstractmethod
    def feature_domains(self) -> dict[str, list[str]]: ...   # domain -> [columns]
    @abstractmethod
    def targets(self) -> list[str]: ...
    @abstractmethod
    def variable_dictionary(self) -> dict[str, dict]: ...     # code -> human meaning
```

### Surrogate generator requirements
- Configurable N patients (default 1,700).
- 78 binary, 22 ordinal, 11 continuous features (match real shape).
- Inject correlations (e.g., anterior MI ↑ AV-block risk; prior HF ↑ ZSN).
- Inject ~10–15% missingness per column.
- Deterministic via seed for reproducible tests.
- Output ground-truth complication labels so evaluation works.

---

## 3. System Architecture (Data Flow)

```
Tabular patient row (surrogate now, MIMIC later)
   → Clinical Vignette Generator (templates + LLM glue)   tabular → clinical English
   → Feature Partitioner (split 111 feats → 3 domain masks)
   → scispaCy NER (entities)
   → KG Retrieval (Vector/GraphRAG/Hybrid, per-agent context)
   → 3 LLM Agents debate (History&Risk / Diagnostic / Treatment) [LangGraph]
   → Symbolic Resolution (Dung's AAF + Walton schemes)
   → Explanation Generator (LLM + arg tree → narrative)
   → OUTPUT: recommendation + explanation + arg tree + confidence
```

### The 3 agents + supervisor
| Agent | Sees (~feat) | Role |
|-------|--------------|------|
| History & Risk | demographics, prior MI, comorbidities, vitals (~37) | "Who is this patient?" |
| Diagnostic | ECG, MI location, labs, admission status (~46) | "What's happening now?" |
| Treatment & Progression | meds, fibrinolytics, pain/opioid trends (~28) | "What was done, how responding?" |
| Supervisor | all 111 | moderator, convergence, gap detection |

Information partitioning (not tone/attitude prompts) is the independent variable — agents disagree
because they hold different data, mirroring a real Multidisciplinary Team.

---

## 4. Tech Stack (pinned)

| Layer | Tool | Notes |
|-------|------|-------|
| Orchestration | LangGraph 1.0.9 | graph state machine, debate rounds |
| KG-RAG | Microsoft GraphRAG 3.0.2 + Neo4j 5.x | + ChromaDB vector store |
| LLM primary | Llama-3-Meditron-8B via Ollama | local, free |
| LLM baseline | GPT-4o (API) | comparison only |
| Embeddings | BGE-large-en-v1.5 | |
| NER | scispaCy en_core_sci_lg | |
| Argumentation | NetworkX (custom Dung's AAF) | |
| UI | Streamlit + Graphviz | arg tree viz |
| Tracking | MLflow | experiments |
| Python | >= 3.10 | venv |

For Track 1 you may stub Neo4j/GraphRAG with ChromaDB-only RAG to move fast; keep the interface ready.

---

## 5. Directory Structure (create this)

```
Dissertation - Copy/
├── IMPLEMENTATION_CONTEXT.md   ← this file
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example                # OPENAI_API_KEY etc.
├── data/
│   ├── surrogate/              # generated synthetic patients
│   ├── mi_complications/       # later (UCI #579)
│   └── knowledge/              # guideline PDFs for RAG
├── src/
│   ├── data/loaders.py         # BaseDatasetLoader, SurrogateLoader
│   ├── data/surrogate.py       # SurrogatePatientGenerator
│   ├── agents/{history_risk,diagnostic,treatment,supervisor}.py
│   ├── argumentation/{framework,schemes,resolver,explanation}.py
│   ├── knowledge/{retriever,graph_rag,neo4j_client}.py
│   ├── pipeline/{graph,state,runner}.py
│   ├── evaluation/{metrics,baselines,analysis}.py
│   └── utils/{vignette_generator,feature_partitioner,prompts}.py
├── ui/app.py
├── experiments/{configs,results}
└── tests/{test_surrogate,test_partition,test_argumentation,test_pipeline}.py
```

---

## 6. Build Order (TDD — write test first each step)

1. **Repo skeleton + venv + requirements** (`git init`, push to remote).
2. **SurrogatePatientGenerator** + `SurrogateLoader` → test shape, missingness, labels.
3. **FeaturePartitioner** → test 3 masks are disjoint and cover domains.
4. **Vignette Generator** (templates only first, LLM glue later) → test deterministic decode.
5. **One agent (History&Risk)** stub → returns structured args from its partition.
6. **3 agents in LangGraph** with mock convergence.
7. **Dung's AAF resolver** (NetworkX) → test preferred extensions on toy graph.
8. **Explanation generator**.
9. **Evaluation metrics** (multi-label F1, recall, explainability) on surrogate.
10. **Streamlit UI** arg-tree viz.
11. **RAG** (ChromaDB) then GraphRAG/Neo4j.
12. **Swap loader → real data** once MIMIC/UCI access granted.

Each step: RED (failing test) → GREEN (impl) → REFACTOR. Keep modules small.

---

## 7. Setup Commands

```powershell
cd "C:\Projects\Dissertation - Copy"
python -m venv venv ; .\venv\Scripts\Activate.ps1
pip install -U langgraph langchain langchain-openai langchain-community
pip install graphrag chromadb neo4j scispacy networkx streamlit mlflow pandas numpy pytest
pip install transformers torch accelerate
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz
git init ; git remote add origin https://github.com/Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field
```

---

## 8. Evaluation (start on surrogate, repeat on real)
Dimensions: (1) Clinical outcome — multi-label F1 macro/micro, per-complication recall; (2) Explainability;
(3) Process transparency — debate depth, attack rate; (4) Trust — calibration (ECE); (5) Robustness;
(6) Information fusion — cross-domain discovery. Baselines B1–B5, ablations A1–A5 (see roadmap).

---

## 9. Datasets (later, after credentialing)
- Primary: UCI #579 MI Complications (CC-BY 4.0) — surrogate mimics this.
- Secondary: CKD (UCI #336), Heart Failure (UCI #519).
- MIMIC-IV / IV-Note / CXR-JPG after PhysioNet + CITI approval.

## 10. Guardrails
- Research prototype only, not clinical advice (label all outputs).
- No real patient data in surrogate track. Pin versions. Keep loader interface stable.
- Commit often, small PRs, tests must pass before merge.

---

## Appendix A: Surrogate Generator Skeleton

```python
# src/data/surrogate.py
import numpy as np, pandas as pd

DOMAINS = {
    "history_risk": ["AGE","SEX","INF_ANAM","STENOK_AN","FK_STENOK","GB","SIM_GIPERT","ZSN_A"],
    "diagnostic":   ["S_AD_ORIT","D_AD_ORIT","K_BLOOD","Na_BLOOD","ALT_BLOOD","AST_BLOOD",
                      "L_BLOOD","ROE","ant_im","lat_im","inf_im","post_im","ritm_ecg"],
    "treatment":    ["FIBR_TER","NA_R_1_n","NOT_NA_1_n","TRENT","NITR_S","B_BLOK","ASP","TIKL"],
}
TARGETS = ["FIBR_PREDS","PREDS_TAH","JELUD_TAH","FIBR_JELUD","A_V_BLOK","OTEK_LANC",
           "RAZRIV","DRESSLER","ZSN","REC_IM","P_IM_STEN","LET_IS"]

def generate(n=1700, missing=0.12, seed=42):
    rng = np.random.default_rng(seed)
    cols = sum(DOMAINS.values(), [])
    X = pd.DataFrame(rng.integers(0,3,size=(n,len(cols))), columns=cols)
    X["AGE"] = rng.integers(40,90,n); X["SEX"] = rng.integers(0,2,n)
    # correlations: anterior MI -> AV block; prior HF -> heart failure
    y = pd.DataFrame(0,index=X.index,columns=TARGETS)
    y["A_V_BLOK"] = (X["ant_im"]>1).astype(int) & (rng.random(n)<0.3)
    y["ZSN"]      = (X["ZSN_A"]>0).astype(int) | (rng.random(n)<0.2)
    mask = rng.random(X.shape)<missing; X = X.mask(mask)
    return X, y
```

## Appendix B: Dung's AAF Resolver

```python
# src/argumentation/resolver.py
import itertools
def preferred_extensions(args:set, attacks:set):
    def conflict_free(s): return not any(a in s and b in s for a,b in attacks)
    def defends(s,a): return all(any((d,att) in attacks for d in s)
                                 for att in args if (att,a) in attacks)
    admissible=[set(c) for k in range(len(args)+1)
                for c in itertools.combinations(args,k)
                if conflict_free(set(c)) and all(defends(set(c),a) for a in c)]
    return [s for s in admissible if not any(s<t for t in admissible)]
```

## Appendix C: LangGraph State + Agent Prompt Skeleton

```python
class DebateState(TypedDict):
    patient_case: dict; partitions: dict; kg: dict
    arguments: Annotated[list, operator.add]; attacks: list
    round: int; converged: bool; extension: list; explanation: str
```

Agent prompt = role + VISIBLE partition + CANNOT-SEE list + "use Walton schemes, cite feature
values, challenge conflicting claims, flag missing data." Three roles: History&Risk, Diagnostic,
Treatment&Progression. Full templates are in the roadmap's Appendix B — copy verbatim.

## Appendix D: Definition of Done (Track 1)
End-to-end run on surrogate data → 3 agents debate → AAF resolves → explanation + arg tree shown in
Streamlit → metrics logged in MLflow → all tests green → pushed to GitHub. Then swap loader for real data.
```
