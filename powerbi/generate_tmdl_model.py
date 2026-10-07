"""
Generates the complete Tabular Model Definition Language (TMDL) files
for 'powerbi/Controller project.SemanticModel' conforming to Microsoft Fabric / Power BI Desktop PBIP standards.
"""

import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SEMANTIC_MODEL_DIR = BASE_DIR / "powerbi" / "Controller project.SemanticModel"
DEF_DIR = SEMANTIC_MODEL_DIR / "definition"
TABLES_DIR = DEF_DIR / "tables"

def uid():
    return str(uuid.uuid4())

def generate_dim_project():
    content = f"""table Dim_Project
\tlineageTag: {uid()}

\tcolumn project_id
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: project_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn project_name
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: project_name

\t\tannotation SummarizationSetBy = Automatic

\tcolumn bac
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: bac

\t\tannotation SummarizationSetBy = Automatic

\tcolumn pv
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: pv

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ev
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: ev

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ac
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: ac

\t\tannotation SummarizationSetBy = Automatic

\tcolumn status
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: status

\t\tannotation SummarizationSetBy = Automatic

\tpartition Dim_Project-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Parquet.Document(File.Contents("C:\\Users\\frank\\Desktop\\UIA-Controller\\data\\staging\\parquet\\Dim_Project.parquet")),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{
\t\t\t\t        {{"project_id", type text}},
\t\t\t\t        {{"project_name", type text}},
\t\t\t\t        {{"bac", type number}},
\t\t\t\t        {{"pv", type number}},
\t\t\t\t        {{"ev", type number}},
\t\t\t\t        {{"ac", type number}},
\t\t\t\t        {{"status", type text}}
\t\t\t\t    }})
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    return content

def generate_dim_date():
    content = f"""table Dim_Date
\tlineageTag: {uid()}

\tcolumn Date
\t\tdataType: dateTime
\t\tformatString: yyyy-MM-dd
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Date

\t\tannotation SummarizationSetBy = Automatic
\t\tannotation UnderlyingDateTimeDataType = Date

\tcolumn Year
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Year

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Month
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Month

\t\tannotation SummarizationSetBy = Automatic

\tcolumn MonthName
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: MonthName
\t\tsortByColumn: Month

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ReportingPeriod
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ReportingPeriod

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Quarter
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Quarter

\t\tannotation SummarizationSetBy = Automatic

\tpartition Dim_Date-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Parquet.Document(File.Contents("C:\\Users\\frank\\Desktop\\UIA-Controller\\data\\staging\\parquet\\Dim_Date.parquet")),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{
\t\t\t\t        {{"Date", type datetime}},
\t\t\t\t        {{"Year", Int64.Type}},
\t\t\t\t        {{"Month", Int64.Type}},
\t\t\t\t        {{"MonthName", type text}},
\t\t\t\t        {{"ReportingPeriod", type text}},
\t\t\t\t        {{"Quarter", Int64.Type}}
\t\t\t\t    }})
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    return content

def generate_dim_model_parameter():
    content = f"""table Dim_Model_Parameter
\tlineageTag: {uid()}

\tcolumn ModelCode
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ModelCode

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ModelName
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ModelName

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Description
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Description

\t\tannotation SummarizationSetBy = Automatic

\tpartition Dim_Model_Parameter-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    ModelTable = #table(
\t\t\t\t        type table [ModelCode = text, ModelName = text, Description = text],
\t\t\t\t        {{
\t\t\t\t            {{"CPI", "Typisk CPI Modell", "BAC / CPI — Forutsetter at historisk kostnadseffektivitet fortsetter"}},
\t\t\t\t            {{"COMPOSITE", "Sammensatt CPI x SPI Modell", "AC + (BAC - EV)/(CPI*SPI) — Tar hensyn til fremdriftsavvik"}},
\t\t\t\t            {{"WEIGHTED", "Vektet 80/20 Modell", "AC + (BAC - EV)/(0.8 CPI + 0.2 SPI) — Vekter kostnad 80% og fremdrift 20%"}}
\t\t\t\t        }}
\t\t\t\t    )
\t\t\t\tin
\t\t\t\t    ModelTable
"""
    return content

def generate_fact_evm_snapshots():
    content = f"""table Fact_EVM_Snapshots
\tlineageTag: {uid()}

\tcolumn reporting_period
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: reporting_period

\t\tannotation SummarizationSetBy = Automatic

\tcolumn snapshot_timestamp
\t\tdataType: dateTime
\t\tformatString: yyyy-MM-dd HH:mm:ss
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: snapshot_timestamp

\t\tannotation SummarizationSetBy = Automatic

\tcolumn project_id
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: project_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn bac
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: bac

\t\tannotation SummarizationSetBy = Automatic

\tcolumn pv
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: pv

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ev
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: ev

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ac
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: ac

\t\tannotation SummarizationSetBy = Automatic

\tcolumn cpi
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: {uid()}
\t\tsummarizeBy: average
\t\tsourceColumn: cpi

\t\tannotation SummarizationSetBy = Automatic

\tcolumn spi
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: {uid()}
\t\tsummarizeBy: average
\t\tsourceColumn: spi

\t\tannotation SummarizationSetBy = Automatic

\tcolumn eac_cpi
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: eac_cpi

\t\tannotation SummarizationSetBy = Automatic

\tcolumn eac_composite
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: eac_composite

\t\tannotation SummarizationSetBy = Automatic

\tcolumn eac_weighted
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: eac_weighted

\t\tannotation SummarizationSetBy = Automatic

\tcolumn vac
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: vac

\t\tannotation SummarizationSetBy = Automatic

\tcolumn tcpi
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: {uid()}
\t\tsummarizeBy: average
\t\tsourceColumn: tcpi

\t\tannotation SummarizationSetBy = Automatic

\tcolumn status
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: status

\t\tannotation SummarizationSetBy = Automatic

\tpartition Fact_EVM_Snapshots-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Parquet.Document(File.Contents("C:\\Users\\frank\\Desktop\\UIA-Controller\\data\\staging\\parquet\\Fact_EVM_Snapshots.parquet")),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{
\t\t\t\t        {{"reporting_period", type text}},
\t\t\t\t        {{"snapshot_timestamp", type datetime}},
\t\t\t\t        {{"project_id", type text}},
\t\t\t\t        {{"bac", type number}},
\t\t\t\t        {{"pv", type number}},
\t\t\t\t        {{"ev", type number}},
\t\t\t\t        {{"ac", type number}},
\t\t\t\t        {{"cpi", type number}},
\t\t\t\t        {{"spi", type number}},
\t\t\t\t        {{"eac_cpi", type number}},
\t\t\t\t        {{"eac_composite", type number}},
\t\t\t\t        {{"eac_weighted", type number}},
\t\t\t\t        {{"vac", type number}},
\t\t\t\t        {{"tcpi", type number}},
\t\t\t\t        {{"status", type text}}
\t\t\t\t    }})
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    return content

def generate_fact_ubw_audit():
    content = f"""table Fact_UBW_Audit
\tlineageTag: {uid()}

\tcolumn transaksjon_id
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: transaksjon_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn konto
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: konto

\t\tannotation SummarizationSetBy = Automatic

\tcolumn beskrivelse
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: beskrivelse

\t\tannotation SummarizationSetBy = Automatic

\tcolumn belop_nok
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: belop_nok

\t\tannotation SummarizationSetBy = Automatic

\tcolumn bdm_id
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: bdm_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn attestant_id
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: attestant_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn kvittering_vedlagt
\t\tdataType: int64
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: kvittering_vedlagt

\t\tannotation SummarizationSetBy = Automatic

\tcolumn formaal
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: formaal

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Kontrollflagg
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Kontrollflagg

\t\tannotation SummarizationSetBy = Automatic

\tpartition Fact_UBW_Audit-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Parquet.Document(File.Contents("C:\\Users\\frank\\Desktop\\UIA-Controller\\data\\staging\\parquet\\Fact_UBW_Audit.parquet")),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{
\t\t\t\t        {{"transaksjon_id", type text}},
\t\t\t\t        {{"konto", type text}},
\t\t\t\t        {{"beskrivelse", type text}},
\t\t\t\t        {{"belop_nok", type number}},
\t\t\t\t        {{"bdm_id", type text}},
\t\t\t\t        {{"attestant_id", type text}},
\t\t\t\t        {{"kvittering_vedlagt", Int64.Type}},
\t\t\t\t        {{"formaal", type text}},
\t\t\t\t        {{"Kontrollflagg", type text}}
\t\t\t\t    }})
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    return content

def generate_fact_travel_audit():
    content = f"""table Fact_Travel_Audit
\tlineageTag: {uid()}

\tcolumn Reise_ID
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Reise_ID

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Ansatt
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Ansatt

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Dato
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Dato

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Formaal
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Formaal

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Belop_NOK
\t\tdataType: double
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Belop_NOK

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Maltid_Dekket
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Maltid_Dekket

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Fradrag_Utfort
\t\tdataType: boolean
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Fradrag_Utfort

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Km_Godtgjorelse
\t\tdataType: int64
\t\tformatString: #,##0
\t\tlineageTag: {uid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Km_Godtgjorelse

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Kvittering_Vedlagt
\t\tdataType: boolean
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Kvittering_Vedlagt

\t\tannotation SummarizationSetBy = Automatic

\tcolumn BDM_ID
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BDM_ID

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Attestant_ID
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Attestant_ID

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Km_Rute_Beskrevet
\t\tdataType: boolean
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Km_Rute_Beskrevet

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Avvik_Beskrivelse
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Avvik_Beskrivelse

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Status
\t\tdataType: string
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Status

\t\tannotation SummarizationSetBy = Automatic

\tpartition Fact_Travel_Audit-partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Parquet.Document(File.Contents("C:\\Users\\frank\\Desktop\\UIA-Controller\\data\\staging\\parquet\\Fact_Travel_Audit.parquet")),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{
\t\t\t\t        {{"Reise_ID", type text}},
\t\t\t\t        {{"Ansatt", type text}},
\t\t\t\t        {{"Dato", type text}},
\t\t\t\t        {{"Formaal", type text}},
\t\t\t\t        {{"Belop_NOK", type number}},
\t\t\t\t        {{"Maltid_Dekket", type text}},
\t\t\t\t        {{"Fradrag_Utfort", type logical}},
\t\t\t\t        {{"Km_Godtgjorelse", Int64.Type}},
\t\t\t\t        {{"Kvittering_Vedlagt", type logical}},
\t\t\t\t        {{"BDM_ID", type text}},
\t\t\t\t        {{"Attestant_ID", type text}},
\t\t\t\t        {{"Km_Rute_Beskrevet", type logical}},
\t\t\t\t        {{"Avvik_Beskrivelse", type text}},
\t\t\t\t        {{"Status", type text}}
\t\t\t\t    }})
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    return content

def generate_measures_table():
    content = f"""table _Measures
\tlineageTag: {uid()}

\tmeasure 'Total Budget' = SUM('Fact_EVM_Snapshots'[bac])
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Budget YTD' = SUM('Fact_EVM_Snapshots'[pv])
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Progress Value' = SUM('Fact_EVM_Snapshots'[ev])
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Actual YTD' = SUM('Fact_EVM_Snapshots'[ac])
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Cost Variance' = [Progress Value] - [Actual YTD]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Forecast' = DIVIDE([Total Budget], [Portfolio CPI], [Total Budget])
\t\tformatString: #,##0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'Forecast Variance' = [Total Budget] - [Forecast]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'Total BAC' = [Total Budget]
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Total PV' = [Budget YTD]
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Total EV' = [Progress Value]
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Total AC' = [Actual YTD]
\t\tformatString: #,##0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Cost Variance NOK' = [Cost Variance]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Schedule Variance NOK' = [Progress Value] - [Budget YTD]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Portfolio CPI' = DIVIDE([Total EV], [Total AC], 1.0)
\t\tformatString: 0.00
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'Portfolio SPI' = DIVIDE([Total EV], [Total PV], 1.0)
\t\tformatString: 0.00
\t\tdisplayFolder: '01 Core EVM'
\t\tlineageTag: {uid()}

\tmeasure 'EAC Typical CPI' = DIVIDE([Total BAC], [Portfolio CPI], [Total BAC])
\t\tformatString: #,##0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'EAC Composite CPI_SPI' = VAR RemainingWork = [Total BAC] - [Total EV] VAR CompositeIndex = [Portfolio CPI] * [Portfolio SPI] RETURN IF(CompositeIndex > 0, [Total AC] + DIVIDE(RemainingWork, CompositeIndex, RemainingWork), [Total BAC])
\t\tformatString: #,##0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'EAC Weighted 80_20' = VAR RemainingWork = [Total BAC] - [Total EV] VAR WeightedIndex = 0.8 * [Portfolio CPI] + 0.2 * [Portfolio SPI] RETURN IF(WeightedIndex > 0, [Total AC] + DIVIDE(RemainingWork, WeightedIndex, RemainingWork), [Total BAC])
\t\tformatString: #,##0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'EAC Selected Model' = VAR SelectedModel = SELECTEDVALUE('Dim_Model_Parameter'[ModelCode], "CPI") RETURN SWITCH(SelectedModel, "CPI", [EAC Typical CPI], "COMPOSITE", [EAC Composite CPI_SPI], "WEIGHTED", [EAC Weighted 80_20], [EAC Typical CPI])
\t\tformatString: #,##0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'VAC Selected Model' = [Total BAC] - [EAC Selected Model]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '02 EAC Forecasting'
\t\tlineageTag: {uid()}

\tmeasure 'TCPI Target BAC' = VAR RemainingWork = [Total BAC] - [Total EV] VAR RemainingFund = [Total BAC] - [Total AC] RETURN IF(RemainingFund > 0, DIVIDE(RemainingWork, RemainingFund, 9.99), 9.99)
\t\tformatString: 0.00
\t\tdisplayFolder: '03 TCPI & Risk'
\t\tlineageTag: {uid()}

\tmeasure 'Project Risk Status' = VAR CurrentCPI = [Portfolio CPI] VAR CurrentSPI = [Portfolio SPI] VAR CurrentVAC = [VAC Selected Model] RETURN SWITCH(TRUE(), CurrentCPI < 0.85 || CurrentSPI < 0.85 || CurrentVAC < -1000000, "CRITICAL", CurrentCPI < 0.95 || CurrentSPI < 0.95 || CurrentVAC < -250000, "WARNING", "ON TRACK")
\t\tdisplayFolder: '03 TCPI & Risk'
\t\tlineageTag: {uid()}

\tmeasure 'Status Color Hex' = SWITCH([Project Risk Status], "CRITICAL", "#ef4444", "WARNING", "#f59e0b", "ON TRACK", "#34d399", "#94a3b8")
\t\tdisplayFolder: '03 TCPI & Risk'
\t\tlineageTag: {uid()}

\tmeasure 'Statlig Rammebevilgning NOK' = 1200000000
\t\tformatString: #,##0
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'Reell Driftsavsetning NOK' = 72000000
\t\tformatString: #,##0
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'Reserve Share Pct' = DIVIDE([Reell Driftsavsetning NOK], [Statlig Rammebevilgning NOK], 0)
\t\tformatString: 0.0%
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'Reserve Cap 5% Limit NOK' = [Statlig Rammebevilgning NOK] * 0.05
\t\tformatString: #,##0
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'Reserve Cap Excess NOK' = MAX(0, [Reell Driftsavsetning NOK] - [Reserve Cap 5% Limit NOK])
\t\tformatString: #,##0
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'F-05-20 Status Flag' = IF([Reserve Cap Excess NOK] > 0, "DISPENSASJON PÅKREVD", "INNENFOR GRENSE")
\t\tdisplayFolder: '04 F-05-20 Reserve Cap'
\t\tlineageTag: {uid()}

\tmeasure 'Total Scanned Claims Count' = COUNTROWS('Fact_Travel_Audit')
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Flagged Claims Count' = CALCULATE(COUNTROWS('Fact_Travel_Audit'), 'Fact_Travel_Audit'[Status] = "FLAGGED")
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Total Flagged Amount NOK' = CALCULATE(SUM('Fact_Travel_Audit'[Belop_NOK]), 'Fact_Travel_Audit'[Status] = "FLAGGED")
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Self-Approval Breach Amount NOK' = CALCULATE(SUM('Fact_Travel_Audit'[Belop_NOK]), SEARCH("Egengodkjenning", 'Fact_Travel_Audit'[Avvik_Beskrivelse], 1, 0) > 0)
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Total UBW Transactions Count' = COUNTROWS('Fact_UBW_Audit')
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Total UBW Amount NOK' = SUM('Fact_UBW_Audit'[belop_nok])
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'Flagged UBW Transactions Count' = CALCULATE(COUNTROWS('Fact_UBW_Audit'), 'Fact_UBW_Audit'[Kontrollflagg] <> "OK")
\t\tformatString: #,##0
\t\tdisplayFolder: '05 Compliance & Audit'
\t\tlineageTag: {uid()}

\tmeasure 'SCurve Cumulative PV' = [Total PV]
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'SCurve Cumulative AC' = [Total AC]
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'SCurve Cumulative EAC' = [EAC Selected Model]
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'SCurve Cost Variance Line' = [SCurve Cumulative PV] - [SCurve Cumulative AC]
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Statlig Ramme Inntekt NOK' = [Total BAC] * 0.78
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'BOA Ekstern Forskning NOK' = [Total BAC] * 0.14
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Oppdragsaktivitet Inntekt NOK' = [Total BAC] * 0.05
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Oevrige Inntekter NOK' = [Total BAC] * 0.03
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Loenn & Sosiale Kostnader NOK' = [Total AC] * 0.64
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Andre Driftskostnader NOK' = [Total AC] * 0.23
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Husleie & Eiendom NOK' = [Total AC] * 0.08
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Avskrivninger & Investeringer NOK' = [Total AC] * 0.05
\t\tformatString: #,##0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Loennsinnsparing Vakanser NOK' = [Cost Variance NOK] * 0.55
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Driftsinnsparing Konsulent Reise NOK' = [Cost Variance NOK] * 0.30
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Eiendomsinnsparing Enoek NOK' = [Cost Variance NOK] * 0.10
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tmeasure 'Investeringsinnsparing Periodisering NOK' = [Cost Variance NOK] * 0.05
\t\tformatString: +#,##0;-#,##0;0
\t\tdisplayFolder: '06 Visual Analytics'
\t\tlineageTag: {uid()}

\tcolumn _Placeholder
\t\tdataType: string
\t\tisHidden
\t\tlineageTag: {uid()}
\t\tsummarizeBy: none
\t\tsourceColumn: _Placeholder

\t\tannotation SummarizationSetBy = Automatic

\tpartition _Measures-partition = m
\t\tmode: import
\t\tsource = let Source = #table({{"_Placeholder"}}, {{{{1}}}}) in Source
"""
    return content

def generate_relationships():
    content = """relationship Fact_EVM_Snapshots_Dim_Project
\tfromColumn: Fact_EVM_Snapshots.project_id
\ttoColumn: Dim_Project.project_id

relationship Fact_EVM_Snapshots_Dim_Date
\tfromCardinality: many
\ttoCardinality: many
\tfromColumn: Fact_EVM_Snapshots.reporting_period
\ttoColumn: Dim_Date.ReportingPeriod
\tcrossFilteringBehavior: bothDirections
"""
    return content

def generate_model_tmdl():
    content = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tvalueFilterBehavior: independent
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation PBI_QueryOrder = ["Dim_Project","Dim_Date","Dim_Model_Parameter","Fact_EVM_Snapshots","Fact_UBW_Audit","Fact_Travel_Audit","_Measures"]

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBI_ProTooling = ["DevMode"]

ref table Dim_Project
ref table Dim_Date
ref table Dim_Model_Parameter
ref table Fact_EVM_Snapshots
ref table Fact_UBW_Audit
ref table Fact_Travel_Audit
ref table _Measures

ref cultureInfo en-US
"""
    return content

def main():
    print("=== Generating TMDL Semantic Model for Power BI PBIP ===")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Clean out any leftover or orphaned TMDL table files (e.g. LocalDateTable_*)
    for old_file in TABLES_DIR.glob("*.tmdl"):
        try:
            old_file.unlink()
        except Exception as e:
            print(f"  - Warning removing {old_file}: {e}")
    
    tables = {
        "Dim_Project.tmdl": generate_dim_project(),
        "Dim_Date.tmdl": generate_dim_date(),
        "Dim_Model_Parameter.tmdl": generate_dim_model_parameter(),
        "Fact_EVM_Snapshots.tmdl": generate_fact_evm_snapshots(),
        "Fact_UBW_Audit.tmdl": generate_fact_ubw_audit(),
        "Fact_Travel_Audit.tmdl": generate_fact_travel_audit(),
        "_Measures.tmdl": generate_measures_table(),
    }
    
    for filename, content in tables.items():
        filepath = TABLES_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  + Created table: {filepath.relative_to(BASE_DIR)}")
        
    rel_path = DEF_DIR / "relationships.tmdl"
    with open(rel_path, "w", encoding="utf-8") as f:
        f.write(generate_relationships())
    print(f"  + Created relationships: {rel_path.relative_to(BASE_DIR)}")
    
    model_path = DEF_DIR / "model.tmdl"
    with open(model_path, "w", encoding="utf-8") as f:
        f.write(generate_model_tmdl())
    print(f"  + Updated model: {model_path.relative_to(BASE_DIR)}")
    
    print("=== TMDL Generation Complete! ===")

if __name__ == "__main__":
    main()
