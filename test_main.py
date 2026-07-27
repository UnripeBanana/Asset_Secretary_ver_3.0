from collector.data_reader.domestic_stock_data_reader import domestic_stock_data_reader
from collector.data_reader.index_data_reader import index_data_reader
#from collector.data_reader.price_data_reader import price_data_reader
#from collector.data_reader.standard_interest_data_reader import standard_interest_data_reader

#from collector.chart_maker.domestic_stock_chart_maker import domestic_stock_chart_maker
from collector.chart_maker.domestic_stock_chart_maker import domestic_stock_candle_chart_maker
from collector.chart_maker.index_chart_maker import index_chart_maker
from collector.chart_maker.index_chart_maker import index_candle_chart_maker
#from collector.chart_maker.price_chart_maker import price_chart_maker
#from collector.chart_maker.standard_interest_chart_maker import standard_interest_chart_maker


# 작업 완료
#domestic_stock_candle_chart_maker(domestic_stock_data_reader("2025-07-20", "2026-07-24", "005930"), "삼성전자")
#index_chart_maker(index_data_reader("2025-07-20", "2026-07-24", "KOSPI"))


# 작업 중
index_candle_chart_maker(index_data_reader("2025-07-20", "2026-07-24", "KOSPI"))
#domestic_stock_chart_maker(domestic_stock_data_reader("2025-07-20", "2026-07-24", "005930"), "삼성전자")
