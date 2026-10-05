# UiA Controller App (v23 - Canonical Production Release)

An agentic financial controlling, project controls & statutory compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with statutory state reporting (KD, DBH/HK-dir, Riksrevisjonen), Finance & Project Controls Account Statements (Engineering, Procurement, Construction, UiA Faculties), capital project controlling (DuckDB, EVM, composite EAC modeling), preskriptiv action planning (EOY balance forecasting), interactive Streamlit web dashboarding, and a complete Single Page Web Application (`index.html`) featuring Excel exports for Statens Kontoplan 2026, Financial Glossary, Account Statements, and Annual Wheel Check-Off Matrix.

## Key Features in v23:

1. **Finance & Project Controls Account Statement Engine (`account_statement_engine.py`)**:
   - **8-Column Layout**: Account | Total Budget | Budget YTD | Actual YTD | Progress Value (EV) | Cost Variance (CV) | Forecast (EAC) | Forecast Variance (VAC).
   - **Dual Model Support**: Supports both Project Controls (Engineering, Procurement, Construction) and UiA Departmental Rames (TN, HH, HELS, Fellesadministrasjon).
   - **Parquet & CSV Export**: Automatically exports `Fact_Account_Statement_ProjectControls` and `Fact_Account_Statement_UiA` tables for Power BI and Excel integration.

2. **Statutory & State Reporting Specialist (`statutory_reporting_engine.py`)**:
   - **Kunnskapsdepartementet (KD):** Årsrapport & Årsregnskap (SRS), F-05-20 reserve compliance (5,0 % cap), Utviklingsavtale monitoring.
   - **DBH / HK-dir:** Automatic generation of Student Credits (STP), Graduating Candidates, PhD completions, NVI Research Publication Points, and Staff Competence Ratios.
   - **Riksrevisjonen:** Bevilgningsreglement, BDM Fire-øyne-kontroll (`BDM_ID != Attestant_ID`), and R-102 Chart of Accounts audit.
   - **Skatteetaten:** MVA-kompensasjon and BOA/TDI research accounting reconciliation.

3. **Integrated Web Portal (`index.html`)**:
   - Single Page Application featuring v23 Account Statement reporting & 6 interactive tabs.

4. **Multi-Month Data Ingestion Engine (`data_ingestion.py`)**:
   - Handles multi-period data imports (`test2026T1`, `2026T1sep`, `2026T1okt`) into SQLite and DuckDB snapshots.

5. **10-Step Consolidated Pipeline (`antigravity_workflow.py`)**:
   - Executes full 10-step month-end, annual wheel, statutory reporting & Account Statement close pipeline.

## Installation & Setup

```bash
# 1. Clone or extract project repository
cd uia-controller-app-v23

# 2. Synchronize virtual environment & dependencies using uv
uv sync
```

## Running the Automated Pipeline (Pipeline v23)

```bash
# Execute the full 10-step consolidated month-end, annual wheel, statutory & Account Statement pipeline
uv run python src/tools/antigravity_workflow.py
```

## Running the Web Interfaces

- **Static HTML Web Portal**: Open `index.html` directly in any web browser.
- **Streamlit Web App**: Run `uv run streamlit run src/tools/app.py`.
