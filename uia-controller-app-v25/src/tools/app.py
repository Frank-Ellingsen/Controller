"""
Streamlit Web Dashboard for UiA Controlling App (v25)
Interactive financial controlling interface with Account Statement reporting,
faculty drill-down explorer (YTD totals, YTD variances, EOY forecasts),
preskriptiv tiltakssimulator, EVM project performance, and travel audit center.
Run via: uv run streamlit run src/tools/app.py
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import sqlite3
import duckdb
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).resolve().parent))
from action_engine import simulate_action_plan, calculate_baseline_status
from ubw_reader import read_ubw_data, henter_transaksjonsflagg
from audit_travel_expenses import audit_travel_claims
from account_statement_engine import (
    get_sample_project_controls_statement,
    get_uia_full_faculty_account_statement,
    get_uia_category_drilldown_statement
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
TRAVEL_CSV_PATH = BASE_DIR / "data" / "staging" / "reiseregninger_august_2026_test2026T1.csv"
DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"

# Streamlit Page Config
st.set_page_config(
    page_title="UiA Financial Controlling & Account Statement Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏛️ Universitetet i Agder (UiA) - Finansiell Controller Dashboard")
st.caption("Interaktivt verktøy for Account Statement rapportering, fakultets-drilldown, F-05-20 avsetningskontroll og EOY prognoser (v25)")

# Sidebar - Interaktiv Tiltakssimulator
st.sidebar.header("⚙️ Preskriptiv Tiltakssimulator")
st.sidebar.markdown("Juster tiltaksparametrene for å simulere finansiell effektreduksjon og revidert EOY-balanse ved 31.12.2026:")

descoping_pct = st.sidebar.slider(
    "Descoping / Kostnadskutt i ETC på Kritiske Prosjekter (%)",
    min_value=0.0,
    max_value=50.0,
    value=20.0,
    step=2.5,
    help="Prosentvis reduksjon i gjenstående estimerte kostnader (ETC) for UM-ENG-03 og UM-FPV-01."
)

investments_activated_nok = st.sidebar.slider(
    "Aktiverte Utstyrs- & Infrastrukturinvesteringer før 31.12 (NOK)",
    min_value=0,
    max_value=20000000,
    value=12000000,
    step=1000000,
    help="Omplassering av ubrukte driftsmidler til styregodkjente varige utstyrsinvesteringer."
)

travel_enforcement_pct = st.sidebar.slider(
    "Stans og Retur av Feilførte Reiseregninger (%)",
    min_value=0,
    max_value=100,
    value=100,
    step=10,
    help="Prosentvis gjennomføring av stans på urettmessige reisekrav (diett/bilagsmangler)."
)

kd_application = st.sidebar.checkbox(
    "Send uoppfordret søknad til KD om avsetningsdispensasjon",
    value=True,
    help="Utarbeider formell dispensasjonssøknad til Kunnskapsdepartementet for strategiske avsetninger."
)

# Run Simulation
sim = simulate_action_plan(
    descoping_pct=descoping_pct,
    investments_activated_nok=float(investments_activated_nok),
    travel_enforcement_pct=float(travel_enforcement_pct),
    kd_application=kd_application
)

b = sim["baseline"]
s = sim["savings"]
bal = sim["revised_eoy_balance"]
p_rev = sim["revised_projects"]

# Main Dashboard Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Account Statement & Fakultets-Drilldown",
    "📈 EVM Prosjektstyring & Descoping",
    "⚖️ F-05-20 Avsetningskontroll",
    "🔍 Internkontroll & Reiseregninger",
    "📁 Dataopplasting & Ingestion"
])

# -----------------------------------------------------------------------------
# TAB 1: Account Statement & Fakultets-Drilldown
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("1. Finance & Project Controls Account Statement")
    st.caption("Intuitiv kontostilling for hele UiA og alle fakulteter for 2026 (faktiske tall til og med oktober M10)")

    # 1. Level 1 & Level 2 Table
    df_full_fac = get_uia_full_faculty_account_statement()
    st.dataframe(df_full_fac, use_container_width=True)

    # Visualization of Faculty YTD & EOY Forecast
    st.markdown("---")
    st.subheader("2. Visualisering av Totalt YTD, Avvik YTD og Prognose EOY per Fakultet")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("##### Budsjett YTD Oct vs. Regnskap YTD Oct (MNOK)")
        df_chart_ytd = df_full_fac[df_full_fac["Enhet_Kode"] != "TOTAL"].set_index("Account / Enhet")[["Budget YTD Oct (MNOK)", "Actual YTD Oct (MNOK)"]]
        st.bar_chart(df_chart_ytd)
    
    with col_v2:
        st.markdown("##### Total Budget 2026 vs. Forecast EOY 2026 (MNOK)")
        df_chart_eoy = df_full_fac[df_full_fac["Enhet_Kode"] != "TOTAL"].set_index("Account / Enhet")[["Total Budget 2026 (MNOK)", "Forecast EOY (MNOK)"]]
        st.bar_chart(df_chart_eoy)

    # 2. Level 3 Category Drill-Down
    st.markdown("---")
    st.subheader("3. Interactive Faculty & Account Category Drill-Down")
    
    selected_unit = st.selectbox(
        "Velg Fakultet / Enhet for detaljert drill-down:",
        options=["ALL (Totalt UiA)"] + [f"{u['code']} - {u['name']}" for u in [
            {"code": "HH", "name": "Handelshøyskolen (HH)"},
            {"code": "HELS", "name": "Fakultet for helse- og idrettsvitenskap (HELS)"},
            {"code": "HUM", "name": "Fakultet for humaniora og pedagogikk (HUM)"},
            {"code": "KUNST", "name": "Fakultet for kunstfag (KUNST)"},
            {"code": "SAMF", "name": "Fakultet for samfunnsvitenskap (SAMF)"},
            {"code": "TN", "name": "Fakultet for teknologi og realfag (TN)"},
            {"code": "ADM", "name": "Fellesadministrasjon & Fellestjenester (ADM)"},
            {"code": "FELLES", "name": "Særkostnader & Fellesutgifter (FELLES)"}
        ]]
    )
    
    unit_code_selected = "ALL" if "ALL" in selected_unit else selected_unit.split(" - ")[0]
    df_cat_drill = get_uia_category_drilldown_statement(unit_code_selected)
    
    st.dataframe(df_cat_drill, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: EVM Prosjektstyring & Descoping Simulator
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("1. Portefølje-oversikt & Descoping-effekt")
    
    rows_evm = []
    for p_id, info in p_rev.items():
        rows_evm.append({
            "Prosjekt ID": p_id,
            "BAC (Budsjett)": f"{info['bac']:,.0f} NOK",
            "AC (Påløpt)": f"{info['ac']:,.0f} NOK",
            "CPI": f"{info['cpi']:.2f}",
            "Baseline EAC": f"{info['baseline_eac']:,.0f} NOK",
            "Revidert EAC": f"{info['revised_eac']:,.0f} NOK",
            "Baseline VAC": f"{info['baseline_vac']:,.0f} NOK",
            "Revidert VAC": f"{info['revised_vac']:,.0f} NOK",
            "Innsparing": f"{info['savings']:,.0f} NOK",
            "Status": info["status"]
        })
    st.dataframe(pd.DataFrame(rows_evm))

    st.subheader("2. Sammenligning av Status Quo EAC vs. Revidert EAC")
    evm_chart_df = pd.DataFrame([
        {"Prosjekt": p_id, "Status Quo EAC": info['baseline_eac'], "Revidert EAC": info['revised_eac']}
        for p_id, info in p_rev.items()
    ]).set_index("Prosjekt")
    st.bar_chart(evm_chart_df)

# -----------------------------------------------------------------------------
# TAB 3: F-05-20 Avsetningskontroll
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Rundskriv F-05-20: Reglement for Ubrukte Budsjettmidler")
    st.markdown("""
    * **Hovedregel:** Akkumulerte ubrukte driftsmidler ved utgangen av regnskapsåret skal ikke overskride **5,0 %** av årets statlige rammebevilgning (Kap. 260, post 50).
    * **Konsekvens ved overskridelse:** Midler utover 5,0 % kan inndras til statskassen dersom skriftlig, begrunnet søknad ikke innvilges av Kunnskapsdepartementet.
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Rammebevilgning:** {bal['rammebevilgning']:,.0f} NOK")
        st.info(f"**Maksimal Lovlig Avsetning (5.0%):** {bal['rammebevilgning']*0.05:,.0f} NOK")
    with c2:
        st.warning(f"**Opprinnelig Avsetning (Status Quo):** {bal['baseline_avsetning']:,.0f} NOK (6.00%)")
        st.success(f"**Revidert Avsetning EOY (Etter Tiltak):** {bal['revised_avsetning']:,.0f} NOK ({bal['revised_avsetning_pct']:.2f}%)")

# -----------------------------------------------------------------------------
# TAB 4: Internkontroll & Reiseregninger
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Internkontroll av Reiseregninger (DFØ / UiA Fullmakter)")
    if TRAVEL_CSV_PATH.exists():
        audit_res = audit_travel_claims(str(TRAVEL_CSV_PATH))
        sum_t = audit_res["summary"]
        
        st.write(f"**Totalt Behandlet:** {sum_t['totalt_behandlet']} krav | **Flaggade Krav:** {sum_t['avvik_claims']} | **Berørt Beløp:** {sum_t['belop_med_avvik_nok']:,.0f} NOK")
        
        if audit_res["findings"]:
            findings_df = pd.DataFrame([
                {
                    "Reise ID": f["Reise_ID"],
                    "Ansatt": f["Ansatt"],
                    "Formål": f["Formaal"],
                    "Beløp (NOK)": f"{f['Belop_NOK']:,.0f}",
                    "BDM ID": f["BDM_ID"],
                    "Attestant ID": f["Attestant_ID"],
                    "Avvikstype": "; ".join(f["Avvik"])
                }
                for f in audit_res["findings"]
            ])
            st.dataframe(findings_df)
    else:
        st.info("Ingen reiseregningsfil funnet i staging.")

# -----------------------------------------------------------------------------
# TAB 5: Dataopplasting & Ingestion
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("📁 Last opp nye datafiler til databasen")
    st.markdown("Last opp nye `.csv` eller `.xlsx` filer med regnskap, reiseregninger eller prosjektdata for å utvide datagrunnlaget.")
    
    uploaded_file = st.file_uploader("Velg datafil (.csv eller .xlsx)", type=["csv", "xlsx"])
    file_tag = st.text_input("Angi tag for opplastede data:", value="2026_UiA_Full_Oct")
    
    if uploaded_file is not None and st.button("🚀 Ingest Data til Database"):
        save_path = BASE_DIR / "data" / "staging" / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        from data_ingestion import ingest_data_file
        res = ingest_data_file(str(save_path), tag=file_tag)
        st.success(f"Fil {uploaded_file.name} ble vellykket lastet inn! Rader: {res.get('rows_ingested')}, Tag: {file_tag}")
