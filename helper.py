import datetime

def check_time_difference(x, y, interval=5):
  """
  Checks if the time difference between two datetime.now() timestamps is smaller than X seconds.

  Args:
    x: The first timestamp.
    y: The second timestamp.

  Returns:
    True if the difference is smaller than X seconds, False otherwise.
  """

  now = datetime.datetime.now()
  t1 = now + datetime.timedelta(seconds=x)
  t2 = now + datetime.timedelta(seconds=y)
  return (t1 - t2).total_seconds() < interval