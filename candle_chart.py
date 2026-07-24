# stock

#date  ticker  name    open  ...     low   close    volume        amount
#0 2026-07-13  005930  삼성전자  285000  ...  253000  254500  31882652  8.455131e+12
#1 2026-07-14  005930  삼성전자  255000  ...  247000  263000  39989493  1.039033e+13
#[2 rows x 9 columns]

from matplotlib.patches import Rectangle

def make_candle_chart(ax, stock):
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
