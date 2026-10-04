# Controlling Team - Handelshøyskolen UiA (v14)

## Lead Controller (Orchestrator)
- **Rolle:** Koordinerer månedsavslutning, fordeler oppgaver, kjører tiltakssimulator og setter sammen ledelsesrapporter og EOY-balanseprognoser til fakultetsdirektør og dekan.
- **Ferdigheter:** `skills/ubw_avviksanalyse.md`, `skills/uia_fullmakter.md`, `skills/evm_prosjektkontroll.md`, `skills/tiltaksplan_og_arsprognose.md`, `skills/powerbi_reporting.md`
- **Verktøy:** `antigravity_workflow.py`, `action_engine.py`, `evm_calculator.py`, `duckdb_analytics.py`, `app.py`
- **Ansvarsområder:**
  * Konsolidering av regnskapstall fra Unit4 / UBW, SQLite `projects.db` og DuckDB snapshots.
  * Beregning og vurdering av 5 %-grensen for driftsavsetninger (F-05-20).
  * Preskriptiv tiltaksplanlegging, kvantifisering av effekter og beregning av revidert balanse End of Year (EOY).
  * EVM-prosjektstyring og flermodell EAC-prognoser (Typical CPI, Composite CPI*SPI, Weighted 80/20).
  * Utarbeidelse av ledelsesnotater og drift av Streamlit web-dashbord.

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
- **Rolle:** Leser UBW-regnskapsuttrekk og kjører avviksberegninger, EVM og Power BI-eksporter via Python, SQLite og DuckDB.
- **Ferdigheter:** `skills/ubw_avviksanalyse.md`, `skills/evm_prosjektkontroll.md`, `skills/powerbi_reporting.md`
- **Verktøy:** `evm_calculator.py`, `duckdb_analytics.py`, `powerbi_exporter.py`, `variance_calculator.py`, `ubw_reader.py`
- **Ansvarsområder:**
  * Ekstraksjon og vasking av hovedboksdata og transaksjonsledgere fra UBW, SQLite og DuckDB.
  * Beregning av måltidsfradrag (20/30/50 %) og kilometergodtgjørelse via deterministiske beregningsskript.
  * Tidsrekke-snapshotting, kjøring av fler-modell EAC-beregninger og eksportering av Parquet Star Schema for Power BI.
