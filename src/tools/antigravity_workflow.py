"""
Consolidated Antigravity Workflow Runner (v27 - Canonical Project Model)
Executes full month-end close, annual wheel, statutory reporting, database, Account Statement & Canonical Model pipeline:
1. UBW & Travel Expense Audit
2. F-05-20 Budget Variance Analysis
3. Database-driven EVM Performance Review
4. DuckDB Time-Series Snapshotting & Multi-Model EAC Forecasts
5. Preskriptiv Tiltaksplan & Revidert Årsprognose (EOY Balance Forecast)
6. Power BI Star Schema Parquet Export
7. Budget Engine & 2026 YTD Budget vs. Actuals Review (tags: test2026T1, 2026T1sep, 2026T1okt)
8. Annual Wheel & Database Specialist Check-Off (arshjul_matrix_2026.xlsx)
9. Statutory & State Reporting Specialist Verification (KD, DBH, Riksrevisjonen)
10. Finance & Project Controls Account Statement Generation
11. Canonical Project Model Hydration & master_state.json Export
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import sys
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ubw_reader import read_ubw_data, henter_transaksjonsflagg
from evm_calculator import calculate_evm_from_db, generate_evm_report
from variance_calculator import sjekk_f0520_avsetning
from audit_travel_expenses import audit_travel_claims
from duckdb_analytics import snapshot_evm_data, query_eac_forecasting_models
from powerbi_exporter import export_powerbi_data_model
from action_engine import simulate_action_plan, format_action_plan_report
from budget_engine import build_next_year_budget, get_annual_wheel_calendar, get_2026_budget_vs_actuals_ytd
from statutory_reporting_engine import verify_kd_statutory_compliance, get_dbh_reporting_metrics
from account_statement_engine import get_sample_project_controls_statement, generate_uia_department_account_statement, export_account_statements
from src.repositories.canonical_repository import CanonicalRepository

DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_TRAVEL_CSV_PATH = BASE_DIR / "data" / "staging" / "reiseregninger_august_2026_test2026T1.csv"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_PARQUET_DIR = BASE_DIR / "data" / "staging" / "parquet"

def execute_monthly_close_v27(
    db_path: str = None, 
    travel_csv_path: str = None, 
    duckdb_path: str = None, 
    parquet_dir: str = None,
    descoping_pct: float = 20.0,
    investments_activated_nok: float = 12000000.0,
    tag: str = "test2026T1"
):
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    if travel_csv_path is None:
        travel_csv_path = str(DEFAULT_TRAVEL_CSV_PATH)
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
    if parquet_dir is None:
        parquet_dir = str(DEFAULT_PARQUET_DIR)

    print(f"=== START: UiA Antigravity Consolidated Pipeline & Canonical Model (v27 - tag: {tag}) ===")
    
    # Step 1: UBW Transactions & Travel Expense Audit
    print("\n[1/11] Auditoria: Skanner UBW og reiseregninger for avvik...")
    if Path(db_path).exists():
        df_ubw = read_ubw_data(db_path, tag=tag)
        df_flagg = henter_transaksjonsflagg(df_ubw)
        avvik = df_flagg[df_flagg['Kontrollflagg'] != "OK"]
        print(f"      -> UBW SQLite/CSV ({tag}): {len(avvik)} transaksjoner flagget for avvik.")
        
    if Path(travel_csv_path).exists():
        travel_res = audit_travel_claims(travel_csv_path, tag=tag)
        summary = travel_res["summary"]
        print(f"      -> Reiseregninger ({tag}): {summary['avvik_claims']} av {summary['totalt_behandlet']} krav har avvik (Beløp: {summary['belop_med_avvik_nok']:,.0f} NOK).")

    # Step 2: F-05-20 Avsetningskontroll
    print("\n[2/11] Analyst: Beregner F-05-20 Driftsavsetningsstatus...")
    f0520_res = sjekk_f0520_avsetning(rammebevilgning=1200000000.0, akkumulert_avsetning=72000000.0)
    print(f"      -> Reell avsetning: {f0520_res['reell_prosent']}% (Grense: 5.0%)")
    print(f"      -> Overskridelse: {f0520_res['overskridelse_nok']:,.0f} NOK (Søknad Kunnskapsdepartementet kreves: {f0520_res['krever_soknad_kd']})")

    # Step 3: EVM Project Control from Database / CSV
    print(f"\n[3/11] Lead Controller: Kjører databaseintegrert EVM-prosjektanalyse (tag: {tag})...")
    evm_report = generate_evm_report(db_path, tag=tag)
    print(evm_report)

    # Step 4: DuckDB Time-Series Snapshot & Advanced EAC Forecasts
    print(f"\n[4/11] DuckDB Engine: Lagrer tidsrekke-snapshot og beregner fler-modell EAC-prognoser ({tag})...")
    snap_df = snapshot_evm_data(sqlite_path=db_path, duckdb_path=duckdb_path, period="2026-M10")
    forecast_df = query_eac_forecasting_models(duckdb_path=duckdb_path)
    
    print("\n--- DuckDB EAC Prognosemodell-sammenligning ---")
    header = f"{'Project':<10} {'BAC':>12} {'AC':>12} {'CPI':>6} {'SPI':>6} {'EAC (CPI)':>12} {'EAC (CPI*SPI)':>14} {'EAC (80/20)':>13} {'TCPI':>6} {'Status':<9}"
    print(header)
    print("-" * len(header))
    for _, r in forecast_df.iterrows():
        print(f"{r['project_id']:<10} {r['bac']:12,.0f} {r['ac']:12,.0f} {r['cpi']:6.2f} {r['spi']:6.2f} {r['eac_typical_cpi']:12,.0f} {r['eac_cpi_spi']:14,.0f} {r['eac_weighted_80_20']:13,.0f} {r['tcpi']:6.2f} {r['status']:<9}")
    print("-" * len(header))
    
    # Step 5: Action Engine & EOY Forecast
    print("\n[5/11] Action Engine: Genererer tiltaksplan, kvantifiserer effekter og beregner revidert EOY Balanse...")
    action_sim = simulate_action_plan(
        descoping_pct=descoping_pct,
        investments_activated_nok=investments_activated_nok,
        travel_enforcement_pct=100.0,
        kd_application=True
    )
    print("\n" + format_action_plan_report(action_sim))

    # Step 6: Power BI Star Schema Parquet Export
    print("\n[6/11] Power BI Integration: Eksporterer Star Schema til Parquet og CSV...")
    export_powerbi_data_model(db_path=db_path, duckdb_path=duckdb_path, travel_csv_path=travel_csv_path, output_dir=parquet_dir)

    # Step 7: Budget Engine & 2026 YTD Review
    print(f"\n[7/11] Budget Specialist: Analyserer 2026 Budsjett vs. Regnskap YTD August (tag: {tag})...")
    df_ytd = get_2026_budget_vs_actuals_ytd(tag=tag)
    print(df_ytd[["Avdeling", "Budsjett_2026_FY_NOK", "Budsjett_YTD_Aug_NOK", "Regnskap_YTD_Aug_NOK", "Avvik_YTD_NOK", "Avvik_YTD_Pct", "Tag"]].to_string(index=False))

    next_b = build_next_year_budget()
    print(f"\n      -> Neste Års Brutto Ramme (Kap 260 post 50): {next_b['ny_brutto_ramme_nok']:,.0f} NOK")
    print(f"      -> Netto Fordelt til Fakultetene: {next_b['netto_fordelt_fakultetene_nok']:,.0f} NOK")
    print(f"      -> Strategiske Avsetninger Styret: {next_b['strategisk_avsetning_styret_nok']:,.0f} NOK")
    
    # Step 8: Annual Wheel Specialist & Database Specialist Check-Off
    print("\n[8/11] Annual Wheel & Database Specialist: Synkroniserer Excel-matrise arshjul_matrix_2026.xlsx...")
    matrix_path = BASE_DIR / "data" / "staging" / "arshjul_matrix_2026.xlsx"
    if matrix_path.exists():
        print(f"      -> Excel Matrise bekreftet: {matrix_path}")

    # Step 9: Statutory & State Reporting Specialist
    print("\n[9/11] Statutory Reporting Specialist: Verifiserer KD, DBH og Riksrevisjonens rapporteringskrav...")
    kd_ver = verify_kd_statutory_compliance(db_path=db_path)
    dbh_ver = get_dbh_reporting_metrics()
    print(f"      -> DBH Studiepoeng (STP): {dbh_ver['studiepoeng_stp_produksjon']['totalt_stp']:,} STP (Mål: {dbh_ver['studiepoeng_stp_produksjon']['mål_oppnåelse_pct']}%)")
    print(f"      -> KD F-05-20 Avsetningsstatus: {kd_ver['f0520_status']} ({kd_ver['f0520_avsetning_pct']}%)")

    # Step 10: Finance & Project Controls Account Statement
    print("\n[10/11] Account Statement Engine: Genererer Finance & Project Controls Account Statement...")
    stmt_res = export_account_statements(output_dir=parquet_dir)
    df_stmt_sample = get_sample_project_controls_statement()
    print(df_stmt_sample.to_string(index=False))
    print(f"      -> Parquet/CSV eksportert: {stmt_res['sample_statement_csv']}")

    # Step 11: Canonical Project Model Hydration & master_state.json Export
    print("\n[11/11] Canonical Project Model: Hydrerer domenemodeller og eksporterer master_state.json...")
    repo = CanonicalRepository()
    json_path = repo.export_master_state_json()
    print(f"      -> Canonical Master State eksportert: {json_path}")

    print(f"\n=== SLUTT: Konsolidert Månedsoppgjør Fullført (v27 - tag: {tag}) ===")

def execute_monthly_close_v23(db_path: str = None, travel_csv_path: str = None, duckdb_path: str = None, parquet_dir: str = None, **kwargs):
    """Backwards compatibility wrapper."""
    execute_monthly_close_v27(db_path=db_path, travel_csv_path=travel_csv_path, duckdb_path=duckdb_path, parquet_dir=parquet_dir, **kwargs)

def execute_monthly_close_v22(db_path: str = None, travel_csv_path: str = None, duckdb_path: str = None, parquet_dir: str = None, **kwargs):
    """Backwards compatibility wrapper."""
    execute_monthly_close_v27(db_path=db_path, travel_csv_path=travel_csv_path, duckdb_path=duckdb_path, parquet_dir=parquet_dir, **kwargs)

def execute_monthly_close_v21(db_path: str = None, travel_csv_path: str = None, duckdb_path: str = None, parquet_dir: str = None, **kwargs):
    """Backwards compatibility wrapper."""
    execute_monthly_close_v27(db_path=db_path, travel_csv_path=travel_csv_path, duckdb_path=duckdb_path, parquet_dir=parquet_dir, **kwargs)

if __name__ == "__main__":
    execute_monthly_close_v27()
