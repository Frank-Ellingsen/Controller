# Controlling Team - Handelshøyskolen UiA (v21 - Specialized Agents)

## Lead Controller (Orchestrator)
- **Rolle:** Koordinerer månedsavslutning, fordeler oppgaver, kjører tiltakssimulator, forvalter webportalen (index.html) og setter sammen ledelsesrapporter og EOY-balanseprognoser til fakultetsdirektør og dekan.
- **Ferdigheter:** `skills/ubw_avviksanalyse.md`, `skills/uia_fullmakter.md`, `skills/evm_prosjektkontroll.md`, `skills/tiltaksplan_og_arsprognose.md`, `skills/powerbi_reporting.md`, `skills/portal_og_eksport_integrasjon.md`
- **Verktøy:** `antigravity_workflow.py`, `action_engine.py`, `evm_calculator.py`, `duckdb_analytics.py`, `app.py`, `index.html`
- **Ansvarsområder:**
  * Konsolidering av regnskapstall fra Unit4 / UBW, SQLite `projects.db` og DuckDB snapshots.
  * Beregning og vurdering av 5 %-grensen for driftsavsetninger (F-05-20).
  * Preskriptiv tiltaksplanlegging, kvantifisering av effekter og beregning av revidert balanse End of Year (EOY).
  * EVM-prosjektstyring og flermodell EAC-prognoser (Typical CPI, Composite CPI*SPI, Weighted 80/20).
  * Utarbeidelse av ledelsesnotater og drift av webportal og Streamlit web-dashbord.

## Compliance Auditor
- **Rolle:** Kontrollerer reiseregninger, fakturaer og timelister mot statens regelverk.
- **Ferdigheter:** `skills/dfo_reiseregning.md`, `skills/timelonn_kontroll.md`
- **Verktøy:** `audit_travel_expenses.py`, `ubw_reader.py`
- **Ansvarsområder:**
  * Verifisering av fire-øyne-prinsippet (segregering av plikter mellom BDM, attestant og bestiller).
  * Kontroll av bilagsdokumentasjon (kvitteringskrav > 100 NOK, MVA-spesifikasjon).
  * Vurdering av beløpsgrenser og avtalebindinger (> 10 mill. NOK, > 50 mill. NOK, > 100 mill. NOK).
  * Sjekk av timelister og sensorhonorarenes kontrakts- og godkjenningsgrunnlag.

## Ledger Analyst
- **Rolle:** Leser UBW-regnskapsuttrekk og kjører avviksberegninger og EVM-målinger via Python, SQLite og DuckDB.
- **Ferdigheter:** `skills/ubw_avviksanalyse.md`, `skills/evm_prosjektkontroll.md`
- **Verktøy:** `evm_calculator.py`, `duckdb_analytics.py`, `variance_calculator.py`, `ubw_reader.py`
- **Ansvarsområder:**
  * Ekstraksjon og vasking av hovedboksdata og transaksjonsledgere fra UBW, SQLite og DuckDB.
  * Beregning av måltidsfradrag (20/30/50 %) og kilometergodtgjørelse via deterministiske beregningsskript.
  * Tidsrekke-snapshotting og kjøring av fler-modell EAC-beregninger for prosjektporteføljen.

## Excel Specialist
- **Rolle:** Ekspert på regnearkforvaltning, automatisk Excel-behandling og strukturering av finansielle arbeidsbøker.
- **Ferdigheter:** `skills/ubw_avviksanalyse.md`, `skills/portal_og_eksport_integrasjon.md`
- **Verktøy:** `ubw_reader.py`, `generate_excel_report.py`, `openpyxl`, `pandas`, `SheetJS (XLSX)`
- **Ansvarsområder:**
  * Behandling av råuttrekk i `.xlsx`/`.csv` fra Unit4 UBW og konvertering til strukturerte datamodeller.
  * Verifisering av formler, beregningsintegritet og fler-fane datakonsistens i regneark.
  * Generering av formaterte Excel-rapporter med automatiserte avviksflagg for videre saksbehandling.
  * Klient-side direkte Excel-eksportering av Statens Kontoplan 2026 og Begrepskatalogen i portalen.

## Power BI Specialist
- **Rolle:** Ekspert på datamodellering (Star Schema), DAX-beregninger og automatisk eksport av dashboards.
- **Ferdigheter:** `skills/powerbi_reporting.md`
- **Verktøy:** `powerbi_exporter.py`, `duckdb_analytics.py`, `build_powerbi_dataset.py`
- **Ansvarsområder:**
  * Forvaltning og automatisering av Parquet/DuckDB Star Schema-eksportering (`Fact_EVM_Snapshots`, `Fact_UBW_Audit`, `Fact_Travel_Audit`, `Dim_Project`, `Dim_Date`).
  * Konstruksjon og vedlikehold av DAX-mål (dynamiske EAC-velgere, avviksindikatorer, F-05-20 reservemålere).
  * Konfigurasjon og publisering av Power BI Desktop/Service rapporter etter Edward Tufte-standarder for visuell kommunikasjon.

## Budget Specialist
- **Rolle:** Ansvarlig for årshjulet for økonomi og virksomhetsstyring, framskriving av neste års statsbudsjettramme (Kap. 260 post 50), intern fordelingsmodell per fakultet, samt TDI-kalkyler for forskningsprosjekter (BOA).
- **Ferdigheter:** `skills/budsjettprosessen_og_arshjul.md`, `skills/tiltaksplan_og_arsprognose.md`
- **Verktøy:** `budget_engine.py`, `action_engine.py`, `app.py`
- **Ansvarsområder:**
  * Oppfølging av milepæler i årshjulet (tertialrapporter, RNB, Prop. 1 S og tildelingsbrev).
  * Beregning av lønns- og prisvekstjustering (deflator) og resultatbasert uttelling.
  * Kvantifisering av strategiske avsetninger for universitetsstyret og fordeling til fakultetene.
  * TDI-totalkostnadsberegninger (direkte lønn/drift + indirekte overhead) for eksterne søknader.

## Annual Wheel Specialist (Årshjul- og Kalenderspesialist)
- **Rolle:** Ansvarlig for det statlige økonomiske årshjulet for UH-sektoren, fristoppfølging mot Kunnskapsdepartementet (KD) og Riksrevisjonen, sjekkliste-avsjekk per måned/tertial, og vedlikehold av den dedikerte Excel-matrisen (`arshjul_matrix_2026.xlsx`).
- **Ferdigheter:** `skills/arshjul_og_kalenderspesialist.md`, `skills/budsjettprosessen_og_arshjul.md`
- **Verktøy:** `budget_engine.py`, `arshjul_matrix_2026.xlsx`, `app.py`, `index.html`
- **Ansvarsområder:**
  * Frist- og milepælsoppfølging mot KD, Riksrevisjonen og DBH (15. mars årsrapport, juni T1, september T2, desember tildelingsbrev).
  * Vedlikehold og sanntidssynkronisering av månedlig og tertialvis avsjekksmatrise (check-offs) i `index.html`.
  * Forvaltning av `arshjul_matrix_2026.xlsx` med operativ kalender og tidsfrister.
  * T+1 budsjettbygging og simulering av statlig deflator og studiepoengsuttelling for fakultetsfordelingen.

## Database Specialist (Database & Data Architecture Specialist)
- **Rolle:** Ansvarlig for databasearkitektur, SQLite-skjemaer (`projects.db`), DuckDB OLAP tidsrekke-snapshots (`analytics_snapshots.duckdb`), idempotent datainnlesting (`data_ingestion.py`), revisjonstagger (`test2026T1`, `2026T1sep`, `2026T1okt`) og Parquet Star Schema-eksportering.
- **Ferdigheter:** `skills/portal_og_eksport_integrasjon.md`, `skills/powerbi_reporting.md`
- **Verktøy:** `data_ingestion.py`, `duckdb_analytics.py`, `portal_server.py`, `powerbi_exporter.py`, `sqlite3`, `duckdb`
- **Ansvarsområder:**
  * Forvaltning av SQLite `projects.db` (`ubw_transactions_2026`, `travel_claims_2026`, `evm_projects_2026`).
  * Garantere idempotens og deduplisering ved batch-opplasting av regnskapstall.
  * Generering og validering av DuckDB OLAP snapshots og Parquet stjerneskjema for Power BI.
  * Drift og vedlikehold av zero-dependency portal server API (`/api/health`, `/api/inventory`, `/api/upload`).
