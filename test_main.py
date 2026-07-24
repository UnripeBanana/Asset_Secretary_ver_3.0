from collector.data_reader.domestic_stock_data_reader import domestic_stock_data_reader
#from collector.data_reader.index_data_reader import index_data_reader
#from collector.data_reader.price_data_reader import price_data_reader
#from collector.data_reader.standard_interest_data_reader import standard_interest_data_reader

#from collector.data_processor.index_data_processor import index_data_processor
#from collector.data_processor.price_data_processor import price_data_processor
#from collector.data_processor.standard_interest_data_processor import standard_interest_data_processor

#from collector.chart_maker.domestic_stock_chart_maker import domestic_stock_chart_maker
#from collector.chart_maker.index_chart_maker import index_chart_maker
#from collector.chart_maker.price_chart_maker import price_chart_maker
#from collector.chart_maker.standard_interest_chart_maker import standard_interest_chart_maker


#print(domestic_stock_data_reader(20250720, 20260724, "005930"))

domestic_stock_chart_maker(domestic_stock_data_reader(20250720, 20260724, "005930"), "삼성전자"):
