#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

cd "$REPO_ROOT/shared-agentops-engine"
python3 scripts/generate_portfolio_artifacts.py >/tmp/findevil-shared-generate.log
python3 scripts/verify_artifacts.py >/tmp/findevil-shared-verify.log

cd "$REPO_ROOT"
python3 findevil/scripts/run_evidence_locked_agent.py >/tmp/findevil-terminal.log
python3 findevil/scripts/build_dfir_case_report.py >/tmp/findevil-report.log
bash findevil/scripts/build_demo_video.sh >/tmp/findevil-video.log

python3 - <<'PY'
import json
import subprocess
from pathlib import Path

root = Path("findevil")
required = [
    root / "case_data" / "ground_truth.json",
    root / "reports" / "agent-claims.json",
    root / "reports" / "accuracy-report.json",
    root / "reports" / "accuracy-report.md",
    root / "reports" / "evidence-lock-execution-log.jsonl",
    root / "reports" / "terminal-transcript.txt",
    root / "prototype" / "terminal-session.html",
    root / "prototype" / "evidence-locked-dfir-report.html",
    root / "media" / "evidence-locked-dfir-agent-demo.mp4",
]
missing = [str(path) for path in required if not path.exists() or path.stat().st_size == 0]
if missing:
    raise SystemExit(f"missing required outputs: {missing}")

score = json.loads((root / "reports" / "accuracy-report.json").read_text())
if score["false_confident_supported_claims"] != 0:
    raise SystemExit("evidence lock failed: false confident claims remained")
if score["unsupported_claims_blocked"] < 1:
    raise SystemExit("evidence lock failed: no unsupported claim was blocked")

transcript = (root / "reports" / "terminal-transcript.txt").read_text()
for needle in [
    "claim-malware-executed: not_supported_by_current_evidence",
    "mailbox containment requires human approval",
    "no live SIFT execution claimed",
]:
    if needle not in transcript:
        raise SystemExit(f"terminal transcript missing: {needle}")

probe = subprocess.check_output(
    [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=nw=1:nk=1",
        str(root / "media" / "evidence-locked-dfir-agent-demo.mp4"),
    ],
    text=True,
).strip()
duration = float(probe)
if duration < 45:
    raise SystemExit(f"demo video too short: {duration}")

audio_probe = subprocess.check_output(
    [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "csv=p=0",
        str(root / "media" / "evidence-locked-dfir-agent-demo.mp4"),
    ],
    text=True,
).strip()
if "audio" not in audio_probe:
    raise SystemExit("demo video has no audio stream")

print("findevil_local_checks_ok")
print(f"claims_total={score['claims_total']}")
print(f"exact_status_accuracy={score['exact_status_accuracy']}")
print(f"unsupported_claims_blocked={score['unsupported_claims_blocked']}")
print(f"false_confident_supported_claims={score['false_confident_supported_claims']}")
print(f"video_seconds={duration:.1f}")
print("claim_boundary=verified_local_sift_ready_no_live_sift_execution_claim")
PY
