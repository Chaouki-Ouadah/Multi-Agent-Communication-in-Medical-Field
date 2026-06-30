# data/

Track-1 surrogate datasets (real, open-licensed — mirror MIMIC formats). Swap to real MIMIC later.

| Dir | Contents | Source | Tracked? |
|-----|----------|--------|----------|
| `chestxray14/` | CXR images + labels (Vision Agent) | NIH ChestX-ray14 (CC0) | No (gitignored) |
| `openi/` | CXR-report pairs (Report Agent) | OpenI Indiana University | No |
| `mimic_demo/` | structured EHR (Clinical Agent) | MIMIC-IV Demo (open access) | No |
| `mimic/` | real MIMIC-CXR/IV-Note/IV — **only after credentialing** | PhysioNet | No |
| `knowledge/` | guideline + ontology sources for GraphRAG | ACR/Fleischner/ESC, UMLS/SNOMED/ICD-10/PrimeKG | No |

**Guardrail:** Track-1 surrogates are open-licensed and may be downloaded freely. **Credentialed/real
MIMIC data enters only after PhysioNet + CITI + Heriot-Watt ethics approval** (see
`Track2_MIMIC_Credentialing_Guide.md`). Nothing here is committed; never push real patient data.
