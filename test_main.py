from collector.data_reader.domestic_stock_data_reader import domestic_stock_data_reader
from collector.data_reader.index_data_reader import index_data_reader
from collector.data_reader.price_data_reader import price_data_reader
#from collector.data_reader.standard_interest_data_reader import standard_interest_data_reader

from collector.chart_maker.domestic_stock_chart_maker import domestic_stock_chart_maker
from collector.chart_maker.domestic_stock_candle_chart_maker import domestic_stock_candle_chart_maker
from collector.chart_maker.index_chart_maker import index_chart_maker
from collector.chart_maker.index_candle_chart_maker import index_candle_chart_maker
from collector.chart_maker.price_chart_maker import price_chart_maker
#from collector.chart_maker.standard_interest_chart_maker import standard_interest_chart_maker

#-------------------------------------------
# 작업 완료
#-------------------------------------------
#domestic_stock_chart_maker(domestic_stock_data_reader("2025-07-20", "2026-07-27", "005930"), "삼성전자")
#domestic_stock_candle_chart_maker(domestic_stock_data_reader("2025-07-20", "2026-07-27", "005930"), "삼성전자")

#index_chart_maker(index_data_reader("2025-07-20", "2026-07-27", "KOSPI"))                
# 입력 가능한 항목 : "KOSPI", "KOSDAQ", "KOSPI_200", "NASDAQ", "S&P_500", "Dow_Jones", "VIX"

#index_candle_chart_maker(index_data_reader("2025-07-20", "2026-07-27", "KOSPI"))         
# 입력 가능한 항목 : "KOSPI", "KOSDAQ", "KOSPI_200", "NASDAQ", "S&P_500", "Dow_Jones", "VIX"

#price_chart_maker(price_data_reader("2025-07-20", "2026-07-27", "KRW_Gold"))              
# 입력 가능한 항목 : "US2Y", "US10Y", "US30Y", "KR3Y", "KR10Y", "KR30Y", "USD/KRW", "Dolar_Index", "USD/JPY", "USD/EUR", 
#                   "KRW_Gold", "International_Gold", "Silver", "WTI_Crude_Oil", "Brent_Crude_Oil", "Natural_Gas", "Copper"


#-------------------------------------------
# 작업 중
#-------------------------------------------
standard_interest_chart_maker(standard_interest_data_reader("2000-04-27", "2026-07-27", "Korea_Rate"))  #<- 기준 금리 작업 중임. 함수 이름 바꾸고 미국 금리의 경우 데이터에 "-"가 있어서 처리가 안됨. 해결해야 함.
