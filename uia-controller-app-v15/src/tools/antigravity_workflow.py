"""
Consolidated Antigravity Workflow Runner (v15)
Executes full month-end close:
1. UBW & Travel Expense Audit
2. F-05-20 Budget Variance Analysis
3. Database-driven EVM Performance Review
4. DuckDB Time-Series Snapshotting & Multi-Model EAC Forecasts
5. Preskriptiv Tiltaksplan & Revidert Årsprognose (EOY Balance Forecast)
6. Power BI Star Schema Parquet Export
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import json
from ubw_reader import read_ubw_data, henter_transaksjonsflagg
from evm_calculator import calculate_evm_from_db, generate_evm_report
from variance_calculator import sjekk_f0520_avsetning
from audit_travel_expenses import audit_travel_claims
from duckdb_analytics import snapshot_evm_data, query_eac_forecasting_models
from powerbi_exporter import export_powerbi_data_model
from action_engine import simulate_action_plan, format_action_plan_report

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_TRAVEL_CSV_PATH = BASE_DIR / "data" / "staging" / "reiseregninger_15_stk.csv"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_PARQUET_DIR = BASE_DIR / "data" / "staging" / "parquet"

def execute_monthly_close_v15(
    db_path: str = None, 
    travel_csv_path: str = None, 
    duckdb_path: str = None, 
    parquet_dir: str = None,
    descoping_pct: float = 20.0,
    investments_activated_nok: float = 12000000.0
):
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    if travel_csv_path is None:
        travel_csv_path = str(DEFAULT_TRAVEL_CSV_PATH)
    if duckdb_path is None:
        duckdb_path = str(DEFAULT_DUCKDB_PATH)
    if parquet_dir is None:
        parquet_dir = str(DEFAULT_PARQUET_DIR)

    print("=== START: UiA Antigravity Consolidated Monthly Close (v15) ===")
    
    # Step 1: UBW Transactions & Travel Expense Audit
    print("\n[1/6] Auditoria: Skanner UBW og reiseregninger for avvik...")
    if Path(db_path).exists():
        df_ubw = read_ubw_data(db_path)
        df_flagg = henter_transaksjonsflagg(df_ubw)
        avvik = df_flagg[df_flagg['Kontrollflagg'] != "OK"]
        print(f"      -> UBW SQLite: {len(avvik)} transaksjoner flagget for avvik.")
        
    if Path(travel_csv_path).exists():
        travel_res = audit_travel_claims(travel_csv_path)
        summary = travel_res["summary"]
        print(f"      -> Reiseregninger: {summary['avvik_claims']} av {summary['totalt_behandlet']} krav har avvik (Beløp: {summary['belop_med_avvik_nok']:,.0f} NOK).")

    # Step 2: F-05-20 Avsetningskontroll
    print("\n[2/6] Analyst: Beregner F-05-20 Driftsavsetningsstatus...")
    f0520_res = sjekk_f0520_avsetning(rammebevilgning=1200000000.0, akkumulert_avsetning=72000000.0)
    print(f"      -> Reell avsetning: {f0520_res['reell_prosent']}% (Grense: 5.0%)")
    print(f"      -> Overskridelse: {f0520_res['overskridelse_nok']:,.0f} NOK (Søknad Kunnskapsdepartementet kreves: {f0520_res['krever_soknad_kd']})")

    # Step 3: EVM Project Control from Database
    print("\n[3/6] Lead Controller: Kjører databaseintegrert EVM-prosjektanalyse...")
    evm_report = generate_evm_report(db_path)
    print(evm_report)

    # Step 4: DuckDB Time-Series Snapshot & Advanced EAC Forecasts
    print("\n[4/6] DuckDB Engine: Lagrer tidsrekke-snapshot og beregner fler-modell EAC-prognoser...")
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
    print("\n[5/6] Action Engine: Genererer tiltaksplan, kvantifiserer effekter og beregner revidert EOY Balanse...")
    action_sim = simulate_action_plan(
        descoping_pct=descoping_pct,
        investments_activated_nok=investments_activated_nok,
        travel_enforcement_pct=100.0,
        kd_application=True
    )
    print("\n" + format_action_plan_report(action_sim))

    # Step 6: Power BI Star Schema Parquet Export
    print("\n[6/6] Power BI Integration: Eksporterer Star Schema til Parquet og CSV...")
    export_powerbi_data_model(db_path=db_path, duckdb_path=duckdb_path, travel_csv_path=travel_csv_path, output_dir=parquet_dir)
    
    print("\n=== SLUTT: Konsolidert Månedsoppgjør Fullført (v15) ===")

def execute_monthly_close_v14(db_path: str = None, travel_csv_path: str = None, duckdb_path: str = None):
    """Backwards compatibility wrapper."""
    execute_monthly_close_v15(db_path=db_path, travel_csv_path=travel_csv_path, duckdb_path=duckdb_path)

def execute_monthly_close_v8(db_path: str = None, travel_csv_path: str = None, duckdb_path: str = None):
    """Backwards compatibility wrapper."""
    execute_monthly_close_v15(db_path=db_path, travel_csv_path=travel_csv_path, duckdb_path=duckdb_path)

if __name__ == "__main__":
    execute_monthly_close_v15()
