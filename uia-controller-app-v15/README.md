# UiA Controller App (v15 - Canonical Production Release)

An agentic financial controlling & compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with capital project controlling (DuckDB, EVM, composite EAC modeling), prescriptive action planning (EOY balance forecasting), interactive web dashboarding (Streamlit & unified HTML hub), and dedicated specialized agent roles (Excel & Power BI Specialists).

---

## Specialized Agent Team (`.agents/agents.md`)

1. **Lead Controller (Orchestrator)**: Oversees month-end close, action engine simulations, EOY balance forecasting, and executive reporting.
2. **Compliance Auditor**: Audits travel claims, invoices, and time logs against DFØ regulations and UiA delegation rules.
3. **Ledger Analyst**: Extracts and cleans UBW ledger data, running EVM and F-05-20 compliance calculations.
4. **Excel Specialist**: Handles raw `.xlsx`/`.csv` exports from Unit4 UBW, validating cell formulas, multi-tab workbooks, and formatted Excel reporting (`generate_excel_report.py`).
5. **Power BI Specialist**: Manages the Star Schema Parquet/DuckDB export pipeline (`powerbi_exporter.py`), DAX measures, and Power BI Desktop datasets/service dashboards.

---

## Directory Architecture

```text
uia-controller-app-v15/
├── .agents/                    # Agent role definitions (5 roles) and skill definitions
├── .antigravity/               # Standard Operating Procedures (SOPs)
├── data/                       # Staging, raw inputs, and institutional dimension tables
│   ├── raw/                    # Reiseregninger and raw UBW extracts
│   ├── reports/                # Generated Excel workbooks
│   └── staging/                # SQLite (projects.db), DuckDB, Parquet/CSV Star Schema
├── docs/                       # Structured documentation
│   ├── USER_GUIDE.md           # Master User Guide with workflows & CLI commands
│   ├── guides/                 # Setup & dashboard guides (Power BI, Streamlit)
│   └── reports/                # Executive summaries, audit notes & action plans
├── powerbi/                    # DAX measures, Power Query M-code & dataset builders
├── Regelverk/                  # State regulations (DFØ, KD F-05-20, SRS, Kontoplan)
├── src/tools/                  # Core Python modules & controllers
│   ├── action_engine.py        # Prescriptive action planning & EOY balance forecast
│   ├── antigravity_workflow.py # Consolidated month-end close workflow runner (v15)
│   ├── app.py                  # Interactive Streamlit Web Dashboard
│   ├── audit_travel_expenses.py# DFØ travel claim & meal deduction auditor
│   ├── duckdb_analytics.py     # DuckDB snapshotting & multi-model EAC forecasts
│   ├── evm_calculator.py       # Earned Value Management (EVM) calculator
│   ├── generate_excel_report.py# Professional formatted Excel report generator
│   ├── powerbi_exporter.py     # Star Schema Parquet/CSV export pipeline
│   ├── ubw_reader.py           # Unit4 UBW general ledger extraction
│   └── variance_calculator.py  # F-05-20 reserve cap compliance calculator
├── tests/                      # Automated pytest test suite (13 tests)
├── index.html                  # Unified executive dashboard with live Streamlit & data explorer
├── pyproject.toml              # Project dependencies & package metadata (v15.0.0)
└── requirements.txt            # Dependency specification
```

---

## Quick Start & Installation

```bash
# 1. Navigate to directory
cd uia-controller-app-v15

# 2. Synchronize dependencies using uv (or pip)
uv sync
# eller: pip install -r requirements.txt
```

---

## Running the Automated Month-End Close (Pipeline v15)

Execute the full consolidated 6-step month-end close:

```bash
uv run python src/tools/antigravity_workflow.py
```

### Pipeline Execution Steps:
1. **[1/6] Auditoria**: Scans UBW ledger and 15 DFØ travel claims for discrepancies (meal deductions, 4-eyes principle, receipts > 100 NOK).
2. **[2/6] Analyst**: Verifies F-05-20 operating reserve status against 5.0 % threshold (72M vs 60M limit = 12M overskridelse).
3. **[3/6] Lead Controller**: Computes EVM metrics (BAC, PV, EV, AC, CV, SV, CPI, SPI) from `projects.db`.
4. **[4/6] DuckDB Analytics**: Stores time-series snapshot and computes multi-model EAC forecasts (`Typical CPI`, `Composite CPI*SPI`, `Weighted 80/20`, `TCPI`).
5. **[5/6] Action Engine**: Quantifies prescriptive mitigation plan (descoping, investment advance, claim enforcement) and projects revised EOY balance.
6. **[6/6] Power BI Exporter**: Exports Star Schema tables to Parquet and CSV for Power BI Desktop.

---

## User Interfaces

### 1. Interactive Streamlit Web Dashboard (`app.py`)
```bash
uv run streamlit run src/tools/app.py
```
* Interactive sliders for ETC Descoping, Equipment Activation, and Claim Enforcement.
* Real-time EOY reserve forecast and KD exemption application generator.
* Live EVM performance table and DFØ audit center.

### 2. Unified HTML Executive Hub (`index.html`)
* Simply open `index.html` in any web browser.
* **⚡ Live Streamlit Integration**: Embedded Streamlit iframe with live connectivity check, fullscreen toggle, and built-in client-side simulation engine.
* **📂 Datakilder & Filer Explorer**: Interactive browser for all 9 data repositories across SQLite, DuckDB, DFØ CSVs, Power BI tables, and local file drag-and-drop.
* **Edward Tufte Data-Ink Design**: Zero vertical table gridlines, dark theme `#0f172a`, muted container cards, right-aligned numeric data in monospace.

---

## Automated Verification

Run the comprehensive pytest suite:
```bash
uv run pytest
```
All 13 automated tests cover EVM calculations, F-05-20 threshold logic, travel claim audit algorithms, DuckDB analytics, and Power BI star schema exporters.
