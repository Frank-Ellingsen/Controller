"""
Budget Engine & Annual Wheel Tool for UiA Controlling App (v18)
Provides deterministic calculations for:
1. Annual Wheel (Årshjul) status tracking & milestone checks.
2. Next-Year Budget Building (Framskriving av Kap 260 post 50, pris/lønnsvekst, resultatindikatorer).
3. 2026 Full-Year Budget vs. YTD August Actuals Comparison (supporting dataset tag 'test2026T1').
4. TDI (Totalkostnadsmodell) overhead calculations for research projects (BOA).
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import pandas as pd
import sqlite3
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"

def get_annual_wheel_calendar() -> pd.DataFrame:
    """Returnerer UiAs offisielle økonomiske årshjul med frister og oppgaver."""
    calendar_data = [
        {"Kvartal": "Q1", "Måned": "Januar", "Frist/Milepæl": "Månedsavslutning M12", "Ansvarlig": "Ledger Analyst", "Status": "COMPLETED", "Beskrivelse": "Avstemming av hovedbok og årsavslutning."},
        {"Kvartal": "Q1", "Måned": "Mars", "Frist/Milepæl": "15. mars: Årsrapport til KD", "Ansvarlig": "Lead Controller", "Status": "COMPLETED", "Beskrivelse": "Styregodkjent årsrapport og årsregnskap oversendes Kunnskapsdepartementet."},
        {"Kvartal": "Q2", "Måned": "Mai/Juni", "Frist/Milepæl": "1. Tertialrapport & RNB", "Ansvarlig": "Lead Controller", "Status": "COMPLETED", "Beskrivelse": "Behandling av 1. tertialregnskap og eventuelle rammejusteringer etter Revidert nasjonalbudsjett."},
        {"Kvartal": "Q3", "Måned": "September", "Frist/Milepæl": "2. Tertialrapport & Budsjettmodell", "Ansvarlig": "Budget Specialist", "Status": "IN_PROGRESS", "Beskrivelse": "Gjennomgang av internasjonal/nasjonal resultatutvikling og revisjon av intern fordelingsmodell."},
        {"Kvartal": "Q4", "Måned": "Oktober", "Frist/Milepæl": "Statsbudsjettet (Prop 1 S)", "Ansvarlig": "Budget Specialist", "Status": "PENDING", "Beskrivelse": "Ekstraksjon av foreløpig rammebevilgning (Kap 260 post 50) for UiA."},
        {"Kvartal": "Q4", "Måned": "November", "Frist/Milepæl": "Endelig Intern Budsjettfordeling", "Ansvarlig": "Lead Controller", "Status": "PENDING", "Beskrivelse": "Universitetsstyrets vedtak av neste års budsjettrammer per fakultet."},
        {"Kvartal": "Q4", "Måned": "Desember", "Frist/Milepæl": "Internt Tildelingsbrev", "Ansvarlig": "Universitetsdirektør", "Status": "PENDING", "Beskrivelse": "Utsending av interne tildelingsbrev og opprettelse av nye budsjettrammer i Unit4/UBW."}
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
        # Fallback to SQLite database tables
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
    current_ramme_nok: float = 1990904000.0,
    price_inflation_pct: float = 3.6,
    result_adjustment_nok: float = 12500000.0,
    strategic_reserve_pct: float = 2.5
) -> dict:
    """
    Beregner neste års budsjettramme for UiA basert på lønns/prisvekst,
    resultatbasert uttelling og strategiske avsetninger.
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
