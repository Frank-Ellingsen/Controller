# Brukerveiledning: Power BI Importering og Datamodellering (`powerbi_setup_guide.md`)

Denne veiledningen forklarer hvordan du importerer de auto-genererte Parquet- og CSV-filene fra `data/staging/parquet/` inn i **Power BI Desktop**, setter opp stjerneskjemaet (Star Schema) og bygger de anbefalte rapportsidene.

---

## 1. Importere Parquet-filer i Power BI Desktop

1. Åpne **Power BI Desktop**.
2. Velg **Hent data (Get Data)** -> **Mer... (More...)** -> Velg **Parquet**.
3. Naviger til prosjektmappen: `data/staging/parquet/`.
4. Importer følgende 5 tabeller:
   * `Fact_EVM_Snapshots.parquet`
   * `Fact_UBW_Audit.parquet`
   * `Fact_Travel_Audit.parquet`
   * `Dim_Project.parquet`
   * `Dim_Date.parquet`

---

## 2. Etablere Stjerneskjema (Relasjoner)

Gå til **Model View** i Power BI og opprett følgende 1:N-relasjoner (Single direction cross-filtering):

```plaintext
Dim_Project[project_id]  1 ────► N  Fact_EVM_Snapshots[project_id]
Dim_Date[ReportingPeriod] 1 ────► N  Fact_EVM_Snapshots[reporting_period]
Dim_Date[Date]            1 ────► N  Fact_Travel_Audit[Dato]
Dim_Project[project_id]  1 ────► N  Fact_UBW_Audit[prosjekt]
```

---

## 3. Nyttige DAX-Mål (DAX Measure Library)

Opprett en egen **Measure Table** (`_Measures`) i Power BI og lim inn følgende DAX-formler:

### Dynamic EAC Switcher
```dax
EAC_Dynamic = 
VAR SelectedModel = SELECTEDVALUE('Param_EAC_Model'[ModelName], "Weighted 80/20")
RETURN
    SWITCH(
        SelectedModel,
        "Typical CPI", SUM(Fact_EVM_Snapshots[eac_typical_cpi]),
        "Composite (CPIxSPI)", SUM(Fact_EVM_Snapshots[eac_cpi_spi]),
        "Weighted 80/20", SUM(Fact_EVM_Snapshots[eac_weighted_80_20]),
        SUM(Fact_EVM_Snapshots[eac_weighted_80_20])
    )
```

### Cost & Schedule Variances
```dax
Total_CV_NOK = SUM(Fact_EVM_Snapshots[cv])
Total_SV_NOK = SUM(Fact_EVM_Snapshots[sv])
Total_VAC_NOK = SUM(Fact_EVM_Snapshots[vac])

Critical_Projects_Count = 
CALCULATE(
    COUNTROWS(Fact_EVM_Snapshots),
    Fact_EVM_Snapshots[status] = "CRITICAL"
)
```

### F-05-20 Reserve Gauge
```dax
Operating_Reserve_Pct = 
DIVIDE(
    SUM(Fact_UBW_Audit[akkumulert_avsetning_nok]),
    SUM(Fact_UBW_Audit[rammebevilgning_nok])
)
```

---

## 4. Layout for Rapport-sider

* **Side 1: Executive Portfolio Overview**
  * Top KPI Cards: Dynamic EAC, Total VAC at Risk, Reserve Pct (6.0%).
  * Scatterplot Chart: X-Axis = SPI, Y-Axis = CPI, Bubbles = Projects (viser risikokvadrant).
* **Side 2: EVM Project S-Curve & Deep Dive**
  * Line Chart: Time-Series trend for PV, EV og AC per reporting_period.
  * Clustered Bar Chart: Sammenligning av BAC vs EAC (CPI) vs EAC (80/20).
* **Side 3: Compliance & Audit Center**
  * Matrix Visual: Avvik per BDM og avvikstype.
  * Table Visual: Enkelttransaksjoner med flagg og beløp.
