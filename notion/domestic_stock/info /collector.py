# naver_finance.py에서 함수를 호출해서 증권사 데이터 뽑아오기

from collectors.naver_finance import put_ticker_to_get_naver_prop

def get_domestic_stock_info(ticker):
  properties = put_ticker_to_get_naver_prop(ticker)  # dictionary
  
  return properties
