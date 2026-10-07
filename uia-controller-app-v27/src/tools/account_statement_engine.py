"""
Account Statement & Project Controls Reporting Engine for UiA Controlling App (v26)
Generates intuitive 8-column Finance/Project-Controls Account Statements,
full UiA Faculty/Unit Drill-Down Statements up to October 2026 with EOY Forecasts,
and Monthly Time-Series for S-Curve Visualizations (M01-M12 PV, EV, AC, EAC).
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import pandas as pd
import sqlite3
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_PARQUET_DIR = BASE_DIR / "data" / "staging" / "parquet"

def get_sample_project_controls_statement() -> pd.DataFrame:
    """Returnerer den brukerdefinerte prøveoppstillingen for prosjektstyring."""
    data = [
        {
            "Account": "Engineering",
            "Total Budget": 20.0,
            "Budget YTD": 12.0,
            "Actual YTD": 11.0,
            "Progress Value": 10.5,
            "Cost Variance": -0.5,
            "Forecast": 21.0,
            "Forecast Variance": -1.0
        },
        {
            "Account": "Procurement",
            "Total Budget": 45.0,
            "Budget YTD": 25.0,
            "Actual YTD": 21.0,
            "Progress Value": 18.0,
            "Cost Variance": -3.0,
            "Forecast": 49.0,
            "Forecast Variance": -4.0
        },
        {
            "Account": "Construction",
            "Total Budget": 35.0,
            "Budget YTD": 13.0,
            "Actual YTD": 8.0,
            "Progress Value": 6.5,
            "Cost Variance": -1.5,
            "Forecast": 39.0,
            "Forecast Variance": -4.0
        }
    ]
    df = pd.DataFrame(data)
    
    total_row = {
        "Account": "Total",
        "Total Budget": round(df["Total Budget"].sum(), 1),
        "Budget YTD": round(df["Budget YTD"].sum(), 1),
        "Actual YTD": round(df["Actual YTD"].sum(), 1),
        "Progress Value": round(df["Progress Value"].sum(), 1),
        "Cost Variance": round(df["Progress Value"].sum() - df["Actual YTD"].sum(), 1),
        "Forecast": round(df["Forecast"].sum(), 1),
        "Forecast Variance": round(df["Total Budget"].sum() - df["Forecast"].sum(), 1)
    }
    df_total = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
    return df_total

def get_uia_full_faculty_account_statement(db_path: str = None) -> pd.DataFrame:
    """
    Genererer konsolidert 8-kolonners konto- og avdelingsstilling for ALLE 8 UiA enheter
    for 2026 med regnskap YTD til og med oktober 2026 (M01-M10) i MNOK.
    """
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)

    p_csv = Path(BASE_DIR / "data" / "staging" / "fakultet_drilldown_statement_2026.csv")
    if p_csv.exists():
        df_raw = pd.read_csv(p_csv)
    else:
        conn = sqlite3.connect(db_path)
        df_raw = pd.read_sql_query("SELECT * FROM faculty_drilldown_2026", conn)
        conn.close()

    df_costs = df_raw[df_raw["Kategori"].isin(["5xxx Lønn", "6xxx Drift", "7xxx Reiser"])]
    
    unit_grp = df_costs.groupby(["Avdeling_Kode", "Avdeling"]).agg({
        "Total_Budget_FY_NOK": "sum",
        "Budget_YTD_Oct_NOK": "sum",
        "Actual_YTD_Oct_NOK": "sum",
        "Progress_Value_Oct_NOK": "sum",
        "Cost_Variance_YTD_NOK": "sum",
        "Forecast_EOY_NOK": "sum",
        "Forecast_Variance_EOY_NOK": "sum"
    }).reset_index()

    rows = []
    for _, r in unit_grp.iterrows():
        b_fy = r["Total_Budget_FY_NOK"] / 1e6
        b_ytd = r["Budget_YTD_Oct_NOK"] / 1e6
        a_ytd = r["Actual_YTD_Oct_NOK"] / 1e6
        p_val = r["Progress_Value_Oct_NOK"] / 1e6
        c_var = r["Cost_Variance_YTD_NOK"] / 1e6
        f_eoy = r["Forecast_EOY_NOK"] / 1e6
        f_var = r["Forecast_Variance_EOY_NOK"] / 1e6

        rows.append({
            "Enhet_Kode": r["Avdeling_Kode"],
            "Account / Enhet": r["Avdeling"],
            "Total Budget 2026 (MNOK)": round(b_fy, 1),
            "Budget YTD Oct (MNOK)": round(b_ytd, 1),
            "Actual YTD Oct (MNOK)": round(a_ytd, 1),
            "Progress Value Oct (MNOK)": round(p_val, 1),
            "Cost Variance YTD (MNOK)": round(c_var, 2),
            "Forecast EOY (MNOK)": round(f_eoy, 1),
            "Forecast Variance EOY (MNOK)": round(f_var, 2)
        })

    df_res = pd.DataFrame(rows)

    tot_row = {
        "Enhet_Kode": "TOTAL",
        "Account / Enhet": "TOTALT UIA BRUTTO RAMME",
        "Total Budget 2026 (MNOK)": round(df_res["Total Budget 2026 (MNOK)"].sum(), 1),
        "Budget YTD Oct (MNOK)": round(df_res["Budget YTD Oct (MNOK)"].sum(), 1),
        "Actual YTD Oct (MNOK)": round(df_res["Actual YTD Oct (MNOK)"].sum(), 1),
        "Progress Value Oct (MNOK)": round(df_res["Progress Value Oct (MNOK)"].sum(), 1),
        "Cost Variance YTD (MNOK)": round(df_res["Cost Variance YTD (MNOK)"].sum(), 2),
        "Forecast EOY (MNOK)": round(df_res["Forecast EOY (MNOK)"].sum(), 1),
        "Forecast Variance EOY (MNOK)": round(df_res["Forecast Variance EOY (MNOK)"].sum(), 2)
    }

    df_total = pd.concat([df_res, pd.DataFrame([tot_row])], ignore_index=True)
    return df_total

def generate_uia_department_account_statement(db_path: str = None, duckdb_path: str = None) -> pd.DataFrame:
    """Backwards compatibility wrapper for UiA department statement."""
    return get_uia_full_faculty_account_statement(db_path=db_path)

def get_uia_category_drilldown_statement(unit_code: str = None) -> pd.DataFrame:
    """
    Genererer drill-down for kontokategorier (3xxx Inntekter, 5xxx Lønn, 6xxx Drift, 7xxx Reiser)
    for alle enheter eller en spesifisert fakultetskode.
    """
    p_csv = Path(BASE_DIR / "data" / "staging" / "fakultet_drilldown_statement_2026.csv")
    if not p_csv.exists():
        from generate_2026_full_data import generate_and_ingest_uia_2026_data
        generate_and_ingest_uia_2026_data()
        
    df_raw = pd.read_csv(p_csv)
    if unit_code and unit_code != "ALL":
        df_raw = df_raw[df_raw["Avdeling_Kode"] == unit_code]

    cat_grp = df_raw.groupby(["Kategori", "Konto", "Kontonavn"]).agg({
        "Total_Budget_FY_NOK": "sum",
        "Budget_YTD_Oct_NOK": "sum",
        "Actual_YTD_Oct_NOK": "sum",
        "Progress_Value_Oct_NOK": "sum",
        "Cost_Variance_YTD_NOK": "sum",
        "Forecast_EOY_NOK": "sum",
        "Forecast_Variance_EOY_NOK": "sum"
    }).reset_index()

    rows = []
    for _, r in cat_grp.iterrows():
        rows.append({
            "Kategori": r["Kategori"],
            "Account / Artskonto": f"{r['Konto']} - {r['Kontonavn']}",
            "Total Budget FY (NOK)": round(r["Total_Budget_FY_NOK"], 2),
            "Budget YTD Oct (NOK)": round(r["Budget_YTD_Oct_NOK"], 2),
            "Actual YTD Oct (NOK)": round(r["Actual_YTD_Oct_NOK"], 2),
            "Progress Value Oct (NOK)": round(r["Progress_Value_Oct_NOK"], 2),
            "Cost Variance YTD (NOK)": round(r["Cost_Variance_YTD_NOK"], 2),
            "Forecast EOY (NOK)": round(r["Forecast_EOY_NOK"], 2),
            "Forecast Variance EOY (NOK)": round(r["Forecast_Variance_EOY_NOK"], 2)
        })

    return pd.DataFrame(rows)

def get_uia_scurve_monthly_time_series() -> pd.DataFrame:
    """
    Genererer kumulativ månedlig tidsrekke (M01-M12 2026) for S-kurve visualisering.
    Kolonner: Måned | PV_MNOK | EV_MNOK | AC_MNOK | EAC_Forecast_MNOK
    """
    monthly_data = [
        {"Maaned": "2026-M01", "PV_MNOK": 172.9, "EV_MNOK": 169.0, "AC_MNOK": 168.2, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M02", "PV_MNOK": 345.8, "EV_MNOK": 340.0, "AC_MNOK": 338.5, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M03", "PV_MNOK": 518.8, "EV_MNOK": 509.5, "AC_MNOK": 507.0, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M04", "PV_MNOK": 691.7, "EV_MNOK": 680.0, "AC_MNOK": 678.2, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M05", "PV_MNOK": 864.6, "EV_MNOK": 852.0, "AC_MNOK": 849.0, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M06", "PV_MNOK": 1037.5, "EV_MNOK": 1024.0, "AC_MNOK": 1021.5, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M07", "PV_MNOK": 1210.5, "EV_MNOK": 1195.5, "AC_MNOK": 1191.0, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M08", "PV_MNOK": 1383.4, "EV_MNOK": 1368.0, "AC_MNOK": 1362.4, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M09", "PV_MNOK": 1556.3, "EV_MNOK": 1538.5, "AC_MNOK": 1532.0, "EAC_Forecast_MNOK": None},
        {"Maaned": "2026-M10", "PV_MNOK": 1729.3, "EV_MNOK": 1711.3, "AC_MNOK": 1703.5, "EAC_Forecast_MNOK": 1703.5},
        {"Maaned": "2026-M11", "PV_MNOK": 1902.2, "EV_MNOK": None, "AC_MNOK": None, "EAC_Forecast_MNOK": 1873.9},
        {"Maaned": "2026-M12", "PV_MNOK": 2075.1, "EV_MNOK": None, "AC_MNOK": None, "EAC_Forecast_MNOK": 2044.4}
    ]
    return pd.DataFrame(monthly_data)

def export_account_statements(output_dir: str = None) -> dict:
    """Eksporterer kontostillingstabellene til Parquet og CSV for Power BI og Excel."""
    if output_dir is None:
        output_dir = str(DEFAULT_PARQUET_DIR)
        
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)
    
    df_sample = get_sample_project_controls_statement()
    df_uia_fac = get_uia_full_faculty_account_statement()
    df_drill = get_uia_category_drilldown_statement()
    df_scurve = get_uia_scurve_monthly_time_series()
    
    csv_sample = p / "Fact_Account_Statement_ProjectControls.csv"
    parquet_sample = p / "Fact_Account_Statement_ProjectControls.parquet"
    df_sample.to_csv(csv_sample, index=False)
    df_sample.to_parquet(parquet_sample, index=False)
    
    csv_uia = p / "Fact_Account_Statement_UiA.csv"
    parquet_uia = p / "Fact_Account_Statement_UiA.parquet"
    df_uia_fac.to_csv(csv_uia, index=False)
    df_uia_fac.to_parquet(parquet_uia, index=False)

    csv_drill = p / "Fact_Faculty_Drilldown_2026.csv"
    parquet_drill = p / "Fact_Faculty_Drilldown_2026.parquet"
    df_drill.to_csv(csv_drill, index=False)
    df_drill.to_parquet(parquet_drill, index=False)

    csv_scurve = p / "Fact_SCurve_Monthly_2026.csv"
    parquet_scurve = p / "Fact_SCurve_Monthly_2026.parquet"
    df_scurve.to_csv(csv_scurve, index=False)
    df_scurve.to_parquet(parquet_scurve, index=False)
    
    return {
        "sample_statement_csv": str(csv_sample),
        "uia_statement_csv": str(csv_uia),
        "uia_drilldown_csv": str(csv_drill),
        "uia_scurve_csv": str(csv_scurve)
    }

if __name__ == "__main__":
    print("=== PROJECT CONTROLS ACCOUNT STATEMENT (Sample) ===")
    print(get_sample_project_controls_statement().to_string(index=False))
    print("\n=== UiA FULL FACULTY ACCOUNT STATEMENT (MNOK YTD OCT 2026) ===")
    print(get_uia_full_faculty_account_statement().to_string(index=False))
    print("\n=== UiA S-CURVE MONTHLY TIME SERIES (M01-M12 2026) ===")
    print(get_uia_scurve_monthly_time_series().to_string(index=False))
