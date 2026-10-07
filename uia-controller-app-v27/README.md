# UiA Controller App (v22 - Canonical Production Release)

An agentic financial controlling & statutory compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with statutory state reporting (KD, DBH/HK-dir, Riksrevisjonen), capital project controlling (DuckDB, EVM, composite EAC modeling), preskriptiv action planning (EOY balance forecasting), interactive Streamlit web dashboarding, and a complete Single Page Web Application (`index.html`) featuring Excel exports for Statens Kontoplan 2026, Financial Glossary, and Annual Wheel Check-Off Matrix.

## Key Features in v22:

1. **Statutory & State Reporting Specialist (`statutory_reporting_engine.py`)**:
   - **Kunnskapsdepartementet (KD):** Årsrapport & Årsregnskap (SRS), F-05-20 reserve compliance (5,0 % cap), Utviklingsavtale monitoring.
   - **DBH / HK-dir:** Automatic generation of Student Credits (STP), Graduating Candidates, PhD completions, NVI Research Publication Points, and Staff Competence Ratios.
   - **Riksrevisjonen:** Bevilgningsreglement, BDM Fire-øyne-kontroll (`BDM_ID != Attestant_ID`), and R-102 Chart of Accounts audit.
   - **Skatteetaten:** MVA-kompensasjon and BOA/TDI research accounting reconciliation.

2. **Integrated Web Portal (`index.html`)**:
   - Single Page Application with 6 tabs:
     - 📅 **Årshjul & Budsjett**: Annual wheel, KD deadlines, and next-year budget simulator with Excel matrix download (`arshjul_matrix_2026.xlsx`).
     - 🔍 **Månedsoppgjør & Audit**: UBW transaction check, DFØ travel claims audit.
     - 📊 **EVM & Tiltakssimulator**: CPI/SPI/EAC/TCPI metrics & live EOY balance slider simulator.
     - 💾 **Datakilder & Power BI**: Direct links for SQLite (`projects.db`), DuckDB (`analytics_snapshots.duckdb`), Parquet Star Schema, and Power BI links.
     - 📜 **Statlig Rapportering & Statens Kontoplan 2026**: Searchable chart of accounts (Classes 1-8), DBH metrics, and **Direct Excel (.xlsx) Export**.
     - 📖 **Begrepskatalog & Ordliste**: Searchable financial glossary with **Direct Excel (.xlsx) Export**.

3. **Multi-Month Data Ingestion Engine (`data_ingestion.py`)**:
   - Handles multi-period data imports (`test2026T1`, `2026T1sep`, `2026T1okt`) into SQLite and DuckDB snapshots.

4. **Preskriptiv Action Engine (`action_engine.py`)**: Quantifies cost savings and recalculates EOY balances.
5. **Power BI Star Schema Exporter (`powerbi_exporter.py`)**: Exports Snappy-compressed Parquet Star Schema files.

## Installation & Setup

```bash
# 1. Clone or extract project repository
cd uia-controller-app

# 2. Synchronize virtual environment & dependencies using uv
uv sync
```

## Running the Automated Month-End Close & Statutory Pipeline (Pipeline v22)

```bash
# Execute the full 9-step consolidated month-end, annual wheel & statutory close pipeline
uv run python src/tools/antigravity_workflow.py
```

## Running the Web Interfaces

- **Static HTML Web Portal**: Open `index.html` directly in any web browser.
- **Streamlit Web App**: Run `uv run streamlit run src/tools/app.py`.
