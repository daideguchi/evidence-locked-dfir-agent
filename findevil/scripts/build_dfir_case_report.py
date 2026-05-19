#!/usr/bin/env python3
"""Build the FIND EVIL evidence-locked DFIR demo report."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = ROOT.parent / "shared-agentops-engine"
EVENT_FILE = SHARED_ROOT / "data" / "agentops_events.jsonl"
SOURCE_REPORT = SHARED_ROOT / "adapters" / "findevil" / "dfir_report.md"
OUT_FILE = ROOT / "prototype" / "evidence-locked-dfir-report.html"
CASE_PACKET_FILE = ROOT / "reports" / "dfir-case-packet.json"

CASE_ID = "CASE-DFIR-002"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def read_events() -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in EVENT_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event["case_id"] == CASE_ID:
            events.append(event)
    return events


def risk_class(risk: str) -> str:
    if risk in {"critical", "high"}:
        return "danger"
    if risk == "medium":
        return "warn"
    if risk == "low":
        return "ok"
    return "quiet"


def build_timeline(events: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"""
        <article class="timeline-row">
          <div>
            <span class="event-id">{esc(event["event_id"])}</span>
            <span class="subtle">{esc(event["timestamp"])}</span>
          </div>
          <div class="timeline-main">
            <strong>{esc(event["event_type"])}</strong>
            <span>{esc(event["actor_type"])} / {esc(event["actor_name"])}</span>
            <p>{esc(event["summary"])}</p>
          </div>
          <span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span>
        </article>
        """
        for event in events
    )


def build_evidence_chain(events: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"""
        <tr>
          <td><span class="event-id">{esc(event["event_id"])}</span></td>
          <td>{esc(event["phase"])}</td>
          <td>{esc(event["actor_name"])}</td>
          <td>{esc(event["summary"])}</td>
        </tr>
        """
        for event in events
    )


def build_guardrail_rows(events: list[dict[str, Any]]) -> str:
    guardrails = [
        event
        for event in events
        if event.get("risk_reason") or event.get("redaction_applied") or event.get("human_approval_required")
    ]
    return "\n".join(
        f"""
        <tr>
          <td><span class="event-id">{esc(event["event_id"])}</span></td>
          <td><span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span></td>
          <td>{esc(event.get("risk_reason", "human approval / redaction guardrail"))}</td>
          <td>{esc(event.get("decision", "none"))}</td>
        </tr>
        """
        for event in guardrails
    )


def build_html(events: list[dict[str, Any]]) -> str:
    approvals = sum(1 for event in events if event.get("human_approval_required"))
    redactions = sum(1 for event in events if event.get("redaction_applied"))
    unsupported = [event for event in events if event.get("metadata", {}).get("self_correction")]
    evidence_chain = build_evidence_chain(events)
    guardrails = build_guardrail_rows(events)
    timeline = build_timeline(events)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evidence-Locked DFIR Agent — FIND EVIL Demo</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --surface: #fff;
      --ink: #182230;
      --muted: #667085;
      --line: #d8e0e8;
      --brand: #264a8a;
      --brand-soft: #eaf0fb;
      --ok: #087443;
      --ok-soft: #e8f6ef;
      --warn: #b54708;
      --warn-soft: #fff3df;
      --danger: #b42318;
      --danger-soft: #ffebe9;
      --shadow: 0 16px 36px rgba(24, 34, 48, 0.08);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}

    .locator {{
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .hero {{
      background: #172033;
      color: #fff;
      border-radius: 8px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: minmax(0, 1.3fr) minmax(260px, 0.7fr);
      gap: 24px;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
    }}

    h2 {{
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }}

    h3 {{
      margin: 0 0 8px;
      font-size: 16px;
      letter-spacing: 0;
    }}

    p {{ margin: 0; }}

    .hero-copy {{
      margin-top: 14px;
      color: #d7e0ee;
      font-size: 16px;
      max-width: 760px;
    }}

    .finding-card {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      padding: 16px;
    }}

    .finding-card strong {{
      display: block;
      margin-bottom: 8px;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}

    .metric,
    .section {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(24, 34, 48, 0.04);
    }}

    .metric {{
      padding: 16px;
      min-height: 108px;
    }}

    .metric strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      margin-bottom: 8px;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 13px;
    }}

    .section {{
      margin-top: 22px;
      padding: 20px;
    }}

    .hypothesis-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .hypothesis {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fff;
    }}

    .hypothesis.supported {{ border-color: #a9dec5; background: #f8fdf9; }}
    .hypothesis.unsupported {{ border-color: #f2aaa4; background: #fff7f6; }}
    .hypothesis.human {{ border-color: #b8c9ea; background: #f7f9fe; }}

    .status {{
      display: inline-flex;
      width: fit-content;
      padding: 4px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .status.supported {{ color: var(--ok); background: var(--ok-soft); }}
    .status.unsupported {{ color: var(--danger); background: var(--danger-soft); }}
    .status.human {{ color: var(--brand); background: var(--brand-soft); }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}

    th {{
      text-align: left;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
    }}

    td {{
      border-bottom: 1px solid var(--line);
      padding: 12px 8px;
      vertical-align: top;
    }}

    .event-id {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      color: var(--brand);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}

    .risk-pill {{
      display: inline-flex;
      align-items: center;
      width: fit-content;
      min-height: 24px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .risk-pill.danger {{ color: var(--danger); background: var(--danger-soft); }}
    .risk-pill.warn {{ color: var(--warn); background: var(--warn-soft); }}
    .risk-pill.ok {{ color: var(--ok); background: var(--ok-soft); }}
    .risk-pill.quiet {{ color: var(--muted); background: #edf1f4; }}

    .timeline {{
      display: grid;
      gap: 10px;
    }}

    .timeline-row {{
      display: grid;
      grid-template-columns: 210px minmax(0, 1fr) 92px;
      gap: 14px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
    }}

    .timeline-main {{
      display: grid;
      gap: 4px;
    }}

    .timeline-main span,
    .timeline-main p,
    .subtle {{
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 920px) {{
      .hero,
      .metrics,
      .hypothesis-grid {{
        grid-template-columns: 1fr;
      }}

      .timeline-row {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 620px) {{
      main {{ padding: 16px 12px 32px; }}
      h1 {{ font-size: 27px; }}
      table {{
        display: block;
        overflow-x: auto;
        white-space: nowrap;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="locator">FIND EVIL! · Evidence-Locked DFIR Agent · Demo Artifact</div>

    <section class="hero">
      <div>
        <h1>AI can move fast in DFIR, but every claim must stay tied to evidence.</h1>
        <p class="hero-copy">
          This report shows an AI-assisted suspicious email investigation where the agent flags its own unsupported malware-execution claim,
          redacts low-confidence indicator output, and leaves the final containment decision to a human analyst.
        </p>
      </div>
      <aside class="finding-card">
        <strong>Critical guardrail</strong>
        <p>Unsupported endpoint malware execution is marked as not proven instead of being promoted into the final finding.</p>
      </aside>
    </section>

    <section class="metrics">
      <div class="metric"><strong>{len(events)}</strong><span>evidence events in this DFIR case</span></div>
      <div class="metric"><strong>{len(unsupported)}</strong><span>AI self-correction guardrail event</span></div>
      <div class="metric"><strong>{redactions}</strong><span>redacted low-confidence indicator</span></div>
      <div class="metric"><strong>{approvals}</strong><span>human containment approval</span></div>
    </section>

    <section class="section">
      <h2>Hypotheses And Status</h2>
      <div class="hypothesis-grid">
        <article class="hypothesis supported">
          <span class="status supported">Supported</span>
          <h3>Suspicious email / phishing attempt</h3>
          <p>Supported at low-to-medium confidence by collected artifacts and hash lookup.</p>
          <p><span class="event-id">evt-0014</span> <span class="event-id">evt-0017</span></p>
        </article>
        <article class="hypothesis unsupported">
          <span class="status unsupported">Not supported</span>
          <h3>Endpoint malware execution</h3>
          <p>The agent flagged this as unsupported because process evidence was missing.</p>
          <p><span class="event-id">evt-0015</span> <span class="event-id">evt-0016</span></p>
        </article>
        <article class="hypothesis human">
          <span class="status human">Human decision</span>
          <h3>Mailbox-only containment</h3>
          <p>Human analyst approved message containment and did not approve endpoint isolation.</p>
          <p><span class="event-id">evt-0018</span></p>
        </article>
      </div>
    </section>

    <section class="section">
      <h2>Evidence Chain</h2>
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Phase</th>
            <th>Actor</th>
            <th>Evidence Summary</th>
          </tr>
        </thead>
        <tbody>{build_evidence_chain(events)}</tbody>
      </table>
    </section>

    <section class="section">
      <h2>Guardrails</h2>
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Risk</th>
            <th>Reason</th>
            <th>Decision</th>
          </tr>
        </thead>
        <tbody>{guardrails}</tbody>
      </table>
    </section>

    <section class="section">
      <h2>Timeline</h2>
      <div class="timeline">{timeline}</div>
    </section>
  </main>
</body>
</html>
"""


def write_case_packet(events: list[dict[str, Any]]) -> None:
    packet = {
        "case_id": CASE_ID,
        "product": "Evidence-Locked DFIR Agent",
        "source_events": str(EVENT_FILE.relative_to(ROOT.parent)),
        "source_report": str(SOURCE_REPORT.relative_to(ROOT.parent)),
        "verified_facts": [
            "Suspicious email investigation was opened by a human analyst.",
            "Artifacts were collected from email headers, attachment hash, browser timeline, and endpoint process list.",
            "The AI agent marked malware execution as unsupported by current evidence.",
            "Human containment approval was mailbox-only.",
        ],
        "unsupported_claims": [
            {
                "claim": "Malware executed on the endpoint.",
                "status": "not_supported_by_current_evidence",
                "evidence": ["evt-0015", "evt-0016"],
            }
        ],
        "events": events,
    }
    CASE_PACKET_FILE.parent.mkdir(parents=True, exist_ok=True)
    CASE_PACKET_FILE.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    events = read_events()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_html(events), encoding="utf-8")
    write_case_packet(events)
    print(
        json.dumps(
            {
                "status": "ok",
                "case_id": CASE_ID,
                "output": str(OUT_FILE.relative_to(ROOT)),
                "case_packet": str(CASE_PACKET_FILE.relative_to(ROOT)),
                "event_count": len(events),
                "self_correction_events": sum(
                    1 for event in events if event.get("metadata", {}).get("self_correction")
                ),
                "redactions": sum(1 for event in events if event.get("redaction_applied")),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
