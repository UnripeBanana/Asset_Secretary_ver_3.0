import exchange_calendars as xcals
from utils.day_log import today_is

krx = xcals.get_calendar("XKRX")

def is_trading_day():
    return krx.is_session(str(today_is()))
