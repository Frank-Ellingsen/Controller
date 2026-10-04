---
name: powerbi-reporting-integration
description: Retningslinjer for datamodellering, Parquet-eksportering og Power BI-rapportering for UiA Controlling.
---

### Standarder for Power BI Datamodellering og Rapportering:

1. **Datamodell-arkitektur (Star Schema):**
   - **Faktatabeller:** `Fact_EVM_Snapshots` (månedlige EVM-momentskudd fra DuckDB), `Fact_UBW_Audit` (hovedbokstransaksjoner og avvik fra SQLite), `Fact_Travel_Audit` (revisjonsfunn for reiseregninger).
   - **Dimensjonstabeller:** `Dim_Project` (prosjektstammedata), `Dim_Date` (kalendertabell koblet på rapporteringsperiode), `Dim_Department` (organisasjonsstruktur og BDM-ansvarlige), `Dim_Account` (Statens Kontoplan).

2. **Parquet-eksportering & Lagring:**
   - Alle faktatabeller og dimensjoner skal eksporteres deterministisk til Parquet- og CSV-format i `data/staging/parquet/` via `powerbi_exporter.py`.
   - Filene skal bruke Snappy-komprimering for optimal ytelse og direkte import i Power BI Desktop/Service.

3. **Innebygde DAX-mål (Templates):**
   - **Dynamisk EAC-valg:**
     ```dax
     EAC_Dynamic = 
     VAR SelectedModel = SELECTEDVALUE('Param_EAC_Model'[ModelName], "Weighted 80/20")
     RETURN
         SWITCH(
             SelectedModel,
             "Typical CPI", SUM(Fact_EVM_Snapshots[eac_cpi]),
             "Composite (CPIxSPI)", SUM(Fact_EVM_Snapshots[eac_composite]),
             "Weighted 80/20", SUM(Fact_EVM_Snapshots[eac_weighted]),
             SUM(Fact_EVM_Snapshots[eac_weighted])
         )
     ```
   - **Avviksindikatorer:**
     `CV_NOK = SUM(Fact_EVM_Snapshots[cv])`
     `SV_NOK = SUM(Fact_EVM_Snapshots[sv])`
     `Operating_Reserve_Pct = DIVIDE(SUM(Fact_UBW_Audit[akkumulert_avsetning_nok]), SUM(Fact_UBW_Audit[rammebevilgning_nok]))`

4. **Visualiserings- og Rapportprinsipper (Tufte Standards):**
   - **Side 1 (Fakultetsdirektør):** Porteføljematrise (CPI vs SPI scatterplot), F-05-20 avsetningsmåler (6.0% vs 5.0% tak), samt EAC-modellsammenligning.
   - **Side 2 (Prosjektcontroller):** S-kurver for kumulativ PV, EV og AC over tid, samt TCPI-terskelmåler.
   - **Side 3 (Compliance Auditor):** Avviks-heatmap per institutt og BDM, med drill-through til enkelttransaksjoner.
