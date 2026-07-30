# 네이버 증권에서 정보를 받아오기 위해 필요한 함수들 정리

import requests            # 네이버 증권에서 데이터 받아오기

# 국내주식 정보를 받아오기 위한 함수
def put_ticker_to_get_naver_prop(ticker):

    # 네이버는 브라우저가 아닌 프로그램의 요청을 차단하는 경우가 있어서, 브라우저인 척 속이는 역할 수행
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = (
        f"https://polling.finance.naver.com/api/realtime"
        f"?query=SERVICE_ITEM:{ticker}"
    )

    data = requests.get(
        url,
        headers=headers,
        timeout=10 # 최대 10초까지만 기다리겠다는 의미.
    ).json()

    krx_item = data["result"]["areas"][0]["datas"][0]
    nxt_item = data["result"]["areas"][0]["datas"][0]["nxtOverMarketPriceInfo"]
  
    return {
        "cd": krx_item["cd"],      # 티커
        "nm": krx_item["nm"],      # 종목명
        "nv": krx_item["nv"],      # 현재가
        "cv": krx_item["cv"],      # 전일 대비 가격 변화(원)
        "cr": krx_item["cr"],      # 등락률(%)
        "rf": krx_item["rf"],      # 등락 구분(2:상승/3:보합/5:하락을 나타내는 코드)
        "ms": krx_item["ms"],      # 장상태(OPEN/CLOSE)
        "pcv": krx_item["pcv"],    # Previous Close Value, 전일종가
        "ov": krx_item["ov"],      # 시가
        "hv": krx_item["hv"],      # 고가
        "lv": krx_item["lv"],      # 저가
        "aq": krx_item["aq"],      # 거래량
        "aa": krx_item["aa"],      # 거래대금 : 하루동안 얼마가 거래되었는가 (평균 거래대금보다 많은 양이 거래될 시 신뢰도 있는 등락이라고 판단)
        "countOfListedStock": krx_item["countOfListedStock"]  # 상장주식수
    }

def to_int(value):
    if value in (None, "", "-"):
        return None
    return int(value.replace(",", ""))

def get_gold_prop():
    # 직접 접속 : https://m.stock.naver.com/marketindex/metals/M04020000
    url = "https://m.stock.naver.com/front-api/realTime/marketIndex/metals"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://m.stock.naver.com",
        "Referer": "https://m.stock.naver.com/marketindex/metals/M04020000",
    }
    
    payload = {
        "reutersCodes": ["M04020000"]
    }
    
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )
    
    gold = response.json()["result"]["metals"]["M04020000"]

    return {
        "ticker": gold["symbolCode"],                                        # 'M04020000'
        "name": gold["name"],                                                # 이름 : "국내 금"
        "price": to_int(gold["closePrice"]),                                 # 현재가
        "change": to_int(gold["fluctuations"]),                              # 전일대비
        "rate": float(gold["fluctuationsRatio"]),                            # 등락률
        "direction": gold["fluctuationsType"]["code"],                       # 등락여부
        "open_price": to_int(gold["openPrice"]),                             # 시가
        "high": to_int(gold["highPrice"]),                                   # 고가
        "low": to_int(gold["lowPrice"]),                                     # 저가
        "close_price": to_int(gold["closePrice"]),                           # 종가
        "volume": to_int(gold["accumulatedTradingVolume"]),                  # 거래량
        "value": gold["accumulatedTradingValue"]                             # 거래대금
    }
