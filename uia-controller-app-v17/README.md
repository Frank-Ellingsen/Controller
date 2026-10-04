# UiA Controller App (v17 - Production Release)

An agentic financial controlling & compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with capital project controlling (DuckDB, EVM, composite EAC modeling), prescriptive action planning (EOY balance forecasting), annual wheel and budget building (Kap. 260 post 50, deflator, TDI overhead), interactive web portal (6-tab SPA with SheetJS Excel exports), Streamlit dashboard, and a dedicated team of 6 specialized agent roles.

---

## Specialized Agent Team (`.agents/agents.md`)

1. **Lead Controller (Orchestrator)**: Coordinates month-end close, oversees action engine simulations, manages the web portal (`index.html`), and drafts executive EOY balance reports.
2. **Budgeting Specialist**: Manages the statutory annual wheel (Årshjul), allocation letters, tertial reporting, next-year budget building (Prop. 1 S), and BOA / TDI overhead models.
3. **Compliance Auditor**: Conducts compliance audits on DFØ travel expenses, invoices, and timesheets against the 4-eyes principle and delegation rules.
4. **Ledger Analyst**: Extracts and cleans Unit4 UBW general ledger entries, running variance analysis, EVM calculations, and DuckDB time-series snapshots.
5. **Excel Specialist**: Validates cell formulas and multi-tab workbooks from Unit4 UBW, manages automated reporting (`generate_excel_report.py`), and oversees client-side SheetJS Excel exports.
6. **Power BI Specialist**: Manages Star Schema Parquet/DuckDB export pipelines (`Fact_EVM_Snapshots`, `Fact_UBW_Audit`, `Fact_Travel_Audit`, `Dim_Project`, `Dim_Date`), DAX measures, and Power BI dashboards.

---

## Directory Architecture

```text
uia-controller-app-v17/
├── .agents/                    # Agent role definitions (6 roles) and skill definitions
│   └── skills/                 # Domain skills (DFØ, EVM, Power BI, Tiltak, Årshjul, Portal & Eksport)
├── .antigravity/               # Standard Operating Procedures (SOPs)
│   └── knowledge/              # Controlling SOP & Portal Architecture SOP
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
├── src/tools/                  # Core Python modules & controllers (11 tools)
│   ├── action_engine.py        # Prescriptive action planning & EOY balance forecast
│   ├── antigravity_workflow.py # Consolidated month-end close & annual wheel runner (v17)
│   ├── app.py                  # Interactive Streamlit Web Dashboard (5 tabs)
│   ├── audit_travel_expenses.py# DFØ travel claim & meal deduction auditor
│   ├── budget_engine.py        # Annual wheel tracker & next-year budget builder
│   ├── duckdb_analytics.py     # DuckDB snapshotting & multi-model EAC forecasts
│   ├── evm_calculator.py       # Earned Value Management (EVM) calculator
│   ├── generate_excel_report.py# Professional formatted Excel report generator
│   ├── powerbi_exporter.py     # Star Schema Parquet/CSV export pipeline
│   ├── ubw_reader.py           # Unit4 UBW general ledger extraction
│   └── variance_calculator.py  # F-05-20 reserve cap compliance calculator
├── tests/                      # Automated pytest test suite (16 tests)
├── index.html                  # Single Page Application (SPA) Web Portal (6 tabs & SheetJS)
├── pyproject.toml              # Project dependencies & package metadata (v17.0.0)
└── requirements.txt            # Dependency specification
```

---

## Quick Start & Installation

```bash
# 1. Navigate to directory
cd uia-controller-app-v17

# 2. Synchronize dependencies using uv (or pip)
uv sync
# eller: pip install -r requirements.txt
```

---

## Running the Automated Month-End Close (Pipeline v17)

Execute the full consolidated 7-step month-end close and annual wheel review:

```bash
uv run python src/tools/antigravity_workflow.py
```

### 7-Step Pipeline Execution:
1. **[1/7] Auditoria**: Scans UBW ledger and 15 DFØ travel claims for discrepancies (meal deductions, 4-eyes rule, receipts > 100 NOK).
2. **[2/7] Analyst**: Verifies F-05-20 operating reserve status against 5.0 % threshold (72M vs 60M limit = 12M overskridelse).
3. **[3/7] Lead Controller**: Computes EVM metrics (BAC, PV, EV, AC, CV, SV, CPI, SPI) from `projects.db`.
4. **[4/7] DuckDB Analytics**: Stores time-series snapshot and computes multi-model EAC forecasts (`Typical CPI`, `Composite CPI*SPI`, `Weighted 80/20`, `TCPI`).
5. **[5/7] Action Engine**: Quantifies prescriptive mitigation plan (descoping, investment advance, claim enforcement) and projects revised EOY balance.
6. **[6/7] Power BI Exporter**: Exports Star Schema tables to Parquet and CSV for Power BI Desktop.
7. **[7/7] Budgeting Specialist**: Evaluates annual wheel milestone status, projects next-year budget frame (Kap. 260 post 50), and calculates faculty allocations.

---

## User Interfaces

### 1. Unified Web Portal (`index.html` - 6 Tabs & SheetJS)
Open `index.html` directly in any web browser:
* **Tab 1: 📅 Årshjul & Budsjett**: Annual wheel calendar (Q1-Q4 milestones) and dynamic next-year budget frame calculator (Kap. 260 post 50) with deflator, performance, and strategic reserve sliders.
* **Tab 2: 🔍 Månedsoppgjør & Audit**: Travel claims compliance center (15 claims, meal deduction errors, 4-eyes breaches).
* **Tab 3: 📊 EVM & Tiltakssimulator**: Earned Value KPIs and live interactive sliders for Descoping and Accelerated Investments with real-time F-05-20 compliance status.
* **Tab 4: 💾 Datakilder & Power BI**: Live status indicators for SQLite, DuckDB, and Parquet Star Schema.
* **Tab 5: 📜 Regelverk & Kontoplan**: Statens Kontoplan 2026 (Kontoklasser 1-8) with live search and client-side SheetJS **Excel-eksport (`.xlsx`)**.
* **Tab 6: 📖 Begrepskatalog & Ordliste**: Complete financial controlling dictionary (BAC, EAC, TCPI, BDM, TDI, SRS, EOY) with live search and SheetJS **Excel-eksport (`.xlsx`)**.

### 2. Interactive Streamlit Web Dashboard (`app.py`)
```bash
uv run streamlit run src/tools/app.py
```
* 5 tabs for real-time prescriptive simulations, EVM tracking, and budget building.

---

## Automated Verification

Run the comprehensive pytest suite:
```bash
uv run pytest
```
All 16 automated tests verify EVM formulas, F-05-20 threshold logic, travel claim audit algorithms, DuckDB OLAP analytics, Power BI star schema exports, and the Budget Engine (Annual Wheel, inflation adjustments, and TDI calculations).
