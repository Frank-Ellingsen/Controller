"""
Enhanced EVM Calculator for UiA Controlling App (v11)
Integrates directly with SQLite database (projects.db) and calculates:
CPI, SPI, CV, SV, EAC, VAC, ETC, TCPI. Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"

def calculate_evm_from_db(db_path: str = None) -> pd.DataFrame:
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    p = Path(db_path)
    if not p.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(str(p))
    df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
    conn.close()

    # Calculate EVM Metrics
    df['CPI'] = (df['ev'] / df['ac']).round(2)
    df['SPI'] = (df['ev'] / df['pv']).round(2)
    df['CV'] = (df['ev'] - df['ac']).round(2)
    df['SV'] = (df['ev'] - df['pv']).round(2)
    df['EAC'] = (df['bac'] / df['CPI']).round(2)
    df['VAC'] = (df['bac'] - df['EAC']).round(2)
    df['ETC'] = (df['EAC'] - df['ac']).round(2)
    
    # TCPI = (BAC - EV) / (BAC - AC)
    df['TCPI'] = ((df['bac'] - df['ev']) / (df['bac'] - df['ac'])).round(2)

    # Determine status
    def determine_status(row):
        if row['CPI'] < 0.85 or row['SPI'] < 0.85 or row['VAC'] < -1000000:
            return "CRITICAL"
        elif row['CPI'] < 0.95 or row['SPI'] < 0.95:
            return "WARNING"
        return "ON TRACK"

    df['Status'] = df.apply(determine_status, axis=1)
    return df

def generate_evm_report(db_path: str = None) -> str:
    df = calculate_evm_from_db(db_path)
    output = []
    output.append("=== PROJECT CONTROLLER MONTHLY PERFORMANCE REVIEW (EVM v11) ===")
    output.append("Reporting Currency: NOK | Method: Typical CPI Forecast & Database Integrated\n")
    
    header = f"{'Project ID':<10} {'BAC':>12} {'PV':>10} {'EV':>10} {'AC':>10} {'CPI':>6} {'SPI':>6} {'CV':>10} {'SV':>10} {'EAC':>12} {'VAC':>11} {'ETC':>10} {'TCPI':>6} {'Status':<9}"
    output.append(header)
    output.append("-" * len(header))

    for _, row in df.iterrows():
        line = f"{row['project_id']:<10} {row['bac']:12,.0f} {row['pv']:10,.0f} {row['ev']:10,.0f} {row['ac']:10,.0f} {row['CPI']:6.2f} {row['SPI']:6.2f} {row['CV']:10,.0f} {row['SV']:10,.0f} {row['EAC']:12,.0f} {row['VAC']:11,.0f} {row['ETC']:10,.0f} {row['TCPI']:6.2f} {row['Status']:<9}"
        output.append(line)

    output.append("-" * len(header))
    return "\n".join(output)

if __name__ == "__main__":
    print(generate_evm_report())
