from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    id: str
    broker: str
    timestamp: datetime
    category: Optional[str] = None
    type: Optional[str] = None
    transfer_type: Optional[str] = None
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    quantity: float = 0.0
    price: float = 0.0
    asset_currency: Optional[str] = None
    cash_amount: float = 0.0
    cash_currency: Optional[str] = None
    exchange_rate: float = 1.0
    realized_pnl: float = 0.0
    dividend_gross: float = 0.0
    dividend_net: float = 0.0
    dividend_tax: float = 0.0
    fee: float = 0.0
    source_description: str = ""


@dataclass
class Position:
    asset_id: str
    asset_name: str
    quantity: float
    avg_cost_eur: float
    invested_eur: float
    realized_pnl_eur: float
    unrealized_pnl_eur: float
    current_price: Optional[float]
    current_value_eur: float
