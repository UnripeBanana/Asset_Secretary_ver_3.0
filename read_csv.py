import pandas as pd

def read_csv(path, ticker):
    df = pd.read_csv(path, dtype={"ticker": str})
    
    stock = df[df["ticker"] == ticker].copy()
    
    stock["date"] = pd.to_datetime(stock["date"])
    stock = stock.sort_values("date").reset_index(drop=True)
    
    return stock  
