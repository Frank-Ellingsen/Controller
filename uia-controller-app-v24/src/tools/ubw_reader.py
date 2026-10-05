"""
UBW Reader Tool for UiA Controlling App (v18)
Reads transaction data from CSV, Excel or SQLite database and checks compliance rules.
Supports dataset tag 'test2026T1' for 2026 transactions.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def read_ubw_data(source_path: str = None, tag: str = "test2026T1") -> pd.DataFrame:
    if source_path is None:
        source_path = str(DEFAULT_DB_PATH)
        
    p = Path(source_path)
    csv_2026 = DEFAULT_STAGING_DIR / f"regnskap_august_2026_{tag}.csv"

    if csv_2026.exists():
        df = pd.read_csv(csv_2026)
    elif p.exists() and p.suffix in [".db", ".sqlite"]:
        conn = sqlite3.connect(str(p))
        try:
            df = pd.read_sql_query("SELECT * FROM ubw_transactions_2026", conn)
        except Exception:
            df = pd.read_sql_query("SELECT * FROM ubw_transactions", conn)
        conn.close()
    elif p.suffix == ".csv":
        df = pd.read_csv(p)
    elif p.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(p)
    else:
        raise ValueError(f"Utsøkt filformat ikke støttet: {source_path}")
        
    return df

def henter_transaksjonsflagg(df: pd.DataFrame) -> pd.DataFrame:
    """Legger til kontrollflagg for fire-øyne-prinsipp og bilagskrav (>100 NOK)."""
    df = df.copy()
    flagg_liste = []
    
    col_map = {c: c.lower() for c in df.columns}
    df_lower = df.rename(columns=col_map)

    for idx, row in df_lower.iterrows():
        flagg = []
        bdm = str(row.get('bdm_id', '')).strip()
        attestant = str(row.get('attestant_id', '')).strip()
        belop = float(row.get('belop_nok', 0))
        kvittering = row.get('kvittering_vedlagt', True)
        
        # Sjekk 1: Egengodkjenning
        if bdm and attestant and bdm == attestant:
            flagg.append("BRUDD: Egengodkjent (BDM == Attestant)")
            
        # Sjekk 2: Kvitteringskrav over 100 kr
        if belop > 100 and (kvittering is False or str(kvittering).lower() in ['0', 'false', 'f']):
            flagg.append("BRUDD: Mangler kvittering (>100 NOK)")
            
        flagg_liste.append("; ".join(flagg) if flagg else "OK")
        
    df['Kontrollflagg'] = flagg_liste
    return df

if __name__ == "__main__":
    df = read_ubw_data()
    df_flagg = henter_transaksjonsflagg(df)
    print("--- UBW Transaksjonskontroll (2026 - tag: test2026T1) ---")
    print(df_flagg[['transaksjon_id', 'konto', 'belop_nok', 'Kontrollflagg']].head(10))
