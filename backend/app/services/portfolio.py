from collections import defaultdict
from app.models import Position


def compute_positions(transactions, prices=None):
    prices = prices or {}
    state = defaultdict(lambda: {"qty": 0.0, "cost": 0.0, "realized": 0.0, "name": ""})
    closed = []
    for tx in transactions:
        if not tx.asset_id:
            continue
        item = state[tx.asset_id]
        item["name"] = tx.asset_name or item["name"]
        ttype = (tx.type or "").lower()
        if "buy" in ttype:
            item["qty"] += tx.quantity
            item["cost"] += abs(tx.cash_amount)
        elif "sell" in ttype and tx.quantity > 0:
            avg = item["cost"] / item["qty"] if item["qty"] else 0
            sold_cost = avg * tx.quantity
            item["qty"] -= tx.quantity
            item["cost"] -= sold_cost
            pnl = tx.realized_pnl if tx.realized_pnl else (abs(tx.cash_amount) - sold_cost)
            item["realized"] += pnl
            closed.append({"asset_id": tx.asset_id, "asset_name": item["name"], "sold_qty": tx.quantity, "sold_value": abs(tx.cash_amount), "realized_pnl": pnl, "sold_at": tx.timestamp.isoformat()})
    positions = []
    for aid, item in state.items():
        if item["qty"] <= 0:
            continue
        current_price = prices.get(aid)
        value = item["qty"] * current_price if current_price else 0
        unreal = value - item["cost"] if current_price else 0
        positions.append(Position(aid, item["name"], item["qty"], item["cost"] / item["qty"], item["cost"], item["realized"], unreal, current_price, value))
    return positions, closed


def compute_kpis(transactions, positions):
    sums = {
        "totale_stortingen": 0.0,
        "totale_opnames": 0.0,
        "gerealiseerde_pnl": 0.0,
        "dividend_netto": 0.0,
        "rente": 0.0,
        "totale_fees": 0.0,
    }
    for tx in transactions:
        cat = (tx.category or "").lower()
        if "deposit" in cat:
            sums["totale_stortingen"] += abs(tx.cash_amount)
        if "withdraw" in cat:
            sums["totale_opnames"] += abs(tx.cash_amount)
        sums["gerealiseerde_pnl"] += tx.realized_pnl
        sums["dividend_netto"] += tx.dividend_net
        sums["totale_fees"] += tx.fee
        if "interest" in cat:
            sums["rente"] += tx.cash_amount
    sums["open_portefeuillewaarde"] = sum(p.current_value_eur for p in positions)
    sums["netto_resultaat"] = sums["gerealiseerde_pnl"] + sums["dividend_netto"] + sums["rente"] - sums["totale_fees"]
    return sums
