# data/

| Dir | Contents | Tracked? |
|-----|----------|----------|
| `surrogate/` | Synthetic patients from `SurrogatePatientGenerator` (regenerable, seed=42) | No (gitignored) |
| `mi_complications/` | UCI #579 MI Complications — **only after** dataset download | No |
| `knowledge/` | Clinical guideline PDFs for RAG | No |

**Guardrail:** No real patient data in the surrogate track. MIMIC/UCI data enters only after
PhysioNet + CITI credentialing (see `Track2_MIMIC_Credentialing_Guide.md`). Nothing here is
committed — surrogate data is regenerable; real data must never be pushed.
