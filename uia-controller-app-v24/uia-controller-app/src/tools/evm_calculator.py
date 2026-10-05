"""
Enhanced EVM Calculator for UiA Controlling App (v18)
Integrates directly with SQLite database (projects.db) or CSV staging files.
Supports dataset tag 'test2026T1' for 2026 project testing.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def calculate_evm_from_db(db_path: str = None, table_name: str = "evm_projects_2026") -> pd.DataFrame:
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    p = Path(db_path)
    csv_file = DEFAULT_STAGING_DIR / "evm_prosjekter_2026_test2026T1.csv"

    if csv_file.exists():
        df = pd.read_csv(csv_file)
        # Rename uppercase columns to lower case if needed
        df = df.rename(columns={
            "Project_ID": "project_id",
            "Project_Name": "project_name",
            "BAC_NOK": "bac",
            "PV_Aug_NOK": "pv",
            "EV_Aug_NOK": "ev",
            "AC_Aug_NOK": "ac"
        })
    elif p.exists():
        conn = sqlite3.connect(str(p))
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        conn.close()
    else:
        raise FileNotFoundError(f"Finner verken prosjektdatabase {db_path} eller CSV-fil {csv_file}")

    # Standardize column names
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
    return df

def generate_evm_report(db_path: str = None) -> str:
    df = calculate_evm_from_db(db_path)
    output = []
    output.append("=== PROJECT CONTROLLER MONTHLY PERFORMANCE REVIEW (EVM 2026 - tag: test2026T1) ===")
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
    print(generate_evm_report())
