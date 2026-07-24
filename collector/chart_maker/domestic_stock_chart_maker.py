from config.notion import NOTION_DOMESTIC_STOCK_INFO_DB_ID
from config.csv import DOMESTIC_STOCK_CSV_PATH
from notion.get_all_pages import get_all_pages
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# -----------------------------
# 국내주식 차트 생성
# -----------------------------
from assets.domestic_stock.info.reader import get_ticker
from charts.read_csv import read_csv
from charts.candle_chart import make_candle_chart
from charts.moving_average import moving_average
from charts.axis import set_axis
from charts.high_low import present_high_and_low
from charts.current_price import present_current_price
from notion.client import notion
from notion.initialize_info_page import initialize_stock_page

from data_ver2.domestic_stock.reader import domestic_stock_data_reader

# 나중에는
# make_chart 함수 하나, delete_chart 하나 update_chart 하나 이렇게 구성하는 것도 괜찮을 듯. 깔끔하게

for page in get_all_pages(NOTION_DOMESTIC_STOCK_INFO_DB_ID):
    # 티커 데이터 추출
    ticker = get_ticker(page)
    if not ticker:
        continue

    if ticker != "005930":
        continue

    # 가격 데이터 네이버 증권에서 읽어오기
    start = 20250720
    end = 20260720
    ticker = "005930"
    stock = domestic_stock_data_reader(start, end, ticker)

    # chart 사이즈 설정
    fig, ax = plt.subplots(figsize=(15, 8))
    x = np.arange(len(stock))

    # 캔들차트 생성
    make_candle_chart(ax, stock)

    # 이동평균선
    moving_average(ax, stock, x)

    # 축 설정
    set_axis(ax, stock)

    # 최고가 최저가 표시
    present_high_and_low (ax, stock)

    # 현재가 표시
    present_current_price(ax, stock)
    
    # 저장
    plt.tight_layout()
    name = page["properties"]["종목"]["title"][0]["plain_text"]
    
    title = f"data_ver2/image/{name}_{ticker}.png"
    
    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )

    # 노션에 있는 기존 이미지 삭제
    blocks = notion.blocks.children.list(block_id=page["id"])
    if len(blocks["results"]):
        for block in blocks["results"]:
            notion.blocks.delete(block["id"])
    
    # 노션 업로드
    chart_url = (
        "https://raw.githubusercontent.com/"
        "UnripeBanana/Asset_Secretary_ver_2.5/main/"
        f"data_ver2/image/{name}_{ticker}.png"
    )

    notion.blocks.children.append(
        block_id=page["id"],
        #after=heading_block_id,
        children=[
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": chart_url
                    }
                }
            }
        ]
    )
