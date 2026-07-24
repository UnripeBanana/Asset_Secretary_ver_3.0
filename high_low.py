def present_high_and_low (ax, stock):
    # 최고가 / 최저가
    high_idx = stock["high"].idxmax()
    low_idx = stock["low"].idxmin()
    
    high_price = stock.loc[high_idx, "high"]
    low_price = stock.loc[low_idx, "low"]
    
    # 최고가 표시
    ax.plot(
        high_idx,
        high_price + 700,
        marker="v",                          # ▼ 표시
        color="gray",
        markersize=5
    )
    ax.text(
        high_idx + 4,                      # 왼쪽으로 약간 이동
        high_price + 700,          # ▼와 같은 높이
        f"High Price {high_price:,}",
        va="center",
        ha="right",
        fontsize=8,
        color="gray"
    )
    
    # 최저가 표시
    ax.plot(
        low_idx,
        low_price - 700,
        marker="^",                          # ▲ 표시
        color="gray",
        markersize=5
    )
    ax.text(
        low_idx + 0.5,                       # 오른쪽으로 약간 이동
        low_price - 700,           # ▲와 같은 높이
        f"Low Price {low_price:,}",
        va="center",
        ha="left",
        fontsize=8,
        color="gray"
    )
