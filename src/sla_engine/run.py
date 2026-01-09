import argparse
import pandas as pd
from datetime import datetime
import pytz

from sla_engine.config import ACTIVE_STATUSES, TERMINAL_STATUSES, REPORTING_TIMEZONE
from sla_engine.loader import load_case_history
from sla_engine.handle_time import calculate_handle_time
from sla_engine.validators import is_history_truncated
from sla_engine.metadata import build_run_metadata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--as-of", default=None)
    args = parser.parse_args()

    df = load_case_history(args.input)
    df["Edit Date"] = pd.to_datetime(df["Edit Date"])

    tz = pytz.timezone(REPORTING_TIMEZONE)
    as_of = pd.Timestamp(args.as_of) if args.as_of else pd.Timestamp.now(tz)

    results = []

    for case, events in df.groupby("Case Number"):
        events = events.sort_values("Edit Date")
        truncated = is_history_truncated(events, TERMINAL_STATUSES)
        ht = calculate_handle_time(events, ACTIVE_STATUSES, TERMINAL_STATUSES, as_of)
        results.append({
            "Case Number": case,
            "handle_time_hours": round(ht, 2),
            "history_truncated": truncated
        })

    out_df = pd.DataFrame(results)
    meta_df = pd.DataFrame([build_run_metadata(as_of, REPORTING_TIMEZONE)])

    with pd.ExcelWriter(args.output) as writer:
        out_df.to_excel(writer, sheet_name="Case_SLA", index=False)
        meta_df.to_excel(writer, sheet_name="Run_Metadata", index=False)

if __name__ == "__main__":
    main()
