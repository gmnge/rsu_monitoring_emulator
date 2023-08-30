import datetime

def has_record_within_seconds(logs, seconds):
    current_time = datetime.now()
    timestamps = []
    
    for log in logs:
        timestamps.append(log['timestamp'])

    for timestamp in timestamps:
        time_diff = current_time - timestamp
        if time_diff.total_seconds() < seconds:
            return True

    return False
