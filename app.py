"""
app.py — Flask application entry point
Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, jsonify, request
from model import run_all, run_analysis, CONFIGS, COMPANIES

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the dashboard page."""
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    """
    Return full simulation results as JSON.
    Query params:
      risk_life   — float, GPU depreciation life in years (default 3.0)
      growth_rate — float, annual revenue growth 0-1   (default 0.12)
      energy_rate — float, energy cost escalation 0-1  (default 0.05)
      method      — str,   "DDB" or "SL"               (default "DDB")
    """
    risk_life   = float(request.args.get("risk_life",   3.0))
    growth_rate = float(request.args.get("growth_rate", 0.12))
    energy_rate = float(request.args.get("energy_rate", 0.05))
    method      = request.args.get("method", "DDB")

    # Main simulation
    data = run_all(risk_life, growth_rate, energy_rate, method)

    # DDB vs SL comparison for year 3 (for the comparison chart)
    ddb_year3 = {co: run_analysis(co, risk_life, growth_rate, energy_rate, "DDB")[2]["depr"]
                 for co in COMPANIES}
    sl_year3  = {co: run_analysis(co, risk_life, growth_rate, energy_rate, "SL")[2]["depr"]
                 for co in COMPANIES}

    return jsonify({
        "data":      data,
        "ddb_year3": ddb_year3,
        "sl_year3":  sl_year3,
        "configs":   CONFIGS,
        "companies": COMPANIES,
    })


if __name__ == "__main__":
    app.run(debug=True)
