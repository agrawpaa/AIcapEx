import pandas as pd
import matplotlib.pyplot as plt

# model inputs
oracle_config = {
    "gross_server_cost": 30345.0,  # computer/network equipment
    "annual_capex_actual": 21215.0,  # FY2025 cash capex
    "annual_revenue": 57400.0,  # FY2025 base revenue
    "annual_op_income": 17700.0,  # FY2025 base operating income
    "acct_life_yrs": 5.0,  # stated policy
    "econ_life_yrs": 3.0,  # risk assumption
    "forecast_years": 4  # 2025 - 2028 projection
}


def run_oracle_risk_model(data, life_yrs, scenario_name):
    years = [2025 + i for i in range(data["forecast_years"])]
    results = []

    # from doc
    current_fleet_value = data["gross_server_cost"]

    for year in years:
        # calculate depreciation for this life assumption
        # shorter life = higher annual cost
        depr_expense = current_fleet_value / life_yrs

        # Calculate change to earnings
        # compare test life vs the 5 year accounting standard
        base_depr = current_fleet_value / data["acct_life_yrs"]
        depr_hit = depr_expense - base_depr
        adj_op_inc = data["annual_op_income"] - depr_hit

        results.append({
            "Year": year,
            "Scenario": scenario_name,
            "Fleet_Value": round(current_fleet_value),
            "Depreciation": round(depr_expense),
            "Adj_Op_Income": round(adj_op_inc),
            "Margin_%": round((adj_op_inc / data["annual_revenue"]) * 100, 1)
        })

        # fleet grows by new capex minus what we retire
        current_fleet_value += data["annual_capex_actual"] - depr_expense

    return pd.DataFrame(results)


df_base = run_oracle_risk_model(oracle_config, oracle_config["acct_life_yrs"], "Accounting (5yr)")
df_risk = run_oracle_risk_model(oracle_config, oracle_config["econ_life_yrs"], "Risk (3yr)")

print("ORACLE RISK MODEL ($ million)")
final_view = pd.concat([df_base.iloc[1:2], df_risk.iloc[1:2]])
print(final_view.to_string(index=False))

plt.figure(figsize=(10, 6))

plt.plot(df_base["Year"], df_base["Margin_%"], marker='o', linestyle='-',
         color='#f80000', linewidth=3, label='Accounting Case (5-Year Life)')

plt.plot(df_risk["Year"], df_risk["Margin_%"], marker='s', linestyle='--',
         color='#2c3e50', linewidth=3, label='AI Risk Case (3-Year Life)')

plt.fill_between(df_base["Year"], df_base["Margin_%"], df_risk["Margin_%"],
                 color='gray', alpha=0.1, label='The Earnings Gap')

plt.title('Oracle AI Risk: Margin Erosion Forecast (2025-2028)', fontsize=14, pad=20)
plt.xlabel('Fiscal Year', fontsize=12)
plt.ylabel('Operating Margin (%)', fontsize=12)
plt.xticks(df_base["Year"])
plt.ylim(10, 40)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower left')

plt.annotate('9.6% Margin Gap in 2026',
             xy=(2026, 21.2), xytext=(2026.2, 18),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()
