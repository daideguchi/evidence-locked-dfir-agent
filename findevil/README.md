# Evidence-Locked DFIR Agent

Target: FIND EVIL!

URL: https://findevil.devpost.com/

Status: Devpost joined. P2 derivative security lane.

Current local proof:

- Evidence-locked DFIR report: `prototype/evidence-locked-dfir-report.html`
- Report screenshot: `media/evidence-locked-dfir-report-full.png`
- Case packet: `reports/dfir-case-packet.json`
- Builder: `scripts/build_dfir_case_report.py`

![Evidence-Locked DFIR Agent report](media/evidence-locked-dfir-report-full.png)

## Position

P2 derivative security lane.

This lane should reuse the shared engine, but package it as a defensive investigation workflow.

## Product Thesis

AI can help incident responders move faster, but only if every conclusion is tied to evidence.

Evidence-Locked DFIR Agent helps analysts investigate suspicious activity while forcing every hypothesis, summary, and next action to cite an artifact or event.

## MVP

- ingest sample forensic artifacts
- generate investigation timeline
- detect suspicious pivots
- produce evidence-cited hypothesis
- record self-correction when evidence contradicts a hypothesis
- export analyst report

## Shared Engine Use

Reuse:

- event timeline
- risk signals
- approval/handoff events
- evidence-grounded summary

Adapt:

- evidence_ref becomes artifact ID
- risk signals become suspicious indicators
- handoff report becomes analyst report

Current generated artifacts:

- Shared engine: `../shared-agentops-engine/`
- Canonical events: `../shared-agentops-engine/data/agentops_events.jsonl`
- DFIR report: `../shared-agentops-engine/adapters/findevil/dfir_report.md`
- Handoff report: `../shared-agentops-engine/reports/handoff_report.md`

Build the FIND EVIL-focused local demo:

```bash
cd /Users/dd/000_AI組織/__hackason/findevil
python3 scripts/build_dfir_case_report.py
```

Expected proof:

- builder returns `status: ok`
- `prototype/evidence-locked-dfir-report.html` exists
- `reports/dfir-case-packet.json` exists
- screenshot exists at `media/evidence-locked-dfir-report-full.png`

The strongest story for this lane is not "AI solves forensics alone."

The story is:

```text
AI can accelerate an investigation only when every claim is tied to evidence, unsupported certainty is caught, and a human analyst keeps final control.
```

## Immediate Next Steps

1. Confirm SANS/SIFT resources and rules.
2. Expand the sanitized DFIR sample dataset.
3. Add screenshots from the evidence report and event dashboard.
4. Avoid unsupported malware claims unless the evidence packet proves them.

Current boundary:

- Safe claim: an evidence-locked DFIR report, self-correction event, redaction event, and human containment approval are generated from the shared event stream.
- Do not claim: live forensic tooling or SIFT execution until it is actually run and verified.
