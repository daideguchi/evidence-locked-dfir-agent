# Devpost Draft — Evidence-Locked DFIR Agent

## Tagline

AI-assisted incident response where every claim must cite evidence.

## What It Does

Evidence-Locked DFIR Agent helps analysts investigate suspicious activity without letting an AI summary outrun the evidence.

The prototype takes a suspicious email investigation and turns it into:

- an evidence chain
- a hypothesis table
- a guardrail table
- a timeline
- a human containment decision
- a record of unsupported claims that the AI must not present as fact

## Demo Story

A security analyst opens a suspicious email investigation.

The agent collects email headers, attachment hash, browser timeline, and endpoint process information. It initially considers whether malware executed on the endpoint, but then marks that claim as unsupported because the process evidence is missing.

The report keeps the phishing hypothesis as low-to-medium confidence, redacts a low-confidence indicator output, and leaves containment to a human analyst.

## Why It Matters

AI can help defenders move faster, but speed is dangerous if an AI turns weak evidence into confident claims.

This project shows the safer pattern: AI can suggest, organize, and accelerate, but every conclusion is tied to evidence and unsupported claims stay visibly provisional.

## Built With

- Shared AgentOps event stream
- Evidence-locked DFIR report generator
- Static HTML report
- Sanitized synthetic DFIR case data

Current local artifacts:

- `prototype/evidence-locked-dfir-report.html`
- `media/evidence-locked-dfir-report-full.png`
- `reports/dfir-case-packet.json`
- `../shared-agentops-engine/adapters/findevil/dfir_report.md`

## Claim Boundary

This is currently a local prototype generated from sanitized evidence events.

Do not claim live SIFT execution or real forensic tooling until it is actually verified.
