"""
Power BI Data Exporter & Model Generator for UiA Controlling App (v11)
Extracts Star Schema tables from SQLite (projects.db) and DuckDB (analytics_snapshots.duckdb),
and exports compressed Parquet and CSV files to data/staging/parquet/ for Power BI import.
"""

import os
import sqlite3
import pandas as pd
import duckdb
from pathlib import Path

def export_powerbi_data_model(
    db_path: str = None, 
    duckdb_path: str = None, 
    travel_csv_path: str = None,
    output_dir: str = None
) -> dict:
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    if db_path is None:
        db_path = str(base_dir / "data" / "staging" / "projects.db")
    if duckdb_path is None:
        duckdb_path = str(base_dir / "data" / "staging" / "analytics_snapshots.duckdb")
    if travel_csv_path is None:
        travel_csv_path = str(base_dir / "data" / "staging" / "reiseregninger_15_stk.csv")
    if output_dir is None:
        output_dir = str(base_dir / "data" / "staging" / "parquet")
        
    os.makedirs(output_dir, exist_ok=True)
    exported_files = {}

    # 1. Fact_EVM_Snapshots (from DuckDB)
    if os.path.exists(duckdb_path):
        con_duck = duckdb.connect(duckdb_path, read_only=True)
        df_evm = con_duck.execute("SELECT * FROM evm_snapshots").fetchdf()
        con_duck.close()
        
        evm_parquet = os.path.join(output_dir, "Fact_EVM_Snapshots.parquet")
        evm_csv = os.path.join(output_dir, "Fact_EVM_Snapshots.csv")
        df_evm.to_parquet(evm_parquet, index=False)
        df_evm.to_csv(evm_csv, index=False)
        exported_files["Fact_EVM_Snapshots"] = evm_parquet

    # 2. Fact_UBW_Audit & Dim_Project (from SQLite)
    if os.path.exists(db_path):
        con_sqlite = sqlite3.connect(db_path)
        df_ubw = pd.read_sql_query("SELECT * FROM ubw_transactions", con_sqlite)
        df_proj = pd.read_sql_query("SELECT * FROM evm_projects", con_sqlite)
        con_sqlite.close()

        # Add compliance flag to UBW
        try:
            from ubw_reader import henter_transaksjonsflagg
            df_ubw_flagged = henter_transaksjonsflagg(df_ubw)
        except Exception:
            df_ubw_flagged = df_ubw
        
        ubw_parquet = os.path.join(output_dir, "Fact_UBW_Audit.parquet")
        ubw_csv = os.path.join(output_dir, "Fact_UBW_Audit.csv")
        df_ubw_flagged.to_parquet(ubw_parquet, index=False)
        df_ubw_flagged.to_csv(ubw_csv, index=False)
        exported_files["Fact_UBW_Audit"] = ubw_parquet

        proj_parquet = os.path.join(output_dir, "Dim_Project.parquet")
        proj_csv = os.path.join(output_dir, "Dim_Project.csv")
        df_proj.to_parquet(proj_parquet, index=False)
        df_proj.to_csv(proj_csv, index=False)
        exported_files["Dim_Project"] = proj_parquet

    # 3. Fact_Travel_Audit (from Travel CSV)
    if os.path.exists(travel_csv_path):
        try:
            from audit_travel_expenses import audit_travel_claims
            audit_res = audit_travel_claims(travel_csv_path)
            df_travel = pd.read_csv(travel_csv_path)
            
            # Add finding flags
            findings_map = {f["Reise_ID"]: "; ".join(f["Avvik"]) for f in audit_res["findings"]}
            df_travel["Avvik_Beskrivelse"] = df_travel["Reise_ID"].map(lambda x: findings_map.get(x, "OK"))
            df_travel["Status"] = df_travel["Avvik_Beskrivelse"].map(lambda x: "FLAGGED" if x != "OK" else "APPROVED")
        except Exception:
            df_travel = pd.read_csv(travel_csv_path)

        travel_parquet = os.path.join(output_dir, "Fact_Travel_Audit.parquet")
        travel_csv = os.path.join(output_dir, "Fact_Travel_Audit.csv")
        df_travel.to_parquet(travel_parquet, index=False)
        df_travel.to_csv(travel_csv, index=False)
        exported_files["Fact_Travel_Audit"] = travel_parquet

    # 4. Dim_Date
    dates = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")
    df_date = pd.DataFrame({
        "Date": dates,
        "Year": dates.year,
        "Month": dates.month,
        "MonthName": dates.strftime("%B"),
        "ReportingPeriod": dates.strftime("2026-M%m"),
        "Quarter": dates.quarter
    })
    date_parquet = os.path.join(output_dir, "Dim_Date.parquet")
    date_csv = os.path.join(output_dir, "Dim_Date.csv")
    df_date.to_parquet(date_parquet, index=False)
    df_date.to_csv(date_csv, index=False)
    exported_files["Dim_Date"] = date_parquet

    print(f"Power BI Star Schema exported successfully to: {output_dir}")
    for name, path in exported_files.items():
        print(f" - {name}: {os.path.basename(path)}")

    return exported_files

if __name__ == "__main__":
    export_powerbi_data_model()
