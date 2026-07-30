from config.notion import NOTION_DOMESTIC_STOCK_DIVIDEND_DB_ID
from notion.get_all_pages import get_all_pages

#-----------------------------------------
# 국내주식 거래내역 DB 업데이트
#-----------------------------------------
from assets.dividend.reader import read_dividend
from assets.dividend.updater import update_dividend

for page in get_all_pages(NOTION_DOMESTIC_STOCK_DIVIDEND_DB_ID):
    # 각 페이지별로 데이터 읽기
    properties = read_dividend(page)
    
    # 노션에 데이터 업데이트
    update_dividend(properties)
