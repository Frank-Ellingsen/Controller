# Veiledning for Streamlit Webgrensesnitt (`streamlit_guide.md`)

Denne veiledningen beskriver hvordan du setter opp, kjører og tilpasser det interaktive webgrensesnittet for **UiA Controller App** med **Streamlit**.

---

## 1. Installasjon og Kjøring

### Forutsetninger
Streamlit er inkludert i prosjektets `requirements.txt` / `pyproject.toml`.

```bash
# Med uv (anbefalt)
uv add streamlit
uv run streamlit run src/tools/app.py

# Med standard virtualenv
pip install streamlit
streamlit run src/tools/app.py
```

---

## 2. Struktur for Streamlit-Applikasjonen (`src/tools/app.py`)

Legg inn følgende kodedokumentasjon i `src/tools/app.py` for å koble webgrensesnittet direkte mot prosjektets SQLite- og DuckDB-databaser:

```python
import streamlit as st
import pandas as pd
import sqlite3
import duckdb
from pathlib import Path

# Sideoppsett
st.set_page_config(
    page_title="UiA Controller Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
TRAVEL_CSV = BASE_DIR / "data" / "staging" / "reiseregninger_15_stk.csv"

st.title("📊 UiA Controlling & EVM Dashboard")
st.caption("Handelshøyskolen UiA — Månedsoppgjør og prosjektstyring")

# Tab-navigasjon
tab1, tab2, tab3 = st.tabs(["🚀 EVM Prosjektkontroll", "🏛️ F-05-20 Driftsavsetning", "🔍 Reiseregningsrevisjon"])

# --- TAB 1: EVM PROSJEKTKONTROLL ---
with tab1:
    st.header("Earned Value Management (EVM) Portefølje")
    if DUCKDB_PATH.exists():
        con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
        df_evm = con.execute("SELECT * FROM evm_snapshots").fetchdf()
        con.close()
        
        # Slicer
        selected_period = st.selectbox("Velg rapporteringsperiode:", df_evm["reporting_period"].unique())
        df_filtered = df_evm[df_evm["reporting_period"] == selected_period]
        
        # KPIer
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Totalt BAC", f"{df_filtered['bac'].sum():,.0f} NOK")
        col2.metric("Totalt AC", f"{df_filtered['ac'].sum():,.0f} NOK")
        col3.metric("Gjennomsnittlig CPI", f"{df_filtered['cpi'].mean():.2f}")
        col4.metric("Kritiske Prosjekter", len(df_filtered[df_filtered["status"] == "CRITICAL"]))
        
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning("Finner ikke analytics_snapshots.duckdb. Kjør antigravity_workflow.py først.")

# --- TAB 2: F-05-20 DRIFTSAVSETNING ---
with tab2:
    st.header("Kunnskapsdepartementets Avsetningsregelverk (F-05-20)")
    ramme = 1200000000.0
    avsetning = 72000000.0
    grense = ramme * 0.05
    reell_pct = (avsetning / ramme) * 100
    
    st.metric("Akkumulert Driftsavsetning", f"{avsetning:,.0f} NOK", delta=f"{reell_pct:.1f}% (Maks 5.0%)", delta_color="inverse")
    if avsetning > grense:
        st.error(f"⚠️ Driftsavsetningen overskrider 5 %-grensen med {(avsetning - grense):,.0f} NOK. Uoppfordret søknad til KD er påkrevd.")

# --- TAB 3: REISEREGNINGSREVISJON ---
with tab3:
    st.header("Internkontroll av Reiseregninger")
    if TRAVEL_CSV.exists():
        df_travel = pd.read_csv(TRAVEL_CSV)
        st.dataframe(df_travel, use_container_width=True)
    else:
        st.warning("Finner ikke reiseregninger_15_stk.csv.")
```

---

## 3. Funksjonalitet og Visualiseringer

1. **Realtidsfiltrering:** Dynamiske velgere for rapporteringsperioder (`2026-M10`), avdelinger og prosjektstatuser.
2. **Interaktive Tabeller:** Innebygd sortering, søk og Parquet/CSV-nedlasting for vilkårlig uttrekk.
3. **Varslinger:** Visuelle `st.error()` og `st.warning()` indikatorer når F-05-20 grenser overskrides eller prosjekter når status `CRITICAL`.
