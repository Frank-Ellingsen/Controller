"""
Enhanced EVM Calculator for UiA Controlling App (v25)
Integrates directly with SQLite database (projects.db) or CSV staging files.
Supports dataset tags 'test2026T1' (August), '2026T1sep' (September), and '2026_UiA_Full_Oct'
while maintaining full backwards compatibility with baseline portfolio models and tests.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def calculate_evm_from_db(db_path: str = None, table_name: str = None, tag: str = None) -> pd.DataFrame:
    """
    Beregner fullstendige EVM-nøkkeltall (CPI, SPI, CV, SV, EAC, VAC, ETC, TCPI).
    Standard leser 'evm_projects' fra SQLite projects.db (3 baseline-prosjekter).
    """
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    p = Path(db_path)
    csv_file = None
    if tag == "2026T1sep" or (table_name and "sep" in table_name):
        csv_file = DEFAULT_STAGING_DIR / "evm_prosjekter_september_2026_2026T1sep.csv"
    elif tag in ["test2026T1", "2026_UiA_Full_Oct"] or (table_name and "2026" in table_name):
        p_oct = DEFAULT_STAGING_DIR / f"evm_prosjekter_2026_{tag}.csv"
        p_aug = DEFAULT_STAGING_DIR / "evm_prosjekter_2026_test2026T1.csv"
        csv_file = p_oct if p_oct.exists() else (p_aug if p_aug.exists() else None)

    if csv_file and csv_file.exists():
        df = pd.read_csv(csv_file)
        for c in df.columns:
            cl = c.lower()
            if cl.startswith("pv"): df = df.rename(columns={c: "pv"})
            elif cl.startswith("ev"): df = df.rename(columns={c: "ev"})
            elif cl.startswith("ac"): df = df.rename(columns={c: "ac"})
            elif cl == "project_id": df = df.rename(columns={c: "project_id"})
            elif cl == "project_name": df = df.rename(columns={c: "project_name"})
            elif cl in ["bac_nok", "bac"]: df = df.rename(columns={c: "bac"})
    elif p.exists():
        target_table = table_name if table_name else ("evm_projects_2026" if tag else "evm_projects")
        conn = sqlite3.connect(str(p))
        try:
            if tag:
                df = pd.read_sql_query(f"SELECT * FROM {target_table} WHERE Tag = ?", conn, params=[tag])
                if df.empty:
                    df = pd.read_sql_query(f"SELECT * FROM {target_table}", conn)
            else:
                df = pd.read_sql_query(f"SELECT * FROM {target_table}", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        conn.close()
        
        for c in df.columns:
            cl = c.lower()
            if cl.startswith("pv"): df = df.rename(columns={c: "pv"})
            elif cl.startswith("ev"): df = df.rename(columns={c: "ev"})
            elif cl.startswith("ac"): df = df.rename(columns={c: "ac"})
            elif cl.startswith("bac"): df = df.rename(columns={c: "bac"})
    else:
        raise FileNotFoundError(f"Finner verken prosjektdatabase {db_path} eller EVM CSV-filer.")

    # Standardize column names to lower
    df.columns = [c.lower() for c in df.columns]

    # Calculate EVM Metrics
    df['cpi'] = (df['ev'] / df['ac']).round(2)
    df['spi'] = (df['ev'] / df['pv']).round(2)
    df['cv'] = df['ev'] - df['ac']
    df['sv'] = df['ev'] - df['pv']
    df['eac'] = (df['bac'] / df['cpi']).round(2)
    df['vac'] = df['bac'] - df['eac']
    df['etc'] = df['eac'] - df['ac']

    remaining_work = df['bac'] - df['ev']
    remaining_fund = df['bac'] - df['ac']
    df['tcpi'] = (remaining_work / remaining_fund).round(2)

    def determine_status(row):
        if row['cpi'] < 0.85 or row['spi'] < 0.85 or row['vac'] < -1000000:
            return "CRITICAL"
        elif row['cpi'] < 0.95 or row['spi'] < 0.95:
            return "WARNING"
        return "ON TRACK"

    df['status'] = df.apply(determine_status, axis=1)

    # Upper case aliases for backward compatibility with tests & templates
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

def determine_status(row):
    cpi = row.get('cpi', row.get('CPI', 1.0))
    spi = row.get('spi', row.get('SPI', 1.0))
    vac = row.get('vac', row.get('VAC', 0.0))
    if cpi < 0.85 or spi < 0.85 or vac < -1000000:
        return "CRITICAL"
    elif cpi < 0.95 or spi < 0.95:
        return "WARNING"
    return "ON TRACK"

def generate_evm_report(db_path: str = None, tag: str = None, table_name: str = None) -> str:
    target_table = table_name or ("evm_projects_2026" if tag in ["test2026T1", "2026T1sep"] else None)
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
    print(generate_evm_report())
