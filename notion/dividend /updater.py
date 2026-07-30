from notion.client import notion # notion : 로그인 된 앱에 접근할 수 있도록 해주는 역할
from net_profit import net_profit

def update_dividend(properties):
	if properties["dividend"] and not properties["profit_saved"]: 
		net_profit("dividend", properties["dividend"])
		new_properties = {"순수익 반영": {"checkbox": True}}

		notion.pages.update(
			page_id = properties["page_id"],
			properties = new_properties
		)
