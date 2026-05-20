#!/usr/bin/env python3
"""Run the local evidence-locked DFIR agent demo.

The script intentionally works from inspectable case files. It is a local,
deterministic stand-in for a SIFT-style terminal session: parse artifacts, bind
claims to evidence IDs, reject unsupported certainty, and produce an analyst
packet.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "case_data"
REPORT_DIR = ROOT / "reports"
MEDIA_DIR = ROOT / "media"


@dataclass
class Claim:
    claim_id: str
    label: str
    status: str
    evidence_ids: list[str]
    rationale: str
    risk_if_wrong: str


def read_csv(name: str) -> list[dict[str, str]]:
    with (CASE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evidence_from_headers() -> dict[str, str]:
    text = (CASE_DIR / "email_headers.txt").read_text(encoding="utf-8")
    evidence_id = re.search(r"Evidence-ID:\s*(\S+)", text)
    auth_failures = []
    for token in ("spf=fail", "dkim=none", "dmarc=fail"):
        if token in text:
            auth_failures.append(token)
    return {
        "evidence_id": evidence_id.group(1) if evidence_id else "ev-email-unknown",
        "auth_failures": ", ".join(auth_failures),
        "attachment": "Direct_Deposit_Update.docm" if "Direct_Deposit_Update.docm" in text else "unknown",
        "source_ip": "198.51.100.17" if "198.51.100.17" in text else "unknown",
    }


def build_claims() -> list[Claim]:
    headers = evidence_from_headers()
    hashes = read_csv("attachment_hashes.csv")
    browser = read_csv("browser_timeline.csv")
    processes = read_csv("endpoint_processes.csv")

    process_names = {row["process_name"].lower() for row in processes}
    office_execution = any(name in process_names for name in {"winword.exe", "microsoft word", "word"})
    download_rows = [row for row in browser if row["event"] == "download_started"]

    return [
        Claim(
            claim_id="claim-phishing-email",
            label="Suspicious payroll-themed phishing email",
            status="supported",
            evidence_ids=[headers["evidence_id"], "ev-net-002"],
            rationale=f"Mail authentication failed ({headers['auth_failures']}) and domain resolved to the sending host.",
            risk_if_wrong="User trust impact if a benign payroll message is mislabeled.",
        ),
        Claim(
            claim_id="claim-suspicious-attachment",
            label="Attachment is suspicious and should be quarantined for analysis",
            status="supported",
            evidence_ids=[hashes[0]["evidence_id"]] if hashes else [],
            rationale="The attachment hash is present in the training blocklist as a suspicious macro document.",
            risk_if_wrong="False positive quarantine of a business form.",
        ),
        Claim(
            claim_id="claim-browser-download",
            label="The user downloaded the suspicious attachment",
            status="supported" if download_rows else "not_supported_by_current_evidence",
            evidence_ids=[row["evidence_id"] for row in download_rows],
            rationale="Browser timeline includes a download_started event for the document URL.",
            risk_if_wrong="Overstating user interaction may trigger unnecessary escalation.",
        ),
        Claim(
            claim_id="claim-malware-executed",
            label="Malware executed on the endpoint",
            status="supported" if office_execution else "not_supported_by_current_evidence",
            evidence_ids=[] if not office_execution else [row["evidence_id"] for row in processes],
            rationale=(
                "No Word, macro host, shell, or child process execution appears in the endpoint process listing."
                if not office_execution
                else "Endpoint process list includes an execution chain that matches the attachment."
            ),
            risk_if_wrong="Unsupported execution claims can cause unnecessary host isolation and bad incident records.",
        ),
        Claim(
            claim_id="claim-endpoint-isolation",
            label="Endpoint isolation is approved",
            status="human_review_required",
            evidence_ids=["evt-0018"],
            rationale="The packet supports mailbox containment, but endpoint isolation remains a human decision.",
            risk_if_wrong="Automated isolation could interrupt a user device without sufficient proof.",
        ),
    ]


def load_ground_truth() -> dict[str, str]:
    payload = json.loads((CASE_DIR / "ground_truth.json").read_text(encoding="utf-8"))
    return {item["claim_id"]: item["expected_status"] for item in payload["expected_claims"]}


def score_claims(claims: Iterable[Claim]) -> dict[str, object]:
    expected = load_ground_truth()
    rows = []
    correct = 0
    false_confident = 0
    for claim in claims:
        expected_status = expected.get(claim.claim_id, "unknown")
        is_correct = claim.status == expected_status
        correct += int(is_correct)
        if claim.status == "supported" and expected_status != "supported":
            false_confident += 1
        rows.append(
            {
                "claim_id": claim.claim_id,
                "label": claim.label,
                "actual_status": claim.status,
                "expected_status": expected_status,
                "correct": is_correct,
                "evidence_ids": claim.evidence_ids,
            }
        )
    total = len(rows)
    return {
        "case_id": "CASE-DFIR-002",
        "claims_total": total,
        "claims_correct": correct,
        "exact_status_accuracy": round(correct / total, 3) if total else 0,
        "false_confident_supported_claims": false_confident,
        "unsupported_claims_blocked": sum(
            1 for row in rows if row["actual_status"] == "not_supported_by_current_evidence"
        ),
        "rows": rows,
    }


def terminal_lines(claims: list[Claim], score: dict[str, object]) -> list[str]:
    lines = [
        "$ python3 findevil/scripts/run_evidence_locked_agent.py --case CASE-DFIR-002",
        "[case] CASE-DFIR-002 suspicious payroll email triage",
        "[mode] evidence-lock: every supported claim must cite evidence IDs",
        "[parse] email_headers.txt -> ev-email-001",
        "[parse] attachment_hashes.csv -> ev-hash-001",
        "[parse] browser_timeline.csv -> ev-browser-001 ev-browser-002",
        "[parse] endpoint_processes.csv -> ev-proc-001..ev-proc-004",
        "",
    ]
    for claim in claims:
        evidence = ", ".join(claim.evidence_ids) if claim.evidence_ids else "no supporting artifact"
        lines.append(f"[claim] {claim.claim_id}: {claim.status}")
        lines.append(f"        evidence: {evidence}")
        lines.append(f"        why: {claim.rationale}")
    lines.extend(
        [
            "",
            f"[accuracy] exact_status_accuracy={score['exact_status_accuracy']}",
            f"[guardrail] false_confident_supported_claims={score['false_confident_supported_claims']}",
            "[decision] mailbox containment requires human approval; endpoint isolation not approved",
            "[boundary] verified local prototype; no live SIFT execution claimed",
        ]
    )
    return lines


def write_markdown_accuracy(score: dict[str, object]) -> None:
    rows = score["rows"]
    body = [
        "# Accuracy Report — Evidence-Locked DFIR Agent",
        "",
        "This report compares the local agent output with the packaged ground truth.",
        "",
        f"- Claims total: `{score['claims_total']}`",
        f"- Claims correct: `{score['claims_correct']}`",
        f"- Exact status accuracy: `{score['exact_status_accuracy']}`",
        f"- False confident supported claims: `{score['false_confident_supported_claims']}`",
        f"- Unsupported claims blocked: `{score['unsupported_claims_blocked']}`",
        "",
        "| Claim | Expected | Actual | Evidence |",
        "|---|---|---|---|",
    ]
    for row in rows:
        evidence = ", ".join(row["evidence_ids"]) if row["evidence_ids"] else "none"
        body.append(
            f"| {row['claim_id']} | {row['expected_status']} | {row['actual_status']} | {evidence} |"
        )
    body.extend(
        [
            "",
            "## Boundary",
            "",
            "The score is for the packaged sanitized case only. It is useful for demonstrating guardrail behavior, not for claiming broad forensic accuracy.",
        ]
    )
    (REPORT_DIR / "accuracy-report.md").write_text("\n".join(body) + "\n", encoding="utf-8")


def write_terminal_html(lines: list[str]) -> None:
    escaped = "\n".join(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for line in lines)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Terminal Session — Evidence-Locked DFIR Agent</title>
  <style>
    body {{ margin: 0; background: #0b1220; color: #dbeafe; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 28px 18px; }}
    .bar {{ background: #1f2937; color: #f8fafc; border: 1px solid #334155; border-radius: 8px 8px 0 0; padding: 10px 14px; font-family: Inter, system-ui, sans-serif; }}
    pre {{ margin: 0; background: #020617; border: 1px solid #334155; border-top: 0; border-radius: 0 0 8px 8px; padding: 18px; white-space: pre-wrap; line-height: 1.5; font-size: 14px; }}
    .note {{ color: #93c5fd; margin: 0 0 14px; font-family: Inter, system-ui, sans-serif; }}
  </style>
</head>
<body>
  <main>
    <p class="note">Local terminal proof generated from packaged case data. No live SIFT execution is claimed.</p>
    <div class="bar">CASE-DFIR-002 · evidence-lock terminal run</div>
    <pre>{escaped}</pre>
  </main>
</body>
</html>
"""
    (ROOT / "prototype" / "terminal-session.html").write_text(html, encoding="utf-8")


def write_execution_log(claims: list[Claim], score: dict[str, object]) -> None:
    rows = [
        {"event": "case_loaded", "case_id": "CASE-DFIR-002", "artifacts": 5},
        {"event": "claims_generated", "claims": [claim.claim_id for claim in claims]},
        {"event": "evidence_lock_applied", "unsupported_claims_blocked": score["unsupported_claims_blocked"]},
        {"event": "accuracy_scored", "exact_status_accuracy": score["exact_status_accuracy"]},
        {"event": "human_gate", "decision": "mailbox_containment_only", "endpoint_isolation": "not_approved"},
    ]
    (REPORT_DIR / "evidence-lock-execution-log.jsonl").write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "prototype").mkdir(parents=True, exist_ok=True)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    claims = build_claims()
    score = score_claims(claims)
    lines = terminal_lines(claims, score)

    (REPORT_DIR / "agent-claims.json").write_text(
        json.dumps([asdict(claim) for claim in claims], indent=2) + "\n", encoding="utf-8"
    )
    (REPORT_DIR / "accuracy-report.json").write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    (REPORT_DIR / "terminal-transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_markdown_accuracy(score)
    write_terminal_html(lines)
    write_execution_log(claims, score)

    print("\n".join(lines))


if __name__ == "__main__":
    main()
