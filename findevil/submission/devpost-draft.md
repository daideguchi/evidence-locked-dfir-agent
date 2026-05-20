# Devpost Draft — Evidence-Locked DFIR Agent

## Tagline

AI-assisted incident response where every claim must cite evidence.

## What It Does

Evidence-Locked DFIR Agent helps analysts investigate suspicious activity without letting an AI summary outrun the evidence.

The prototype runs a local terminal workflow against a packaged suspicious-email case. It parses email headers, attachment hash data, browser timeline events, endpoint process data, and network observations. Then it produces:

- an evidence-bound claim table
- a terminal transcript
- an analyst report
- an accuracy report against packaged ground truth
- a replayable execution log
- a human approval gate for containment

## Demo Story

A security analyst opens a suspicious payroll email investigation.

The agent finds enough evidence to support a phishing email claim, a suspicious attachment claim, and a download claim. Then it reaches the dangerous question: did malware execute?

Instead of sounding confident, the agent blocks that claim. The process listing does not show Word, a macro host, shell activity, or a child process chain, so the report marks malware execution as `not_supported_by_current_evidence`.

The agent can help the analyst move faster, but it cannot approve endpoint isolation or turn weak evidence into fact.

## Why It Matters

AI can help defenders move faster, but speed is dangerous if an AI turns weak evidence into confident incident claims.

This project shows the safer pattern: AI can suggest, organize, and accelerate, but every conclusion is tied to evidence and unsupported claims stay visibly provisional.

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- ImageMagick
- ffmpeg
- Edge TTS neural narration
- Sanitized suspicious-email case data

## Current Local Artifacts

- YouTube demo: `https://www.youtube.com/watch?v=Z0kuG3GabyY`
- `findevil/case_data/`
- `findevil/scripts/run_evidence_locked_agent.py`
- `findevil/scripts/run_findevil_local_checks.sh`
- `findevil/prototype/evidence-locked-dfir-report.html`
- `findevil/prototype/terminal-session.html`
- `findevil/reports/agent-claims.json`
- `findevil/reports/accuracy-report.md`
- `findevil/reports/evidence-lock-execution-log.jsonl`
- `findevil/media/evidence-locked-dfir-agent-demo.mp4`
- `ARCHITECTURE.md`

## Verification Output

```text
findevil_local_checks_ok
claims_total=5
exact_status_accuracy=1.0
unsupported_claims_blocked=1
false_confident_supported_claims=0
claim_boundary=verified_local_sift_ready_no_live_sift_execution_claim
```

## Claim Boundary

This is a local verified prototype generated from sanitized evidence files.

Do not claim live SIFT execution, real victim data, real forensic tooling, or real malware attribution until those integrations are separately verified.
