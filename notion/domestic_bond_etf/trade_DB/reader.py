from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할

def read_domestic_bond_etf_trade(page):
	props = page["properties"]

	relation_page_id = props["종목"]["relation"][0]["id"]
	relation_page = notion.pages.retrieve(relation_page_id)

	trade = {
			"page_id": page["id"],
			"ticker": relation_page["properties"]["종목"]["title"][0]["plain_text"],
			"type": props["매수/매도"]["select"]["name"],
			"date": props["날짜"]["date"]["start"],
			"qty": props["거래량"]["number"],
			"price": props["단가"]["number"],
			"amount": props["거래금액"]["formula"]["number"],
			"profit_saved": props["순수익 반영"]["checkbox"]
		}
	
	return trade
