# UiA Controller App (v16 - Production Release)

An agentic financial controlling & compliance application for Universitetet i Agder (UiA), bridging Norwegian public sector regulations (DFØ, UBW/Unit4, F-05-20) with capital project controlling (DuckDB, EVM, composite EAC modeling), prescriptive action planning (EOY balance forecasting), annual wheel and next-year budget building (Kap. 260 post 50, deflator, TDI overhead), interactive web dashboarding (Streamlit & unified HTML hub), and a dedicated team of 6 specialized agent roles.

---

## Specialized Agent Team (`.agents/agents.md`)

1. **Lead Controller (Orchestrator)**: Oversees month-end close, action engine simulations, EOY balance forecasting, and executive reporting.
2. **Compliance Auditor**: Audits travel claims, invoices, and time logs against DFØ regulations and UiA delegation rules.
3. **Ledger Analyst**: Extracts and cleans UBW ledger data, running EVM and F-05-20 compliance calculations.
4. **Excel Specialist**: Handles raw `.xlsx`/`.csv` exports from Unit4 UBW, validating cell formulas, multi-tab workbooks, and formatted Excel reporting (`generate_excel_report.py`).
5. **Power BI Specialist**: Manages the Star Schema Parquet/DuckDB export pipeline (`powerbi_exporter.py`), DAX measures, and Power BI Desktop datasets/service dashboards.
6. **Budget Specialist**: Manages the economic annual wheel (Årshjul), next-year budget frame building (Kap. 260 post 50, deflator/prisjustering), internal allocation across faculties, and TDI overhead calculations for research grants (`budget_engine.py`).

---

## Directory Architecture

```text
uia-controller-app-v16/
├── .agents/                    # Agent role definitions (6 roles) and skill definitions
│   └── skills/                 # Domain skills (DFØ, EVM, Power BI, Tiltak, Årshjul)
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
├── src/tools/                  # Core Python modules & controllers (11 tools)
│   ├── action_engine.py        # Prescriptive action planning & EOY balance forecast
│   ├── antigravity_workflow.py # Consolidated month-end close & annual wheel runner (v16)
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
├── index.html                  # Unified executive dashboard with live Streamlit & data explorer
├── pyproject.toml              # Project dependencies & package metadata (v16.0.0)
└── requirements.txt            # Dependency specification
```

---

## Quick Start & Installation

```bash
# 1. Navigate to directory
cd uia-controller-app-v16

# 2. Synchronize dependencies using uv (or pip)
uv sync
# eller: pip install -r requirements.txt
```

---

## Running the Automated Month-End Close (Pipeline v16)

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
7. **[7/7] Budget Specialist**: Evaluates annual wheel milestone status, projects next-year budget frame (Kap. 260 post 50), and calculates faculty allocations.

---

## User Interfaces

### 1. Interactive Streamlit Web Dashboard (`app.py`)
```bash
uv run streamlit run src/tools/app.py
```
* **Tab 1:** Revidert EOY Balanse & Resultat (31.12 forecast)
* **Tab 2:** EVM Prosjektstyring & Descoping (UM-DEF-02, UM-ENG-03, UM-FPV-01)
* **Tab 3:** F-05-20 Avsetningskontroll & KD Søknad
* **Tab 4:** Internkontroll & Reiseregninger (DFØ compliance audit)
* **Tab 5:** Årshjul & Neste Års Budsjett (Annual Wheel milestones, deflator sliders, faculty allocation, TDI calculator)

### 2. Unified HTML Executive Hub (`index.html`)
* Open `index.html` directly in any modern browser.
* **⚡ Live Streamlit Integration**: Embedded Streamlit iframe with live connectivity check, fullscreen toggle, and built-in client-side simulation engine.
* **📂 Datakilder & Filer Explorer**: Interactive browser for all 9 data repositories across SQLite, DuckDB, DFØ CSVs, Power BI tables, and local CSV drag-and-drop.
* **Edward Tufte Data-Ink Design**: Zero vertical table gridlines, dark theme `#0f172a`, muted container cards, right-aligned monospace numbers.

---

## Automated Verification

Run the comprehensive pytest suite:
```bash
uv run pytest
```
All 16 automated tests verify EVM formulas, F-05-20 threshold logic, travel claim audit algorithms, DuckDB OLAP analytics, Power BI star schema exports, and the v16 Budget Engine (Annual Wheel, inflation adjustments, and TDI calculations).
