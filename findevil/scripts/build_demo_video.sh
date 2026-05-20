#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
MONO_FONT="/System/Library/Fonts/Menlo.ttc"
EDGE_TTS_PYTHON="${EDGE_TTS_PYTHON:-python3.11}"
EDGE_TTS_VOICE="${EDGE_TTS_VOICE:-en-US-AvaNeural}"
EDGE_TTS_RATE="${EDGE_TTS_RATE:--7%}"
OUT="$ROOT/media/evidence-locked-dfir-agent-demo.mp4"
LEGACY_OUT="$ROOT/media/evidence-locked-dfir-agent-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

if [ ! -s "$ROOT/reports/terminal-transcript.txt" ]; then
  python3 "$ROOT/scripts/run_evidence_locked_agent.py" >/dev/null
fi

make_screenshot_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local out="$4"

  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#000000B8" -draw "rectangle 0,810 1920,1080" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+900 "$title" \
    -font "$FONT" -fill white -pointsize 34 -annotate +72+980 "$subtitle" \
    "$out"
}

make_text_slide() {
  local title="$1"
  local subtitle="$2"
  local body="$3"
  local out="$4"

  magick -size 1920x1080 xc:"#f6f7f9" \
    -fill "#172033" -draw "rectangle 0,0 1920,260" \
    -fill "#ffffff" -font "$FONT" -pointsize 72 -annotate +82+150 "$title" \
    -fill "#dbe7f5" -font "$FONT" -pointsize 34 -annotate +86+218 "$subtitle" \
    -fill "#ffffff" -stroke "#d8e0e8" -strokewidth 3 -draw "roundrectangle 120,410 1800,760 24,24" \
    -stroke none -fill "#172033" -font "$FONT" -pointsize 46 -annotate +170+520 "$body" \
    -fill "#667085" -font "$FONT" -pointsize 28 -annotate +170+640 "The agent is useful because it refuses to turn weak evidence into confident incident facts." \
    "$out"
}

make_terminal_slide() {
  local out="$1"

  magick -size 1920x1080 xc:"#0b1220" \
    -fill "#1f2937" -draw "roundrectangle 90,80 1830,980 18,18" \
    -fill "#111827" -draw "rectangle 90,80 1830,148" \
    -fill "#f8fafc" -font "$FONT" -pointsize 30 -annotate +130+124 "CASE-DFIR-002 · evidence-lock terminal run" \
    -fill "#bfdbfe" -font "$MONO_FONT" -pointsize 30 -annotate +130+220 "$ python3 findevil/scripts/run_evidence_locked_agent.py" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+285 "[mode] evidence-lock: every supported claim must cite evidence IDs" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+335 "[claim] claim-phishing-email: supported · ev-email-001, ev-net-002" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+385 "[claim] claim-suspicious-attachment: supported · ev-hash-001" \
    -fill "#fecaca" -font "$MONO_FONT" -pointsize 28 -annotate +130+435 "[claim] claim-malware-executed: not_supported_by_current_evidence" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+485 "        why: no Word, macro host, shell, or child process was observed" \
    -fill "#fde68a" -font "$MONO_FONT" -pointsize 28 -annotate +130+555 "[decision] mailbox containment requires human approval" \
    -fill "#bbf7d0" -font "$MONO_FONT" -pointsize 28 -annotate +130+625 "[accuracy] exact_status_accuracy=1.0" \
    -fill "#bbf7d0" -font "$MONO_FONT" -pointsize 28 -annotate +130+675 "[guardrail] false_confident_supported_claims=0" \
    -fill "#93c5fd" -font "$MONO_FONT" -pointsize 28 -annotate +130+745 "[boundary] verified local prototype; no live SIFT execution claimed" \
    "$out"
}

cat > "$TMP_DIR/narration.txt" <<'TEXT'
Evidence-Locked DFIR Agent is a defensive investigation assistant for FIND EVIL.

The idea is simple. AI can help responders move faster, but in forensics, speed is dangerous when it creates certainty without evidence.

This demo runs a local terminal workflow against a packaged suspicious email case. The agent parses email headers, an attachment hash, browser timeline, endpoint process data, and network observations.

Then it creates claims. A phishing email claim is supported. The suspicious attachment claim is supported. The download claim is supported.

But the tempting claim is malware execution. The agent refuses to mark that as proven, because the process list does not show Word, a macro host, shell activity, or a child process chain.

That is the product: an AI assistant that can be helpful without becoming careless. It binds conclusions to evidence IDs, writes an analyst report, scores itself against ground truth, and leaves endpoint isolation behind a human approval gate.

This submission is honest about its boundary. It is a verified local prototype with sanitized case data and a SIFT-ready shape. It does not claim live SIFT execution or real malware attribution.
TEXT

"$EDGE_TTS_PYTHON" -m edge_tts \
  --voice "$EDGE_TTS_VOICE" \
  --rate="$EDGE_TTS_RATE" \
  --file "$TMP_DIR/narration.txt" \
  --write-media "$TMP_DIR/narration.mp3"

make_text_slide \
  "Evidence-Locked DFIR Agent" \
  "AI-assisted incident response where evidence controls every claim" \
  "Fast AI is useful only when unsupported certainty is treated as a risk." \
  "$TMP_DIR/slide-0.png"

make_terminal_slide "$TMP_DIR/slide-1.png"

make_screenshot_slide "$ROOT/media/evidence-locked-dfir-report-full.png" \
  "Analyst Report With Claim Boundaries" \
  "Supported, unsupported, and human-review claims are separated." \
  "$TMP_DIR/slide-2.png"

make_screenshot_slide "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "AgentOps Timeline For DFIR" \
  "AI, human, robot, and evidence events stay reviewable." \
  "$TMP_DIR/slide-3.png"

make_text_slide \
  "Safer Than Confident Summaries" \
  "The agent blocks the unproven malware-execution claim" \
  "Mailbox containment is visible; endpoint isolation remains a human decision." \
  "$TMP_DIR/slide-4.png"

make_screenshot_slide "$ROOT/media/evidence-locked-dfir-report-full.png" \
  "Submission Boundary" \
  "Verified local prototype. Live SIFT execution is not claimed yet." \
  "$TMP_DIR/slide-5.png"

ffmpeg -y \
  -loop 1 -t 14 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-2.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-3.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-4.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-5.png" \
  -i "$TMP_DIR/narration.mp3" \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v];[6:a]loudnorm=I=-16:TP=-1.5:LRA=11,volume=0.85[a]" \
  -map "[v]" -map "[a]" -r 30 -shortest -movflags +faststart "$OUT"

cp "$OUT" "$LEGACY_OUT"
rm -rf "$TMP_DIR"
echo "$OUT"
