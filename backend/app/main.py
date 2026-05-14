from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.parsers.bux import BuxParser
from app.services.portfolio import compute_positions, compute_kpis
from app.services.market_data import MockMarketDataProvider

app = FastAPI(title="Aandelenbeheer API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
STATE = {"transactions": []}

@app.post('/import/bux')
async def import_bux(file: UploadFile = File(...)):
    path = Path('/tmp') / file.filename
    path.write_bytes(await file.read())
    parser = BuxParser()
    tx = list(parser.parse(path))
    STATE["transactions"] = tx
    return {"imported": len(tx)}

@app.get('/reporting')
def reporting():
    provider = MockMarketDataProvider()
    tx = STATE["transactions"]
    tickers = [t.asset_id for t in tx if t.asset_id]
    quotes = provider.get_quotes(list(set(tickers)))
    prices = {k: v["price"] for k, v in quotes.items()}
    positions, closed = compute_positions(tx, prices=prices)
    kpis = compute_kpis(tx, positions)
    return {
        "kpis": kpis,
        "positions": [p.__dict__ for p in positions],
        "closed_positions": closed,
    }

@app.get('/quotes')
def quotes():
    provider = MockMarketDataProvider()
    tx = STATE["transactions"]
    tickers = sorted({t.asset_id for t in tx if t.asset_id})
    return provider.get_quotes(tickers)

@app.get('/scenario/not-sold')
def scenario_not_sold():
    report = reporting()
    quotes = quotes()
    rows = []
    for c in report["closed_positions"]:
        q = quotes.get(c["asset_id"], {"price": 0})
        theoretical = c["sold_qty"] * q["price"]
        rows.append({**c, "theoretical_current_value": theoretical, "extra_pnl_if_held": theoretical - c["sold_value"] - c["realized_pnl"]})
    return rows
