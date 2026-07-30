def get_ticker(page):
    ticker_data = page["properties"]["티커"]["rich_text"]
    if not ticker_data:
        return None
    return ticker_data[0]["plain_text"]
