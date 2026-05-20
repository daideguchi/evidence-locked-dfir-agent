# Accuracy Report — Evidence-Locked DFIR Agent

This report compares the local agent output with the packaged ground truth.

- Claims total: `5`
- Claims correct: `5`
- Exact status accuracy: `1.0`
- False confident supported claims: `0`
- Unsupported claims blocked: `1`

| Claim | Expected | Actual | Evidence |
|---|---|---|---|
| claim-phishing-email | supported | supported | ev-email-001, ev-net-002 |
| claim-suspicious-attachment | supported | supported | ev-hash-001 |
| claim-browser-download | supported | supported | ev-browser-001 |
| claim-malware-executed | not_supported_by_current_evidence | not_supported_by_current_evidence | none |
| claim-endpoint-isolation | human_review_required | human_review_required | evt-0018 |

## Boundary

The score is for the packaged sanitized case only. It is useful for demonstrating guardrail behavior, not for claiming broad forensic accuracy.
