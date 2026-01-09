def calculate_handle_time(events, active_statuses, terminal_statuses, as_of_ts):
    handle_time = 0
    last_active_start = None

    for _, row in events.iterrows():
        new = row["New Value"]
        ts = row["Edit Date"]

        if new in active_statuses and last_active_start is None:
            last_active_start = ts

        if new in terminal_statuses and last_active_start is not None:
            handle_time += (ts - last_active_start).total_seconds()
            last_active_start = None

    if last_active_start is not None:
        handle_time += (as_of_ts - last_active_start).total_seconds()

    return handle_time / 3600
