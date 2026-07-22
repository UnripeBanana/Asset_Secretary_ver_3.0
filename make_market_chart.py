import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def make_market_index_chart(df):
    # ---------------------------------
    # 그래프 생성
    # ---------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    x = range(len(df))
    
    ax.plot(
        x,
        df["close"],
        linewidth=2
    )
    
    # ---------------------------------
    # 제목
    # ---------------------------------
    ax.set_title(df.iloc[0]["name"], fontsize=18)
    
    # ---------------------------------
    # 축 이름
    # ---------------------------------
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Price ({df.iloc[0]["currency"]})")
    
    # ---------------------------------
    # x축 날짜 표시
    # 월요일만 표시
    # ---------------------------------
    # x축 눈금 위치 (5거래일마다 하나씩)
    ax.set_xticks(range(0, len(df), 5))
    
    # x축에 표시할 날짜
    ax.set_xticklabels(
        df["date"].dt.strftime("%m-%d")[::5]
    )
    
    # ---------------------------------
    # 격자
    # ---------------------------------
    ax.grid(True)
    
    # ---------------------------------
    # 현재 가격 표시
    # ---------------------------------
    last_x = len(df) - 1
    last_price = df.iloc[-1]["close"]
    
    ax.text(
        last_x,
        last_price,
        f"{last_price:,}",
        fontsize=10,
        ha="left",
        va="bottom"
    )
    
    # ---------------------------------
    # 여백 자동 조절
    # ---------------------------------
    plt.tight_layout()
    
    # ---------------------------------
    # 화면 출력
    # ---------------------------------
    plt.show()

    # 저장
    plt.tight_layout()
    name = df.iloc[0]["name"]
    
    title = f"data_ver2/image/{name}.png"
    
    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )
