# Submission Package — Evidence-Locked DFIR Agent

## Project Title

Evidence-Locked DFIR Agent

## Short Description

AI-assisted incident response where every claim must cite evidence and unsupported certainty is treated as a risk.

## Public Links

- Repository: https://github.com/daideguchi/evidence-locked-dfir-agent
- Live demo: https://daideguchi.github.io/evidence-locked-dfir-agent/
- YouTube demo: https://www.youtube.com/watch?v=Z0kuG3GabyY
- Architecture: https://raw.githubusercontent.com/daideguchi/evidence-locked-dfir-agent/main/ARCHITECTURE.md

## Demo Video

YouTube demo:

- https://www.youtube.com/watch?v=Z0kuG3GabyY

Final local demo video:

- `findevil/media/evidence-locked-dfir-agent-demo.mp4`

Compatibility copy:

- `findevil/media/evidence-locked-dfir-agent-demo-draft.mp4`

Regenerate:

```bash
bash findevil/scripts/build_demo_video.sh
```

## The Simple Story

Security analysts do not need an AI that sounds certain. They need an AI that
keeps the evidence visible.

Evidence-Locked DFIR Agent turns a suspicious email case into a terminal-run
investigation where every supported conclusion cites an artifact. When the agent
is tempted to say "malware executed", it blocks that claim because the process
evidence does not prove it.

That is the core value: faster investigation without unsupported certainty.

## What It Does

- Parses sanitized suspicious-email case files.
- Builds a claim table for phishing, attachment, download, execution, and containment.
- Requires evidence IDs for supported claims.
- Downgrades malware execution to `not_supported_by_current_evidence`.
- Keeps endpoint isolation behind human approval.
- Writes a terminal transcript, analyst report, accuracy report, and execution log.
- Publishes a GitHub Pages review hub.

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- ImageMagick
- ffmpeg
- Edge TTS neural narration
- Sanitized DFIR case artifacts

## What Is Working

```text
findevil_local_checks_ok
claims_total=5
exact_status_accuracy=1.0
unsupported_claims_blocked=1
false_confident_supported_claims=0
claim_boundary=verified_local_sift_ready_no_live_sift_execution_claim
```

## Verification Commands

```bash
cd /path/to/evidence-locked-dfir-agent
bash findevil/scripts/run_findevil_local_checks.sh
```

This command runs the shared artifact generator, shared verifier, local DFIR
agent, report builder, demo-video builder, and output checks.

## Screenshots

- `architecture-diagram.svg`
- `findevil/media/evidence-locked-dfir-report-full.png`
- `findevil/media/evidence-locked-terminal-session-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Demo Script Summary

1. Open the live review hub.
2. Show the terminal run against packaged case data.
3. Show the claim table and evidence IDs.
4. Show the malware-execution claim being blocked as unsupported.
5. Show the analyst report, accuracy report, and human containment gate.
6. State the boundary: local verified prototype, no live SIFT claim yet.

## What Makes It Different

Many security demos make AI look useful by letting it be confident. This project
makes AI useful by constraining confidence.

The agent does not win by sounding smart. It wins by refusing to overclaim.

## Challenges

The hardest part was keeping the demo honest. The product needs to feel practical
for incident responders without pretending to run live forensic tooling that was
not verified in this environment.

## Accomplishments

- Added a terminal-executable local agent.
- Added packaged case data and a ground-truth file.
- Added claim/evidence output and an accuracy report.
- Added an execution log for replayability.
- Added an architecture page and diagram.
- Rebuilt the demo video with natural English narration and audio.

## What We Learned

In DFIR, AI assistance is only valuable when analysts can see why a conclusion
was made and where the evidence stops.

## What's Next

- Connect the parser to live SANS SIFT artifacts.
- Add larger case packets and analyst feedback loops.
- Add a model-assisted summarizer that can only quote from approved evidence IDs.
- Add export formats for incident tickets and handoff reports.

## Claim Boundary

This is a local verified prototype using sanitized evidence events and packaged
case data. It does not claim live SIFT execution, live forensic tooling, real
victim data, or real malware attribution.
