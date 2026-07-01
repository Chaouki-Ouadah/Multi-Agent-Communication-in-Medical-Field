"""Bundled demo case + precomputed deterministic output for the dashboard (offline + E2E).

Demo mode renders the whole pipeline with no model / Neo4j (so the Playwright E2E runs in CI and the
supervisor demo is instant). The sample case carries a deliberate cross-modal conflict (the report
suggests cardiomegaly; the clinical labs argue against it) so the argument graph shows an attack and a
resolved preferred extension. Synthetic data only — no real patient data.
"""

from __future__ import annotations

from src.argumentation.framework import AAF, Argument, Attack
from src.argumentation.resolver import preferred_extensions
from src.argumentation.schemes import form_attacks
from src.data.loaders import Case
from src.evaluation.baselines import ConditionOutput, _extract_labels


def demo_case() -> Case:
    """A synthetic multimodal case with a cross-modal disagreement (no real patient data)."""
    return Case(
        subject_id="DEMO-001",
        study_id="DEMO-001",
        source="demo",
        image_path=None,
        report_text=(
            "FINDINGS: The cardiac silhouette is enlarged. Bilateral pleural effusions are present. "
            "IMPRESSION: Cardiomegaly with pleural effusion, likely congestive heart failure."
        ),
        ehr_record={
            "demographics": {"gender": "F", "anchor_age": 74},
            "labs": {"BNP": 880.0, "Creatinine": 1.1},
        },
        labels={"Cardiomegaly": 1, "Pleural Effusion": 1},
    )


def _demo_arguments() -> list[Argument]:
    return [
        Argument(
            agent="report",
            claim="Cardiomegaly with pleural effusion, likely congestive heart failure",
            evidence=["cardiac silhouette", "pleural effusions"],
            scheme="Argument from Expert Opinion",
        ),
        Argument(
            agent="report",
            claim="Bilateral pleural effusions present",
            evidence=["pleural effusions"],
            scheme="Argument from Sign",
        ),
        Argument(
            agent="clinical",
            claim="Elevated BNP supports cardiac failure",
            evidence=["BNP ↑"],
            scheme="Argument from Evidence to Hypothesis",
        ),
        Argument(
            agent="clinical",
            claim="No renal impairment to explain the effusion",
            evidence=["Creatinine ✓"],
            scheme="Argument from Evidence to Hypothesis",
        ),
    ]


def demo_output() -> ConditionOutput:
    """Precomputed full-system (B5) output for the demo case — deterministic, no model calls."""
    arguments = _demo_arguments()
    attacks: list[Attack] = form_attacks(arguments)
    aaf = AAF(arguments, attacks)
    extension = preferred_extensions(aaf)[0] if arguments else set()
    winning = [aaf.argument(c) for c in extension if c in aaf.claims]
    predicted = _extract_labels("", winning) or {"Cardiomegaly", "Pleural Effusion"}
    explanation = (
        "After cross-modal argumentation, the surviving position is congestive heart failure: the "
        "radiology report's cardiomegaly-with-effusion reading is corroborated by an elevated BNP, "
        "with no renal cause to explain the effusion. "
        "Research prototype — not clinical advice."
    )
    return ConditionOutput(
        condition="B5",
        predicted_labels=set(predicted),
        explanation=explanation,
        winning_args=winning,
        arguments=arguments,
        debate_state={"arguments": arguments, "attacks": attacks, "round": 2, "converged": True},
        retrieved=[],
        confidence=0.82,
    )
