"""
Full 2026 Dataset Generator & Account Statement Engine for UiA (v25)
Generates realistic full-year 2026 budget data for ALL UiA faculties/units and
actuals up to October 2026 (M01-M10), with full drill-down capability:
Level 1: Total UiA Consolidated
Level 2: Faculty / Unit (8 units)
Level 3: Account Category / Artskonto (3xxx, 5xxx, 6xxx, 7xxx)
Level 4: Detailed Monthly Transactions & Snapshots
"""

from pathlib import Path
import pandas as pd
import numpy as np
import sqlite3
import duckdb
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STAGING_DIR = BASE_DIR / "data" / "staging"
PARQUET_DIR = STAGING_DIR / "parquet"

# UiA Units and Share of Ramme (Total NOK 2,075,076,544)
UIA_UNITS = [
    {"name": "Handelshøyskolen (HH)", "code": "HH", "share": 0.065, "type": "Fakultet"},
    {"name": "Fakultet for helse- og idrettsvitenskap (HELS)", "code": "HELS", "share": 0.100, "type": "Fakultet"},
    {"name": "Fakultet for humaniora og pedagogikk (HUM)", "code": "HUM", "share": 0.102, "type": "Fakultet"},
    {"name": "Fakultet for kunstfag (KUNST)", "code": "KUNST", "share": 0.050, "type": "Fakultet"},
    {"name": "Fakultet for samfunnsvitenskap (SAMF)", "code": "SAMF", "share": 0.082, "type": "Fakultet"},
    {"name": "Fakultet for teknologi og realfag (TN)", "code": "TN", "share": 0.142, "type": "Fakultet"},
    {"name": "Fellesadministrasjon & Fellestjenester (ADM)", "code": "ADM", "share": 0.220, "type": "Administrasjon"},
    {"name": "Særkostnader & Fellesutgifter (FELLES)", "code": "FELLES", "share": 0.239, "type": "Fellesutgifter"}
]

TOTAL_BUDGET_2026 = 2075076544.0

ACCOUNT_CATEGORIES = [
    {"konto": "3000", "kontonavn": "Statlig Rammebevilgning (Kap 260.50)", "kategori": "3xxx Inntekter", "share": -0.82},
    {"konto": "3400", "kontonavn": "BOA Ekstern Prosjektstøtte (NFR/EU)", "kategori": "3xxx Inntekter", "share": -0.18},
    {"konto": "5000", "kontonavn": "Fast Lønn & Sosiale Kostnader", "kategori": "5xxx Lønn", "share": 0.64},
    {"konto": "5330", "kontonavn": "Sensorhonorar & Timelønnede", "kategori": "5xxx Lønn", "share": 0.06},
    {"konto": "6000", "kontonavn": "Husleie & Eiendomsdrift", "kategori": "6xxx Drift", "share": 0.14},
    {"konto": "6800", "kontonavn": "IKT, Rekvisita & Utstyr", "kategori": "6xxx Drift", "share": 0.08},
    {"konto": "7100", "kontonavn": "Reise & Representasjon", "kategori": "7xxx Reiser", "share": 0.05},
    {"konto": "7800", "kontonavn": "Andre Driftskostnader & Konsulenter", "kategori": "7xxx Reiser", "share": 0.03}
]

# Actual Performance Multipliers up to October (M01-M10) by Unit
ACTUAL_RUN_RATES = {
    "HH": 0.985,      # HH: 1.5% under budget
    "HELS": 0.970,    # HELS: 3.0% under budget (delayed recruiting)
    "HUM": 0.990,     # HUM: 1.0% under budget
    "KUNST": 0.975,   # KUNST: 2.5% under budget
    "SAMF": 0.980,    # SAMF: 2.0% under budget
    "TN": 1.015,      # TN: 1.5% over budget (lab equipment & energy)
    "ADM": 0.965,     # ADM: 3.5% under budget (IT project deferral)
    "FELLES": 0.995   # FELLES: 0.5% under budget
}

def generate_and_ingest_uia_2026_data():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)

    budget_rows = []
    actual_rows = []
    drilldown_rows = []
    
    months_all = [f"2026-M{m:02d}" for m in range(1, 13)]
    months_actual = [f"2026-M{m:02d}" for m in range(1, 11)]

    # 1. Generate Full Year Budget
    for unit in UIA_UNITS:
        unit_annual_budget = TOTAL_BUDGET_2026 * unit["share"]

        for cat in ACCOUNT_CATEGORIES:
            cat_annual_budget = unit_annual_budget * cat["share"]
            cat_monthly_budget = cat_annual_budget / 12.0

            for m_idx, m_str in enumerate(months_all, 1):
                quarter = f"Q{(m_idx-1)//3 + 1}"
                tertial = f"T{(m_idx-1)//4 + 1}"
                
                budget_rows.append({
                    "Budsjett_ID": f"BUD2026-{unit['code']}-{cat['konto']}-{m_idx:02d}",
                    "Maaned": m_str,
                    "Kvartal": quarter,
                    "Tertial": tertial,
                    "Avdeling_Kode": unit["code"],
                    "Avdeling": unit["name"],
                    "Enhet_Type": unit["type"],
                    "Konto": cat["konto"],
                    "Kontonavn": cat["kontonavn"],
                    "Kategori": cat["kategori"],
                    "Budsjett_Maaned_NOK": round(cat_monthly_budget, 2),
                    "Tag": "2026_UiA_Full_Oct"
                })

    df_budget_all = pd.DataFrame(budget_rows)

    # 2. Generate Actuals M01-M10
    tx_id_counter = 20001
    for unit in UIA_UNITS:
        run_rate = ACTUAL_RUN_RATES[unit["code"]]
        unit_budget = TOTAL_BUDGET_2026 * unit["share"]

        for cat in ACCOUNT_CATEGORIES:
            cat_annual_budget = unit_budget * cat["share"]
            cat_monthly_budget = cat_annual_budget / 12.0

            for m_idx, m_str in enumerate(months_actual, 1):
                quarter = f"Q{(m_idx-1)//3 + 1}"
                tertial = f"T{(m_idx-1)//4 + 1}"
                
                noise = np.random.uniform(0.985, 1.015)
                m_actual_val = cat_monthly_budget * run_rate * noise
                
                sub_vals = np.random.dirichlet(np.ones(3)) * m_actual_val
                
                for s_idx, val in enumerate(sub_vals, 1):
                    day = min(s_idx * 9, 28)
                    date_str = f"2026-{m_idx:02d}-{day:02d}"
                    
                    flag = "OK"
                    if cat["konto"] in ["6800", "7100"] and np.random.rand() < 0.08:
                        flag = "BRUDD: Mangler kvittering (>100 NOK)" if np.random.rand() < 0.5 else "BRUDD: Egengodkjent (BDM == Attestant)"

                    bdm_id = f"EMP-{100 + (hash(unit['code']) % 20)}"
                    attest_id = bdm_id if "Egengodkjent" in flag else f"EMP-{120 + (hash(unit['code']) % 20)}"

                    actual_rows.append({
                        "Transaksjon_ID": f"TX-{tx_id_counter}",
                        "Dato": date_str,
                        "Maaned": m_str,
                        "Kvartal": quarter,
                        "Tertial": tertial,
                        "Avdeling_Kode": unit["code"],
                        "Avdeling": unit["name"],
                        "Enhet_Type": unit["type"],
                        "Konto": cat["konto"],
                        "Kontonavn": cat["kontonavn"],
                        "Kategori": cat["kategori"],
                        "Beskrivelse": f"{cat['kontonavn']} - {m_str} ({unit['code']})",
                        "Belop_NOK": round(val, 2),
                        "BDM_ID": bdm_id,
                        "Attestant_ID": attest_id,
                        "Kvittering_Vedlagt": False if "Mangler" in flag else True,
                        "Kontrollflagg": flag,
                        "Tag": "2026_UiA_Full_Oct"
                    })
                    tx_id_counter += 1

    df_actuals_all = pd.DataFrame(actual_rows)

    # 3. Build Account Statement Drill-Down Dataset (Level 1, 2, 3)
    for unit in UIA_UNITS:
        unit_code = unit["code"]
        unit_name = unit["name"]
        
        b_unit = df_budget_all[df_budget_all["Avdeling_Kode"] == unit_code]
        a_unit = df_actuals_all[df_actuals_all["Avdeling_Kode"] == unit_code]

        for cat in ACCOUNT_CATEGORIES:
            konto = cat["konto"]
            cat_name = cat["kontonavn"]
            kategori = cat["kategori"]

            total_budget_fy = b_unit[b_unit["Konto"] == konto]["Budsjett_Maaned_NOK"].sum()
            budget_ytd_oct = b_unit[(b_unit["Konto"] == konto) & (b_unit["Maaned"].isin(months_actual))]["Budsjett_Maaned_NOK"].sum()
            actual_ytd_oct = a_unit[a_unit["Konto"] == konto]["Belop_NOK"].sum()
            
            progress_ratio = (actual_ytd_oct / budget_ytd_oct) if budget_ytd_oct != 0 else 1.0
            progress_value_oct = budget_ytd_oct * (1.0 + (progress_ratio - 1.0) * 0.7)

            cost_variance_nok = progress_value_oct - actual_ytd_oct
            cost_variance_pct = (cost_variance_nok / abs(budget_ytd_oct) * 100.0) if budget_ytd_oct != 0 else 0.0

            remaining_budget_nov_des = total_budget_fy - budget_ytd_oct
            run_rate = ACTUAL_RUN_RATES[unit_code]
            forecast_eoy = actual_ytd_oct + (remaining_budget_nov_des * run_rate)
            forecast_variance_eoy_nok = total_budget_fy - forecast_eoy
            forecast_variance_eoy_pct = (forecast_variance_eoy_nok / abs(total_budget_fy) * 100.0) if total_budget_fy != 0 else 0.0

            drilldown_rows.append({
                "Avdeling_Kode": unit_code,
                "Avdeling": unit_name,
                "Enhet_Type": unit["type"],
                "Konto": konto,
                "Kontonavn": cat_name,
                "Kategori": kategori,
                "Total_Budget_FY_NOK": round(total_budget_fy, 2),
                "Budget_YTD_Oct_NOK": round(budget_ytd_oct, 2),
                "Actual_YTD_Oct_NOK": round(actual_ytd_oct, 2),
                "Progress_Value_Oct_NOK": round(progress_value_oct, 2),
                "Cost_Variance_YTD_NOK": round(cost_variance_nok, 2),
                "Cost_Variance_YTD_Pct": round(cost_variance_pct, 2),
                "Forecast_EOY_NOK": round(forecast_eoy, 2),
                "Forecast_Variance_EOY_NOK": round(forecast_variance_eoy_nok, 2),
                "Forecast_Variance_EOY_Pct": round(forecast_variance_eoy_pct, 2),
                "Tag": "2026_UiA_Full_Oct"
            })

    df_drilldown = pd.DataFrame(drilldown_rows)

    # 4. Save CSV Files
    df_budget_all.to_csv(STAGING_DIR / "budsjett_2026_totalt_uia_alle_fakulteter.csv", index=False)
    df_actuals_all.to_csv(STAGING_DIR / "regnskap_oktober_2026_totalt_uia_alle_fakulteter.csv", index=False)
    df_drilldown.to_csv(STAGING_DIR / "fakultet_drilldown_statement_2026.csv", index=False)

    # 5. Save Parquet Exports
    df_budget_all.to_parquet(PARQUET_DIR / "Fact_Budget_2026_Full.parquet", index=False)
    df_actuals_all.to_parquet(PARQUET_DIR / "Fact_Actuals_2026_Oct.parquet", index=False)
    df_drilldown.to_parquet(PARQUET_DIR / "Fact_Faculty_Drilldown_2026.parquet", index=False)
    df_drilldown.to_csv(PARQUET_DIR / "Fact_Faculty_Drilldown_2026.csv", index=False)

    # 6. Save SQLite DB
    conn_sqlite = sqlite3.connect(STAGING_DIR / "projects.db")
    df_budget_all.to_sql("budget_2026_full", conn_sqlite, if_exists="replace", index=False)
    df_actuals_all.to_sql("actuals_2026_oct", conn_sqlite, if_exists="replace", index=False)
    df_drilldown.to_sql("faculty_drilldown_2026", conn_sqlite, if_exists="replace", index=False)
    conn_sqlite.close()

    # 7. Save DuckDB Snapshots
    con_duck = duckdb.connect(str(STAGING_DIR / "analytics_snapshots.duckdb"))
    con_duck.execute("CREATE TABLE IF NOT EXISTS faculty_drilldown_snapshots AS SELECT * FROM df_drilldown WHERE 1=0")
    con_duck.execute("DELETE FROM faculty_drilldown_snapshots WHERE Tag = '2026_UiA_Full_Oct'")
    con_duck.register("df_view", df_drilldown)
    con_duck.execute("INSERT INTO faculty_drilldown_snapshots SELECT * FROM df_view")
    con_duck.close()

    print("Data generation and ingestion complete!")
    print(f" - Budget 2026 Full: {len(df_budget_all)} rows, Total FY = {df_budget_all['Budsjett_Maaned_NOK'].sum():,.2f} NOK")
    print(f" - Actuals YTD Oct: {len(df_actuals_all)} rows, Total YTD = {df_actuals_all['Belop_NOK'].sum():,.2f} NOK")
    print(f" - Drilldown Statement: {len(df_drilldown)} rows across {len(UIA_UNITS)} units and {len(ACCOUNT_CATEGORIES)} accounts")

    return df_drilldown

if __name__ == "__main__":
    generate_and_ingest_uia_2026_data()
