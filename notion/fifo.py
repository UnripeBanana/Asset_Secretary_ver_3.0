from collections import deque

def process_fifo(groups):
    updates = {}
    for ticker, trades in groups.items():
        queue = deque()
        realized_profit = 0

        for trade in trades:
            page_id = trade["page_id"]

            # 페이지 정보가 없으면 생성
            if page_id not in updates:
                updates[page_id] = {}

            updates[page_id]["ticker"] = trade["ticker"]
            updates[page_id]["date"] = trade["date"]
            updates[page_id]["profit_saved"] = trade["profit_saved"]
            
            # 매수
            if trade["type"] == "매수":
                queue.append({
                    "page_id": page_id,
                    "qty": trade["qty"],
                    "price": trade["price"]
                })
                updates[page_id]["remaining"] = trade["qty"]
                updates[page_id]["profit"] = 0

            # 매도
            else:
                sell_qty = trade["qty"]
                sell_profit = 0

                # 매도 페이지의 잔량은 항상 0
                updates[page_id]["remaining"] = 0

                while sell_qty > 0:
                    if not queue:
                        raise ValueError(
                            f"{ticker}의 보유수량보다 많은 매도가 발생했습니다."
                        )

                    oldest = queue[0]

                    matched = min(
                        sell_qty,
                        oldest["qty"]
                    )

                    profit = (
                        trade["price"] - oldest["price"]
                    ) * matched

                    realized_profit += profit
                    sell_profit += profit

                    oldest["qty"] -= matched
                    sell_qty -= matched

                    # 기존 매수 페이지 잔량 감소
                    updates[oldest["page_id"]]["remaining"] -= matched

                    if oldest["qty"] == 0:
                        queue.popleft()

                updates[page_id]["profit"] = sell_profit

    return updates
