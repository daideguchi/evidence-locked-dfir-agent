# Manual Devpost Submit Guide — FIND EVIL!

Use this if Devpost automation hits reCAPTCHA.

## Links

- Hackathon: https://findevil.devpost.com/
- Repository: https://github.com/daideguchi/evidence-locked-dfir-agent
- Live demo: https://daideguchi.github.io/evidence-locked-dfir-agent/
- YouTube demo: https://www.youtube.com/watch?v=Z0kuG3GabyY
- Submission package: https://raw.githubusercontent.com/daideguchi/evidence-locked-dfir-agent/main/SUBMISSION_PACKAGE.md
- Architecture: https://raw.githubusercontent.com/daideguchi/evidence-locked-dfir-agent/main/ARCHITECTURE.md
- Terminal proof: https://daideguchi.github.io/evidence-locked-dfir-agent/findevil/prototype/terminal-session.html
- Accuracy report: https://raw.githubusercontent.com/daideguchi/evidence-locked-dfir-agent/main/findevil/reports/accuracy-report.md

## Project Name

```text
Evidence-Locked DFIR Agent
```

## Elevator Pitch

```text
AI-assisted incident response where every claim must cite evidence and unsupported certainty is treated as a risk.
```

## Inspiration

```text
AI can help defenders move faster, but in incident response, speed is dangerous when it creates confidence without evidence.

The idea behind Evidence-Locked DFIR Agent is simple: an AI assistant should help an analyst organize a case, but it should never turn weak evidence into a confident forensic claim. If the evidence stops, the AI must stop too.
```

## What It Does

```text
Evidence-Locked DFIR Agent runs a local terminal workflow against a packaged suspicious-email case.

It parses email headers, attachment hash data, browser timeline events, endpoint process data, and network observations. Then it creates an evidence-bound claim table.

The important moment is the malware-execution claim. A normal AI summary might be tempted to say the document executed. This agent refuses to mark that as proven because the process list does not show Word, a macro host, shell activity, or a child process chain.

The product outputs:
- a terminal transcript
- an evidence-bound analyst report
- an accuracy report against packaged ground truth
- a replayable execution log
- a human approval gate for containment
- a GitHub Pages review hub
- a narrated demo video
```

## How We Built It

```text
We built a deterministic local DFIR agent in Python.

The case data lives in inspectable files: email headers, attachment hash lookup, browser timeline, endpoint process list, network observations, and packaged ground truth.

The agent converts those artifacts into claims. A claim can only be marked supported when it cites concrete evidence IDs. Unsupported claims are explicitly downgraded to not_supported_by_current_evidence, and endpoint isolation stays behind human review.

The static review hub, analyst report, terminal proof page, architecture diagram, accuracy report, and demo video are all generated from the repository artifacts.
```

## Built With

```text
Python, HTML, CSS, JSON, JSONL, ImageMagick, ffmpeg, Edge TTS, sanitized DFIR case data
```

## Challenges

```text
The biggest challenge was making the project compelling without overclaiming.

Security demos often make AI look good by letting it sound confident. DFIR needs the opposite. The agent had to show useful acceleration while also showing where the evidence is not strong enough.

That meant the demo needed concrete artifacts, terminal execution, ground-truth scoring, and a visible boundary around live forensic tooling.
```

## Accomplishments

```text
- Built a terminal-executable local DFIR agent.
- Added packaged suspicious-email case data.
- Added evidence-bound claim generation.
- Added an unsupported malware-execution guardrail.
- Added an accuracy report against ground truth.
- Added a replayable execution log.
- Added a human containment approval gate.
- Added a GitHub Pages review hub and natural English demo video.
```

## What We Learned

```text
For incident response, AI is only useful when analysts can see why a conclusion was made and where the evidence stops.

The best defensive AI is not the most confident one. It is the one that knows how to stay inside the evidence.
```

## What's Next

```text
- Connect the parser to live SANS SIFT artifacts.
- Add larger case packets and analyst feedback loops.
- Add a model-assisted summarizer that can only quote approved evidence IDs.
- Export incident tickets and handoff reports.
- Add live tool execution only after it is separately verified.
```

## Try It Out / Installation

```text
Live demo:
https://daideguchi.github.io/evidence-locked-dfir-agent/

Local verification:
git clone https://github.com/daideguchi/evidence-locked-dfir-agent
cd evidence-locked-dfir-agent
bash findevil/scripts/run_findevil_local_checks.sh
```

## Verification Proof

```text
findevil_local_checks_ok
claims_total=5
exact_status_accuracy=1.0
unsupported_claims_blocked=1
false_confident_supported_claims=0
video_seconds=84.0
claim_boundary=verified_local_sift_ready_no_live_sift_execution_claim
```

## Claim Boundary

```text
This is a verified local prototype using sanitized case data.

It does not claim live SANS SIFT execution, live forensic tooling, real victim data, real malware attribution, or automated endpoint isolation.
```
