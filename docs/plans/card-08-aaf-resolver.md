# Plan — Card 8: Dung's AAF + preferred-extension resolver

## Context
The debate (Card 7) produces `Argument`s + cross-modal `Attack`s but nothing yet *resolves* which
arguments win. Card 8 adds the **symbolic layer**: build Dung's Abstract Argumentation Framework
⟨A, R⟩ (A = arguments, R = attacks) as a NetworkX digraph, then compute **preferred extensions**
(maximal admissible sets) — the sets of arguments that mutually survive the cross-modal conflict.
Per IMPLEMENTATION_CONTEXT §4 (dissertation pp.41–43). Branch `feature/aaf`.

Also folds in (user request) the **stashed pip-audit chromadb ignore** (`stash@{0}`): PYSEC-2026-311
is ChromaDB *server-mode* RCE, unreachable (we use embedded EphemeralClient), no fixed release yet.

## Decisions (Dung semantics, dissertation-faithful)
- **AAF node identity = claim string.** `Attack` references `source_claim`/`target_claim` (strings),
  so nodes are keyed by `Argument.claim`; each node stores its `Argument` as an attr. An attack edge
  is added only when both endpoints exist as argument nodes (dangling attacks ignored).
- **Unweighted Dung** (plain AAF). Walton-scheme weighting is Card 9 — out of scope here.
- **Preferred = maximal admissible.** Compute by enumerating subsets of the *controversial* nodes
  (those with ≥1 attack edge); isolated/unattacked args are always included (they break no
  conflict-freeness and have no attackers to defend against). Practical because the supervisor yields
  few attacks → the controversial subgraph is small. Documented; swap to a dedicated solver if it
  ever grows. Extensions returned as `list[set[str]]` (claim ids); `AAF.argument(claim)` maps back.
- **Semantics functions are pure** and operate on an `AAF`: `conflict_free`, `defends`, `admissible`,
  `preferred_extensions`.

## State map
- `framework.py` — has `Argument` + `Attack` (Card 4/7). Add `AAF` (NetworkX wrapper).
- `resolver.py` — docstring-only stub. Implement the Dung semantics here.
- `tests/test_argumentation.py` — skip-placeholder. Replace with the RED toy-graph suite.
- networkx 3.6.1 installed + pinned (`requirements.txt:36`).

## Approach (files)
- **`src/argumentation/framework.py`** — add `AAF`:
  - `__init__(arguments: list[Argument], attacks: list[Attack])` → builds `nx.DiGraph`; nodes =
    claims (attr `argument`), edges = attacks (attr `attack`).
  - props/helpers: `arguments`, `attacks` (edge list), `claims`, `argument(claim)`, `attackers(claim)`.
- **`src/argumentation/resolver.py`** — pure Dung semantics over an `AAF`:
  - `conflict_free(aaf, S)` — no attack edge within S.
  - `defends(aaf, S, a)` — every attacker of `a` is attacked by some member of S.
  - `admissible(aaf, S)` — conflict-free ∧ S defends each of its members.
  - `preferred_extensions(aaf) -> list[set[str]]` — maximal admissible sets (controversial-subgraph
    enumeration + always-in isolated args; dedup; maximal-only).
  - (optional helper) `grounded_extension` — NOT in AC; skip to keep scope tight.
- **`tests/test_argumentation.py`** — toy graphs (claims a/b/c…): no attacks → all args; single
  attack; 2-cycle → two extensions; 3-cycle (odd) → empty extension; defended chain (a→b→c) → {a,c};
  empty AAF → [∅]; plus `conflict_free`/`admissible`/`defends` unit checks and an AAF-build test
  (dangling attack ignored, node/edge counts).
- **fold-in:** `git stash pop stash@{0}` → ci.yml + security.yml `--ignore-vuln PYSEC-2026-311` +
  requirements.txt justification comment.

Reuse: `Argument`/`Attack` (framework.py), networkx.

## Out of scope (verbatim from cards.md Card 8 + this)
- Walton-7 scheme enum + critical questions + scheme weighting (Card 9).
- Explanation narrative (Card 9). Wiring the resolver into `pipeline/graph.py` / populating
  `DebateState.extension` (later — keep Card 8 to framework + resolver + tests per card's file list).
- GraphRAG/Neo4j (Card 10); UI arg-tree (Card 13).

## Verification matrix (AC → test)
- AC "empty attacks → all args" → `test_no_attacks_all_in` (3 args, 0 attacks → one ext = all 3).
- AC "2-cycle → two extensions" → `test_two_cycle_two_extensions` ({a},{b}).
- AC "defended arg included" → `test_defended_arg_included` (a→b→c → {a,c}, c present).
- AC "returns maximal admissible sets" → `test_preferred_are_maximal_admissible` (each ext admissible;
  none is a subset of another) + `test_odd_cycle_empty` (3-cycle → [∅]).
- Build correctness → `test_aaf_build_nodes_edges` + `test_dangling_attack_ignored`.
- Semantics units → `test_conflict_free`, `test_admissible_defends`.

## Risks + rollback
- Subset enumeration is exponential in the controversial-node count — bounded because attacks are
  few; documented assumption. Rollback: revert branch.
- Claim-string node identity collides if two args share an identical claim — attack then applies to
  the shared node (acceptable; claims are effectively unique in practice). Noted in docstring.
- Folding the pip-audit chore into a feature PR mixes concerns — explicit user request; called out
  in the PR body.

## Phase plan
- P0 branch `feature/aaf` + `git stash pop`. P2 `AAF` (framework) + `resolver.py`. P5 tests
  (RED→GREEN, all pure — no LLM). P7 self-audit + `/security-review`. P8 gate (pip-audit now clean
  via the ignore). P9 PR → STOP. Skip P1/P3/P4/P6/P10.

## Commit (one PR: `feature/aaf`)
`feat(argumentation): Dung's AAF + preferred-extension resolver` — AAF NetworkX wrapper +
conflict-free/admissible/preferred semantics; pure toy-graph tests. Plus
`chore(security): ignore non-reachable chromadb advisory PYSEC-2026-311 in pip-audit`.
ruff/ruff-format/mypy/bandit/pip-audit green; /security-review run. STOP for merge.
