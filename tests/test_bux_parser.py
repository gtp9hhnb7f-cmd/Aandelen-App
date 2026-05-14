from pathlib import Path
from app.parsers.bux import BuxParser
from app.services.portfolio import compute_positions, compute_kpis


def test_bux_parser_deduplicates_asset_cash_rows():
    tx = list(BuxParser().parse(Path('data/sample_bux.csv')))
    assert len(tx) == 4


def test_realized_pnl_uses_broker_field():
    tx = list(BuxParser().parse(Path('data/sample_bux.csv')))
    _, closed = compute_positions(tx)
    assert closed[0]['realized_pnl'] == 20


def test_fees_and_dividend_and_closed_positions():
    tx = list(BuxParser().parse(Path('data/sample_bux.csv')))
    positions, _ = compute_positions(tx)
    assert positions == []
    kpis = compute_kpis(tx, positions)
    assert kpis['totale_fees'] == 2
    assert kpis['dividend_netto'] == 4


def test_not_sold_scenario_with_mock_prices():
    tx = list(BuxParser().parse(Path('data/sample_bux.csv')))
    _, closed = compute_positions(tx, prices={'NN.AS':100})
    c = closed[0]
    theoretical = c['sold_qty'] * 100
    extra = theoretical - c['sold_value'] - c['realized_pnl']
    assert theoretical == 200
    assert extra == 60
