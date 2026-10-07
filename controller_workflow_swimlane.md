# UiA Controlling Workflow — End-to-End Swimlane & Process Architecture

**Organisasjon:** Universitetet i Agder (UiA)  
**Dokumenttype:** Operativ Prosessarkitektur & Dataflytdiagram  
**Rapporteringsperiode:** 2026 (M01–M12 / Q1–Q4)  

---

## 1. Executive Summary & Process Overview

Denne prosessbeskrivelsen og det tilhørende Swimlane-diagrammet kartlegger den **end-to-end finansielle controllingprosessen ved Universitetet i Agder (UiA)**. Prosessen brobygger statlige føringsregler (**DFØ, Kunnskapsdepartementet F-05-20, Statens Kontoplan R-102**), prosjektstyring etter **Earned Value Management (EVM)** og **TDI-modellen for BOA**, med den agentiske applikasjonsarkitekturen (**SQLite `projects.db`, DuckDB OLAP, Streamlit, Power BI Star Schema og `index.html`**).

---

## 2. Vertikale Swimlanes (Roller, Avdelinger & Systemer)

Prosessen er strukturert horisontalt gjennom 5 faser på tvers av 4 vertikalt ordnede swimlanes:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SWIMLANE 1: Linjeledelse & BDM (Dekan, Instituttleder, Prosjektleder)                                  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SWIMLANE 2: Controlling & Audit Team (Lead Ctrl, Compliance Auditor, Budget Spec., Ledger Analyst)     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SWIMLANE 3: Kjerne IT-Systemer & Databaser (Unit4 UBW, DFØ, SQLite `projects.db`, DuckDB)              │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SWIMLANE 4: Statlig Rapportering & BI (KD, DBH / HK-dir, Riksrevisjonen, Power BI)                      │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. End-to-End Dataflyt & Arbeidsprosess (Fase 1 til 5)

### 📍 Fase 1: Pre-Award & Budsjettforberedelse (T+1)
1. **BOA-Søknad & TDI-Kalkyle (Swimlane 1):** Prosjektleder (PL) og prosjektcontroller utarbeider prosjektkalkyle basert på Totalkostnadsmodellen (TDI = Direkte lønn/drift + TDI Overhead).
2. **BDM-Godkjenning & Ramme (Swimlane 1):** Dekan/Instituttleder (BDM-holder) gir skriftlig forhåndssamtykke til frikjøp, egenandel og kapasitetsbruk.
3. **Opprettelse i UBW & Master Database (Swimlane 3):** Prosjektet tildeles prosjekt-ID i Unit4 UBW. Masterdata synkroniseres til SQLite `projects.db`.

### 📍 Fase 2: Bilagsbehandling & Transaksjonskontroll (M01–M12)
4. **Varemottak & Bestilling (Swimlane 1):** Mottaker bekrefter leveranse i ERP. Ved avvik utløses en maskinell sperre i fakturaflyten.
5. **Attestasjonskontroll (Swimlane 2):** Compliance Auditor sjekker utgiftsbilag mod Statens Kontoplan (R-102), MVA-snudd avregning og kvitteringskrav (>100 NOK).
6. **BDM Utbetalingsgodkjenning (Swimlane 1):** To-manns-prinsippet håndheves (`BDM_ID != Attestant_ID`). Unntak: Bagatellmessige kjøp under kr 5 000 NOK.
7. **Bokføring & Betaling (Swimlane 3):** Sentral regnskapsføring i Unit4 UBW og DFØ. Automatisk umanipulerbar audit-trail genereres.

### 📍 Fase 3: Månedsoppgjør & EVM Analytics (Månedlig)
8. **Data Ingestion & Snapshots (Swimlane 3):** `data_ingestion.py` leser inn nye transaksjoner med tags (`test2026T1`, `2026T1sep`, `2026T1okt`). DuckDB lagrer tidsrekke-snapshots.
9. **EVM Performance Review (Swimlane 2):** `evm_calculator.py` beregner CPI, SPI, CV, SV, EAC og TCPI. Statusflagg settes (`CRITICAL`, `WARNING`, `ON TRACK`).
10. **Account Statement Generation (Swimlane 2):** `account_statement_engine.py` sammenstiller 8-kolonners kontostilling YTD (Total Budget, Budget YTD, Actual YTD, Progress Value/EV, Cost Variance, Forecast EOY, Forecast Variance EOY).

### 📍 Fase 4: Preskriptiv Tiltakssimulator & EOY Balanseprognose
11. **Preskriptiv Tiltaksanalyse (Swimlane 2):** `action_engine.py` simulerer kostnadskutt (descoping i ETC) og omplassering av investeringer.
12. **F-05-20 Avsetningskontroll (Swimlane 1 & 2):** Sjekker at akkumulert driftsavsetning per 31.12 ikke overstiger **5,0 %-taket** i KDs Rundskriv F-05-20. Utarbeider uoppfordret dispensasjonssøknad ved behov.
13. **Interaktiv Web Dashboard (Swimlane 2 & 3):** Ledelsen tester glidebrytere i Streamlit (`app.py`) og `index.html` for simulering av revidert EOY-balanse.

### 📍 Fase 5: Lovpålagt Rapportering & BI-Eksport
14. **DBH & HK-dir Rapportering (Swimlane 4):** Innrapportering av 278 500 STP, kandidatproduksjon, Ph.d.-grader og NVI-publiseringspoeng.
15. **Riksrevisjonen & SRS Årsregnskap (Swimlane 4):** Periodisert virksomhetsregnskap føres iht. Statlige RegnskapsStandarder (SRS) og R-102 kontoplan.
16. **Power BI Parquet Export (Swimlane 4):** `powerbi_exporter.py` eksporterer Parquet Star Schema-filer (`Fact_EVM_Snapshots.parquet`, `Fact_Account_Statement_UiA.parquet`).

---

## 4. Visuelt Workflow-Diagram (Swimlane PNG)

Prosessoversikten er visuelt fremstilt i det genererte diagrammet:
`controller_workflow_swimlane.png`

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               UiA CONTROLLING WORKFLOW — SWIMLANE MAP                                       │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬──────────────────────────────┤
│ FASE 1: PRE-AWARD │ FASE 2: BILAG &   │ FASE 3: MÅNEDS-   │ FASE 4: TILTAK    │ FASE 5: LOVPÅLAGT            │
│ & BUDSJETT (T+1)  │ TRANSAKSJON       │ OPPGJØR & EVM     │ & EOY FORECAST    │ RAPPORTERING & BI            │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────────────────┤
│ 1. BOA / TDI      │ 4. Varemottak     │                   │ 12. F-05-20       │                              │
│ 2. BDM Samtykke   │ 6. BDM Godkjenning│                   │     Søknad        │                              │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────────────────┤
│                   │ 5. Attestasjon    │ 9. EVM Review     │ 11. Action Engine │                              │
│                   │    Compliance     │ 10. Account Stmt  │ 13. Web Dashboard │                              │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────────────────┤
│ 3. UBW & DB       │ 7. Bokføring &    │ 8. Ingestion &    │                   │                              │
│    Opprettelse    │    Betaling (DFØ) │    DuckDB Snap    │                   │                              │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────────────────┤
│                   │                   │                   │                   │ 14. DBH / HK-dir             │
│                   │                   │                   │                   │ 15. SRS / Riksrevisjonen     │
│                   │                   │                   │                   │ 16. Power BI Parquet         │
└───────────────────┴───────────────────┴───────────────────┴───────────────────┴──────────────────────────────┘
```

---

## 5. Oppsummering og Tilgang

Både denne Markdown-rapporten og diagram-bildet ligger klare i Studio-panelet og i kildekodepakken for UiA Controlling App:
- 📄 `controller_workflow_swimlane.md`
- 🖼️ `controller_workflow_swimlane.png`
