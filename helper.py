import datetime

def check_time_difference(timestamp, seconds):
  """
  Checks if the time difference between two ISO 8601 formatted timestamps is smaller than 5 seconds.

  Args:
    t1: The first timestamp.
    t2: The second timestamp.

  Returns:
    True if the difference is smaller than 5 seconds, False otherwise.
  """

  t1 = datetime.datetime.now()
  t2 = datetime.datetime.fromisoformat(timestamp)

  print(t1)
  print(t2)
  print((t1 - t2).total_seconds())

  return (t1 - t2).total_seconds() < seconds