// ===============================================================================
// Power Query (M) Load & Transformation Scripts for UiA Controller App
// Ingests Parquet & CSV files from data/staging/parquet/ into Power BI Desktop
// ===============================================================================

// -------------------------------------------------------------------------------
// 1. Fact_EVM_Snapshots Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\md_files\uia-controller-app-v12\uia-controller-app\data\staging\parquet\",
    SourceFile = SourceFolder & "Fact_EVM_Snapshots.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"reporting_period", type text},
        {"snapshot_timestamp", type datetime},
        {"project_id", type text},
        {"bac", type number},
        {"pv", type number},
        {"ev", type number},
        {"ac", type number},
        {"cpi", type number},
        {"spi", type number},
        {"eac_cpi", type number},
        {"eac_composite", type number},
        {"eac_weighted", type number},
        {"vac", type number},
        {"tcpi", type number},
        {"status", type text}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 2. Dim_Project Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\md_files\uia-controller-app-v12\uia-controller-app\data\staging\parquet\",
    SourceFile = SourceFolder & "Dim_Project.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"project_id", type text},
        {"project_name", type text},
        {"department", type text},
        {"pm_name", type text},
        {"bac", type number}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 3. Fact_Travel_Audit Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\md_files\uia-controller-app-v12\uia-controller-app\data\staging\parquet\",
    SourceFile = SourceFolder & "Fact_Travel_Audit.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"Reise_ID", type text},
        {"Ansatt_Navn", type text},
        {"Enhet", type text},
        {"Belop_NOK", type number},
        {"Avvik_Beskrivelse", type text},
        {"Status", type text}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 4. Dim_Date Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\md_files\uia-controller-app-v12\uia-controller-app\data\staging\parquet\",
    SourceFile = SourceFolder & "Dim_Date.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"Date", type date},
        {"Year", Int64.Type},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"ReportingPeriod", type text},
        {"Quarter", Int64.Type}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 5. Dim_Model_Parameter Query (Disconnected Slicer Table)
// -------------------------------------------------------------------------------
let
    ModelTable = #table(
        type table [ModelCode = text, ModelName = text, Description = text],
        {
            {"CPI", "Typisk CPI Modell", "BAC / CPI — Forutsetter at historisk kostnadseffektivitet fortsetter"},
            {"COMPOSITE", "Sammensatt CPI x SPI Modell", "AC + (BAC - EV)/(CPI*SPI) — Tar hensyn til fremdriftsavvik"},
            {"WEIGHTED", "Vektet 80/20 Modell", "AC + (BAC - EV)/(0.8 CPI + 0.2 SPI) — Vekter kostnad 80% og fremdrift 20%"}
        }
    )
in
    ModelTable
