#[['날짜', '시가', '고가', '저가', '종가', '거래량', '외국인소진율'],
#["20240213", 74800, 75200, 74400, 75200, 21966745, 54.52]]
#-> 이런 식으로 구성돼있음

import requests
import pandas as pd
import ast
import re

def domestic_stock_data_reader(start, end, ticker):
    # 입력 형식 표시하려고 남겨둔 내용. 지우지 말 것
    #start = 20260420
    #end = 20260720
    #ticker = "005930"
    
    url = (
        f"https://m.stock.naver.com/front-api/external/chart/domestic/info"
        f"?symbol={ticker}"
        f"&requestType=1"
        f"&startTime={start}"
        f"&endTime={end}"
        f"&timeframe=day"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(
        url, 
        headers=headers,
        timeout=10
    )
    
    text = response.text

    # 줄바꿈, 탭 제거
    text = re.sub(r'[\n\r\t]', '', text)
    
    # 앞뒤 공백 제거
    text = text.strip()
    #print(repr(text))

    # 문자열 → 리스트
    domestic_stock_data = ast.literal_eval(text)

    # DataFrame 생성
    domestic_stock_df = pd.DataFrame(domestic_stock_data[1:], columns=domestic_stock_data[0])

    domestic_stock_df["날짜"] = pd.to_datetime(domestic_stock_df["날짜"], format="%Y%m%d")
    
    domestic_stock_df = domestic_stock_df.rename(columns={
        "날짜": "date",
        "시가": "open",
        "고가": "high",
        "저가": "low",
        "종가": "close",
        "거래량": "volume"
    })

    return domestic_stock_df
