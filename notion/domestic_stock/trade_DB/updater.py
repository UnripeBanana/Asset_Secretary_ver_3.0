from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할
from net_profit import net_profit

# 'e816e5ae-e083-836a-9f48-01e15f18cd77': {'ticker': '한온시스템', 'date': '2026-06-18', 'profit_saved': False, 'remaining': 1, 'profit': 0}

def update_domestic_stock_trade_DB(results):
    for id, raw_prop in results.items():
        properties = {
            "잔량": {"number": raw_prop["remaining"]},
            "실현수익": {"number": raw_prop["profit"]}
        }

        if raw_prop["profit"] and not raw_prop["profit_saved"]: 
            net_profit("domestic_stock", raw_prop["profit"])
            properties["순수익 반영"] = {
                "checkbox": True
            }

        notion.pages.update(
            page_id = id,
            properties = properties
        )
