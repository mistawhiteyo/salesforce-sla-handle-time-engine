# Salesforce SLA Handle-Time Analytics Engine

**Event-based SLA handle-time analytics engine built on Salesforce Case History to replace case-age–driven SLA reporting.**

## Business Problem
Traditional SLA reporting relied on case age, inflating SLA breaches when cases sat in Resolved or Closed states.
This produced noisy signals, reduced trust in reports, and weakened capacity planning.

## Solution
This engine reconstructs each case lifecycle using Salesforce status history and calculates **handle time** as time spent
only in active workflow states.

## Active vs Terminal States
**Active:** New, To Do, Reopen, Escalated, In Progress  
**Terminal:** Resolved, Closed

## Key Features
- Event-based handle-time calculation
- Explicit reopen handling
- Deterministic and auditable results
- Reproducible reporting via `as_of_timestamp`
- Truncated-history detection (no heuristic guessing)
- Safe Excel/CSV ingestion and timezone-safe exports

## Outputs
- One row per Case Number
- Handle time (hours)
- SLA hours
- SLA compliance flag
- Times reopened
- History truncated flag
- Run metadata (as-of timestamp, timezone)

## Known Limitation
If case history is truncated by the extract window, handle time cannot be reconstructed.
Such cases are explicitly flagged.

## Quickstart
```bash
pip install -r requirements.txt
pip install -e .
python -m sla_engine --input data/sample_input/case_history_sample.csv --output outputs/sample_output.xlsx
```
