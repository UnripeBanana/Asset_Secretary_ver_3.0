# https://m.stock.naver.com/front-api/marketIndex/prices?category=bond&reutersCode=US2YT%3DRR&page=1
"""
- US 2-Year Treasury Yield
- US 10-Year Treasury Yield
- US 30-Year Treasury Yield
- KR 3-Year Government Bond Yield
- KR 10-Year Government Bond Yield
- KR 30-Year Government Bond Yield
- USD/KRW
- Dollar Index (DXY)
- USD/JPY
- EUR/USD
- Gold
- Silver
- WTI Crude Oil
- Brent Crude Oil
- Natural Gas
- Copper
"""

import requests
import pandas as pd
from cololector.data_processor.price_data_processor import price_data_processor

def price_data_reader(start, end, category, ticker, name, currency):
    start = pd.to_datetime(str(start), format="%Y%m%d")
    end = pd.to_datetime(str(end), format="%Y%m%d")

    page = 1
    dfs = []
    
    while True:
        url = (
            "https://m.stock.naver.com/front-api/marketIndex/prices"
            f"?category={category}"
            f"&reutersCode={ticker}"
            f"&page={page}"
        )
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://m.stock.naver.com/"
        }
        
        response = requests.get(url, headers=headers)
        
        price_data = response.json()

        if not price_data.get("result"):
            break    

        page_df = make_market_index_df(price_data, ticker, name)

        page_df["date"] = (
            pd.to_datetime(page_df["date"], utc=True)
              .dt.date
        )
        page_df["date"] = pd.to_datetime(page_df["date"])

        dfs.append(page_df)
        
        oldest = page_df["date"].min()

        
        if oldest <= start:
            break
    
        page += 1        

    price_data = pd.concat(dfs, ignore_index=True)

    price_data["currency"] = currency

    price_data = price_data[
        (price_data["date"] >= start) &
        (price_data["date"] <= end)
    ]
    
    price_data = (
        price_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    return price_data
