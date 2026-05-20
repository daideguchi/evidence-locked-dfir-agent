# Case Data — Sanitized Phishing Triage Packet

This folder contains the packaged case data used by the local terminal demo.

The goal is not to claim a real victim investigation. The goal is to show the
agent workflow against concrete, inspectable artifacts instead of a slide-only
story.

## Files

- `email_headers.txt` - sanitized suspicious email headers.
- `attachment_hashes.csv` - attachment hash and reputation lookup result.
- `browser_timeline.csv` - browser/download timeline for the affected user.
- `endpoint_processes.csv` - endpoint process listing around the reported time.
- `network_observations.log` - sanitized proxy/DNS observations.
- `ground_truth.json` - expected claim outcomes used by the accuracy report.

## Evidence Rules

- A claim is `supported` only when it has at least one concrete evidence ID.
- A claim is `not_supported_by_current_evidence` when the agent considered it
  but the packet does not prove it.
- A containment action is `human_review_required` unless a human decision event
  exists.

## Submission Boundary

This is a verified local prototype using sanitized case data. It is SIFT-ready
in shape, but this repository does not claim live SIFT execution or real malware
attribution.
