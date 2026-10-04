"""
Travel Expense Audit Tool for UiA Controlling App (v18)
Audits travel claims against DFØ guidelines and UiA delegation rules.
Supports 2026 claims tagged 'test2026T1' while maintaining full compatibility
with baseline 15-item compliance audit datasets and test suites.
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
        if not p.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

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
        belop = float(row.get("Belop_NOK", 0))
        kvittering = bool(row.get("Kvittering_Vedlagt", True))
        if belop > 100 and not kvittering:
            violations.append("BRUDD_KVITTERING: Beløp over 100 NOK mangler vedlagt originalkvittering.")
            summary["avvik_kategorier"]["mangler_kvittering"] += 1
            
        # Rule 2: Segregation of duties (BDM != Attestant)
        bdm = str(row.get("BDM_ID", ""))
        attestant = str(row.get("Attestant_ID", ""))
        if bdm == attestant and bdm != "":
            violations.append("BRUDD_FIRE_OYNE: BDM og attestant er samme person (egengodkjenning).")
            summary["avvik_kategorier"]["egengodkjent_bdm"] += 1
            
        # Rule 3: Meal deductions
        dekket = str(row.get("Maltid_Dekket", "Ingen"))
        fradrag = bool(row.get("Fradrag_Utfort", True))
        if dekket.lower() != "ingen" and not fradrag:
            violations.append(f"BRUDD_MALTID: Måltid var dekket ({dekket}), men måltidsfradrag er ikke trukket fra diett.")
            summary["avvik_kategorier"]["mangler_maltidsfradrag"] += 1
            
        # Rule 4: Mileage description
        km = float(row.get("Km_Godtgjorelse", 0))
        rute = bool(row.get("Km_Rute_Beskrevet", True))
        if km > 0 and not rute:
            violations.append("BRUDD_KM_RUTE: Kilometergodtgjørelse krever spesifisert rutebeskrivelse.")
            summary["avvik_kategorier"]["mangler_rutebeskrivelse"] += 1
            
        if violations:
            summary["avvik_claims"] += 1
            summary["belop_med_avvik_nok"] += belop
            findings.append({
                "Reise_ID": row.get("Reise_ID", "UKJENT"),
                "Ansatt": row.get("Ansatt", "UKJENT"),
                "Dato": row.get("Dato", ""),
                "Formaal": row.get("Formaal", ""),
                "Belop_NOK": belop,
                "BDM_ID": bdm,
                "Attestant_ID": attestant,
                "Avvik": violations
            })
        else:
            summary["godkjente_claims"] += 1
            
    return {"summary": summary, "findings": findings}

if __name__ == "__main__":
    res = audit_travel_claims()
    print(json.dumps(res, indent=2, ensure_ascii=False))
