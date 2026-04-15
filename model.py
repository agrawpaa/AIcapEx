"""
model.py — AI Infrastructure Financial Risk Model
All original calculation logic lives here, untouched.
"""

CONFIGS = {
    "Oracle": {
        "gross_server_cost": 30345.0, "annual_capex": 21215.0, "annual_revenue": 57400.0,
        "annual_op_income": 17700.0, "acct_life_yrs": 5.0, "gpu_ratio": 0.70,
        "tax_rate": 0.21, "market_cap": 435000.0, "equity": 20450.0, "energy_base": 4200.0
    },
    "Microsoft": {
        "gross_server_cost": 160000.0, "annual_capex": 145000.0, "annual_revenue": 281700.0,
        "annual_op_income": 128500.0, "acct_life_yrs": 6.0, "gpu_ratio": 0.70,
        "tax_rate": 0.19, "market_cap": 3010000.0, "equity": 270000.0, "energy_base": 12000.0
    },
    "Meta": {
        "gross_server_cost": 95000.0, "annual_capex": 125000.0, "annual_revenue": 200966.0,
        "annual_op_income": 83276.0, "acct_life_yrs": 5.5, "gpu_ratio": 0.80,
        "tax_rate": 0.15, "market_cap": 1590000.0, "equity": 170000.0, "energy_base": 8000.0
    }
}

COMPANIES = list(CONFIGS.keys())


def run_analysis(company_name, risk_life=3.0, growth_rate=0.12, energy_rate=0.05, method="DDB"):
    """
    Run 3-year financial simulation for a given company.
    Preserves original logic exactly; growth_rate and energy_rate are now parameters.
    """
    d = CONFIGS[company_name]
    gpu_f   = d["gross_server_cost"] * d["gpu_ratio"]
    other_f = d["gross_server_cost"] * (1 - d["gpu_ratio"])
    rev     = d["annual_revenue"]
    op_inc  = d["annual_op_income"]
    energy  = d["energy_base"]

    results = []

    for year in range(1, 4):
        if method == "DDB":
            g_depr = gpu_f   * (2.0 / risk_life)
            o_depr = other_f * (2.0 / 6.0)
        else:
            g_depr = gpu_f   / d["acct_life_yrs"]
            o_depr = other_f / 6.0

        t_depr    = g_depr + o_depr
        base_depr = (gpu_f + other_f) / d["acct_life_yrs"]
        depr_hit  = t_depr - base_depr

        adj_op_inc = op_inc - depr_hit - (energy * energy_rate)
        ni_adj     = adj_op_inc * (1 - d["tax_rate"])

        pe  = d["market_cap"] / ni_adj if ni_adj > 0 else float("inf")
        roe = (ni_adj / d["equity"]) * 100

        results.append({
            "year":    year,
            "fleet":   round(gpu_f + other_f),
            "depr":    round(t_depr),
            "adj_inc": round(adj_op_inc),
            "ni":      round(ni_adj),
            "pe":      round(pe, 1),
            "roe":     round(roe, 1),
            "margin":  round((adj_op_inc / rev) * 100, 1),
        })

        # Roll forward
        gpu_f   += (d["annual_capex"] * d["gpu_ratio"])           - g_depr
        other_f += (d["annual_capex"] * (1 - d["gpu_ratio"]))     - o_depr
        op_inc  *= (1 + growth_rate)

    return results


def run_all(risk_life=3.0, growth_rate=0.12, energy_rate=0.05, method="DDB"):
    """Return full simulation results for all companies."""
    return {co: run_analysis(co, risk_life, growth_rate, energy_rate, method)
            for co in COMPANIES}
