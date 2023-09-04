import datetime

def check_time_difference(t1, t2, seconds):
  """
  Checks if the time difference between two ISO 8601 formatted timestamps is smaller than 5 seconds.

  Args:
    t1: The first timestamp.
    t2: The second timestamp.

  Returns:
    True if the difference is smaller than 5 seconds, False otherwise.
  """

  t1 = datetime.datetime.fromisoformat(t1)
  t2 = datetime.datetime.fromisoformat(t2)

  print(t1)
  print(t2)
  print((t1 - t2).total_seconds())

  return (t1 - t2).total_seconds() < seconds