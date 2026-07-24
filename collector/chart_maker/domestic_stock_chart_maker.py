from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def domestic_stock_chart_maker(stock):
    #-----------------------------------------------------
    # chart 사이즈 설정
    #-----------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 8))
    x = np.arange(len(stock))
    stock = stock.reset_index(drop=True)          # stock index 초기화 작업(오류 방지)

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
    # 최고가 / 최저가
    high_idx = stock["high"].idxmax()
    low_idx = stock["low"].idxmin()
    
    high_price = stock.loc[high_idx, "high"]
    low_price = stock.loc[low_idx, "low"]

    offset = (price_max - price_min) * 0.03
    
    # 최고가 표시
    ax.plot(
        high_idx,
        high_price + offset,
        marker="v",                          # ▼ 표시
        color="gray",
        markersize=5
    )
    ax.text(
        high_idx + 4,                      # 왼쪽으로 약간 이동
        high_price + offset,          # ▼와 같은 높이
        f"High Price {high_price:,}",
        va="center",
        ha="right",
        fontsize=8,
        color="gray"
    )
    
    # 최저가 표시
    ax.plot(
        low_idx,
        low_price - offset,
        marker="^",                          # ▲ 표시
        color="gray",
        markersize=5
    )
    ax.text(
        low_idx + 0.5,                       # 오른쪽으로 약간 이동
        low_price - offset,           # ▲와 같은 높이
        f"Low Price {low_price:,}",
        va="center",
        ha="left",
        fontsize=8,
        color="gray"
    )

    #-----------------------------------------------------
    # 현재가 표시
    #-----------------------------------------------------
    last_close = stock.iloc[-1]["close"]
    
    # 당일 상승/하락에 따라 색상 결정
    current_color = (
        "#e53935"
        if last_close >= stock.iloc[-1]["open"]
        else "#1565c0"
    )
    
    ax.annotate(
        f"{last_close:,}",
        xy=(len(stock), last_close),             # 화살표 끝
        xytext=(len(stock) + 4.2, last_close),   # 박스 위치
        ha="left",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="white",
    
        bbox=dict(
            boxstyle="larrow,pad=0.35",
            fc=current_color,
            ec=current_color
        ),
    
        annotation_clip=False
    )

    #-----------------------------------------------------
    # 저장
    #-----------------------------------------------------
    plt.tight_layout()
    name = 
    ticker = 
    
    title = f"data_ver2/image/{name}_{ticker}.png"
    
    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)
