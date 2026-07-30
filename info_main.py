from config.notion import NOTION_DOMESTIC_STOCK_INFO_DB_ID, NOTION_KRX_GOLD_INFO_DB_ID, NOTION_DOMESTIC_BOND_ETF_INFO_DB_ID
from notion.get_all_pages import get_all_pages

#-----------------------------------------
# 국내주식 종목 DB 업데이트
#-----------------------------------------
from assets.domestic_stock.info.reader import get_ticker
from assets.domestic_stock.info.collector import get_domestic_stock_info
from assets.domestic_stock.info.updater import update_domestic_stock_info_DB

for page in get_all_pages(NOTION_DOMESTIC_STOCK_INFO_DB_ID):
    # 티커 데이터 추출
    ticker = get_ticker(page)
    if not ticker:
        continue

    # 네이버증권에서 데이터 받아오기
    domestic_stock_info = get_domestic_stock_info(ticker) # dictionary

    # 노션에 데이터 업로드
    update_domestic_stock_info_DB(page, domestic_stock_info)


#-----------------------------------------
# KRX 금현물 종목 DB 업데이트
#-----------------------------------------
from assets.krx_gold.info.collector import get_krx_gold_info
from assets.krx_gold.info.updater import update_krx_gold_info_DB

for page in get_all_pages(NOTION_KRX_GOLD_INFO_DB_ID):
    # 네이버증권에서 데이터 받아오기
    krx_gold_info = get_krx_gold_info()

    # 노션에 데이터 업로드
    update_krx_gold_info_DB(page, krx_gold_info)


#-----------------------------------------
# 국내 채권 ETF 종목 DB 업데이트
#-----------------------------------------
# 국내 채권 ETF는 데이터를 받아오는 구조가 국내 주식과 동일함. 따라서 같은 함수를 적용.

for page in get_all_pages(NOTION_DOMESTIC_BOND_ETF_INFO_DB_ID):
    # 티커 데이터 추출
    ticker = get_ticker(page)
    if not ticker:
        continue

    # 네이버증권에서 데이터 받아오기
    domestic_stock_info = get_domestic_stock_info(ticker) # dictionary

    # 노션에 데이터 업로드
    update_domestic_stock_info_DB(page, domestic_stock_info)
