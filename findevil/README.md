# Evidence-Locked DFIR Agent

Target: FIND EVIL!

URL: https://findevil.devpost.com/

Status: P2 security lane, upgraded from static report to terminal-executable local prototype.

## Product Thesis

AI can help incident responders move faster, but only if every conclusion is tied to evidence.

Evidence-Locked DFIR Agent helps analysts investigate suspicious activity while forcing every hypothesis, summary, and next action to cite an artifact or event.

## Current Local Proof

- Terminal agent: `scripts/run_evidence_locked_agent.py`
- Local verifier: `scripts/run_findevil_local_checks.sh`
- Case data: `case_data/`
- Analyst report: `prototype/evidence-locked-dfir-report.html`
- Terminal transcript page: `prototype/terminal-session.html`
- Case packet: `reports/dfir-case-packet.json`
- Agent claims: `reports/agent-claims.json`
- Accuracy report: `reports/accuracy-report.md`
- Execution log: `reports/evidence-lock-execution-log.jsonl`
- Demo video: `media/evidence-locked-dfir-agent-demo.mp4`

![Evidence-Locked DFIR Agent report](media/evidence-locked-dfir-report-full.png)

## Run

```bash
cd /Users/dd/000_AI組織/__hackason/evidence-locked-dfir-agent-public
bash findevil/scripts/run_findevil_local_checks.sh
```

Expected proof:

```text
findevil_local_checks_ok
claims_total=5
exact_status_accuracy=1.0
unsupported_claims_blocked=1
false_confident_supported_claims=0
```

## Story

The strongest story for this lane is not "AI solves forensics alone."

The story is:

```text
AI can accelerate an investigation only when every claim is tied to evidence, unsupported certainty is caught, and a human analyst keeps final control.
```

## Boundary

Safe claim:

- A terminal-executable local DFIR workflow runs against packaged sanitized case data and produces evidence-bound claims, a report, accuracy output, and execution logs.

Do not claim:

- Live forensic tooling.
- Live SANS SIFT execution.
- Real malware attribution.
