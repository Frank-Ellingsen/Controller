# Workflow: `/manedsavslutning`

Denne arbeidsflyten utfører en helautomatisk månedsoppgjørskontroll for UiA basert på opplastede UBW-data, reiseregninger, prosjektenes EVM-status og preskriptiv tiltaksanalyse.

## Trinn i gjennomføringen:

### Trinn 1: Datainntak og Videresending
* Leser inn transaksjoner fra `data/staging/projects.db` (eller CSV/Excel-rapporter), reiseregninger fra `data/staging/reiseregninger_15_stk.csv`, og prosjektdata.

### Trinn 2: Kjør Deterministiske Verktøy & Tiltaksmotor
* Utfør den konsoliderte månedsoppgjørskjøringen direkte via **`src/tools/antigravity_workflow.py`**:
  * **Auditor-modul (`audit_travel_expenses.py`, `ubw_reader.py`):** Skanner UBW-hovedbok og reiseregninger for regelbrudd (egengodkjenning BDM == Attestant, manglende bilag > 100 kr, måltidsfradrag 20/30/50 %, rutebeskrivelse).
  * **Analyst-modul (`variance_calculator.py`):** Beregner sum driftsavsetninger mot årets rammebevilgning og vurderer 5 %-grensen iht. Kunnskapsdepartementets rundskriv F-05-20.
  * **Lead Controller & DuckDB Analytics Engine (`evm_calculator.py`, `duckdb_analytics.py`):** Utfører databaseintegrert EVM-prosjektanalyse, lagrer tidsrekke-snapshots i DuckDB (`analytics_snapshots.duckdb`), og beregner avanserte EAC-prognoser (Typical CPI, Composite CPI*SPI, Weighted 80/20).
  * **Action Engine (`action_engine.py`):** Simulering av preskriptiv tiltaksplan, finansiell effektreduksjon (descope, diettkorreksjon, investeringsfremskyndelse) og beregning av revidert EOY-balanse ved 31.12.
  * **Power BI Integration (`powerbi_exporter.py`):** Eksporterer stjerneskjemaets Parquet- og CSV-filer til `data/staging/parquet/`.

### Trinn 3: Agentrevisjon, Interaktivt Dashbord og Rapportering
* **Compliance Auditor Agent:** Genererer revisjonstabell over bilags- og fullmaktsavvik (`revisjonsrapport_reiseregninger.md`).
* **Ledger Analyst Agent:** Oppdaterer tidsrekker i DuckDB, eksporterer Parquet-filer og rapporterer avsetningsstatus.
* **Lead Controller Agent:** Utarbeider den endelige avviks- og prosjektrapporten med anbefalt tiltaksplan og revidert EOY-balanse (`action_plan_report.md`).
* **Interactive Streamlit Dashboard:** Kjøres via `uv run streamlit run src/tools/app.py` for å la ledelsen simulere tiltaksparametre med glidebrytere i et nettlesergrensesnitt.
