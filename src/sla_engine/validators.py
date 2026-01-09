def is_history_truncated(events, terminal_statuses):
    first_old = events.iloc[0]["Old Value"]
    first_new = events.iloc[0]["New Value"]
    return first_old in terminal_statuses or (first_old == "Closed" and first_new == "Resolved")
