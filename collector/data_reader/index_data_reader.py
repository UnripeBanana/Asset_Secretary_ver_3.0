#https://m.stock.naver.com/front-api/stock/domestic/index/price/list?code=KOSPI&page=1&pageSize=50
#(일봉, 주봉, 월봉 그리기 가능)
"""
- KOSPI
- KOSDAQ
- S&P 500
- NASDAQ
- VIX
"""

import requests
import pandas as pd
from data_ver2.market_index.naver_to_df import make_market_index_df

def index_data_reader(start, end, category, ticker, name, currency):
    start = pd.to_datetime(str(start), format="%Y%m%d")
    end = pd.to_datetime(str(end), format="%Y%m%d")

    page = 1
    dfs = []
    
    while True:
        url = (
            "https://m.stock.naver.com/stock/domestic/index/price/list"
            f"?code={code}"
            f"&page={page}"
            f"&pageSize=50"
        )
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://m.stock.naver.com/"
        }
        
        response = requests.get(url, headers=headers)
        
        data = response.json()

        if not data.get("result"):
            break    

        page_df = make_market_index_df(data, ticker, name)

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

    market_index_data = pd.concat(dfs, ignore_index=True)

    market_index_data["currency"] = currency

    market_index_data = market_index_data[
        (market_index_data["date"] >= start) &
        (market_index_data["date"] <= end)
    ]
    
    market_index_data = (
        market_index_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    return market_index_data
