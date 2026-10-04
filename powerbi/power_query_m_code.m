// ===============================================================================
// Power Query (M) Load & Transformation Scripts for UiA Controller App
// Ingests Parquet files from data/staging/parquet/ into Power BI Desktop
// Base Path: C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\
// ===============================================================================

// -------------------------------------------------------------------------------
// 1. Fact_EVM_Snapshots Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\",
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
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\",
    SourceFile = SourceFolder & "Dim_Project.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"project_id", type text},
        {"project_name", type text},
        {"bac", type number},
        {"pv", type number},
        {"ev", type number},
        {"ac", type number},
        {"status", type text}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 3. Fact_UBW_Audit Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\",
    SourceFile = SourceFolder & "Fact_UBW_Audit.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"transaksjon_id", type text},
        {"konto", type text},
        {"beskrivelse", type text},
        {"belop_nok", type number},
        {"bdm_id", type text},
        {"attestant_id", type text},
        {"kvittering_vedlagt", Int64.Type},
        {"formaal", type text},
        {"Kontrollflagg", type text}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 4. Fact_Travel_Audit Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\",
    SourceFile = SourceFolder & "Fact_Travel_Audit.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"Reise_ID", type text},
        {"Ansatt", type text},
        {"Dato", type text},
        {"Formaal", type text},
        {"Belop_NOK", type number},
        {"Maltid_Dekket", type text},
        {"Fradrag_Utfort", type logical},
        {"Km_Godtgjorelse", Int64.Type},
        {"Kvittering_Vedlagt", type logical},
        {"BDM_ID", type text},
        {"Attestant_ID", type text},
        {"Km_Rute_Beskrevet", type logical},
        {"Avvik_Beskrivelse", type text},
        {"Status", type text}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 5. Dim_Date Query
// -------------------------------------------------------------------------------
let
    SourceFolder = "C:\Users\frank\Desktop\UIA-Controller\data\staging\parquet\",
    SourceFile = SourceFolder & "Dim_Date.parquet",
    Source = Parquet.Document(File.Contents(SourceFile)),
    #"Changed Type" = Table.TransformColumnTypes(Source,{
        {"Date", type datetime},
        {"Year", Int64.Type},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"ReportingPeriod", type text},
        {"Quarter", Int64.Type}
    })
in
    #"Changed Type"

// -------------------------------------------------------------------------------
// 6. Dim_Model_Parameter Query (Disconnected Slicer Table)
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

// -------------------------------------------------------------------------------
// 7. _Measures Query (Empty Container Table)
// -------------------------------------------------------------------------------
let
    Source = #table({"_Placeholder"}, {{1}})
in
    Source
