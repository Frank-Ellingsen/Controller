"""
Budget Engine & Annual Wheel Tool for UiA Controlling App (v18)
Provides deterministic calculations for:
1. Annual Wheel (Årshjul) status tracking & milestone checks.
2. Next-Year Budget Building (Framskriving av Kap 260 post 50, pris/lønnsvekst, resultatindikatorer).
3. 2026 Full-Year Budget vs. YTD August Actuals Comparison (supporting dataset tag 'test2026T1').
4. Internal Frame Allocations across UiA departments (Handelshøyskolen, TR, HH, etc.).
5. TDI (Totalkostnadsmodell) overhead calculations for research projects (BOA).
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def get_annual_wheel_calendar() -> pd.DataFrame:
    """Returnerer de lovpålagte styringsmilepælene i det statlige økonomiske årshjulet."""
    calendar_data = [
        {"Måned": "Januar", "Frist/Milepæl": "Tildelingsbrev mottatt fra KD", "Ansvarlig": "Ledelse / Økonomidirektør", "Status": "Fullført"},
        {"Måned": "Februar", "Frist/Milepæl": "Intern budsjettfordeling vedtas i Universitetsstyret", "Ansvarlig": "Budget Specialist", "Status": "Fullført"},
        {"Måned": "Mai", "Frist/Milepæl": "1. Tertialrapport (T1 per 30.04) med EOY-prognose", "Ansvarlig": "Lead Controller", "Status": "Fullført"},
        {"Måned": "Juni", "Frist/Milepæl": "Revidert nasjonalbudsjett (RNB) & innspill til neste års statsbudsjett", "Ansvarlig": "Budget Specialist", "Status": "Fullført"},
        {"Måned": "September", "Frist/Milepæl": "2. Tertialrapport (T2 per 31.08) & F-05-20 tiltaksvurdering", "Ansvarlig": "Lead Controller", "Status": "Aktiv / Pågår"},
        {"Måned": "Oktober", "Frist/Milepæl": "Regjeringens statsbudsjettforslag (Prop. 1 S) fremlegges", "Ansvarlig": "Budget Specialist", "Status": "Planlagt"},
        {"Måned": "Desember", "Frist/Milepæl": "Årsavslutningsinstruks & endelig rammevedtak for neste år", "Ansvarlig": "Økonomidirektør / Styret", "Status": "Planlagt"}
    ]
    return pd.DataFrame(calendar_data)

def get_2026_budget_vs_actuals_ytd(tag: str = "test2026T1", ytd_period: str = "2026-M08") -> pd.DataFrame:
    """
    Sammenligner 2026 Fullstendig Årsbudsjett mot Faktisk Regnskap YTD August (M01-M08).
    Støtter opplasting og filtrering på egendefinert dataset tag (f.eks. test2026T1).
    """
    bud_file = DEFAULT_STAGING_DIR / f"budsjett_2026_hele_aret_{tag}.csv"
    act_file = DEFAULT_STAGING_DIR / f"regnskap_august_2026_{tag}.csv"
    
    if not bud_file.exists() or not act_file.exists():
        conn = sqlite3.connect(str(DEFAULT_DB_PATH))
        try:
            df_bud = pd.read_sql_query("SELECT * FROM budget_2026", conn)
            df_act = pd.read_sql_query("SELECT * FROM ubw_transactions_2026", conn)
        except Exception:
            conn.close()
            raise FileNotFoundError(f"Finner ikke testsett-filer for tag '{tag}' i staging eller SQLite.")
        conn.close()
    else:
        df_bud = pd.read_csv(bud_file)
        df_act = pd.read_csv(act_file)
        
    ytd_months = [f"2026-M{m:02d}" for m in range(1, 9)]
    df_bud_ytd = df_bud[df_bud["Maaned"].isin(ytd_months)]
    
    bud_fy = df_bud.groupby("Avdeling")["Budsjett_Maaned_NOK"].sum().reset_index(name="Budsjett_2026_FY_NOK")
    bud_ytd = df_bud_ytd.groupby("Avdeling")["Budsjett_Maaned_NOK"].sum().reset_index(name="Budsjett_YTD_Aug_NOK")
    act_ytd = df_act.groupby("Avdeling")["Belop_NOK"].sum().reset_index(name="Regnskap_YTD_Aug_NOK")
    
    merged = pd.merge(bud_fy, bud_ytd, on="Avdeling", how="outer").merge(act_ytd, on="Avdeling", how="outer").fillna(0)
    merged["Avvik_YTD_NOK"] = (merged["Regnskap_YTD_Aug_NOK"] - merged["Budsjett_YTD_Aug_NOK"]).round(2)
    merged["Avvik_YTD_Pct"] = ((merged["Avvik_YTD_NOK"] / merged["Budsjett_YTD_Aug_NOK"]) * 100).round(2)
    merged["Prognose_2026_EOY_NOK"] = (merged["Regnskap_YTD_Aug_NOK"] + (merged["Budsjett_2026_FY_NOK"] - merged["Budsjett_YTD_Aug_NOK"])).round(2)
    merged["Prognose_Avvik_EOY_NOK"] = (merged["Prognose_2026_EOY_NOK"] - merged["Budsjett_2026_FY_NOK"]).round(2)
    merged["Tag"] = tag
    
    return merged

def build_next_year_budget(
    current_ramme_nok: float = 2_000_000_000.0,
    price_inflation_pct: float = 3.2,
    result_adjustment_nok: float = 11_076_544.0,
    strategic_reserve_pct: float = 2.5
) -> dict:
    """
    Beregner framskriving av neste års statsbudsjettramme (Kap. 260 post 50).
    """
    prisjustering_nok = current_ramme_nok * (price_inflation_pct / 100.0)
    ny_brutto_ramme_nok = current_ramme_nok + prisjustering_nok + result_adjustment_nok
    strategisk_avsetning_nok = ny_brutto_ramme_nok * (strategic_reserve_pct / 100.0)
    netto_fordelbar_ramme_nok = ny_brutto_ramme_nok - strategisk_avsetning_nok
    
    dept_shares = {
        "Handelshøyskolen": 0.065,
        "Fakultet for helse- og idrettsvitenskap": 0.100,
        "Fakultet for humaniora og pedagogikk": 0.102,
        "Fakultet for kunstfag": 0.050,
        "Fakultet for samfunnsvitenskap": 0.082,
        "Fakultet for teknologi og realfag": 0.142,
        "Fellestjenester & Bibliotek": 0.220,
        "Særkostnader & Fellesutgifter": 0.239
    }
    
    dept_budgets = {dept: round(netto_fordelbar_ramme_nok * share, 0) for dept, share in dept_shares.items()}
    
    return {
        "grunnlag_inneværende_år_nok": current_ramme_nok,
        "pris_og_lonnsjustering_nok": round(prisjustering_nok, 0),
        "resultatbasert_endring_nok": result_adjustment_nok,
        "ny_brutto_ramme_nok": round(ny_brutto_ramme_nok, 0),
        "strategisk_avsetning_styret_nok": round(strategisk_avsetning_nok, 0),
        "netto_fordelt_fakultetene_nok": round(netto_fordelbar_ramme_nok, 0),
        "fakultetsfordeling": dept_budgets
    }

def calculate_tdi_project_budget(
    direct_salary_nok: float,
    direct_operating_nok: float,
    overhead_pct: float = 45.0
) -> dict:
    """Beregner Totalkostnad (TDI) for eksternfinansierte forskningsprosjekter (BOA)."""
    overhead_nok = (direct_salary_nok + direct_operating_nok) * (overhead_pct / 100.0)
    totalkostnad_nok = direct_salary_nok + direct_operating_nok + overhead_nok
    return {
        "direkte_lonn_nok": direct_salary_nok,
        "direkte_drift_nok": direct_operating_nok,
        "indirekte_kostnader_tdi_nok": round(overhead_nok, 0),
        "totalkostnad_tdi_nok": round(totalkostnad_nok, 0),
        "overhead_prosent": overhead_pct
    }

if __name__ == "__main__":
    print("=== UiA ÅRSHJUL & BUDSJETTMOTOR TEST (v18) ===")
    print("\n1. 2026 Budsjett vs Regnskap YTD August (tag: test2026T1):")
    print(get_2026_budget_vs_actuals_ytd("test2026T1").to_string(index=False))
