"""
Data Ingestion Tool for UiA Controlling App (v19)
Handles dynamic uploading and ingestion of new data files (Regnskap/UBW, Reiseregninger, EVM, Budsjett)
into SQLite (projects.db) and DuckDB (analytics_snapshots.duckdb) with custom tags (e.g., 2026T1sep).
"""

from pathlib import Path
import sqlite3
import pandas as pd
import duckdb
import os
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_PARQUET_DIR = BASE_DIR / "data" / "staging" / "parquet"

def detect_file_type(df: pd.DataFrame, filename: str = "") -> str:
    cols = [c.lower() for c in df.columns]
    fn = filename.lower()
    
    if "reise_id" in cols or "reiseregning" in fn or "maltid_dekket" in cols:
        return "reiseregninger"
    elif "project_id" in cols or any("pv" in c for c in cols) or "evm" in fn or "prosjekter" in fn:
        return "evm_prosjekter"
    elif "budsjett_id" in cols or "budsjett_maaned_nok" in cols or "budsjett" in fn:
        return "budsjett"
    elif "transaksjon_id" in cols or "belop_nok" in cols or "regnskap" in fn or "ubw" in fn:
        return "regnskap_ubw"
    return "regnskap_ubw"

def ingest_data_file(
    file_path: str,
    tag: str = "2026T1sep",
    db_path: str = None,
    duckdb_path: str = None,
    parquet_dir: str = None
) -> dict:
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
    if parquet_dir is None:
        parquet_dir = str(DEFAULT_PARQUET_DIR)

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Fil ikke funnet: {file_path}")

    # Read DataFrame
    if p.suffix == ".csv":
        df = pd.read_csv(p)
    elif p.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(p)
    else:
        raise ValueError(f"Filformat {p.suffix} støttes ikke.")

    file_type = detect_file_type(df, p.name)
    df["Tag"] = tag

    conn_sqlite = sqlite3.connect(db_path)
    inserted_rows = len(df)

    if file_type == "regnskap_ubw":
        # Check for Kontrollflagg
        if "Kontrollflagg" not in df.columns:
            from ubw_reader import henter_transaksjonsflagg
            df = henter_transaksjonsflagg(df)

        df.to_sql("ubw_transactions_2026", conn_sqlite, if_exists="append", index=False)
        
        # Primary ubw_transactions sync
        col_map = {
            'Transaksjon_ID': 'transaksjon_id', 'Konto': 'konto', 'Beskrivelse': 'beskrivelse',
            'Belop_NOK': 'belop_nok', 'BDM_ID': 'bdm_id', 'Attestant_ID': 'attestant_id',
            'Kvittering_Vedlagt': 'kvittering_vedlagt', 'Formaal': 'formaal'
        }
        df_sync = df.rename(columns=col_map)
        if 'formaal' not in df_sync.columns:
            df_sync['formaal'] = df_sync.get('beskrivelse', 'Transaksjon')
        if 'kvittering_vedlagt' not in df_sync.columns:
            df_sync['kvittering_vedlagt'] = True

        cols_primary = ['transaksjon_id', 'konto', 'beskrivelse', 'belop_nok', 'bdm_id', 'attestant_id', 'kvittering_vedlagt', 'formaal']
        df_primary = df_sync[cols_primary]
        
        df_primary.to_sql("ubw_transactions_temp", conn_sqlite, if_exists="replace", index=False)
        conn_sqlite.execute("""
            INSERT OR REPLACE INTO ubw_transactions (transaksjon_id, konto, beskrivelse, belop_nok, bdm_id, attestant_id, kvittering_vedlagt, formaal)
            SELECT transaksjon_id, konto, beskrivelse, belop_nok, bdm_id, attestant_id, kvittering_vedlagt, formaal FROM ubw_transactions_temp
        """)
        conn_sqlite.execute("DROP TABLE IF EXISTS ubw_transactions_temp")
        conn_sqlite.commit()

    elif file_type == "reiseregninger":
        if "Kontrollflagg" not in df.columns:
            from audit_travel_expenses import audit_travel_claims
            res = audit_travel_claims(str(p))
            findings_map = {f["Reise_ID"]: "; ".join(f["Avvik"]) for f in res["findings"]}
            df["Kontrollflagg"] = df["Reise_ID"].map(lambda x: findings_map.get(x, "OK"))

        df.to_sql("travel_claims_2026", conn_sqlite, if_exists="append", index=False)

    elif file_type == "evm_prosjekter":
        # Normalize EVM columns (e.g. PV_Sep_NOK -> PV_NOK)
        rename_dict = {}
        for col in df.columns:
            if col.startswith("PV_"): rename_dict[col] = "PV_NOK"
            elif col.startswith("EV_"): rename_dict[col] = "EV_NOK"
            elif col.startswith("AC_"): rename_dict[col] = "AC_NOK"
        df = df.rename(columns=rename_dict)

        cols_evm_2026 = ['Project_ID', 'Project_Name', 'Avdeling', 'BAC_NOK', 'PV_NOK', 'EV_NOK', 'AC_NOK', 'Tag', 'CPI', 'SPI', 'CV_NOK', 'SV_NOK', 'EAC_NOK', 'VAC_NOK', 'ETC_NOK', 'TCPI', 'Status']
        df_evm_sql = df[[c for c in cols_evm_2026 if c in df.columns]]
        df_evm_sql.to_sql("evm_projects_2026", conn_sqlite, if_exists="append", index=False)
        
        # Primary evm_projects sync
        df_sync = df.rename(columns={
            'Project_ID': 'project_id', 'Project_Name': 'project_name',
            'BAC_NOK': 'bac', 'PV_NOK': 'pv', 'EV_NOK': 'ev', 'AC_NOK': 'ac',
            'Status': 'status'
        })
        cols_primary = ['project_id', 'project_name', 'bac', 'pv', 'ev', 'ac', 'status']
        cols_present = [c for c in cols_primary if c in df_sync.columns]
        df_primary = df_sync[cols_present]
        
        df_primary.to_sql("evm_projects", conn_sqlite, if_exists="replace", index=False)

        # Snapshot in DuckDB
        con_duck = duckdb.connect(duckdb_path)
        con_duck.execute("""
            CREATE TABLE IF NOT EXISTS evm_snapshots (
                reporting_period VARCHAR, snapshot_timestamp TIMESTAMP, project_id VARCHAR,
                project_name VARCHAR, bac DOUBLE, pv DOUBLE, ev DOUBLE, ac DOUBLE,
                cpi DOUBLE, spi DOUBLE, eac_cpi DOUBLE, eac_composite DOUBLE,
                eac_weighted DOUBLE, vac DOUBLE, etc DOUBLE, tcpi DOUBLE,
                status VARCHAR, tag VARCHAR
            )
        """)
        
        period = str(df['Maaned'].iloc[0]) if 'Maaned' in df.columns else "2026-M09"
        con_duck.execute("DELETE FROM evm_snapshots WHERE reporting_period = ? AND tag = ?", [period, tag])
        
        now = datetime.now()
        duck_rows = []
        for _, r in df.iterrows():
            bac = float(r.get('BAC_NOK', r.get('bac', 0)))
            pv = float(r.get('PV_NOK', r.get('pv', 0)))
            ev = float(r.get('EV_NOK', r.get('ev', 0)))
            ac = float(r.get('AC_NOK', r.get('ac', 0)))
            cpi = float(r.get('CPI', round(ev/ac, 2) if ac>0 else 1.0))
            spi = float(r.get('SPI', round(ev/pv, 2) if pv>0 else 1.0))
            eac_cpi = float(r.get('EAC_NOK', round(bac/cpi, 2) if cpi>0 else bac))
            
            comp_idx = cpi * spi
            eac_comp = round(ac + (bac - ev)/comp_idx, 2) if comp_idx>0 else bac
            weight_idx = 0.8*cpi + 0.2*spi
            eac_weight = round(ac + (bac - ev)/weight_idx, 2) if weight_idx>0 else bac
            vac = round(bac - eac_cpi, 2)
            etc = round(eac_cpi - ac, 2)
            tcpi = float(r.get('TCPI', 1.0))
            status = str(r.get('Status', 'ON TRACK'))
            p_id = str(r.get('Project_ID', r.get('project_id', 'PROJ')))
            p_name = str(r.get('Project_Name', r.get('project_name', 'Prosjekt')))
            
            duck_rows.append((
                period, now, p_id, p_name, bac, pv, ev, ac,
                cpi, spi, eac_cpi, eac_comp, eac_weight, vac, etc, tcpi,
                status, tag
            ))
            
        con_duck.executemany("INSERT INTO evm_snapshots VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", duck_rows)
        con_duck.close()

    elif file_type == "budsjett":
        df.to_sql("budget_2026", conn_sqlite, if_exists="append", index=False)

    conn_sqlite.close()

    # Re-export Power BI Parquet Star Schema
    try:
        from powerbi_exporter import export_powerbi_data_model
        export_powerbi_data_model(db_path=db_path, duckdb_path=duckdb_path, output_dir=parquet_dir)
    except Exception as e:
        print(f"Parquet re-export note: {e}")

    return {
        "filename": p.name,
        "file_type": file_type,
        "tag": tag,
        "rows_ingested": inserted_rows,
        "status": "SUCCESS"
    }

if __name__ == "__main__":
    p1 = str(BASE_DIR / "data" / "staging" / "regnskap_september_2026_2026T1sep.csv")
    p2 = str(BASE_DIR / "data" / "staging" / "reiseregninger_september_2026_2026T1sep.csv")
    p3 = str(BASE_DIR / "data" / "staging" / "evm_prosjekter_september_2026_2026T1sep.csv")
    print(ingest_data_file(p1, tag="2026T1sep"))
    print(ingest_data_file(p2, tag="2026T1sep"))
    print(ingest_data_file(p3, tag="2026T1sep"))
