# Aandelenbeheer (MVP)

Lokale full-stack applicatie voor BUX-import, normalisatie en rapportage.

## Structuur
- `frontend/` Next.js UI (Rapportage, Actuele koersen, Niet verkocht scenario, Data import)
- `backend/` FastAPI + pandas parser + portfolio berekeningen
- `data/` voorbeeld BUX export
- `tests/` pytest tests

## Starten
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## API endpoints
- `POST /import/bux` upload CSV
- `GET /reporting` KPI + open posities + gesloten posities
- `GET /quotes` via `MarketDataProvider` (nu mockprovider)
- `GET /scenario/not-sold` theoretische "niet verkocht" scenario-output

## Architectuurkeuzes
- `BrokerParser` interface voorbereid op multi-broker (DEGIRO later).
- `MarketDataProvider` interface met `MockMarketDataProvider` en `YahooMarketDataProvider`.
- BUX parser dedupliceert dubbele cash/asset-regels per order op tijd + beschrijving.

## Tests
```bash
pytest
```
