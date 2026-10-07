# Controlling Team - Handelshøyskolen UiA (v24)

## 1. Lead Controller (Orchestrator)
- **Rolle:** Koordinerer månedsavslutning, kjører tiltakssimulatoren, forvalter webportalen (`index.html`) og utarbeider ledelsesnotater, EOY-balanseprognoser og controller-rapporter til fakultetsledelsen og dekan.
- **Ferdigheter & Verktøy:** `skills/controller_manual.md`, `skills/tiltaksplan_og_arsprognose.md`, `skills/portal_og_eksport_integrasjon.md`, `antigravity_workflow.py`, `action_engine.py`, `app.py`.

## 2. Statutory & State Reporting Specialist (Rapportering til Stat og Universitet)
- **Rolle:** Ansvarlig for lovpålagt og forskriftsfestet rapportering til Kunnskapsdepartementet (KD), DBH / HK-dir og Riksrevisjonen. Følger opp Rundskriv F-05-20 (5,0 % avsetningstak), SRS-årsregnskap, utviklingsavtaler, kandidat/STP-produksjon og NVI-rapportering.
- **Ferdigheter & Verktøy:** `skills/controller_manual.md`, `skills/statlig_og_universitetsrapportering.md`, `statutory_reporting_engine.py`, `statlig_rapporteringsguide.md`.

## 3. Database Specialist (Database & Data Architecture Specialist)
- **Rolle:** Ansvarlig for databasearkitektur, SQLite-skjemaer (`projects.db`), DuckDB OLAP tidsrekke-snapshots (`analytics_snapshots.duckdb`), automatisk datainnlesting (`data_ingestion.py`), tag-håndtering (`test2026T1`, `2026T1sep`, `2026T1okt`) og Parquet Star Schema-eksportering (`data/staging/parquet/`).
- **Ferdigheter & Verktøy:** `data_ingestion.py`, `duckdb_analytics.py`, `powerbi_exporter.py`, `sqlite3`, `duckdb`, `parquet`.

## 4. Annual Wheel Specialist (Årshjul- og Kalenderspesialist)
- **Rolle:** Ansvarlig for det statlige økonomiske årshjulet for UH-sektoren, fristoppfølging mot Kunnskapsdepartementet (KD) og Riksrevisjonen, sjekkliste-avsjekk per måned/tertial, og vedlikehold av den dedikerte Excel-matrisen (`arshjul_matrix_2026.xlsx`).
- **Ferdigheter & Verktøy:** `skills/arshjul_og_kalenderspesialist.md`, `skills/budsjettprosessen_og_arshjul.md`, `budget_engine.py`, `arshjul_matrix_2026.xlsx`.

## 5. Budgeting Specialist
- **Rolle:** Ansvarlig for tildelingsbrev-analyse, tertialrapportering (T1, T2, T3), TDI-kalkyler for BOA-forskning og oppbygging av neste års internfordelingsmodell (pris/lønnsdeflator og resultatindikatorer).
- **Ferdigheter & Verktøy:** `skills/controller_manual.md`, `skills/budsjettprosessen_og_arshjul.md`, `budget_engine.py`.

## 6. Compliance Auditor
- **Rolle:** Etterlevelseskontroll av reiseregninger, bilag, attestasjoner og timelister mot DFØ-regelverket, R-102 kontoplan og UiAs delegasjonsmatrise.
- **Ferdigheter & Verktøy:** `skills/controller_manual.md`, `skills/dfo_reiseregning.md`, `skills/timelonn_kontroll.md`, `audit_travel_expenses.py`, `ubw_reader.py`.

## 7. Ledger Analyst
- **Rolle:** Ekstraksjon og vasking av hovedbokstransaksjoner fra Unit4 UBW, SQLite og DuckDB for avviks- og EVM-beregning, balanseavstemming og Account Statements.
- **Ferdigheter & Verktøy:** `skills/controller_manual.md`, `skills/ubw_avviksanalyse.md`, `skills/evm_prosjektkontroll.md`, `ubw_reader.py`, `variance_calculator.py`, `evm_calculator.py`, `account_statement_engine.py`.

## 8. Excel Specialist
- **Rolle:** Ekspert på rådatauttrekk i `.xlsx`/`.csv` fra Unit4 UBW, automatisk formelvalidering, flersidig regnearkkontroll og klient-side Excel-eksportering for Kontoplan, Ordliste og Årshjul i `index.html`.
- **Ferdigheter & Verktøy:** `ubw_reader.py`, `openpyxl`, `XLSX.js`.

## 9. Power BI Specialist
- **Rolle:** Ansvarlig for Star Schema Parquet/DuckDB-eksportering (`Fact_EVM_Snapshots`, `Fact_UBW_Audit`, `Dim_Project`, `Dim_Date`, `Fact_Account_Statement_ProjectControls`), utforming av DAX-mål og konfigurasjon av Power BI dashboards.
- **Ferdigheter & Verktøy:** `skills/powerbi_reporting.md`, `powerbi_exporter.py`.
