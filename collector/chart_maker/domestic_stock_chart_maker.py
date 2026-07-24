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

    #-----------------------------------------------------
    # 가격 데이터 네이버 증권에서 읽어오기
    #-----------------------------------------------------
    start = 20250720
    end = 20260720
    ticker = "005930"
    stock = domestic_stock_data_reader(start, end, ticker)

    #-----------------------------------------------------
    # chart 사이즈 설정
    #-----------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 8))
    x = np.arange(len(stock))

    #-----------------------------------------------------
    # 캔들차트 생성
    #-----------------------------------------------------
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

    #-----------------------------------------------------
    # 이동평균선
    #-----------------------------------------------------
    stock["MA5"] = stock["close"].rolling(5).mean()
    stock["MA20"] = stock["close"].rolling(20).mean()
    stock["MA60"] = stock["close"].rolling(60).mean()
    stock["MA120"] = stock["close"].rolling(120).mean()
    
    ax.plot(x, stock["MA5"], color="orange", linewidth=1.2, label="5")
    ax.plot(x, stock["MA20"], color="red", linewidth=1.2, label="20")
    ax.plot(x, stock["MA60"], color="green", linewidth=1.2, label="60")
    ax.plot(x, stock["MA120"], color="blue", linewidth=1.2, label="120")
    
    ax.legend(loc="upper left")

    #-----------------------------------------------------
    # 축 설정
    #-----------------------------------------------------
    # 위/오른쪽 테두리 제거
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # y축을 오른쪽으로 이동
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    
    # 오른쪽 spine만 표시
    ax.spines["right"].set_visible(True)
    
    ax.tick_params(
        axis="y",
        left=False,
        labelleft=False,
        right=True,
        labelright=True
    )
    
    ax.set_xlim(-1, len(stock) + 6)
    
    # 여백 조금 주기
    price_min = stock["low"].min()
    price_max = stock["high"].max()
    
    margin = (price_max - price_min) * 0.05
    
    
    # y축을 0부터 보이게 설정
    ax.set_ylim(
        bottom = price_min - margin,
        top = price_max + margin
    )
    
    
    ax.set_ylim(
        price_min - margin,
        price_max + margin
    )

    # 날짜 표시 (매주 첫 거래일)
    tick_positions = []
    tick_labels = []
    
    last_week = None
    
    for i, row in stock.iterrows():
    
        week = row["date"].isocalendar().week
    
        if week != last_week:
            tick_positions.append(i)
            tick_labels.append(row["date"].strftime("%m-%d"))
            last_week = week
    
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(
        tick_labels,
        rotation=0,
        fontsize=9
    )

    #-----------------------------------------------------
    # 최고가 최저가 표시
    #-----------------------------------------------------
    present_high_and_low (ax, stock)

    #-----------------------------------------------------
    # 현재가 표시
    #-----------------------------------------------------
    present_current_price(ax, stock)

    #-----------------------------------------------------
    # 저장
    #-----------------------------------------------------
    plt.tight_layout()
    name = page["properties"]["종목"]["title"][0]["plain_text"]
    
    title = f"data_ver2/image/{name}_{ticker}.png"
    
    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )
    )
