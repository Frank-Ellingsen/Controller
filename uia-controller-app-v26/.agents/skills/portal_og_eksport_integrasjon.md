---
name: portal-og-eksport-integrasjon
description: Retningslinjer for vedlikehold av index.html webgrensesnitt, Excel-eksportering (.xlsx) av kontoplan og ordliste, samt datakildeintegrasjon for UiA Controlling.
---

### Standarder for Webportal og Eksportintegrasjon:

1. **Grensesnittarkitektur ():**
   - Single Page Application (SPA) med 6 operative faner:
     1.  (Statlig tidslinje, milepæler, neste års rammebygger).
     2.  (UBW-hovedbok, DFØ-reiseregninger, avviksflagg).
     3.  (CPI, SPI, EAC, TCPI, glidebrytere for EOY balanse).
     4.  (SQLite projects.db, DuckDB snapshots, Parquet Star Schema, Power BI dashboard).
     5.  (F-05-20, UiA Fullmaktsmatrise, Kontoklasser 1-8 med Excel-eksport).
     6.  (Søkbar finansiell terminologi med Excel-eksport).

2. **Direkte Excel-eksportering (.xlsx):**
   - Webportalen skal tilby direkte klient-side nedlasting av tabeller til -format via SheetJS / HTML-to-XLSX exporter.
   - Både **Statens Kontoplan 2026** og **Begrepskatalog & Ordliste** skal ha egne dedikerte eksporteringsknapper:
     -  -> Genererer 
     -  -> Genererer 

3. **Synkronisering mot Datakildelaget:**
   - Webportalen viser sanntidsstatus fra:
     -  (SQLite masterdata)
     -  (DuckDB tidsrekker)
     -  (Power BI Star Schema)
     -  &  (Prognose- og tiltaksmotorer)
