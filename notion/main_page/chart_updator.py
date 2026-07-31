from collector.data_reader.index_data_reader import index_data_reader
from collector.data_reader.price_data_reader import price_data_reader
from datetime import datetime, timedelta
from notion.client import notion

def main_page_chart_updator(PAGE_ID):
    blocks = notion.blocks.children.list(block_id=PAGE_ID)
    
    #-----------------------------------------------------------------------------------
    # 1. 지표 데이터 일괄 수집 및 데이터 세팅
    #-----------------------------------------------------------------------------------
    today = datetime.now()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    targets = [
        {
            "title": "KOSPI",
            "df": index_data_reader(yesterday_str, today_str, "KOSPI"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/market_index/KOSPI_chart.png"
        },
        {
            "title": "달러/원 환율",
            "df": price_data_reader(yesterday_str, today_str, "USD-KRW"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/price/USD-KRW_chart.png"
        },
        {
            "title": "국제금 / 달러 인덱스",
            "df": price_data_reader(yesterday_str, today_str, "International_Gold"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/price/Dolar_Index_X_International_Gold_chart.png"
        }
    ]
    
    # 지표별 텍스트 및 컬러 데이터 전처리
    for target in targets:
        df = target["df"]
        close = df["close"].iloc[-1]
        change = df["change"].iloc[-1]
        rate = df["rate"].iloc[-1]
    
        triangle = "▲" if change > 0 else "▼" if change < 0 else "-"
        symbol = "+" if change > 0 else "-" if change < 0 else ""
        target["color"] = "red" if change > 0 else "blue" if change < 0 else "default"
        target["text"] = f"{close:,}      {triangle} {change:,}      {symbol}{rate}%"
    
    
    #-----------------------------------------------------------------------------------
    # 2. NOTION UPDATE
    #-----------------------------------------------------------------------------------
    
    for block in blocks["results"]:
        if block["type"] != "column_list":
            continue
    
        columns = notion.blocks.children.list(block_id=block["id"])
    
        for col in columns["results"]:
            col_id = col["id"]
            children = notion.blocks.children.list(block_id=col_id)["results"]
    
            for target in targets:
                # 1) 해당 지표의 heading_2 블록 인덱스 찾기
                h2_index = next(
                    (idx for idx, item in enumerate(children)
                     if item["type"] == "heading_2" and item["heading_2"]["rich_text"][0]["text"]["content"] == target["title"]),
                    None
                )
    
                # 지표 제목을 찾은 경우에만 업데이트 수행
                if h2_index is not None:
                    h2_id = children[h2_index]["id"]
    
                    # 2) heading_2 바로 다음 블록들 중 기존 heading_3와 image 찾기
                    h3_block = next((b for b in children[h2_index+1:] if b["type"] == "heading_3"), None)
                    img_block = next((b for b in children[h2_index+1:] if b["type"] == "image"), None)
    
                    # 3) 기존 heading_3 삭제 후 새 값 추가
                    if h3_block:
                        notion.blocks.delete(h3_block["id"])
                        notion.blocks.children.append(
                            block_id=col_id,
                            after=h2_id,
                            children=[{
                                "object": "block",
                                "type": "heading_3",
                                "heading_3": {
                                    "rich_text": [{
                                        "type": "text",
                                        "text": {"content": target["text"]},
                                        "annotations": {"color": target["color"]}
                                    }]
                                }
                            }]
                        )
    
                    # 4) 기존 image 삭제 후 새 이미지 추가
                    if img_block:
                        notion.blocks.delete(img_block["id"])
                        # 새로 추가된 heading_3 블록 바로 뒤에 연결하고 싶다면 h3_block["id"] 사용
                        notion.blocks.children.append(
                            block_id=col_id,
                            after=h3_block["id"] if h3_block else h2_id,
                            children=[{
                                "object": "block",
                                "type": "image",
                                "image": {
                                    "type": "external",
                                    "external": {"url": target["chart_url"]}
                                }
                            }]
                        )
