"""
Budget Engine & Annual Wheel Tool for UiA Controlling App (v19)
Provides deterministic calculations for:
1. Annual Wheel (Årshjul) status tracking & milestone checks (Q1-Q4).
2. Next-Year Budget Building (Framskriving av Kap 260 post 50, pris/lønnsvekst, resultatindikatorer).
3. 2026 Full-Year Budget vs. YTD Actuals Comparison (supporting dataset tags 'test2026T1' and '2026T1sep').
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
        {"Kvartal": "Q1", "Måned": "Januar", "Frist/Milepæl": "Tildelingsbrev mottatt fra KD", "Ansvarlig": "Ledelse / Økonomidirektør", "Status": "Fullført", "Beskrivelse": "Årsavslutning og tildelingsbrev mottatt fra Kunnskapsdepartementet."},
        {"Kvartal": "Q1", "Måned": "Februar", "Frist/Milepæl": "Intern budsjettfordeling vedtas i Universitetsstyret", "Ansvarlig": "Budget Specialist", "Status": "Fullført", "Beskrivelse": "Universitetsstyrets vedtak av internfordelingsmodell for inneværende år."},
        {"Kvartal": "Q2", "Måned": "Mai", "Frist/Milepæl": "1. Tertialrapport (T1 per 30.04) med EOY-prognose", "Ansvarlig": "Lead Controller", "Status": "Fullført", "Beskrivelse": "Rapportering av regnskap og oppdatert EOY-prognose for T1."},
        {"Kvartal": "Q2", "Måned": "Juni", "Frist/Milepæl": "Revidert nasjonalbudsjett (RNB) & innspill til neste års statsbudsjett", "Ansvarlig": "Budget Specialist", "Status": "Fullført", "Beskrivelse": "Justering av rammer etter RNB og innspill til KD om neste års statsbudsjett."},
        {"Kvartal": "Q3", "Måned": "September", "Frist/Milepæl": "2. Tertialrapport (T2 per 31.08) & F-05-20 tiltaksvurdering", "Ansvarlig": "Lead Controller", "Status": "Aktiv / Pågår", "Beskrivelse": "T2-rapportering og kontroll mot 5 %-regelen for driftsavsetninger."},
        {"Kvartal": "Q4", "Måned": "Oktober", "Frist/Milepæl": "Regjeringens statsbudsjettforslag (Prop. 1 S) fremlegges", "Ansvarlig": "Budget Specialist", "Status": "Planlagt", "Beskrivelse": "Ekstraksjon av foreløpig rammebevilgning (Kap 260 post 50) for UiA."},
        {"Kvartal": "Q4", "Måned": "Desember", "Frist/Milepæl": "Årsavslutningsinstruks & endelig rammevedtak for neste år", "Ansvarlig": "Økonomidirektør / Styret", "Status": "Planlagt", "Beskrivelse": "Endelig styrevedtak om rammer og utsending av interne tildelingsbrev."}
    ]
    return pd.DataFrame(calendar_data)

def get_2026_budget_vs_actuals_ytd(tag: str = "test2026T1", ytd_period: str = None) -> pd.DataFrame:
    """
    Sammenligner 2026 Fullstendig Årsbudsjett mot Faktisk Regnskap YTD.
    Støtter både August (test2026T1), September (2026T1sep) og dynamiske tags.
    """
    bud_file = DEFAULT_STAGING_DIR / f"budsjett_2026_hele_aret_{tag}.csv"
    if not bud_file.exists():
        bud_file = DEFAULT_STAGING_DIR / "budsjett_2026_hele_aret_test2026T1.csv"
        
    act_file = None
    if (DEFAULT_STAGING_DIR / f"regnskap_september_2026_{tag}.csv").exists():
        act_file = DEFAULT_STAGING_DIR / f"regnskap_september_2026_{tag}.csv"
    elif (DEFAULT_STAGING_DIR / f"regnskap_august_2026_{tag}.csv").exists():
        act_file = DEFAULT_STAGING_DIR / f"regnskap_august_2026_{tag}.csv"
    else:
        candidates = list(DEFAULT_STAGING_DIR.glob(f"regnskap_*_{tag}.csv"))
        if candidates:
            act_file = candidates[0]
            
    if not bud_file.exists() or act_file is None or not act_file.exists():
        conn = sqlite3.connect(str(DEFAULT_DB_PATH))
        try:
            df_bud = pd.read_sql_query("SELECT * FROM budget_2026", conn)
            df_act = pd.read_sql_query("SELECT * FROM ubw_transactions_2026 WHERE Tag = ?", conn, params=[tag])
            if df_act.empty:
                df_act = pd.read_sql_query("SELECT * FROM ubw_transactions_2026", conn)
        except Exception:
            conn.close()
            raise FileNotFoundError(f"Finner ikke testsett-filer for tag '{tag}' i staging eller SQLite.")
        conn.close()
    else:
        df_bud = pd.read_csv(bud_file)
        df_act = pd.read_csv(act_file)
        
    max_m = 9 if ("sep" in tag.lower() or (ytd_period and "09" in ytd_period)) else 8
    ytd_months = [f"2026-M{m:02d}" for m in range(1, max_m + 1)]
    df_bud_ytd = df_bud[df_bud["Maaned"].isin(ytd_months)]
    
    col_act_map = {c.lower(): c for c in df_act.columns}
    col_act = col_act_map.get("belop_nok", "Belop_NOK")
    col_avd = col_act_map.get("avdeling", "Avdeling")
    
    bud_fy = df_bud.groupby("Avdeling")["Budsjett_Maaned_NOK"].sum().reset_index(name="Budsjett_2026_FY_NOK")
    bud_ytd = df_bud_ytd.groupby("Avdeling")["Budsjett_Maaned_NOK"].sum().reset_index(name="Budsjett_YTD_Aug_NOK")
    act_ytd = df_act.groupby(col_avd)[col_act].sum().reset_index(name="Regnskap_YTD_Aug_NOK")
    act_ytd = act_ytd.rename(columns={col_avd: "Avdeling"})
    
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
    print("=== UiA ÅRSHJUL & BUDSJETTMOTOR TEST (v19) ===")
    print("\n1. 2026 Budsjett vs Regnskap YTD August (tag: test2026T1):")
    print(get_2026_budget_vs_actuals_ytd("test2026T1").to_string(index=False))
    print("\n2. 2026 Budsjett vs Regnskap YTD September (tag: 2026T1sep):")
    print(get_2026_budget_vs_actuals_ytd("2026T1sep").to_string(index=False))
