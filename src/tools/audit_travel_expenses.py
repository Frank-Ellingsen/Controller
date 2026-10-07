"""
Travel Expense Audit Tool for UiA Controlling App (v25)
Audits travel claims against DFØ guidelines and UiA delegation rules.
Supports 2026 claims tagged 'test2026T1', '2026T1sep', and '2026_UiA_Full_Oct'.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import pandas as pd
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"
DEFAULT_CSV_PATH = DEFAULT_STAGING_DIR / "reiseregninger_15_stk.csv"

def audit_travel_claims(csv_path: str = None, tag: str = None) -> dict:
    if csv_path is None:
        if tag:
            p_tag = DEFAULT_STAGING_DIR / f"reiseregninger_august_2026_{tag}.csv"
            csv_path = str(p_tag) if p_tag.exists() else str(DEFAULT_CSV_PATH)
        else:
            csv_path = str(DEFAULT_CSV_PATH)
        
    p = Path(csv_path)
    if not p.exists():
        p_fallback = DEFAULT_STAGING_DIR / "reiseregninger_15_stk.csv"
        p = p_fallback if p_fallback.exists() else p

    df = pd.read_csv(p)
    
    findings = []
    summary = {
        "totalt_behandlet": len(df),
        "godkjente_claims": 0,
        "avvik_claims": 0,
        "total_belop_nok": float(df["Belop_NOK"].sum()),
        "belop_med_avvik_nok": 0.0,
        "avvik_kategorier": {
            "mangler_kvittering": 0,
            "egengodkjent_bdm": 0,
            "mangler_maltidsfradrag": 0,
            "mangler_rutebeskrivelse": 0
        }
    }
    
    for idx, row in df.iterrows():
        violations = []
        
        # Rule 1: Receipt > 100 NOK
        if row["Belop_NOK"] > 100 and not row["Kvittering_Vedlagt"]:
            violations.append("BRUDD_KVITTERING: Beløp over 100 NOK mangler vedlagt originalkvittering.")
            summary["avvik_kategorier"]["mangler_kvittering"] += 1
            
        # Rule 2: Segregation of duties (BDM != Attestant)
        if str(row["BDM_ID"]) == str(row["Attestant_ID"]):
            violations.append("BRUDD_FIRE_OYNE: BDM og attestant er samme person (egengodkjenning).")
            summary["avvik_kategorier"]["egengodkjent_bdm"] += 1
            
        # Rule 3: Meal deductions
        if row["Maltid_Dekket"] != "Ingen" and not row["Fradrag_Utfort"]:
            violations.append(f"BRUDD_MALTID: Måltid var dekket ({row['Maltid_Dekket']}), men måltidsfradrag er ikke trukket fra diett.")
            summary["avvik_kategorier"]["mangler_maltidsfradrag"] += 1
            
        # Rule 4: Mileage description
        if row["Km_Godtgjorelse"] > 0 and ("Km_Rute_Beskrevet" in row and not row["Km_Rute_Beskrevet"]):
            violations.append("BRUDD_KM_RUTE: Kilometergodtgjørelse krever spesifisert rutebeskrivelse.")
            summary["avvik_kategorier"]["mangler_rutebeskrivelse"] += 1
            
        if violations:
            summary["avvik_claims"] += 1
            summary["belop_med_avvik_nok"] += float(row["Belop_NOK"])
            findings.append({
                "Reise_ID": row["Reise_ID"],
                "Ansatt": row["Ansatt"],
                "Dato": row["Dato"],
                "Formaal": row["Formaal"],
                "Belop_NOK": row["Belop_NOK"],
                "BDM_ID": row["BDM_ID"],
                "Attestant_ID": row["Attestant_ID"],
                "Avvik": violations
            })
        else:
            summary["godkjente_claims"] += 1
            
    return {"summary": summary, "findings": findings}

if __name__ == "__main__":
    res = audit_travel_claims()
    print(json.dumps(res, indent=2, ensure_ascii=False))
