# AI Infrastructure Financial Risk Dashboard — Flask App

## Project Structure

```
flask_dashboard/
├── app.py              # Flask routes & API endpoint
├── model.py            # Financial model logic (original calculations)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Interactive Plotly.js dashboard
└── README.md
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## API Reference

The dashboard fetches all data from a single JSON endpoint:

### `GET /api/data`

| Parameter     | Type   | Default | Description                          |
|---------------|--------|---------|--------------------------------------|
| `risk_life`   | float  | 3.0     | GPU depreciation life in years       |
| `growth_rate` | float  | 0.12    | Annual revenue growth rate (0–1)     |
| `energy_rate` | float  | 0.05    | Energy cost escalation rate (0–1)    |
| `method`      | string | DDB     | Depreciation method: `DDB` or `SL`  |

**Example:**
```
GET /api/data?risk_life=4&growth_rate=0.15&energy_rate=0.08&method=SL
```

**Response:**
```json
{
  "companies": ["Oracle", "Microsoft", "Meta"],
  "configs":   { ... },
  "data": {
    "Oracle":    [{ "year":1, "fleet":..., "depr":..., "adj_inc":..., "ni":..., "pe":..., "roe":..., "margin":... }, ...],
    "Microsoft": [...],
    "Meta":      [...]
  },
  "ddb_year3": { "Oracle": ..., "Microsoft": ..., "Meta": ... },
  "sl_year3":  { "Oracle": ..., "Microsoft": ..., "Meta": ... }
}
```

---

## Dashboard Features

- **GPU Risk Life slider** — drag 1–7 years to stress-test accelerated depreciation impact
- **Revenue Growth slider** — 0–30% annual growth assumption
- **Energy Escalation slider** — 0–20% annual energy cost increase
- **Depreciation Method** — toggle between DDB and Straight-Line
- **Company Toggles** — isolate or compare any subset of Oracle / Microsoft / Meta
- All 10 charts and the KPI summary table update live on every control change

---

## Extending the App

To add a new company, add an entry to `CONFIGS` in `model.py` — the rest of the app
picks it up automatically via the `/api/data` endpoint.

To change the forecast horizon, adjust the `range(1, 4)` loop in `model.py` and add
the new year label in `index.html`.
