def present_current_price(ax, stock):
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
