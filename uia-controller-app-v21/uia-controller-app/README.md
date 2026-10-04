# UiA Controller App (v17 - Canonical Production Release)

An agentic financial controlling & compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with capital project controlling (DuckDB, EVM, composite EAC modeling), preskriptiv action planning (EOY balance forecasting), interactive Streamlit web dashboarding, and a complete Single Page Web Application () featuring Excel exports for Statens Kontoplan 2026 and Financial Glossary.

## Key Features in v17:

1. **Integrated Web Portal ()**:
   - Single Page Application with 6 tabs:
     - 📅 **Årshjul & Budsjett**: Annual wheel, KD deadlines, and next-year budget simulator.
     - 🔍 **Månedsoppgjør & Audit**: UBW transaction check, DFØ travel claims audit.
     - 📊 **EVM & Tiltakssimulator**: CPI/SPI/EAC/TCPI metrics & live EOY balance slider simulator.
     - 💾 **Datakilder & Power BI**: Direct links for SQLite (), DuckDB (), Parquet Star Schema, and Power BI links.
     - 📜 **Regelverk & Statens Kontoplan 2026**: Searchable chart of accounts (Classes 1-8) with **Direct Excel (.xlsx) Export**.
     - 📖 **Begrepskatalog & Ordliste**: Searchable financial glossary with **Direct Excel (.xlsx) Export**.

2. **Preskriptiv Action Engine ()**: Quantifies cost savings and recalculates EOY balances.
3. **Streamlit Web Dashboard ()**: Alternative Python dashboard with interactive sliders.
4. **Power BI Star Schema Exporter ()**: Exports Snappy-compressed Parquet Star Schema files.
5. **Budget Engine ()**: Annual wheel allocation calculator.

## Installation & Setup



## Running the Automated Month-End Close (Pipeline v17)



## Running the Web Interfaces

- **Static HTML Web Portal**: Open  directly in any web browser.
- **Streamlit Web App**: Run 
