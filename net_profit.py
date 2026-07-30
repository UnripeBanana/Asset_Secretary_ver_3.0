from config.notion import NOTION_NET_PROFIT_DB_ID
from notion.client import notion
from notion.rich_text import rich_text
from utils.day_log import today_and_time_is

def net_profit(prop, profit):

    domestic_stock_profit = profit if prop == "domestic_stock" else 0
    dividend_profit = profit if prop == "dividend" else 0
    
    notion.pages.create(
        parent={
            "database_id": NOTION_NET_PROFIT_DB_ID
        },
        
        properties={
            "국내주식 수익": {"number": domestic_stock_profit},
            "국내주식 배당금 수익": {"number": dividend_profit},
            "업데이트 일시": rich_text(today_and_time_is())
        }
    )
