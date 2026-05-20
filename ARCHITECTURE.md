# Architecture — Evidence-Locked DFIR Agent

## One Sentence

Evidence-Locked DFIR Agent is a local, SIFT-ready investigation workflow that
lets AI organize a DFIR case while forcing every supported conclusion to cite a
concrete evidence artifact.

## Data Flow

```text
Sanitized case data
  email headers
  hash lookup
  browser timeline
  process list
  network observations
        |
        v
Local evidence parser
        |
        v
Claim builder + evidence lock
        |
        +--> supported claim only when evidence IDs exist
        +--> unsupported claim downgraded instead of promoted
        +--> containment action held for human approval
        |
        v
Outputs
  terminal transcript
  analyst report
  accuracy report
  execution log
  public demo page
```

## Components

- `findevil/case_data/` - packaged sanitized case artifacts.
- `findevil/scripts/run_evidence_locked_agent.py` - terminal demo and local
  deterministic agent run.
- `findevil/scripts/build_dfir_case_report.py` - HTML analyst report builder.
- `findevil/reports/agent-claims.json` - claim/status/evidence output.
- `findevil/reports/accuracy-report.md` - ground-truth comparison.
- `findevil/reports/evidence-lock-execution-log.jsonl` - replayable execution
  record.
- `findevil/prototype/evidence-locked-dfir-report.html` - analyst review UI.
- `findevil/prototype/terminal-session.html` - terminal transcript UI.

## Human-AI Boundary

The AI can:

- parse case artifacts
- propose claims
- bind claims to evidence IDs
- downgrade unsupported hypotheses
- draft an analyst report

The AI cannot:

- present unsupported execution as fact
- approve endpoint isolation
- hide redactions or low confidence
- claim live SIFT execution unless it was actually run

## Submission Boundary

This repository demonstrates a verified local prototype with SIFT-shaped
artifacts and a terminal workflow. It does not claim live SANS SIFT execution or
real malware attribution.
