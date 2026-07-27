# https://m.stock.naver.com/front-api/marketIndex/standardInterest?category=standardInterest&reutersCode=USA&page=1
"""
- Federal Funds Rate (Fed Rate)
- Bank of Korea Base Rate
"""

import requests
import pandas as pd
#from collector.data_processor.standard_interest_data_processor import standard_interest_data_processor

def price_data_reader(start, end, code):
    start = pd.to_datetime(str(start))
    end = pd.to_datetime(str(end))

    page = 1
    dfs = []

    code_trans = {
        "Korea_Rate": "KOR",
        "Fed_Rate": "USA"
    }

    code = code_trans[code]
    
    while True:
        url = (
            "https://m.stock.naver.com/front-api/marketIndex/standardInterest"
            f"?category=standardInterest"
            f"&reutersCode={code}"
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

        page_df = price_data_processor(price_data, code)

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

    price_data = price_data[
        (price_data["date"] >= start) &
        (price_data["date"] <= end)
    ]
    
    price_data = (
        price_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    return price_data  # ["date", "code", "close", "change", "rate"]
