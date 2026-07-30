from datetime import datetime
from zoneinfo import ZoneInfo

def today_is():
  update_time = datetime.now(
    ZoneInfo("Asia/Seoul")
  ).strftime("%Y-%m-%d")
  return update_time

def today_and_time_is():
  update_time = datetime.now(
    ZoneInfo("Asia/Seoul")
  ).strftime("%Y-%m-%d %H:%M")
  return update_time
