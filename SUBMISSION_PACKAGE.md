# Submission Package — Evidence-Locked DFIR Agent

## Project Title

Evidence-Locked DFIR Agent

## Short Description

AI-assisted incident response where every claim must cite evidence and unsupported certainty is treated as a risk.

## Repository

https://github.com/daideguchi/evidence-locked-dfir-agent

## Try It Out

Open these local demo files after cloning the repository:

- `findevil/prototype/evidence-locked-dfir-report.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `findevil/media/evidence-locked-dfir-report-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Demo Video

Draft silent video:

- `findevil/media/evidence-locked-dfir-agent-demo-draft.mp4`

Regenerate:

```bash
cd findevil
bash scripts/build_demo_video.sh
```

## Inspiration

AI can help defenders move faster, but fast summaries are dangerous when they outrun the evidence.

This project starts from a defensive rule: an AI investigation assistant should organize, cite, and accelerate, but it should not turn weak evidence into confident claims.

## What It Does

Evidence-Locked DFIR Agent turns a suspicious email investigation into:

- an evidence chain
- a timeline
- hypothesis status
- guardrail events
- redaction events
- human containment approval
- explicit self-correction when a claim is unsupported

## How We Built It

- Shared AgentOps event stream
- Sanitized DFIR case packet
- Evidence-locked report generator
- Static HTML investigation report
- Guardrail model for unsupported claims and redactions

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- Sanitized synthetic DFIR events

## What Is Working

```text
verify_ok
status: ok
event_count=8
self_correction_events=1
redactions=1
```

## Verification Commands

```bash
cd shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd ../findevil
python3 scripts/build_dfir_case_report.py
bash scripts/build_demo_video.sh
```

## Demo Script Summary

1. Show the suspicious email case.
2. Show the evidence chain and event timeline.
3. Show the unsupported malware-execution claim being corrected.
4. Show redaction and human containment approval.
5. Explain why evidence-locking matters for AI-assisted DFIR.

## What Makes It Different

The agent is not rewarded for sounding confident. It is constrained to evidence.

That makes the product safer for incident response, where unsupported certainty can cause real damage.

## Challenges

The main challenge was keeping the demo compelling while avoiding unsupported forensic claims. The case is intentionally sanitized and evidence-bound.

## Accomplishments

- Built an evidence-locked DFIR report
- Added self-correction for unsupported claims
- Added redaction and human approval events
- Published a clean public repository

## What We Learned

In security work, AI assistance is only useful when evidence stays visible.

## What's Next

Connect the workflow to real forensic tooling or SIFT-style artifacts after the platform path is verified.

## Claim Boundary

This is a local verified prototype using sanitized evidence events.

It does not claim live forensic tooling or real malware attribution.
