from __future__ import annotations
from pathlib import Path
import pandas as pd
from app.models import Transaction
from app.parsers.base import BrokerParser


class BuxParser(BrokerParser):
    broker = "BUX"

    def parse(self, file_path: Path):
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        key_cols = ["Transaction Time (CET)", "Transaction Description"]
        transactions = []
        for _, group in df.groupby(key_cols, dropna=False):
            row = group[group["Asset Id"].notna() & (group["Asset Id"] != "")]
            row = row.iloc[0] if not row.empty else group.iloc[0]
            amount = pd.to_numeric(row.get("Transaction Amount", 0), errors="coerce")
            qty = pd.to_numeric(row.get("Asset Quantity", 0), errors="coerce")
            price = pd.to_numeric(row.get("Asset Price", 0), errors="coerce")
            pnl = pd.to_numeric(row.get("Profit And Loss Amount", 0), errors="coerce")
            exr = pd.to_numeric(row.get("Exchange Rate", 1), errors="coerce")
            fee = abs(float(amount)) if str(row.get("Transaction Category","")).lower()=="fee" else 0.0
            tx = Transaction(
                id=f"{self.broker}-{row.get('Transaction Time (CET)')}-{row.get('Transaction Description')}",
                broker=self.broker,
                timestamp=pd.to_datetime(row.get("Transaction Time (CET)"), dayfirst=True).to_pydatetime(),
                category=row.get("Transaction Category"),
                type=row.get("Transaction Type"),
                transfer_type=row.get("Transfer Type"),
                asset_id=row.get("Asset Id") if pd.notna(row.get("Asset Id")) else None,
                asset_name=row.get("Asset Name") if pd.notna(row.get("Asset Name")) else None,
                quantity=float(qty if pd.notna(qty) else 0),
                price=float(price if pd.notna(price) else 0),
                asset_currency=row.get("Asset Currency") if pd.notna(row.get("Asset Currency")) else None,
                cash_amount=float(amount if pd.notna(amount) else 0),
                cash_currency=row.get("Transaction Currency") if pd.notna(row.get("Transaction Currency")) else "EUR",
                exchange_rate=float(exr if pd.notna(exr) and exr != 0 else 1),
                realized_pnl=float(pnl if pd.notna(pnl) else 0),
                dividend_gross=float(pd.to_numeric(row.get("Dividend Gross Amount", 0), errors="coerce") or 0),
                dividend_net=float(pd.to_numeric(row.get("Dividend Net Amount", 0), errors="coerce") or 0),
                dividend_tax=float(pd.to_numeric(row.get("Dividend Tax Amount", 0), errors="coerce") or 0),
                fee=fee,
                source_description=str(row.get("Transaction Description", "")),
            )
            transactions.append(tx)
        return sorted(transactions, key=lambda x: x.timestamp)
