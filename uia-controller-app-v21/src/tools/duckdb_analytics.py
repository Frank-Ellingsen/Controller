"""
DuckDB Analytics & Time-Series Snapshotting Tool for UiA Controlling App (v19)
Provides time-series snapshotting and advanced multi-model EAC forecasting with tag support (test2026T1, 2026T1sep).
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import duckdb
import pandas as pd
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def init_duckdb_snapshots(duckdb_path: str = None) -> str:
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
        
    con = duckdb.connect(duckdb_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS evm_snapshots (
            reporting_period VARCHAR,
            snapshot_timestamp TIMESTAMP,
            project_id VARCHAR,
            project_name VARCHAR,
            bac DOUBLE,
            pv DOUBLE,
            ev DOUBLE,
            ac DOUBLE,
            cpi DOUBLE,
            spi DOUBLE,
            eac_cpi DOUBLE,
            eac_composite DOUBLE,
            eac_weighted DOUBLE,
            vac DOUBLE,
            etc DOUBLE,
            tcpi DOUBLE,
            status VARCHAR,
            tag VARCHAR
        )
    """)
    con.close()
    return duckdb_path

def snapshot_evm_data(sqlite_path: str = None, duckdb_path: str = None, period: str = "2026-M10", tag: str = None) -> pd.DataFrame:
    if sqlite_path is None:
        sqlite_path = str(DEFAULT_SQLITE_PATH)
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
        
    init_duckdb_snapshots(duckdb_path)

    csv_file = None
    if tag == "2026T1sep":
        csv_file = DEFAULT_STAGING_DIR / "evm_prosjekter_september_2026_2026T1sep.csv"
    elif tag == "test2026T1":
        csv_file = DEFAULT_STAGING_DIR / "evm_prosjekter_2026_test2026T1.csv"
    elif tag:
        candidates = list(DEFAULT_STAGING_DIR.glob(f"evm_prosjekter_*_{tag}.csv"))
        if candidates: csv_file = candidates[0]

    if csv_file and csv_file.exists():
        df = pd.read_csv(csv_file)
        for c in df.columns:
            cl = c.lower()
            if cl.startswith("pv"): df = df.rename(columns={c: "pv"})
            elif cl.startswith("ev"): df = df.rename(columns={c: "ev"})
            elif cl.startswith("ac"): df = df.rename(columns={c: "ac"})
            elif cl == "project_id": df = df.rename(columns={c: "project_id"})
            elif cl == "project_name": df = df.rename(columns={c: "project_name"})
            elif cl == "bac_nok" or cl == "bac": df = df.rename(columns={c: "bac"})
    else:
        conn = sqlite3.connect(sqlite_path)
        try:
            if tag in ["test2026T1", "2026T1sep"] or period in ["2026-M08", "2026-M09"]:
                if tag:
                    df = pd.read_sql_query("SELECT * FROM evm_projects_2026 WHERE Tag = ?", conn, params=[tag])
                    if df.empty:
                        df = pd.read_sql_query("SELECT * FROM evm_projects_2026", conn)
                else:
                    df = pd.read_sql_query("SELECT * FROM evm_projects_2026", conn)
            else:
                df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        conn.close()
        for c in df.columns:
            cl = c.lower()
            if cl.startswith("pv"): df = df.rename(columns={c: "pv"})
            elif cl.startswith("ev"): df = df.rename(columns={c: "ev"})
            elif cl.startswith("ac"): df = df.rename(columns={c: "ac"})
            elif cl.startswith("bac"): df = df.rename(columns={c: "bac"})

    df.columns = [c.lower() for c in df.columns]

    now = datetime.now()
    results = []

    for _, row in df.iterrows():
        project_name = row.get('project_name', row['project_id'])
        bac = float(row['bac'])
        pv = float(row['pv'])
        ev = float(row['ev'])
        ac = float(row['ac'])

        cpi = round(ev / ac, 2) if ac > 0 else 1.0
        spi = round(ev / pv, 2) if pv > 0 else 1.0

        eac_cpi = round(bac / cpi, 2) if cpi > 0 else bac
        composite_idx = cpi * spi
        eac_composite = round(ac + (bac - ev) / composite_idx, 2) if composite_idx > 0 else bac
        weighted_idx = 0.8 * cpi + 0.2 * spi
        eac_weighted = round(ac + (bac - ev) / weighted_idx, 2) if weighted_idx > 0 else bac

        vac = round(bac - eac_cpi, 2)
        etc = round(eac_cpi - ac, 2)
        remaining_work = bac - ev
        remaining_fund = bac - ac
        tcpi = round(remaining_work / remaining_fund, 2) if remaining_fund > 0 else 1.0

        status = "CRITICAL" if (cpi < 0.85 or spi < 0.85 or vac < -1000000) else ("WARNING" if (cpi < 0.95 or spi < 0.95) else "ON TRACK")

        results.append({
            'reporting_period': period,
            'snapshot_timestamp': now,
            'project_id': row['project_id'],
            'project_name': project_name,
            'bac': bac,
            'pv': pv,
            'ev': ev,
            'ac': ac,
            'cpi': cpi,
            'spi': spi,
            'eac_cpi': eac_cpi,
            'eac_composite': eac_composite,
            'eac_weighted': eac_weighted,
            'vac': vac,
            'etc': etc,
            'tcpi': tcpi,
            'status': status,
            'tag': tag
        })

    res_df = pd.DataFrame(results)

    # Store in DuckDB
    con = duckdb.connect(duckdb_path)
    if tag:
        con.execute("DELETE FROM evm_snapshots WHERE reporting_period = ? AND tag = ?", [period, tag])
    else:
        con.execute("DELETE FROM evm_snapshots WHERE reporting_period = ? AND (tag IS NULL OR tag = '')", [period])
    con.register("df_view", res_df)
    con.execute("INSERT INTO evm_snapshots SELECT * FROM df_view")
    con.close()

    return res_df

def query_eac_forecasting_models(duckdb_path: str = None, tag: str = None) -> pd.DataFrame:
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
        
    con = duckdb.connect(duckdb_path)
    if tag:
        query = f"""
            SELECT 
                project_id,
                project_name,
                bac,
                ac,
                cpi,
                spi,
                eac_cpi AS eac_typical_cpi,
                eac_composite AS eac_cpi_spi,
                eac_weighted AS eac_weighted_80_20,
                tcpi,
                status
            FROM evm_snapshots
            WHERE tag = '{tag}'
            QUALIFY ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY snapshot_timestamp DESC) = 1
        """
    else:
        query = """
            SELECT 
                project_id,
                project_name,
                bac,
                ac,
                cpi,
                spi,
                eac_cpi AS eac_typical_cpi,
                eac_composite AS eac_cpi_spi,
                eac_weighted AS eac_weighted_80_20,
                tcpi,
                status
            FROM evm_snapshots
            QUALIFY ROW_NUMBER() OVER(PARTITION BY project_id ORDER BY snapshot_timestamp DESC) = 1
        """
    df = con.execute(query).fetchdf()
    con.close()
    return df

if __name__ == "__main__":
    db_duck = init_duckdb_snapshots()
    snapshot_df = snapshot_evm_data(period="2026-M09", tag="2026T1sep")
    print("=== DuckDB Time-Series Snapshot & Multi-Model EAC Forecast (September 2026 - tag: 2026T1sep) ===")
    print(query_eac_forecasting_models(tag="2026T1sep"))
