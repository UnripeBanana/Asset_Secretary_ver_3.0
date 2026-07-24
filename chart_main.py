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

    #----------------------------------------
    # 캔들차트 생성    
    #----------------------------------------
    for i, row in stock.iterrows():
        open_price = row["open"]
        high_price = row["high"]
        low_price = row["low"]
        close_price = row["close"]
    
        # 상승 / 하락 색상
        color = "#e53935" if close_price > open_price else "#1565c0" if close_price < open_price else "#000000"
    
        # 심지
        ax.vlines(
            x=i,
            ymin=low_price,
            ymax=high_price,
            color=color,
            linewidth=1.2
        )
    
        # 몸통
        body_bottom = min(open_price, close_price)
        body_height = abs(close_price - open_price)
    
        # 시가 = 종가인 경우도 보이도록
        if body_height == 0:
            body_height = 5

        candle_width = 0.7
        rect = Rectangle(
            (i - candle_width / 2, body_bottom),
            candle_width,
            body_height,
            facecolor=color,
            edgecolor="none"     # ← 테두리 완전 제거
        )
    
        ax.add_patch(rect)

    #----------------------------------------
    # 이동평균선
    #----------------------------------------
    moving_average(ax, stock, x)

    #----------------------------------------
    # 축 설정
    #----------------------------------------
    set_axis(ax, stock)

    #----------------------------------------
    # 최고가 최저가 표시
    #----------------------------------------
    present_high_and_low (ax, stock)

    #----------------------------------------
    # 현재가 표시
    #----------------------------------------
    present_current_price(ax, stock)

    #----------------------------------------
    # 저장
    #----------------------------------------
    plt.tight_layout()
    name = page["properties"]["종목"]["title"][0]["plain_text"]
    
    title = f"data_ver2/image/{name}_{ticker}.png"
    
    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )
