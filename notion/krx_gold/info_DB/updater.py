from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할
from notion.rich_text import rich_text
from utils.day_log import today_and_time_is
from data.csv.domestic_stock.get_high_low_nMonth import get_high_low_nMonth
from assets.domestic_stock.info.updater import update_nMonth_high_low_value

def update_krx_gold_info_DB(page, krx_gold_info):

    change = krx_gold_info["change"]
    rate = krx_gold_info["rate"]
    # 하락이면 음수로 변경
    if krx_gold_info["direction"] == "5":
        change *= -1
        rate *= -1

    path = "data/csv/krx_gold/price_history.csv"
    
    high_low_3m = update_nMonth_high_low_value(page, krx_gold_info["high"], krx_gold_info["low"], krx_gold_info["ticker"], path, 3)              # ticker : 'M04020000'
    high_low_12m = update_nMonth_high_low_value(page, krx_gold_info["high"], krx_gold_info["low"], krx_gold_info["ticker"], path, 12)
    high_low_36m = update_nMonth_high_low_value(page, krx_gold_info["high"], krx_gold_info["low"], krx_gold_info["ticker"], path, 36)
    high_low_60m = update_nMonth_high_low_value(page, krx_gold_info["high"], krx_gold_info["low"], krx_gold_info["ticker"], path, 60)
    high_low_120m = update_nMonth_high_low_value(page, krx_gold_info["high"], krx_gold_info["low"], krx_gold_info["ticker"], path, 120)

    krx_gold_info_naver_finance = {
        # KRX 시장 값을 반환
    
        "현재가_깃허브": {"number": krx_gold_info["price"]},
        "전일대비_깃허브": {"number": change},
        "등락률_깃허브": {"number": rate},
        "거래량_깃허브": {"number": krx_gold_info["volume"]},
        "거래대금_깃허브":  rich_text(krx_gold_info["value"]),
        "3개월_최고가_깃허브": {"number": high_low_3m["high"]},
        "3개월_최저가_깃허브": {"number": high_low_3m["low"]},
        "12개월_최고가_깃허브": {"number": high_low_12m["high"]},
        "12개월_최저가_깃허브": {"number": high_low_12m["low"]},
        "36개월_최고가_깃허브": {"number": high_low_36m["high"]},
        "36개월_최저가_깃허브": {"number": high_low_36m["low"]},
        "60개월_최고가_깃허브": {"number": high_low_60m["high"]},
        "60개월_최저가_깃허브": {"number": high_low_60m["low"]},
        "120개월_최고가_깃허브": {"number": high_low_120m["high"]},
        "120개월_최저가_깃허브": {"number": high_low_120m["low"]},
        "마지막 업데이트": rich_text(today_and_time_is())
    }    
    
    notion.pages.update(
        page_id = page["id"],
        properties = krx_gold_info_naver_finance
    )
  
