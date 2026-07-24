def moving_average(ax, stock, x):
    stock["MA5"] = stock["close"].rolling(5).mean()
    stock["MA20"] = stock["close"].rolling(20).mean()
    stock["MA60"] = stock["close"].rolling(60).mean()
    stock["MA120"] = stock["close"].rolling(120).mean()
    
    ax.plot(x, stock["MA5"], color="orange", linewidth=1.2, label="5")
    ax.plot(x, stock["MA20"], color="red", linewidth=1.2, label="20")
    ax.plot(x, stock["MA60"], color="green", linewidth=1.2, label="60")
    ax.plot(x, stock["MA120"], color="blue", linewidth=1.2, label="120")
    
    ax.legend(loc="upper left")
