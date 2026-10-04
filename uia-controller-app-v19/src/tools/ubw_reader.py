"""
UBW Reader Tool for UiA Controlling App (v19)
Reads transaction data from CSV, Excel or SQLite database and checks compliance rules.
Supports dataset tags 'test2026T1' (August) and '2026T1sep' (September).
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def read_ubw_data(source_path: str = None, tag: str = None) -> pd.DataFrame:
    if source_path is None:
        source_path = str(DEFAULT_DB_PATH)
        
    p = Path(source_path)
    csv_file = None
    if tag == "2026T1sep":
        csv_file = DEFAULT_STAGING_DIR / "regnskap_september_2026_2026T1sep.csv"
    elif tag == "test2026T1":
        csv_file = DEFAULT_STAGING_DIR / "regnskap_august_2026_test2026T1.csv"
    elif tag:
        candidates = list(DEFAULT_STAGING_DIR.glob(f"regnskap_*_{tag}.csv"))
        if candidates:
            csv_file = candidates[0]

    if csv_file and csv_file.exists():
        df = pd.read_csv(csv_file)
    elif p.exists() and p.suffix in [".db", ".sqlite"]:
        conn = sqlite3.connect(str(p))
        try:
            if tag:
                df = pd.read_sql_query("SELECT * FROM ubw_transactions_2026 WHERE Tag = ?", conn, params=[tag])
                if df.empty:
                    df = pd.read_sql_query("SELECT * FROM ubw_transactions_2026", conn)
            else:
                df = pd.read_sql_query("SELECT * FROM ubw_transactions", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM ubw_transactions", conn)
        conn.close()
    elif p.suffix == ".csv":
        df = pd.read_csv(str(p))
    else:
        raise ValueError(f"Ukjent filformat: {p.suffix}")
    return df

def henter_transaksjonsflagg(df: pd.DataFrame) -> pd.DataFrame:
    flagg_liste = []
    
    col_map = {c: c.lower() for c in df.columns}
    df_lower = df.rename(columns=col_map)
    
    for _, rad in df_lower.iterrows():
        flagg = "OK"
        bdm = str(rad.get('bdm_id', ''))
        attestant = str(rad.get('attestant_id', ''))
        belop = float(rad.get('belop_nok', 0))
        konto = int(rad.get('konto', 0)) if pd.notnull(rad.get('konto')) else 0
        
        # Regel: Egengodkjenning
        if bdm == attestant and bdm != '':
            flagg = "BRUDD: Egengodkjent (BDM == Attestant)"
        # Regel: Bilagskrav > 100 NOK (Forenklet sjekk)
        elif belop > 100 and str(rad.get('kvittering_vedlagt', 'True')).lower() == 'false':
            flagg = "BRUDD: Kvittering mangler"
        # Regel: Representasjon krever spesifisering (Konto 7350)
        elif konto == 7350 and belop > 500:
            flagg = "KONTROLL: Representasjon krever formål og deltakerliste"
            
        flagg_liste.append(flagg)
        
    df['Kontrollflagg'] = flagg_liste
    return df

if __name__ == "__main__":
    df = read_ubw_data(tag="2026T1sep")
    df_flagg = henter_transaksjonsflagg(df)
    print("--- UBW Transaksjonskontroll (September 2026 - tag: 2026T1sep) ---")
    print(df_flagg[['Transaksjon_ID', 'Konto', 'Belop_NOK', 'Kontrollflagg']].head(10))
