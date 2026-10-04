"""
Enhanced EVM Calculator for UiA Controlling App (v18)
Integrates directly with SQLite database (projects.db) or CSV staging files.
Supports dataset tag 'test2026T1' for 2026 project testing while maintaining
full backwards compatibility with baseline portfolio models and tests.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def calculate_evm_from_db(db_path: str = None, table_name: str = None, tag: str = None) -> pd.DataFrame:
    """
    Beregner fullstendige EVM-nøkkeltall (CPI, SPI, CV, SV, EAC, VAC, ETC, TCPI).
    Hvis tag='test2026T1' eller table_name='evm_projects_2026', benyttes 2026-datasettet (5 prosjekter).
    Standard er 'evm_projects' fra SQLite projects.db (3 prosjekter).
    """
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    p = Path(db_path)
    csv_file = DEFAULT_STAGING_DIR / "evm_prosjekter_2026_test2026T1.csv"

    # Determine whether 2026 tagged dataset is requested
    use_2026 = (tag == "test2026T1") or (table_name in ["evm_projects_2026", "evm_projects_test2026T1"])

    if use_2026 and csv_file.exists():
        df = pd.read_csv(csv_file)
        df = df.rename(columns={
            "Project_ID": "project_id",
            "Project_Name": "project_name",
            "BAC_NOK": "bac",
            "PV_Aug_NOK": "pv",
            "EV_Aug_NOK": "ev",
            "AC_Aug_NOK": "ac"
        })
    elif p.exists():
        target_table = table_name if table_name else ("evm_projects_2026" if tag == "test2026T1" else "evm_projects")
        conn = sqlite3.connect(str(p))
        try:
            df = pd.read_sql_query(f"SELECT * FROM {target_table}", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        conn.close()
    elif csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        raise FileNotFoundError(f"Finner verken prosjektdatabase {db_path} eller CSV-fil {csv_file}")

    # Standardize column names to lower
    df.columns = [c.lower() for c in df.columns]

    # Calculate EVM Metrics
    df['cpi'] = (df['ev'] / df['ac']).round(2)
    df['spi'] = (df['ev'] / df['pv']).round(2)
    df['cv'] = (df['ev'] - df['ac']).round(2)
    df['sv'] = (df['ev'] - df['pv']).round(2)
    df['eac'] = (df['bac'] / df['cpi']).round(2)
    df['vac'] = (df['bac'] - df['eac']).round(2)
    df['etc'] = (df['eac'] - df['ac']).round(2)
    
    # TCPI = (BAC - EV) / (BAC - AC)
    df['tcpi'] = ((df['bac'] - df['ev']) / (df['bac'] - df['ac'])).round(2)

    # Determine status
    def determine_status(row):
        if row['cpi'] < 0.85 or row['spi'] < 0.85 or row['vac'] < -1000000:
            return "CRITICAL"
        elif row['cpi'] < 0.95 or row['spi'] < 0.95:
            return "WARNING"
        return "ON TRACK"

    df['status'] = df.apply(determine_status, axis=1)

    # Provide uppercase aliases for backwards compatibility with tests and dashboard consumers
    df['CPI'] = df['cpi']
    df['SPI'] = df['spi']
    df['CV'] = df['cv']
    df['SV'] = df['sv']
    df['EAC'] = df['eac']
    df['VAC'] = df['vac']
    df['ETC'] = df['etc']
    df['TCPI'] = df['tcpi']
    df['Status'] = df['status']

    return df

def generate_evm_report(db_path: str = None, tag: str = None, table_name: str = None) -> str:
    target_table = table_name or ("evm_projects_2026" if tag == "test2026T1" else None)
    df = calculate_evm_from_db(db_path, table_name=target_table, tag=tag)
    output = []
    tag_str = f" - tag: {tag}" if tag else ""
    output.append(f"=== PROJECT CONTROLLER MONTHLY PERFORMANCE REVIEW (EVM 2026{tag_str}) ===")
    output.append("Reporting Currency: NOK | Method: Typical CPI Forecast & Database Integrated\n")
    
    header = f"{'Project ID':<12} {'BAC':>12} {'PV':>10} {'EV':>10} {'AC':>10} {'CPI':>6} {'SPI':>6} {'CV':>10} {'SV':>10} {'EAC':>12} {'VAC':>11} {'ETC':>10} {'TCPI':>6} {'Status':<9}"
    output.append(header)
    output.append("-" * len(header))

    for _, row in df.iterrows():
        line = f"{row['project_id']:<12} {row['bac']:12,.0f} {row['pv']:10,.0f} {row['ev']:10,.0f} {row['ac']:10,.0f} {row['cpi']:6.2f} {row['spi']:6.2f} {row['cv']:10,.0f} {row['sv']:10,.0f} {row['eac']:12,.0f} {row['vac']:11,.0f} {row['etc']:10,.0f} {row['tcpi']:6.2f} {row['status']:<9}"
        output.append(line)

    output.append("-" * len(header))
    return "\n".join(output)

if __name__ == "__main__":
    print(generate_evm_report(tag="test2026T1"))
