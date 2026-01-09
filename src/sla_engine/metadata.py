from datetime import datetime

def build_run_metadata(as_of_ts, timezone):
    return {
        "as_of_timestamp": as_of_ts,
        "timezone": timezone,
        "run_generated_at": datetime.utcnow()
    }
