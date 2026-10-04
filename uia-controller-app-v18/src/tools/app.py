"""
Streamlit Web Dashboard for UiA Controlling App (v15)
Interactive financial controlling interface with preskriptiv tiltakssimulator,
EOY balance forecasting, EVM project performance, and travel audit center.
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
from budget_engine import get_annual_wheel_calendar, build_next_year_budget, calculate_tdi_project_budget, get_2026_budget_vs_actuals_ytd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
TRAVEL_CSV_PATH = BASE_DIR / "data" / "staging" / "reiseregninger_15_stk.csv"
DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"

# Streamlit Page Config
st.set_page_config(
    page_title="UiA Financial Controlling & EOY Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏛️ Universitetet i Agder (UiA) - Finansiell Controller Dashboard")
st.caption("Interaktivt verktøy for F-05-20 avsetningskontroll, EVM-prosjektstyring, tiltakssimulering, årshjul og internkontroll (v16)")

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
    "📊 Revidert EOY Balanse & Resultat",
    "📈 EVM Prosjektstyring & Descoping",
    "⚖️ F-05-20 Avsetningskontroll",
    "🔍 Internkontroll & Reiseregninger",
    "📅 Årshjul & Neste Års Budsjett (v16)"
])

# -----------------------------------------------------------------------------
# TAB 1: Revidert EOY Balanse & Resultat
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("1. Hovedindikatorer ved 31.12.2026 (EOY Forecast)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Reell Driftsavsetning EOY",
            value=f"{bal['revised_avsetning_pct']:.2f}%",
            delta=f"{bal['revised_avsetning_pct'] - bal['baseline_avsetning_pct']:.2f}% (Cap: 5.0%)",
            delta_color="normal" if bal['revised_avsetning_pct'] <= 5.0 else "inverse"
        )
    with col2:
        st.metric(
            label="Driftsavsetning EOY (NOK)",
            value=f"{bal['revised_avsetning']:,.0f} NOK",
            delta=f"{-s['investments_activated_nok']:,.0f} NOK omplassert"
        )
    with col3:
        st.metric(
            label="Direkte Kostnadsinnsparing",
            value=f"{s['total_cost_savings']:,.0f} NOK",
            delta=f"EVM + Reise"
        )
    with col4:
        st.metric(
            label="F-05-20 Compliance Status",
            value=bal['f0520_status'],
            delta="Godkjent" if bal['revised_avsetning_pct'] <= 5.0 else "Søknad kreves"
        )

    st.markdown("---")
    st.subheader("2. Balanse- og Resultatsammenligning (Status Quo vs. Revidert Prognose)")
    
    df_bal = pd.DataFrame([
        {
            "Indikator": "Rammebevilgning (Kap. 260, post 50)",
            "Status Quo (Før Tiltak)": f"{bal['rammebevilgning']:,.0f} NOK",
            "Revidert Prognose (Etter Tiltak)": f"{bal['rammebevilgning']:,.0f} NOK",
            "Endring / Effekt": "0 NOK"
        },
        {
            "Indikator": "Akkumulert Driftsavsetning EOY",
            "Status Quo (Før Tiltak)": f"{bal['baseline_avsetning']:,.0f} NOK ({bal['baseline_avsetning_pct']:.2f}%)",
            "Revidert Prognose (Etter Tiltak)": f"{bal['revised_avsetning']:,.0f} NOK ({bal['revised_avsetning_pct']:.2f}%)",
            "Endring / Effekt": f"{-s['investments_activated_nok']:,.0f} NOK"
        },
        {
            "Indikator": "Overskridelse mot 5.0% grense",
            "Status Quo (Før Tiltak)": f"{bal['baseline_overskridelse']:,.0f} NOK",
            "Revidert Prognose (Etter Tiltak)": f"{bal['revised_overskridelse']:,.0f} NOK",
            "Endring / Effekt": f"{-bal['baseline_overskridelse'] + bal['revised_overskridelse']:,.0f} NOK"
        },
        {
            "Indikator": "Status Rundskriv F-05-20",
            "Status Quo (Før Tiltak)": "SØKNAD KREVES",
            "Revidert Prognose (Etter Tiltak)": bal['f0520_status'],
            "Endring / Effekt": "COMPLIANT"
        }
    ])
    st.table(df_bal)

    # Visualisering av Avsetning EOY
    st.subheader("3. Avsetningsprosent mot 5,0 %-grensen")
    chart_data = pd.DataFrame({
        "Scenarium": ["Status Quo (6,0%)", "5,0% Lovlig Grense", f"Revidert EOY ({bal['revised_avsetning_pct']:.2f}%)"],
        "Driftsavsetning (NOK)": [bal['baseline_avsetning'], bal['rammebevilgning'] * 0.05, bal['revised_avsetning']]
    })
    st.bar_chart(chart_data.set_index("Scenarium"))

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
# TAB 5: Årshjul & Neste Års Budsjett (v16)
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("1. UiA Økonomisk Årshjul & Frister")
    calendar_df = get_annual_wheel_calendar()
    st.dataframe(calendar_df, use_container_width=True)

    st.subheader("2. Framskriving av Neste Års Budsjett (Kap. 260 post 50)")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        price_inflation = st.number_input("Pris- og Lønnsvekst / Deflator (%)", min_value=0.0, max_value=10.0, value=3.6, step=0.1)
    with col_b2:
        result_adj = st.number_input("Resultatbasert Endring (NOK)", value=12500000, step=1000000)
    with col_b3:
        strat_reserve = st.number_input("Strategisk Avsetning Styret (%)", min_value=0.0, max_value=10.0, value=2.5, step=0.5)

    budget_res = build_next_year_budget(
        price_inflation_pct=price_inflation,
        result_adjustment_nok=float(result_adj),
        strategic_reserve_pct=strat_reserve
    )

    kpi_b1, kpi_b2, kpi_b3 = st.columns(3)
    with kpi_b1:
        st.metric("Ny Brutto Ramme", f"{budget_res['ny_brutto_ramme_nok']:,.0f} NOK", delta=f"{budget_res['pris_og_lonnsjustering_nok']:,.0f} NOK deflator")
    with kpi_b2:
        st.metric("Strategisk Avsetning Styret", f"{budget_res['strategisk_avsetning_styret_nok']:,.0f} NOK")
    with kpi_b3:
        st.metric("Netto Fordelt Fakultetene", f"{budget_res['netto_fordelt_fakultetene_nok']:,.0f} NOK")

    st.markdown("#### Fordeling per Fakultet / Enhet")
    dept_df = pd.DataFrame([
        {"Enhet": dept, "Tildelt Ramme (NOK)": f"{amount:,.0f} NOK", "Beløp": amount}
        for dept, amount in budget_res["fakultetsfordeling"].items()
    ])
    st.dataframe(dept_df[["Enhet", "Tildelt Ramme (NOK)"]], use_container_width=True)

    st.subheader("3. BOA / TDI Totalkostnadskalkulator")
    c_tdi1, c_tdi2, c_tdi3 = st.columns(3)
    with c_tdi1:
        tdi_salary = st.number_input("Direkte Lønn (NOK)", value=1000000, step=100000)
    with c_tdi2:
        tdi_drift = st.number_input("Direkte Driftskostnader (NOK)", value=200000, step=50000)
    with c_tdi3:
        tdi_overhead = st.number_input("TDI Overhead-sats (%)", value=45.0, step=1.0)

    tdi_calc = calculate_tdi_project_budget(direct_salary_nok=float(tdi_salary), direct_operating_nok=float(tdi_drift), overhead_pct=tdi_overhead)
    st.success(f"**Totalkostnad (TDI):** {tdi_calc['totalkostnad_tdi_nok']:,.0f} NOK (Hvorav indirekte overhead: {tdi_calc['indirekte_kostnader_tdi_nok']:,.0f} NOK)")

    st.subheader("4. 2026 Budsjett vs. Faktisk Regnskap YTD August (tag: test2026T1)")
    try:
        ytd_df = get_2026_budget_vs_actuals_ytd(tag="test2026T1")
        st.dataframe(ytd_df[["Avdeling", "Budsjett_2026_FY_NOK", "Budsjett_YTD_Aug_NOK", "Regnskap_YTD_Aug_NOK", "Avvik_YTD_NOK", "Avvik_YTD_Pct", "Prognose_2026_EOY_NOK", "Prognose_Avvik_EOY_NOK"]], use_container_width=True)
    except Exception as e:
        st.info(f"YTD-data for 2026 ikke tilgjengelig: {e}")

