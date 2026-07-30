from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할

def read_dividend(page):
	props = page["properties"]

	properties = {
		"page_id": page["id"],
		"dividend": props["배당금"]["formula"]["number"],
		"profit_saved": props["순수익 반영"]["checkbox"]
	}

	return properties
