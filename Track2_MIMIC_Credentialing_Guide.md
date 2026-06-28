# Track 2 — MIMIC Credentialed Data Access Guide

**Project:** Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems
**Student:** Chaouki Ouadah (H00498420) — `co4004@hw.ac.uk`
**Supervisor:** Dr Radu-Casian Mihailescu
**Institution:** Heriot-Watt University Dubai

---

## Purpose

Track 2 is the **PhysioNet credentialing path** that grants legal access to the real MIMIC
multimodal datasets (MIMIC-CXR-JPG, MIMIC-IV, MIMIC-IV-Note). It runs **in parallel** with
Track 1 (building the pipeline on non-credentialed surrogate datasets) so development is
never blocked while approval is pending.

> **Why two tracks?** MIMIC requires credentialed access (CITI training + Data Use Agreement),
> and approval can take days to ~2 weeks. Track 1 builds the full system on surrogate data
> (NIH CXR14, OpenI, MIMIC-IV Demo) immediately; Track 2 swaps in real MIMIC data once
> credentialing clears — same code, real linked data.

---

## Critical Path — Start These First

These items depend on **other people or waiting periods**, so begin them on day one:

| Item | Why it's on the critical path |
|------|-------------------------------|
| CITI training | Several hours of modules; cannot be rushed |
| Supervisor reference | Depends on Dr Mihailescu responding to the reference request |
| PhysioNet approval | Days to ~2 weeks of review after submission |

Everything else (signing DUAs, downloading, cohort building) is fast once approval lands.

---

## Step 1 — Create a PhysioNet Account

1. Go to **https://physionet.org/register/**
2. Register using the **Heriot-Watt email** (`co4004@hw.ac.uk`) — an institutional/academic
   email strengthens the credentialing application.
3. Verify the email and complete the profile:
   - Full name
   - Institution = **Heriot-Watt University Dubai**

---

## Step 2 — Complete CITI "Data or Specimens Only Research" Training

This produces the certificate PhysioNet requires. It is the slowest single step, so start now.

1. Go to **https://www.citiprogram.org/**
2. Register. When asked to affiliate, search for **"Massachusetts Institute of Technology"**
   (MIT is the official CITI portal PhysioNet recognises — you do **not** need to be an MIT
   student).
   - If Heriot-Watt has its own CITI subscription, that can be used instead — confirm with
     the supervisor.
3. Add the course: **"Data or Specimens Only Research."**
4. Complete all modules (typically 8–10 short modules, a few hours total; can be done across
   multiple sessions).
5. Pass the quizzes, then **download the Completion Certificate as a PDF**.
   - Keep the **Report ID / verification number** — PhysioNet uses it to verify completion.

---

## Step 3 — Submit the PhysioNet Credentialing Application

1. Log in, then go to **https://physionet.org/settings/credentialing/**
2. Complete the application:
   - **Reference:** an academic who can vouch for you. Use **Dr Radu-Casian Mihailescu**
     with his official HWU email. Notify him in advance so he approves the reference request
     promptly.
   - **Research description:** briefly describe the MSc project — multi-agent explainable
     clinical decision support; no re-identification; local processing only.
3. **Upload the CITI certificate** PDF.
4. Submit.

> **Approval typically takes a few business days to ~2 weeks.** This is why Step 2 and Step 3
> are started early, while Track 1 development proceeds.

---

## Step 4 — Sign the Data Use Agreement (DUA) for Each Dataset

Once credentialed, the DUA must be accepted on **each dataset page separately**:

| Dataset | URL |
|---------|-----|
| **MIMIC-CXR-JPG** | https://physionet.org/content/mimic-cxr-jpg/ |
| **MIMIC-IV** | https://physionet.org/content/mimiciv/ |
| **MIMIC-IV-Note** | https://physionet.org/content/mimic-iv-note/ |

On each page: scroll to the bottom → read and **accept the DUA** → the download panel unlocks.

---

## Step 5 — File the HWU Ethics Amendment

Because real credentialed data is now in scope, keep the ethics record consistent:

1. Open the existing **Infonetica** ethics submission.
2. Add an amendment noting use of **credentialed MIMIC data under the PhysioNet DUA**:
   - Stored **encrypted, locally**
   - **No re-identification**
   - **No cloud upload** of credentialed data
3. This aligns the ethics approval with the DUA terms.

---

## Step 6 — Download the Data

Once DUAs are accepted, download from the local machine using PhysioNet credentials.

```powershell
# MIMIC-CXR-JPG (large — images; consider downloading only the subset of folders needed)
wget -r -N -c -np --user YOUR_PHYSIONET_USER --ask-password `
  https://physionet.org/files/mimic-cxr-jpg/2.1.0/

# MIMIC-IV structured EHR
wget -r -N -c -np --user YOUR_PHYSIONET_USER --ask-password `
  https://physionet.org/files/mimiciv/3.1/

# MIMIC-IV-Note (radiology reports + discharge summaries)
wget -r -N -c -np --user YOUR_PHYSIONET_USER --ask-password `
  https://physionet.org/files/mimic-iv-note/2.2/
```

> **Storage warning:** the full MIMIC-CXR-JPG set is **>500 GB**. For the 2,000–3,000 study
> subset, **do not download everything**. First pull the metadata/label CSVs
> (`mimic-cxr-2.0.0-metadata.csv`, `mimic-cxr-2.0.0-chexpert.csv`), select the
> `subject_id`/`study_id` cohort, then download only those image folders.

---

## Step 7 — Build the Linked Cohort

1. Load the CXR metadata + CheXpert label CSVs.
2. Select **2,000–3,000 frontal-view (AP/PA) studies**.
3. Join to MIMIC-IV-Note (reports) and MIMIC-IV (EHR) on the shared **`subject_id`**.
4. Store the linked subset locally (encrypted), then swap it into the agent pipelines already
   built on surrogates in Track 1.

---

## Dataset Summary

| Component | What it provides | Scale |
|-----------|------------------|-------|
| **MIMIC-CXR-JPG** | Chest X-ray images + CheXpert 14-label pathology annotations | 377,110 images / 65,379 patients |
| **MIMIC-IV-Note** | Free-text radiology reports + discharge summaries | 2.3M radiology reports |
| **MIMIC-IV v3.1** | Structured EHR — ICD diagnoses, labs, vitals, medications | 364,627 patients |

All three are linked by a shared `subject_id`, enabling the modality-partitioned agents
(Vision / Report / Clinical).

---

## Progress Checklist

- [ ] **T2.1** PhysioNet account created with HWU email
- [ ] **T2.2** CITI "Data or Specimens Only Research" training completed + certificate downloaded
- [ ] **T2.3** Supervisor notified and reference request approved
- [ ] **T2.4** Credentialing application submitted (CITI certificate uploaded)
- [ ] **T2.5** Credentialing approved by PhysioNet
- [ ] **T2.6** DUA signed for MIMIC-CXR-JPG
- [ ] **T2.7** DUA signed for MIMIC-IV
- [ ] **T2.8** DUA signed for MIMIC-IV-Note
- [ ] **T2.9** HWU ethics amendment filed
- [ ] **T2.10** Metadata/label CSVs downloaded
- [ ] **T2.11** Cohort (2,000–3,000 frontal studies) selected and linked on `subject_id`
- [ ] **T2.12** Subset stored encrypted locally and integrated into the pipeline
