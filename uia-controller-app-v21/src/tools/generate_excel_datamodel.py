"""
UiA Controller App — Comprehensive Enterprise Excel Data Model Generator (v12)
Generates an executive-grade, Edward Tufte Data-Ink compliant Excel Data Model (.xlsx)
combining Star Schema dimensional tables, multi-model EVM forecasting, S-curve time-series,
F-05-20 statutory reserve cap simulation, and DFØ/UBW compliance audit mechanisms.
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import duckdb
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import LineChart, Reference

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_EXCEL_DIR = BASE_DIR / "excel"
OUTPUT_REPORTS_DIR = BASE_DIR / "data" / "reports"
EXCEL_FILE_PRIMARY = OUTPUT_EXCEL_DIR / "UiA_Controller_DataModel_2026.xlsx"
EXCEL_FILE_SECONDARY = OUTPUT_REPORTS_DIR / "UiA_Controller_DataModel_2026.xlsx"

os.makedirs(OUTPUT_EXCEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_REPORTS_DIR, exist_ok=True)

def create_excel_datamodel():
    print("=== START: Bygger UiA Enterprise Excel Data Model 2026 ===")
    wb = openpyxl.Workbook()
    
    # -------------------------------------------------------------------------
    # TYPOGRAPHY & PALETTE (Edward Tufte Data-Ink Compliant)
    # -------------------------------------------------------------------------
    font_family = "Segoe UI"
    
    title_font = Font(name=font_family, size=16, bold=True, color="0F172A")
    subtitle_font = Font(name=font_family, size=10, italic=True, color="475569")
    section_font = Font(name=font_family, size=12, bold=True, color="0F172A")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    bold_font = Font(name=font_family, size=10, bold=True, color="0F172A")
    regular_font = Font(name=font_family, size=10, color="1E293B")
    mono_font = Font(name="Consolas", size=9, color="0F172A")
    link_font = Font(name=font_family, size=10, underline="single", color="0284C7")
    
    # Highlight & Status Fonts
    critical_font = Font(name=font_family, size=10, bold=True, color="991B1B")
    critical_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    
    warning_font = Font(name=font_family, size=10, bold=True, color="92400E")
    warning_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    
    ontrack_font = Font(name=font_family, size=10, bold=True, color="065F46")
    ontrack_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    accent_header_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    total_row_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    input_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid") # Light Blue for User Inputs
    
    # Borders (Subtle horizontal rules, zero vertical gridlines)
    thin_bottom = Border(bottom=Side(style='thin', color='CBD5E1'))
    double_bottom = Border(top=Side(style='thin', color='CBD5E1'), bottom=Side(style='double', color='1E293B'))
    card_border = Border(
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1'),
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1')
    )
    
    # Number Formats
    fmt_currency = '#,##0 "NOK"'
    fmt_decimal = '0.00'
    fmt_percent = '0.0%'
    fmt_integer = '#,##0'

    # -------------------------------------------------------------------------
    # TAB 1: 00_Navigasjon_Modellarkitektur
    # -------------------------------------------------------------------------
    ws0 = wb.active
    ws0.title = "00_Navigasjon_Arkitektur"
    ws0.views.sheetView[0].showGridLines = True
    
    ws0["A1"] = "UiA Handelshøyskolen — Enterprise Financial Controlling & EVM Data Model"
    ws0["A1"].font = title_font
    ws0["A2"] = "Regnskapsår: 2026 | Modellversjon: v12 Canonical | Ansvarlig: Frank Ellingsen (Lead Project Controller)"
    ws0["A2"].font = subtitle_font
    
    # Metadata Box
    ws0["A4"] = "System- & Integrasjonsparametere"
    ws0["A4"].font = section_font
    
    meta_headers = ["Parameter / Konfigurasjon", "Verdi / Status", "Teknisk Kilde", "Beskrivelse"]
    for idx, text in enumerate(meta_headers, 1):
        c = ws0.cell(row=5, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    meta_data = [
        ("Datamodell Arkitektur", "Stjerneskjema (Star Schema 1:N / M:N)", "Parquet / DuckDB / SQLite", "Relasjonell modell for dimensjoner og faktatabeller"),
        ("Transaksjonsdatabase", "SQLite (projects.db)", "ubw_transactions & evm_projects", "Operasjonell registrering av prosjektdata og hovedboksposter"),
        ("Analytisk Tidsrekke-motor", "DuckDB (analytics_snapshots.duckdb)", "evm_snapshots", "Tidsstempling og historiske snapshots for prosjektporteføljen"),
        ("Regelverksstandarder", "Statens Kontoplan (R-102) & KD F-05-20", "SRS / DFØ Veiledere", "5,0 % overføringstak og 4-øyne attestasjonskrav"),
        ("Basis Rammebevilgning (Kap. 260)", 1200000000, "Statsbudsjettet Prop. 1 S", "Årlig tildelt grunnbevilgning for universitetet"),
        ("Statlig Lønns- og Prisvekst (Deflator)", 0.039, "Finansdepartementet RNB", "Budsjettmessig justeringsfaktor for 2026"),
        ("Power BI Integrasjon", "Controller project.pbip (TMDL 1606)", "Power BI Desktop DevMode", "Direkte synkronisering med Parquet staging filer")
    ]
    
    for r_idx, (p_name, val, src, desc) in enumerate(meta_data, 6):
        c1 = ws0.cell(row=r_idx, column=1, value=p_name)
        c2 = ws0.cell(row=r_idx, column=2, value=val)
        c3 = ws0.cell(row=r_idx, column=3, value=src)
        c4 = ws0.cell(row=r_idx, column=4, value=desc)
        c1.font = bold_font
        c2.font = bold_font if isinstance(val, (int, float)) else regular_font
        c3.font = mono_font
        c4.font = regular_font
        if isinstance(val, int) and val > 1000:
            c2.number_format = fmt_currency
        elif isinstance(val, float) and val < 1.0:
            c2.number_format = fmt_percent
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom
            
    # Sheet Navigation Links
    nav_start_r = 15
    ws0.cell(row=nav_start_r, column=1, value="Arbeidsbokens Innholdsfortegnelse & Hurtignavigasjon").font = section_font
    
    nav_headers = ["Fane Navn", "Område", "Innhold & Funksjonalitet", "Hyperlenke"]
    for idx, text in enumerate(nav_headers, 1):
        c = ws0.cell(row=nav_start_r+1, column=idx, value=text)
        c.font = header_font
        c.fill = accent_header_fill
        
    sheets_info = [
        ("01_Executive_Cockpit", "Ledelse", "Hoveddashboard med KPI-kort, dynamisk EAC-velger og tiltaksplan", "#'01_Executive_Cockpit'!A1"),
        ("02_EVM_Prosjektkontroll", "Prosjektstyring", "Prosjekt-for-prosjekt EVM analyse med CPI, SPI, EAC-modeller og TCPI", "#'02_EVM_Prosjektkontroll'!A1"),
        ("03_S_Kurve_Tidsserie", "Tidsserier", "Månedlig kumulativ PV/EV/AC historikk og visuell S-kurve for 2026", "#'03_S_Kurve_Tidsserie'!A1"),
        ("04_F05_20_Avsetningskalkyle", "Statlig Regelverk", "5 % driftsavsetningstak, 12M NOK overskridelse og interaktiv tiltakssimulator", "#'04_F05_20_Avsetningskalkyle'!A1"),
        ("05_Compliance_Internkontroll", "Revisjon", "DFØ reiseregningskontroll og UBW hovedboksrevisjon med sperreflagg", "#'05_Compliance_Internkontroll'!A1"),
        ("Dim_Project", "Datamodell", "Prosjekt-stamdata og autoriserte budsjettrammer (tbl_Dim_Project)", "#'Dim_Project'!A1"),
        ("Dim_Date", "Datamodell", "Dato- og periodekalender for 2026 (tbl_Dim_Date)", "#'Dim_Date'!A1"),
        ("Dim_Model_Parameter", "Datamodell", "Parametertabell for EAC-framskrivingsmodeller (tbl_Dim_Parameters)", "#'Dim_Model_Parameter'!A1"),
        ("Fact_EVM_Snapshots", "Datamodell", "Historiske EVM månedssnapshots fra DuckDB (tbl_Fact_EVM)", "#'Fact_EVM_Snapshots'!A1"),
        ("Fact_UBW_Audit", "Datamodell", "UBW hovedboksposteringer med automatiserte kontrollflagg (tbl_Fact_UBW)", "#'Fact_UBW_Audit'!A1"),
        ("Fact_Travel_Audit", "Datamodell", "15 DFØ reiseregninger med atestasjons- og måltidskontroll (tbl_Fact_Travel)", "#'Fact_Travel_Audit'!A1"),
        ("Fact_Project_BOA", "Datamodell", "Bidrags- og oppdragsforskning (NFR, EU, Oppdrag) med overhead (tbl_Fact_BOA)", "#'Fact_Project_BOA'!A1"),
        ("Dim_Kontoplan_2026", "Datamodell", "Statens Standard Kontoplan (R-102) med SRS-koblinger (tbl_Dim_Kontoplan)", "#'Dim_Kontoplan_2026'!A1")
    ]
    
    for idx, (s_name, s_area, s_desc, s_link) in enumerate(sheets_info, nav_start_r+2):
        c1 = ws0.cell(row=idx, column=1, value=s_name)
        c2 = ws0.cell(row=idx, column=2, value=s_area)
        c3 = ws0.cell(row=idx, column=3, value=s_desc)
        c4 = ws0.cell(row=idx, column=4, value=f'=HYPERLINK("{s_link}", "Gå til fane ->")')
        c1.font = bold_font
        c2.font = regular_font
        c3.font = regular_font
        c4.font = link_font
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom

    # -------------------------------------------------------------------------
    # TAB 2: 01_Executive_Cockpit
    # -------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="01_Executive_Cockpit")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["A1"] = "Executive Project Controlling Cockpit"
    ws1["A1"].font = title_font
    ws1["A2"] = "Overordnet ledelsesrapport for Fakultetsdirektør og Dekan | Rapporteringsmåned: 2026-M10"
    ws1["A2"].font = subtitle_font
    
    # KPI Summary Cards Block
    ws1["A4"] = "Kritiske Styrings-KPI-er (Dynamisk aggregert fra prosjektmodellen)"
    ws1["A4"].font = section_font
    
    kpi_card_headers = ["Nøkkeltall / Dimensjon", "Verdi", "Mål / Grense", "Avvik / Status", "Formell Forklaring"]
    for idx, text in enumerate(kpi_card_headers, 1):
        c = ws1.cell(row=5, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    cockpit_kpis = [
        ("Total Portefølje BAC", "='02_EVM_Prosjektkontroll'!C14", 71700000, "I rute", "Samlet godkjent budsjettramme ved ferdigstillelse", fmt_currency, False),
        ("Påløpte Kostnader (AC)", "='02_EVM_Prosjektkontroll'!F14", 40000000, "Merforbruk", "Faktiske kostnader bokført i Unit4/UBW per M10", fmt_currency, False),
        ("Opptjent Verdi (EV)", "='02_EVM_Prosjektkontroll'!E14", "='02_EVM_Prosjektkontroll'!D14", "Fremdriftsavvik", "Fysisk fremdrift multiplisert med BAC", fmt_currency, False),
        ("Kostnadsavvik (CV NOK)", "='02_EVM_Prosjektkontroll'!G14", 0, "=IF(B9<0, \"OVERFORBRUK\", \"UNDER BUDSJETT\")", "Netto monetært kostnadsavvik (EV - AC)", fmt_currency, True),
        ("Portefølje CPI (Kostnad)", "='02_EVM_Prosjektkontroll'!I14", 1.00, "=IF(B10<0.9, \"KRITISK\", \"TILFREDSSTILLENDE\")", "Kostnadseffektivitetsindeks (EV / AC)", fmt_decimal, True),
        ("Portefølje SPI (Fremdrift)", "='02_EVM_Prosjektkontroll'!J14", 1.00, "=IF(B11<0.9, \"FORSINKET\", \"I RUTE\")", "Fremdriftsindeks (EV / PV)", fmt_decimal, True),
        ("Sluttkostnad (EAC Valgt Modell)", "='02_EVM_Prosjektkontroll'!N14", "='02_EVM_Prosjektkontroll'!C14", "Projisert Sluttkostnad", "Dynamisk prognose basert på valgt EAC-modell", fmt_currency, False),
        ("Sluttavvik (VAC Valgt Modell)", "='02_EVM_Prosjektkontroll'!O14", 0, "=IF(B13<0, \"SLUTTOVERSKRIDELSE\", \"INSPEKT\")", "Forventet avvik ved fullførelse (BAC - EAC)", fmt_currency, True),
        ("Statlig Driftsavsetning (F-05-20)", "='04_F05_20_Avsetningskalkyle'!C9", 0.05, "DISPENSASJON PÅKREVD", "6,0 % avsetning overstiger 5,0 % lovfestet tak (+12M NOK)", fmt_percent, True),
        ("DFØ Reiseregninger Flagg", "='05_Compliance_Internkontroll'!C20", 0, "7 Saker Flagget", "7 av 15 reiseregninger flagget for atestasjonsbrudd (Unit4 sperret)", fmt_currency, True)
    ]
    
    for r_idx, (kpi_name, val_f, tgt_f, stat_f, note, num_fmt, is_cond) in enumerate(cockpit_kpis, 6):
        c1 = ws1.cell(row=r_idx, column=1, value=kpi_name)
        c2 = ws1.cell(row=r_idx, column=2, value=val_f)
        c3 = ws1.cell(row=r_idx, column=3, value=tgt_f)
        c4 = ws1.cell(row=r_idx, column=4, value=stat_f)
        c5 = ws1.cell(row=r_idx, column=5, value=note)
        
        c1.font = bold_font
        c2.font = critical_font if is_cond else bold_font
        c3.font = regular_font
        c4.font = critical_font if is_cond else ontrack_font
        c5.font = regular_font
        
        c2.number_format = num_fmt
        c3.number_format = num_fmt
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        
        for c in (c1, c2, c3, c4, c5):
            c.border = thin_bottom
            if is_cond and r_idx in (9, 10, 13, 14, 15):
                c.fill = critical_fill
                
    # Model Parameter Slicer Simulator Cell in Cockpit
    ws1["A18"] = "Interaktiv Framskrivingsmodell Slicer (Endre cellen under for å oppdatere EAC-beregninger)"
    ws1["A18"].font = section_font
    
    ws1["A19"] = "Aktiv EAC Modell:"
    ws1["A19"].font = bold_font
    c_slicer = ws1["B19"]
    c_slicer.value = "COMPOSITE"  # Defaults to COMPOSITE, user can change to CPI or WEIGHTED
    c_slicer.font = Font(name=font_family, size=11, bold=True, color="0369A1")
    c_slicer.fill = input_fill
    c_slicer.alignment = Alignment(horizontal='center')
    c_slicer.border = card_border
    
    ws1["C19"] = "Valgbare verdier: 'CPI' | 'COMPOSITE' | 'WEIGHTED' (Se 'Dim_Model_Parameter' for detaljer)"
    ws1["C19"].font = subtitle_font
    
    # Priority Corrective Action Plan
    ws1["A22"] = "Strategisk Ledelses- og Tiltaksplan"
    ws1["A22"].font = section_font
    
    act_headers = ["Prio", "Styringsområde", "Identifisert Risiko / Avvik", "Besluttet Ledelsestiltak", "Ansvarlig", "Frist"]
    for idx, text in enumerate(act_headers, 1):
        c = ws1.cell(row=23, column=idx, value=text)
        c.font = header_font
        c.fill = accent_header_fill
        
    actions = [
        ("P1", "F-05-20 Avsetningskontroll", "12,0 MNOK akkumulert over 5 % taket per M10 (inndragningsfare fra KD)", "Iverksett tiltakskort T1-T4 (9M NOK) + send dispensasjonssøknad for resterende 3M NOK", "Universitetsdirektør / Dekan", "15.11.2026"),
        ("P1", "EVM Prosjekt UM-ENG-03", "Kritisk kostnads- og fremdriftsavvik (CPI 0.76, SPI 0.80, TCPI 2.14)", "Prosjekteiermøte: Kutt i konsulentomfang og reallokering av vitenskapelig personell", "Prosjektleder / Dekan", "20.10.2026"),
        ("P1", "EVM Prosjekt UM-FPV-01", "Monetært kostnadsavvik -2,1 MNOK mot planlagt fremdrift (CPI 0.91)", "Revidert innkjøpsplan for maritim lab for å fange stordriftsfordeler", "Prosjektleder / Kontorsjef", "01.11.2026"),
        ("P2", "DFØ Internkontroll", "2 tilfeller av egengodkjenning av reiser (brudd på UiA fullmaktsmatrise)", "Omruting av bilag til overordnet leder for gyldig atestasjon; sperr utbetaling i Unit4", "Regnskapssjef", "12.10.2026"),
        ("P2", "DFØ Måltidskontroll", "5 tilfeller av manglende diettfradrag (hotellfrokost/lunsj inkludert)", "Automatisk diettkorreksjon på neste lønnskjøring i henhold til statens satser", "Lønnscontroller", "15.10.2026")
    ]
    
    for idx, (prio, area, risk, action, owner, deadline) in enumerate(actions, 24):
        c1 = ws1.cell(row=idx, column=1, value=prio)
        c2 = ws1.cell(row=idx, column=2, value=area)
        c3 = ws1.cell(row=idx, column=3, value=risk)
        c4 = ws1.cell(row=idx, column=4, value=action)
        c5 = ws1.cell(row=idx, column=5, value=owner)
        c6 = ws1.cell(row=idx, column=6, value=deadline)
        
        c1.font = critical_font if prio == "P1" else warning_font
        c2.font = bold_font
        c3.font = regular_font
        c4.font = regular_font
        c5.font = bold_font
        c6.font = mono_font
        
        for c in (c1, c2, c3, c4, c5, c6):
            c.border = thin_bottom

    # -------------------------------------------------------------------------
    # TAB 3: 02_EVM_Prosjektkontroll
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="02_EVM_Prosjektkontroll")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["A1"] = "Earned Value Management (EVM) — Prosjektportefølje & Fler-Modell EAC"
    ws2["A1"].font = title_font
    ws2["A2"] = "Formelverk iht. ANSI/EIA-748 og DFØ prosjektveileder. Modellvelger styres av cellen '01_Executive_Cockpit'!B19"
    ws2["A2"].font = subtitle_font
    
    evm_headers = [
        "Prosjekt-ID", "Prosjektnavn", "Budsjett (BAC)", "Planlagt (PV)", "Opptjent (EV)", "Påløpt (AC)",
        "Kostnadsavvik (CV)", "Fremdriftsavvik (SV)", "CPI", "SPI", 
        "EAC (Typisk CPI)", "EAC (Sammensatt)", "EAC (Vektet 80/20)", "EAC (Aktiv Modell)",
        "Sluttavvik (VAC)", "Gjenstående (ETC)", "TCPI", "Risiko Status"
    ]
    
    for idx, text in enumerate(evm_headers, 1):
        c = ws2.cell(row=4, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal='center' if idx in (1, 18) else ('right' if idx >= 3 else 'left'))
        
    evm_projects = [
        ("UM-DEF-02", "Forsvarsforskning Agder (Skrogmodell)", 18500000, 12000000, 12200000, 11800000),
        ("UM-ENG-03", "Ingeniørutdanning Fornybar (Komposittlab)", 8200000, 6500000, 5200000, 6800000),
        ("UM-FPV-01", "Fotovoltaikk Solceller (Maritim Lab)", 45000000, 22500000, 21000000, 23100000),
        # BOA Projects
        ("NFR001", "NFR-AI: Kunstig intelligens i styring", 4000000, 2600000, 1680000, 1680000),
        ("NFR002", "NFR-Helse: Pasientsikkerhet i helsefag", 2800000, 1450000, 1450000, 1450000),
        ("EU001", "EU Horizon: Green Maritime Tech", 6200000, 3100000, 3100000, 3100000),
        ("EU002", "EU Horizon: Digital Governance", 4500000, 2150000, 2150000, 2150000),
        ("EVU001", "EVU Videreutdanning for kommuner", 1200000, 600000, 600000, 864000),
        ("OPPDRAG01", "Oppdragsforskning Batteriteknologi", 1800000, 900000, 890000, 890000)
    ]
    
    for r_idx, (p_id, p_name, bac, pv, ev, ac) in enumerate(evm_projects, 5):
        ws2.cell(row=r_idx, column=1, value=p_id).font = mono_font
        ws2.cell(row=r_idx, column=2, value=p_name).font = regular_font
        ws2.cell(row=r_idx, column=3, value=bac).number_format = fmt_currency
        ws2.cell(row=r_idx, column=4, value=pv).number_format = fmt_currency
        ws2.cell(row=r_idx, column=5, value=ev).number_format = fmt_currency
        ws2.cell(row=r_idx, column=6, value=ac).number_format = fmt_currency
        
        # Formulas
        ws2.cell(row=r_idx, column=7, value=f"=E{r_idx}-F{r_idx}").number_format = fmt_currency # CV = EV - AC
        ws2.cell(row=r_idx, column=8, value=f"=E{r_idx}-D{r_idx}").number_format = fmt_currency # SV = EV - PV
        
        ws2.cell(row=r_idx, column=9, value=f"=IFERROR(E{r_idx}/F{r_idx}, 1.00)").number_format = fmt_decimal # CPI
        ws2.cell(row=r_idx, column=10, value=f"=IFERROR(E{r_idx}/D{r_idx}, 1.00)").number_format = fmt_decimal # SPI
        
        ws2.cell(row=r_idx, column=11, value=f"=IFERROR(C{r_idx}/I{r_idx}, C{r_idx})").number_format = fmt_currency # EAC CPI
        ws2.cell(row=r_idx, column=12, value=f"=IFERROR(F{r_idx}+(C{r_idx}-E{r_idx})/(I{r_idx}*J{r_idx}), C{r_idx})").number_format = fmt_currency # EAC Composite
        ws2.cell(row=r_idx, column=13, value=f"=IFERROR(F{r_idx}+(C{r_idx}-E{r_idx})/(0.8*I{r_idx}+0.2*J{r_idx}), C{r_idx})").number_format = fmt_currency # EAC Weighted
        
        # Dynamic EAC based on Slicer in 01_Executive_Cockpit!B19
        ws2.cell(row=r_idx, column=14, value=f"=IF('01_Executive_Cockpit'!$B$19=\"CPI\", K{r_idx}, IF('01_Executive_Cockpit'!$B$19=\"COMPOSITE\", L{r_idx}, M{r_idx}))").number_format = fmt_currency
        
        ws2.cell(row=r_idx, column=15, value=f"=C{r_idx}-N{r_idx}").number_format = fmt_currency # VAC = BAC - EAC_Active
        ws2.cell(row=r_idx, column=16, value=f"=N{r_idx}-F{r_idx}").number_format = fmt_currency # ETC = EAC - AC
        ws2.cell(row=r_idx, column=17, value=f"=IFERROR((C{r_idx}-E{r_idx})/(C{r_idx}-F{r_idx}), 9.99)").number_format = fmt_decimal # TCPI
        
        # Risk Status formula
        ws2.cell(row=r_idx, column=18, value=f'=IF(OR(I{r_idx}<0.85, J{r_idx}<0.85, O{r_idx}<-1000000), "CRITICAL", IF(OR(I{r_idx}<0.95, J{r_idx}<0.95), "WARNING", "ON TRACK"))')
        
        # Format alignments and borders
        for c in range(1, 19):
            cell = ws2.cell(row=r_idx, column=c)
            cell.border = thin_bottom
            if c in (1, 18):
                cell.alignment = Alignment(horizontal='center')
            elif c >= 3:
                cell.alignment = Alignment(horizontal='right')
                
        # Critical project status highlights
        c_status = ws2.cell(row=r_idx, column=18)
        if p_id in ("UM-ENG-03", "UM-FPV-01", "EVU001"):
            c_status.fill = critical_fill
            c_status.font = critical_font
        else:
            c_status.fill = ontrack_fill
            c_status.font = ontrack_font
            
    # Portfolio Totals Row
    tot_row = 14
    ws2.cell(row=tot_row, column=1, value="SUM PORTEFØLJE").font = bold_font
    ws2.cell(row=tot_row, column=3, value="=SUM(C5:C13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=4, value="=SUM(D5:D13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=5, value="=SUM(E5:E13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=6, value="=SUM(F5:F13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=7, value="=E14-F14").number_format = fmt_currency
    ws2.cell(row=tot_row, column=8, value="=E14-D14").number_format = fmt_currency
    
    ws2.cell(row=tot_row, column=9, value="=E14/F14").number_format = fmt_decimal # Weighted CPI
    ws2.cell(row=tot_row, column=10, value="=E14/D14").number_format = fmt_decimal # Weighted SPI
    
    ws2.cell(row=tot_row, column=11, value="=SUM(K5:K13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=12, value="=SUM(L5:L13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=13, value="=SUM(M5:M13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=14, value="=SUM(N5:N13)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=15, value="=C14-N14").number_format = fmt_currency
    ws2.cell(row=tot_row, column=16, value="=N14-F14").number_format = fmt_currency
    ws2.cell(row=tot_row, column=17, value="=(C14-E14)/(C14-F14)").number_format = fmt_decimal
    ws2.cell(row=tot_row, column=18, value="PORTEFØLJE").font = bold_font
    ws2.cell(row=tot_row, column=18).alignment = Alignment(horizontal='center')
    
    for c in range(1, 19):
        cell = ws2.cell(row=tot_row, column=c)
        cell.font = bold_font
        cell.border = double_bottom
        cell.fill = total_row_fill
        if c >= 3 and c != 18:
            cell.alignment = Alignment(horizontal='right')

    # -------------------------------------------------------------------------
    # TAB 4: 03_S_Kurve_Tidsserie
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="03_S_Kurve_Tidsserie")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["A1"] = "Kumulativ EVM S-Kurve & Månedlig Tidsserie 2026"
    ws3["A1"].font = title_font
    ws3["A2"] = "Månedsfordelt oppfølging av Planned Value (PV), Earned Value (EV) og Actual Cost (AC) for porteføljen"
    ws3["A2"].font = subtitle_font
    
    ts_headers = [
        "Periode", "Måned", "Planlagt Verdi (PV)", "Opptjent Verdi (EV)", "Påløpt Kostnad (AC)",
        "Kostnadsavvik (CV)", "Fremdriftsavvik (SV)", "Kumulativ CPI", "Kumulativ SPI"
    ]
    for idx, text in enumerate(ts_headers, 1):
        c = ws3.cell(row=4, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal='center' if idx <= 2 else 'right')
        
    timeseries_data = [
        ("2026-M01", "Januar", 3500000, 3600000, 3400000),
        ("2026-M02", "Februar", 7200000, 7100000, 7000000),
        ("2026-M03", "Mars", 11500000, 11000000, 11200000),
        ("2026-M04", "April", 16000000, 15200000, 15900000),
        ("2026-M05", "Mai", 21000000, 19800000, 21100000),
        ("2026-M06", "Juni", 26500000, 24900000, 27000000),
        ("2026-M07", "Juli", 30000000, 28000000, 30500000),
        ("2026-M08", "August", 34500000, 32100000, 35200000),
        ("2026-M09", "September", 38000000, 35000000, 38500000),
        ("2026-M10", "Oktober (Aktuell)", 41000000, 38400000, 41700000),
        ("2026-M11", "November (Prognose)", 55000000, None, None),
        ("2026-M12", "Desember (BAC Mål)", 71700000, None, None)
    ]
    
    for r_idx, (per, m_name, pv_val, ev_val, ac_val) in enumerate(timeseries_data, 5):
        ws3.cell(row=r_idx, column=1, value=per).font = mono_font
        ws3.cell(row=r_idx, column=2, value=m_name).font = regular_font
        ws3.cell(row=r_idx, column=3, value=pv_val).number_format = fmt_currency
        
        c_ev = ws3.cell(row=r_idx, column=4, value=ev_val)
        c_ac = ws3.cell(row=r_idx, column=5, value=ac_val)
        if ev_val is not None:
            c_ev.number_format = fmt_currency
            c_ac.number_format = fmt_currency
            ws3.cell(row=r_idx, column=6, value=f"=D{r_idx}-E{r_idx}").number_format = fmt_currency # CV = EV - AC
            ws3.cell(row=r_idx, column=7, value=f"=D{r_idx}-C{r_idx}").number_format = fmt_currency # SV = EV - PV
            ws3.cell(row=r_idx, column=8, value=f"=D{r_idx}/E{r_idx}").number_format = fmt_decimal   # CPI
            ws3.cell(row=r_idx, column=9, value=f"=D{r_idx}/C{r_idx}").number_format = fmt_decimal   # SPI
        else:
            ws3.cell(row=r_idx, column=6, value="-")
            ws3.cell(row=r_idx, column=7, value="-")
            ws3.cell(row=r_idx, column=8, value="-")
            ws3.cell(row=r_idx, column=9, value="-")
            
        for c in range(1, 10):
            cell = ws3.cell(row=r_idx, column=c)
            cell.border = thin_bottom
            if c <= 2:
                cell.alignment = Alignment(horizontal='center')
            else:
                cell.alignment = Alignment(horizontal='right')
            if r_idx == 14: # Current M10 highlight
                cell.fill = total_row_fill
                cell.font = bold_font
                
    # Add native Excel Line Chart for S-Curve
    chart = LineChart()
    chart.title = "Kumulativ EVM S-Kurve 2026 (Portefølje PV vs. EV vs. AC)"
    chart.style = 10
    chart.y_axis.title = "Beløp (NOK)"
    chart.x_axis.title = "Periode"
    chart.width = 18
    chart.height = 10
    
    data_ref = Reference(ws3, min_col=3, min_row=4, max_col=5, max_row=14)
    cats_ref = Reference(ws3, min_col=1, min_row=5, max_row=14)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    ws3.add_chart(chart, "B19")

    # -------------------------------------------------------------------------
    # TAB 5: 04_F05_20_Avsetningskalkyle
    # -------------------------------------------------------------------------
    ws4 = wb.create_sheet(title="04_F05_20_Avsetningskalkyle")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4["A1"] = "Statlig Avsetningskontroll & Preskriptiv Tiltaksmodell (F-05-20)"
    ws4["A1"].font = title_font
    ws4["A2"] = "Kunnskapsdepartementets regelverk for overføring av ubrukte bevilgninger (Maks 5,0 % av Kap. 260 post 50)"
    ws4["A2"].font = subtitle_font
    
    ws4["A4"] = "Statlige Rammetall & Gjeldende Status (2026-M10)"
    ws4["A4"].font = section_font
    
    f05_headers = ["Bevilgningsparameter / Nøkkeltall", "Beløp (NOK)", "Andel av Ramme", "Status & Merknad"]
    for idx, text in enumerate(f05_headers, 1):
        c = ws4.cell(row=5, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    f05_rows = [
        ("Statlig Grunnbevilgning (Kap. 260, post 50)", 1200000000, 1.0, "Tildeling over statsbudsjettet 2026"),
        ("Maksimalt Lovfestet Avsetningstak (5,0 %)", "=B6*0.05", "=B7/B6", "Grenseverdi fastsatt i rundskriv F-05-20"),
        ("Reell Akkumulert Driftsavsetning (M10)", 72000000, "=B8/B6", "Akkumulert overskudd/mindreforbruk per 31.10.2026"),
        ("Beregnet Overskridelse (Eksponert for Inndragning)", "=MAX(0, B8-B7)", "=B9/B6", "DISPENSASJON PÅKREVD: Risiko for at KD inndrar midler")
    ]
    
    for r_idx, (label, val, pct_f, note) in enumerate(f05_rows, 6):
        c1 = ws4.cell(row=r_idx, column=1, value=label)
        c2 = ws4.cell(row=r_idx, column=2, value=val)
        c3 = ws4.cell(row=r_idx, column=3, value=pct_f)
        c4 = ws4.cell(row=r_idx, column=4, value=note)
        
        c1.font = bold_font
        c2.font = critical_font if r_idx == 9 else bold_font
        c3.font = bold_font
        c4.font = critical_font if r_idx == 9 else regular_font
        
        c2.number_format = fmt_currency
        c3.number_format = fmt_percent
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom
            if r_idx == 9:
                c.fill = critical_fill
                
    # Prescriptive Action What-If Simulator Table
    ws4["A12"] = "Preskriptiv Tiltaksmodell — Simulering av EOY-Balanse (Endre beløp i kolonne B for å simulere effekt)"
    ws4["A12"].font = section_font
    
    sim_headers = ["Tiltaks-ID", "Tiltaksbeskrivelse / Strategisk Formål", "Simulert Tiltakskostnad (NOK)", "Foreslått Ansvarlig", "Gjennomførbarhet"]
    for idx, text in enumerate(sim_headers, 1):
        c = ws4.cell(row=13, column=idx, value=text)
        c.font = header_font
        c.fill = accent_header_fill
        
    sim_actions = [
        ("T1", "Framskyndet utstyrsinnkjøp maritim lab og simulatorer", 5000000, "Fakultetsdirektør", "Høy - Anbud klart"),
        ("T2", "Ekstraordinært IKT-vedlikehold & energieffektivisering", 4000000, "Eiendomssjef", "Høy - Rammekontrakt"),
        ("T3", "Strategiske såkornmidler til EU Horizon forskningskonsortier", 2000000, "Forskningsdekan", "Middels - Utlysning nov"),
        ("T4", "Ph.d.- og postdoktor stipendiatrekrutteringspakke", 1000000, "Instituttleder", "Høy - Rekruttering igangsatt")
    ]
    
    for r_idx, (t_id, desc, cost, owner, feas) in enumerate(sim_actions, 14):
        ws4.cell(row=r_idx, column=1, value=t_id).font = mono_font
        ws4.cell(row=r_idx, column=2, value=desc).font = regular_font
        
        c_cost = ws4.cell(row=r_idx, column=3, value=cost)
        c_cost.font = Font(name=font_family, size=10, bold=True, color="0369A1")
        c_cost.fill = input_fill
        c_cost.number_format = fmt_currency
        c_cost.alignment = Alignment(horizontal='right')
        c_cost.border = card_border
        
        ws4.cell(row=r_idx, column=4, value=owner).font = bold_font
        ws4.cell(row=r_idx, column=5, value=feas).font = regular_font
        
        for c in (ws4.cell(row=r_idx, column=1), ws4.cell(row=r_idx, column=2), ws4.cell(row=r_idx, column=4), ws4.cell(row=r_idx, column=5)):
            c.border = thin_bottom
            
    # Simulator Summary Row
    ws4.cell(row=18, column=1, value="SUM TILTAKSPLAN").font = bold_font
    ws4.cell(row=18, column=3, value="=SUM(C14:C17)").number_format = fmt_currency
    ws4.cell(row=18, column=3).font = bold_font
    ws4.cell(row=18, column=3).alignment = Alignment(horizontal='right')
    for c in range(1, 6):
        cell = ws4.cell(row=18, column=c)
        cell.border = double_bottom
        cell.fill = total_row_fill

    # Revised EOY Reserve Result
    ws4["A20"] = "Revidert Sluttbalanse Prognose (EOY 2026)"
    ws4["A20"].font = section_font
    
    rev_rows = [
        ("Opprinnelig Akkumulert Driftsavsetning M10", "=B8", "=B21/B6", fmt_currency),
        ("Total Effekt av Iverksatte Ledelsestiltak", "=C18", "=B22/B6", fmt_currency),
        ("Revidert Prognostisert Driftsavsetning EOY", "=B21-B22", "=B23/B6", fmt_currency),
        ("Revidert Overskridelse mot 5 % Tak", "=MAX(0, B23-B7)", "=B24/B6", fmt_currency),
        ("Revidert Regelverksstatus", '=IF(B23<=B7, "MÅL OPPNÅDD: INNENFOR 5,0 % GRENSE", "FORTSATT DISPENSASJONSBEHOV (Restbeløp søkes)")', "", "@")
    ]
    
    for r_idx, (label, val_f, pct_f, num_fmt) in enumerate(rev_rows, 21):
        c1 = ws4.cell(row=r_idx, column=1, value=label)
        c2 = ws4.cell(row=r_idx, column=2, value=val_f)
        c3 = ws4.cell(row=r_idx, column=3, value=pct_f)
        c1.font = bold_font
        c2.font = bold_font
        c3.font = bold_font
        c2.number_format = num_fmt
        c3.number_format = fmt_percent
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        if r_idx == 25:
            c2.font = ontrack_font
            c2.alignment = Alignment(horizontal='left')
        for c in (c1, c2, c3):
            c.border = thin_bottom
            if r_idx in (23, 24, 25):
                c.fill = ontrack_fill if r_idx == 25 else total_row_fill

    # -------------------------------------------------------------------------
    # TAB 6: 05_Compliance_Internkontroll
    # -------------------------------------------------------------------------
    ws5 = wb.create_sheet(title="05_Compliance_Internkontroll")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5["A1"] = "DFØ & UBW Internkontroll — Atestering, Bilagskontroll & Sperrelister"
    ws5["A1"].font = title_font
    ws5["A2"] = "Overvåking av 4-øyne-prinsippet, beløpsfullmakter, måltidsfradrag og bilagsdokumentasjon"
    ws5["A2"].font = subtitle_font
    
    # Executive Summary Card for Audit
    ws5["A4"] = "Internkontroll Nøkkeltall (M10)"
    ws5["A4"].font = section_font
    
    aud_summary_headers = ["Område", "Scannede Saker", "Flagg / Avvik", "Eksponert Beløp", "Status Unit4"]
    for idx, text in enumerate(aud_summary_headers, 1):
        c = ws5.cell(row=5, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    aud_kpis = [
        ("DFØ Reiseregninger (15 stk utvalg)", 15, "=COUNTIF(M12:M26, \"FLAGGED\")", "=SUMIF(M12:M26, \"FLAGGED\", E12:E26)", "7 Sperret for utbetaling"),
        ("UBW Hovedboksposteringer (transaksjoner)", 5, "=COUNTIF(Fact_UBW_Audit!I2:I6, \"<>OK\")", "=SUMIF(Fact_UBW_Audit!I2:I6, \"<>OK\", Fact_UBW_Audit!D2:D6)", "1 Egengodkjenning flagget"),
        ("TOTAL EKSPONERING", 20, "=C6+C7", "=D6+D7", "Sperrelister etablert")
    ]
    for r_idx, (area, cnt, flg_f, amt_f, stat) in enumerate(aud_kpis, 6):
        c1 = ws5.cell(row=r_idx, column=1, value=area)
        c2 = ws5.cell(row=r_idx, column=2, value=cnt)
        c3 = ws5.cell(row=r_idx, column=3, value=flg_f)
        c4 = ws5.cell(row=r_idx, column=4, value=amt_f)
        c5 = ws5.cell(row=r_idx, column=5, value=stat)
        
        c1.font = bold_font
        c2.font = regular_font
        c3.font = critical_font if r_idx == 8 else bold_font
        c4.font = critical_font if r_idx == 8 else bold_font
        c5.font = critical_font if "Sperret" in stat else bold_font
        
        c2.number_format = fmt_integer
        c3.number_format = fmt_integer
        c4.number_format = fmt_currency
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        c4.alignment = Alignment(horizontal='right')
        
        for c in (c1, c2, c3, c4, c5):
            c.border = double_bottom if r_idx == 8 else thin_bottom
            if r_idx == 8:
                c.fill = critical_fill
                
    # Detail Travel Audit Table
    ws5["A10"] = "DFØ Reiseregninger — Detaljert Kontrollmatrise (tbl_Travel_Audit)"
    ws5["A10"].font = section_font
    
    tr_headers = [
        "Reise-ID", "Ansatt Navn", "Dato", "Formål", "Beløp (NOK)", "Måltid Dekket", 
        "Fradrag Utført", "Km Godtgj.", "Kvittering", "BDM ID", "Attestant ID", 
        "Avviksbeskrivelse", "Audit Status", "Sperret i Unit4?"
    ]
    for idx, text in enumerate(tr_headers, 1):
        c = ws5.cell(row=11, column=idx, value=text)
        c.font = header_font
        c.fill = accent_header_fill
        c.alignment = Alignment(horizontal='center' if idx in (1, 3, 13, 14) else ('right' if idx in (5, 8) else 'left'))
        
    travel_csv_path = BASE_DIR / "data" / "staging" / "reiseregninger_15_stk.csv"
    if travel_csv_path.exists():
        from audit_travel_expenses import audit_travel_claims
        audit_res = audit_travel_claims(str(travel_csv_path))
        findings_map = {f["Reise_ID"]: "; ".join(f["Avvik"]) for f in audit_res["findings"]}
        df_tr = pd.read_csv(travel_csv_path)
    else:
        df_tr = pd.DataFrame()
        findings_map = {}
        
    for r_idx, (_, row) in enumerate(df_tr.iterrows(), 12):
        r_id = str(row['Reise_ID'])
        avvik = findings_map.get(r_id, "OK")
        status = "FLAGGED" if avvik != "OK" else "APPROVED"
        blocked = "JA" if status == "FLAGGED" else "NEI"
        
        ws5.cell(row=r_idx, column=1, value=r_id).font = mono_font
        ws5.cell(row=r_idx, column=2, value=str(row['Ansatt'])).font = regular_font
        ws5.cell(row=r_idx, column=3, value=str(row['Dato'])).font = mono_font
        ws5.cell(row=r_idx, column=4, value=str(row['Formaal'])).font = regular_font
        ws5.cell(row=r_idx, column=5, value=float(row['Belop_NOK'])).number_format = fmt_currency
        ws5.cell(row=r_idx, column=6, value=str(row['Maltid_Dekket'])).font = regular_font
        ws5.cell(row=r_idx, column=7, value="JA" if row['Fradrag_Utfort'] else "NEI").font = regular_font
        ws5.cell(row=r_idx, column=8, value=int(row['Km_Godtgjorelse'])).number_format = fmt_integer
        ws5.cell(row=r_idx, column=9, value="JA" if row['Kvittering_Vedlagt'] else "NEI").font = regular_font
        ws5.cell(row=r_idx, column=10, value=str(row['BDM_ID'])).font = mono_font
        ws5.cell(row=r_idx, column=11, value=str(row['Attestant_ID'])).font = mono_font
        ws5.cell(row=r_idx, column=12, value=avvik).font = critical_font if status == "FLAGGED" else regular_font
        
        c_stat = ws5.cell(row=r_idx, column=13, value=status)
        c_block = ws5.cell(row=r_idx, column=14, value=blocked)
        
        c_stat.font = critical_font if status == "FLAGGED" else ontrack_font
        c_block.font = critical_font if blocked == "JA" else ontrack_font
        c_stat.alignment = Alignment(horizontal='center')
        c_block.alignment = Alignment(horizontal='center')
        
        for c in range(1, 15):
            cell = ws5.cell(row=r_idx, column=c)
            cell.border = thin_bottom
            if status == "FLAGGED":
                cell.fill = critical_fill
            else:
                cell.fill = ontrack_fill if c in (13, 14) else PatternFill(fill_type=None)
                
    # Audit Totals Row
    aud_tot_r = 27
    ws5.cell(row=aud_tot_r, column=1, value="TOTALT REISEREGNINGER").font = bold_font
    ws5.cell(row=aud_tot_r, column=5, value="=SUM(E12:E26)").number_format = fmt_currency
    ws5.cell(row=aud_tot_r, column=5).font = bold_font
    ws5.cell(row=aud_tot_r, column=8, value="=SUM(H12:H26)").number_format = fmt_integer
    for c in range(1, 15):
        cell = ws5.cell(row=aud_tot_r, column=c)
        cell.border = double_bottom
        cell.fill = total_row_fill
        if c in (5, 8):
            cell.alignment = Alignment(horizontal='right')

    # -------------------------------------------------------------------------
    # TAB 7: Dim_Project (Backend Star Schema Table)
    # -------------------------------------------------------------------------
    ws_dp = wb.create_sheet(title="Dim_Project")
    ws_dp.views.sheetView[0].showGridLines = True
    
    dp_headers = ["project_id", "project_name", "department", "pm_name", "category", "bac", "status"]
    for idx, text in enumerate(dp_headers, 1):
        c = ws_dp.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal='right' if text == 'bac' else 'left')
        
    projects_master = [
        ("UM-DEF-02", "Forsvarsforskning Agder (Skrogmodell)", "Teknologi og realfag", "Prof. T. Gundersen", "Forsvarskontrakt", 18500000, "ON TRACK"),
        ("UM-ENG-03", "Ingeniørutdanning Fornybar (Komposittlab)", "Ingeniørvitenskap", "Dr. E. Hansen", "Utdanning / Lab", 8200000, "CRITICAL"),
        ("UM-FPV-01", "Fotovoltaikk Solceller (Maritim Lab)", "Fornybar Energi", "Prof. S. Vik", "Investering / FOU", 45000000, "CRITICAL"),
        ("NFR001", "NFR-AI: Kunstig intelligens i styring", "Handelshøyskolen", "Prof. R. Møller", "NFR Forskning (SRS 10)", 4000000, "WARNING"),
        ("NFR002", "NFR-Helse: Pasientsikkerhet i helsefag", "Helse- og idrettsfag", "Dr. K. Strand", "NFR Forskning (SRS 10)", 2800000, "ON TRACK"),
        ("EU001", "EU Horizon: Green Maritime Tech", "Teknologi og realfag", "Prof. H. Berg", "EU Horizon Europe (SRS 10)", 6200000, "ON TRACK"),
        ("EU002", "EU Horizon: Digital Governance", "Samfunnsvitenskap", "Dr. L. Aas", "EU Horizon Europe (SRS 10)", 4500000, "ON TRACK"),
        ("EVU001", "EVU Videreutdanning for kommuner", "Etter- og videreutdanning", "A. Lie", "Oppdragsundervisning (SRS 9)", 1200000, "CRITICAL"),
        ("OPPDRAG01", "Oppdragsforskning Batteriteknologi", "Teknologi og realfag", "Dr. O. Dale", "Næringslivsoppdrag (SRS 9)", 1800000, "ON TRACK")
    ]
    
    for r_idx, row in enumerate(projects_master, 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_dp.cell(row=r_idx, column=c_idx, value=val)
            cell.font = mono_font if c_idx == 1 else regular_font
            cell.border = thin_bottom
            if c_idx == 6:
                cell.number_format = fmt_currency
                cell.alignment = Alignment(horizontal='right')
                
    tab_dp = Table(displayName="tbl_Dim_Project", ref=f"A1:G{len(projects_master)+1}")
    tab_dp.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_dp.add_table(tab_dp)

    # -------------------------------------------------------------------------
    # TAB 8: Dim_Date (Backend Star Schema Table)
    # -------------------------------------------------------------------------
    ws_dd = wb.create_sheet(title="Dim_Date")
    ws_dd.views.sheetView[0].showGridLines = True
    
    dates_headers = ["Date", "Year", "Month", "MonthName", "ReportingPeriod", "Quarter"]
    for idx, text in enumerate(dates_headers, 1):
        c = ws_dd.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    dates_df = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")
    for r_idx, d in enumerate(dates_df, 2):
        ws_dd.cell(row=r_idx, column=1, value=d.strftime("%Y-%m-%d")).font = mono_font
        ws_dd.cell(row=r_idx, column=2, value=d.year).number_format = fmt_integer
        ws_dd.cell(row=r_idx, column=3, value=d.month).number_format = fmt_integer
        ws_dd.cell(row=r_idx, column=4, value=d.strftime("%B")).font = regular_font
        ws_dd.cell(row=r_idx, column=5, value=d.strftime("2026-M%m")).font = mono_font
        ws_dd.cell(row=r_idx, column=6, value=d.quarter).number_format = fmt_integer
        for c in range(1, 7):
            ws_dd.cell(row=r_idx, column=c).border = thin_bottom
            
    tab_dd = Table(displayName="tbl_Dim_Date", ref=f"A1:F{len(dates_df)+1}")
    tab_dd.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_dd.add_table(tab_dd)

    # -------------------------------------------------------------------------
    # TAB 9: Dim_Model_Parameter (Backend Slicer Table)
    # -------------------------------------------------------------------------
    ws_mp = wb.create_sheet(title="Dim_Model_Parameter")
    ws_mp.views.sheetView[0].showGridLines = True
    
    mp_headers = ["ModelCode", "ModelName", "Formula_Logic", "Cost_Weight", "Schedule_Weight", "Description"]
    for idx, text in enumerate(mp_headers, 1):
        c = ws_mp.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    mp_data = [
        ("CPI", "Typisk CPI Modell", "BAC / CPI", 1.0, 0.0, "Forutsetter at historisk kostnadseffektivitet fortsetter uendret ut prosjektet"),
        ("COMPOSITE", "Sammensatt CPI x SPI Modell", "AC + (BAC - EV)/(CPI * SPI)", 0.5, 0.5, "Tar eksplisitt hensyn til fremdriftsavvik og leveranseforsinkelse"),
        ("WEIGHTED", "Vektet 80/20 Modell", "AC + (BAC - EV)/(0.8*CPI + 0.2*SPI)", 0.8, 0.2, "Standard controlling-framskriving med 80 % vekt på kostnad og 20 % på fremdrift")
    ]
    for r_idx, row in enumerate(mp_data, 2):
        for c_idx, val in enumerate(row, 1):
            cell = ws_mp.cell(row=r_idx, column=c_idx, value=val)
            cell.font = mono_font if c_idx == 1 else regular_font
            cell.border = thin_bottom
            if c_idx in (4, 5):
                cell.number_format = fmt_percent
                cell.alignment = Alignment(horizontal='right')
                
    tab_mp = Table(displayName="tbl_Dim_Parameters", ref=f"A1:F{len(mp_data)+1}")
    tab_mp.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_mp.add_table(tab_mp)

    # -------------------------------------------------------------------------
    # TAB 10: Fact_EVM_Snapshots (Backend Fact Table)
    # -------------------------------------------------------------------------
    ws_fe = wb.create_sheet(title="Fact_EVM_Snapshots")
    ws_fe.views.sheetView[0].showGridLines = True
    
    fe_headers = [
        "reporting_period", "snapshot_timestamp", "project_id", "bac", "pv", "ev", "ac",
        "cpi", "spi", "eac_cpi", "eac_composite", "eac_weighted", "vac", "tcpi", "status"
    ]
    for idx, text in enumerate(fe_headers, 1):
        c = ws_fe.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    con_dk = duckdb.connect(str(BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"), read_only=True)
    df_evm_snap = con_dk.execute("SELECT * FROM evm_snapshots").fetchdf()
    con_dk.close()
    
    for r_idx, (_, row) in enumerate(df_evm_snap.iterrows(), 2):
        for c_idx, col in enumerate(fe_headers, 1):
            val = row[col]
            if isinstance(val, pd.Timestamp):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            cell = ws_fe.cell(row=r_idx, column=c_idx, value=val)
            cell.font = mono_font if c_idx in (1, 2, 3) else regular_font
            cell.border = thin_bottom
            if col in ('bac', 'pv', 'ev', 'ac', 'eac_cpi', 'eac_composite', 'eac_weighted', 'vac'):
                cell.number_format = fmt_currency
                cell.alignment = Alignment(horizontal='right')
            elif col in ('cpi', 'spi', 'tcpi'):
                cell.number_format = fmt_decimal
                cell.alignment = Alignment(horizontal='right')
                
    tab_fe = Table(displayName="tbl_Fact_EVM", ref=f"A1:O{len(df_evm_snap)+1}")
    tab_fe.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_fe.add_table(tab_fe)

    # -------------------------------------------------------------------------
    # TAB 11: Fact_UBW_Audit (Backend Fact Table)
    # -------------------------------------------------------------------------
    ws_fu = wb.create_sheet(title="Fact_UBW_Audit")
    ws_fu.views.sheetView[0].showGridLines = True
    
    fu_headers = [
        "transaksjon_id", "konto", "beskrivelse", "belop_nok", "bdm_id", "attestant_id",
        "kvittering_vedlagt", "formaal", "Kontrollflagg"
    ]
    for idx, text in enumerate(fu_headers, 1):
        c = ws_fu.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    con_sq = sqlite3.connect(str(BASE_DIR / "data" / "staging" / "projects.db"))
    df_ubw = pd.read_sql("SELECT * FROM ubw_transactions", con_sq)
    con_sq.close()
    
    for r_idx, (_, row) in enumerate(df_ubw.iterrows(), 2):
        ws_fu.cell(row=r_idx, column=1, value=str(row['transaksjon_id'])).font = mono_font
        ws_fu.cell(row=r_idx, column=2, value=str(row['konto'])).font = mono_font
        ws_fu.cell(row=r_idx, column=3, value=str(row['beskrivelse'])).font = regular_font
        c_amt = ws_fu.cell(row=r_idx, column=4, value=float(row['belop_nok']))
        c_amt.number_format = fmt_currency
        c_amt.alignment = Alignment(horizontal='right')
        ws_fu.cell(row=r_idx, column=5, value=str(row['bdm_id'])).font = mono_font
        ws_fu.cell(row=r_idx, column=6, value=str(row['attestant_id'])).font = mono_font
        ws_fu.cell(row=r_idx, column=7, value=int(row['kvittering_vedlagt'])).number_format = fmt_integer
        ws_fu.cell(row=r_idx, column=8, value=str(row['formaal'])).font = regular_font
        
        # Dynamic 4-eyes check formula
        c_flg = ws_fu.cell(row=r_idx, column=9, value=f'=IF(E{r_idx}=F{r_idx}, "BRUDD: Egengodkjenning", IF(G{r_idx}=0, "MANGLER BILAG", "OK"))')
        c_flg.font = critical_font if row['bdm_id'] == row['attestant_id'] else regular_font
        
        for c in range(1, 10):
            ws_fu.cell(row=r_idx, column=c).border = thin_bottom
            if row['bdm_id'] == row['attestant_id']:
                ws_fu.cell(row=r_idx, column=c).fill = critical_fill
                
    tab_fu = Table(displayName="tbl_Fact_UBW", ref=f"A1:I{len(df_ubw)+1}")
    tab_fu.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_fu.add_table(tab_fu)

    # -------------------------------------------------------------------------
    # TAB 12: Fact_Travel_Audit (Backend Fact Table)
    # -------------------------------------------------------------------------
    ws_ft = wb.create_sheet(title="Fact_Travel_Audit")
    ws_ft.views.sheetView[0].showGridLines = True
    
    for idx, text in enumerate(tr_headers, 1):
        c = ws_ft.cell(row=1, column=idx, value=text)
        c.font = header_font
        c.fill = header_fill
        
    for r_idx, (_, row) in enumerate(df_tr.iterrows(), 2):
        r_id = str(row['Reise_ID'])
        avvik = findings_map.get(r_id, "OK")
        status = "FLAGGED" if avvik != "OK" else "APPROVED"
        blocked = "JA" if status == "FLAGGED" else "NEI"
        
        ws_ft.cell(row=r_idx, column=1, value=r_id).font = mono_font
        ws_ft.cell(row=r_idx, column=2, value=str(row['Ansatt'])).font = regular_font
        ws_ft.cell(row=r_idx, column=3, value=str(row['Dato'])).font = mono_font
        ws_ft.cell(row=r_idx, column=4, value=str(row['Formaal'])).font = regular_font
        ws_ft.cell(row=r_idx, column=5, value=float(row['Belop_NOK'])).number_format = fmt_currency
        ws_ft.cell(row=r_idx, column=6, value=str(row['Maltid_Dekket'])).font = regular_font
        ws_ft.cell(row=r_idx, column=7, value="JA" if row['Fradrag_Utfort'] else "NEI").font = regular_font
        ws_ft.cell(row=r_idx, column=8, value=int(row['Km_Godtgjorelse'])).number_format = fmt_integer
        ws_ft.cell(row=r_idx, column=9, value="JA" if row['Kvittering_Vedlagt'] else "NEI").font = regular_font
        ws_ft.cell(row=r_idx, column=10, value=str(row['BDM_ID'])).font = mono_font
        ws_ft.cell(row=r_idx, column=11, value=str(row['Attestant_ID'])).font = mono_font
        ws_ft.cell(row=r_idx, column=12, value=avvik).font = critical_font if status == "FLAGGED" else regular_font
        ws_ft.cell(row=r_idx, column=13, value=status).font = critical_font if status == "FLAGGED" else ontrack_font
        ws_ft.cell(row=r_idx, column=14, value=blocked).font = critical_font if blocked == "JA" else ontrack_font
        
        for c in range(1, 15):
            ws_ft.cell(row=r_idx, column=c).border = thin_bottom
            if status == "FLAGGED":
                ws_ft.cell(row=r_idx, column=c).fill = critical_fill
                
    tab_ft = Table(displayName="tbl_Fact_Travel", ref=f"A1:N{len(df_tr)+1}")
    tab_ft.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_ft.add_table(tab_ft)

    # -------------------------------------------------------------------------
    # TAB 13: Fact_Project_BOA (Backend Fact Table)
    # -------------------------------------------------------------------------
    ws_fb = wb.create_sheet(title="Fact_Project_BOA")
    ws_fb.views.sheetView[0].showGridLines = True
    
    boa_csv_path = BASE_DIR / "data" / "FactProjectBOA.csv"
    if boa_csv_path.exists():
        df_boa = pd.read_csv(boa_csv_path, sep=';')
    else:
        df_boa = pd.DataFrame([
            {"Prosjekt_ID": "BOA-2026-01", "Prosjektnavn": "NFR Maritim AI", "Finansieringskilde": "NFR", "Totalbudsjett_NOK": 15000000.0, "Direkte_Kostnader_NOK": 10344828.0, "Overhead_TDI_NOK": 4655172.0, "Dekningsgrad_Prosent": 0.45},
            {"Prosjekt_ID": "BOA-2026-02", "Prosjektnavn": "EU Horizon Green Energy", "Finansieringskilde": "EU Horizon", "Totalbudsjett_NOK": 25000000.0, "Direkte_Kostnader_NOK": 17241379.0, "Overhead_TDI_NOK": 7758621.0, "Dekningsgrad_Prosent": 0.45}
        ])

    for idx, col in enumerate(df_boa.columns, 1):
        c = ws_fb.cell(row=1, column=idx, value=col)
        c.font = header_font
        c.fill = header_fill
        
    for r_idx, (_, row) in enumerate(df_boa.iterrows(), 2):
        for c_idx, col in enumerate(df_boa.columns, 1):
            val = row[col]
            cell = ws_fb.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_bottom
            if isinstance(val, (int, float)):
                if "Dekningsgrad" in col or "%" in col:
                    cell.number_format = fmt_percent
                elif val > 1000:
                    cell.number_format = fmt_currency
                cell.alignment = Alignment(horizontal='right')
                
    tab_fb = Table(displayName="tbl_Fact_BOA", ref=f"A1:{get_column_letter(len(df_boa.columns))}{len(df_boa)+1}")
    tab_fb.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_fb.add_table(tab_fb)

    # -------------------------------------------------------------------------
    # TAB 14: Dim_Kontoplan_2026 (Backend Dimension Table)
    # -------------------------------------------------------------------------
    ws_kp = wb.create_sheet(title="Dim_Kontoplan_2026")
    ws_kp.views.sheetView[0].showGridLines = True
    
    kp_csv_path = BASE_DIR / "data" / "DimAccount.csv"
    if kp_csv_path.exists():
        df_kp = pd.read_csv(kp_csv_path, sep=';')
    else:
        df_kp = pd.DataFrame([
            {"Konto": 3400, "Kontonavn": "Statlig Bevilgning Kap 260 post 50", "Kontoklasse": 3, "Standard_SRS": "SRS 10 Inntekter"},
            {"Konto": 5000, "Kontonavn": "Fast Lønn & Faste Tillegg", "Kontoklasse": 5, "Standard_SRS": "SRS 20 Lønnskostnader"},
            {"Konto": 6000, "Kontonavn": "Husleie og Eiendomsdrift", "Kontoklasse": 6, "Standard_SRS": "SRS 21 Andre driftskostnader"}
        ])

    for idx, col in enumerate(df_kp.columns, 1):
        c = ws_kp.cell(row=1, column=idx, value=col)
        c.font = header_font
        c.fill = header_fill
        
    for r_idx, (_, row) in enumerate(df_kp.iterrows(), 2):
        for c_idx, col in enumerate(df_kp.columns, 1):
            val = row[col]
            cell = ws_kp.cell(row=r_idx, column=c_idx, value=val)
            cell.font = mono_font if c_idx <= 2 else regular_font
            cell.border = thin_bottom
            if c_idx <= 2:
                cell.alignment = Alignment(horizontal='center')
                
    tab_kp = Table(displayName="tbl_Dim_Kontoplan", ref=f"A1:{get_column_letter(len(df_kp.columns))}{len(df_kp)+1}")
    tab_kp.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    ws_kp.add_table(tab_kp)


    # -------------------------------------------------------------------------
    # AUTO-FIT COLUMN WIDTHS ACROSS ALL SHEETS
    # -------------------------------------------------------------------------
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if cell.number_format and "NOK" in cell.number_format:
                    max_len = max(max_len, len(val_str) + 8)
                else:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    # Save Workbook to both primary and secondary destinations (with fallback if open in Excel)
    actual_primary = EXCEL_FILE_PRIMARY
    try:
        wb.save(EXCEL_FILE_PRIMARY)
    except PermissionError:
        actual_primary = EXCEL_FILE_PRIMARY.with_name("UiA_Controller_DataModel_2026_generated.xlsx")
        wb.save(actual_primary)
        print(f"  ! Merk: {EXCEL_FILE_PRIMARY.name} er i bruk av et annet program (f.eks. Excel). Lagret til: {actual_primary.name}")
        
    try:
        wb.save(EXCEL_FILE_SECONDARY)
    except PermissionError:
        pass
    
    print(f"=== Excel Data Model ferdigstilt: ===")
    print(f"  + Primary Target:   {actual_primary}")
    print(f"  + Secondary Mirror: {EXCEL_FILE_SECONDARY}")
    print(f"  + Antall Faner:     {len(wb.sheetnames)}")
    print(f"  + Faner:            {', '.join(wb.sheetnames)}")
    return str(actual_primary)

if __name__ == "__main__":
    create_excel_datamodel()
