import pandas as pd

def index_data_processor(data, ticker, name):

    # 네이버 증권에서 받은 오리지널 데이터
    df = pd.DataFrame(data["result"])

    # 오리지널 데이터에서 불필요한 부분 제거
    df = df[["localTradedAt", "closePrice", "fluctuations", "fluctuationsRatio"]]

    # 기존에 사용 중인 명칭으로 변경
    df = df.rename(columns={
        "localTradedAt": "date",
        "closePrice": "close",
        "fluctuations": "change",
        "fluctuationsRatio": "rate"
    })

    # 기존에 사용중인 형식으로 변경 (문제 있어보임. 생략)
    #df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # str -> int
    df["close"] = (
        df["close"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -. int
    df["change"] = (
        df["change"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -> float
    df["rate"] = (
        df["rate"]
        .astype(float)
    )

    # 사용자로부터 입력받은 데이터 입력
    df["ticker"] = ticker
    df["name"] = name

    # 데이터프레임 컬럼 순서 설정
    df = df[
        ["date", "ticker", "name", "close", "change", "rate"]
    ]

    # 날짜 순으로 정렬 후 return
    return (
        df
        .sort_values("date")
        .reset_index(drop=True)
    )
