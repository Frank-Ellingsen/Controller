"""
UiA Controller App — Excel Report Generator (v12 Canonical)
Generates an executive-grade, Tufte-compliant Excel report (.xlsx)
with dynamic formulas, Star Schema EVM analysis, F-05-20 reserve cap tracking, and DFØ audit exception detail.
"""

import os
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "reports"
OUTPUT_FILE = OUTPUT_DIR / "UiA_Controller_Maanedsoppgjoer_2026-M10.xlsx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_excel_report():
    wb = openpyxl.Workbook()
    
    # Define Tufte & Corporate Palette Styles
    font_family = "Calibri"
    
    header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    title_font = Font(name=font_family, size=16, bold=True, color="0F172A")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="475569")
    bold_font = Font(name=font_family, size=11, bold=True, color="0F172A")
    regular_font = Font(name=font_family, size=11, color="1E293B")
    mono_font = Font(name="Consolas", size=10, color="0F172A")
    
    # Highlight fonts & fills
    critical_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    critical_font = Font(name=font_family, size=11, bold=True, color="991B1B")
    
    warning_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    warning_font = Font(name=font_family, size=11, bold=True, color="92400E")
    
    ontrack_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    ontrack_font = Font(name=font_family, size=11, bold=True, color="065F46")

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    summary_header_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    total_row_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    
    # Borders (Subtle horizontal borders only, no vertical gridlines)
    thin_bottom = Border(bottom=Side(style='thin', color='CBD5E1'))
    thick_bottom = Border(bottom=Side(style='medium', color='1E293B'))
    double_bottom = Border(
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='double', color='1E293B')
    )
    
    # Number Formats
    fmt_currency = '#,##0 "NOK"'
    fmt_decimal = '0.00'
    fmt_percent = '0.0%'
    
    # =========================================================================
    # TAB 1: EXECUTIVE SAMMENDRAG
    # =========================================================================
    ws1 = wb.active
    ws1.title = "1. Sammendrag & Status"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["A1"] = "UiA Handelshøyskolen — Månedsoppgjør & Prosjektstatus"
    ws1["A1"].font = title_font
    ws1["A2"] = "Rapporteringsperiode: 2026-M10 | Utarbeidet av Lead Controller | Kilde: DuckDB & UBW"
    ws1["A2"].font = subtitle_font
    
    # Executive KPI Cards Block
    kpi_headers = ["Kritiske Nøkkeltall (KPI)", "Verdi", "Måltall / Grense", "Status & Tiltak"]
    for col_idx, text in enumerate(kpi_headers, 1):
        cell = ws1.cell(row=4, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = summary_header_fill
        cell.alignment = Alignment(horizontal='left' if col_idx != 2 else 'right')
        
    kpi_data = [
        ("Portefølje Budsjett (BAC)", 71700000, 71700000, "3 Aktive prosjekter", fmt_currency, False),
        ("Påløpte Kostnader (AC)", 41700000, 40000000, "Gjennomsnittlig CPI: 0.90", fmt_currency, False),
        ("Projisert Sluttavvik (VAC)", -6501888, 0, "KRITISK: Overforbruk på UM-ENG-03 & UM-FPV-01", fmt_currency, True),
        ("F-05-20 Driftsavsetning", 0.06, 0.05, "DISPENSASJON PÅKREVD (+12M NOK over 5% tak)", fmt_percent, True),
        ("DFØ Reiseregning Avvik", 19420, 0, "7 Saker flagget for atestasjonsbrudd (Utbetaling sperret)", fmt_currency, True)
    ]
    
    for row_offset, (label, val, target, desc, num_fmt, is_risk) in enumerate(kpi_data, 5):
        c1 = ws1.cell(row=row_offset, column=1, value=label)
        c2 = ws1.cell(row=row_offset, column=2, value=val)
        c3 = ws1.cell(row=row_offset, column=3, value=target)
        c4 = ws1.cell(row=row_offset, column=4, value=desc)
        
        c1.font = bold_font
        c2.font = critical_font if is_risk else bold_font
        c3.font = regular_font
        c4.font = regular_font
        
        c2.number_format = num_fmt
        c3.number_format = num_fmt
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom
            if is_risk:
                c.fill = critical_fill
                
    # Strategic Action Table
    start_r = 12
    ws1.cell(row=start_r, column=1, value="Anbefalte Ledelsestiltak").font = Font(name=font_family, size=13, bold=True, color="0F172A")
    
    act_headers = ["Prioritet", "Styringsområde", "Beskrivelse av tiltak", "Ansvarlig"]
    for col_idx, text in enumerate(act_headers, 1):
        cell = ws1.cell(row=start_r+1, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        
    actions = [
        ("P1 - Høy", "F-05-20 Avsetningssøknad", "Send formell dispenseringssøknad for 12 mill. NOK overskridelse til KD for å forhindre inndragning.", "Universitetsdirektør"),
        ("P1 - Høy", "Prosjektrevisjon UM-ENG-03", "Kall inn prosjekteier. TCPI på 2.14 krever urealistisk effektivitet. Omfangskutt eller ombudsjettering kreves.", "Dekan / Controller"),
        ("P2 - Medium", "DFØ Attestasjonsstopp", "Sperr utbetaling i Unit4 for 7 flaggede reiseregninger inntil 4-øyne kontrolletablering og diettjusteringer er gjennomført.", "Regnskapssjef")
    ]
    
    for idx, (prio, area, detail, owner) in enumerate(actions, start_r+2):
        c1 = ws1.cell(row=idx, column=1, value=prio)
        c2 = ws1.cell(row=idx, column=2, value=area)
        c3 = ws1.cell(row=idx, column=3, value=detail)
        c4 = ws1.cell(row=idx, column=4, value=owner)
        
        c1.font = critical_font if "P1" in prio else warning_font
        c2.font = bold_font
        c3.font = regular_font
        c4.font = regular_font
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom

    # =========================================================================
    # TAB 2: EVM PROSJEKTPORTEFØLJE
    # =========================================================================
    ws2 = wb.create_sheet(title="2. EVM Prosjektkontroll")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["A1"] = "Earned Value Management (EVM) — Prosjektanalyse & Fler-modell EAC"
    ws2["A1"].font = title_font
    ws2["A2"] = "Formler er konsistente med ANSI/EIA-748 og DFØ prosjektveileder"
    ws2["A2"].font = subtitle_font
    
    evm_headers = [
        "Prosjekt-ID", "Prosjektnavn", "Budsjett (BAC)", "Planlagt (PV)", "Opptjent (EV)", 
        "Påløpt (AC)", "CPI", "SPI", "EAC (Typisk CPI)", "EAC (Sammensatt)", 
        "EAC (Vektet 80/20)", "Avvik (VAC)", "TCPI", "Status"
    ]
    
    for col_idx, text in enumerate(evm_headers, 1):
        cell = ws2.cell(row=4, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center' if col_idx in (1, 14) else ('right' if col_idx >= 3 else 'left'))

    # Raw Project Data
    projects = [
        ("UM-DEF-02", "Forsvarskontrakt skrogmodell", 18500000, 12000000, 12200000, 11800000),
        ("UM-ENG-03", "Komposittstivhet labstudie", 8200000, 6500000, 5200000, 6800000),
        ("UM-FPV-01", "Fornybar energi maritim lab", 45000000, 22500000, 21000000, 23100000)
    ]
    
    for r_idx, (p_id, p_name, bac, pv, ev, ac) in enumerate(projects, 5):
        ws2.cell(row=r_idx, column=1, value=p_id).font = mono_font
        ws2.cell(row=r_idx, column=2, value=p_name).font = regular_font
        ws2.cell(row=r_idx, column=3, value=bac).number_format = fmt_currency
        ws2.cell(row=r_idx, column=4, value=pv).number_format = fmt_currency
        ws2.cell(row=r_idx, column=5, value=ev).number_format = fmt_currency
        ws2.cell(row=r_idx, column=6, value=ac).number_format = fmt_currency
        
        # Excel Formulas for Metrics
        # CPI = EV / AC
        cpi_cell = ws2.cell(row=r_idx, column=7, value=f"=E{r_idx}/F{r_idx}")
        cpi_cell.number_format = fmt_decimal
        
        # SPI = EV / PV
        spi_cell = ws2.cell(row=r_idx, column=8, value=f"=E{r_idx}/D{r_idx}")
        spi_cell.number_format = fmt_decimal
        
        # EAC (CPI) = BAC / CPI
        eac_cpi = ws2.cell(row=r_idx, column=9, value=f"=C{r_idx}/G{r_idx}")
        eac_cpi.number_format = fmt_currency
        
        # EAC (Composite) = AC + (BAC - EV)/(CPI * SPI)
        eac_comp = ws2.cell(row=r_idx, column=10, value=f"=F{r_idx}+(C{r_idx}-E{r_idx})/(G{r_idx}*H{r_idx})")
        eac_comp.number_format = fmt_currency
        
        # EAC (Weighted) = AC + (BAC - EV)/(0.8*CPI + 0.2*SPI)
        eac_weight = ws2.cell(row=r_idx, column=11, value=f"=F{r_idx}+(C{r_idx}-E{r_idx})/(0.8*G{r_idx}+0.2*H{r_idx})")
        eac_weight.number_format = fmt_currency
        
        # VAC = BAC - EAC(CPI)
        vac_cell = ws2.cell(row=r_idx, column=12, value=f"=C{r_idx}-I{r_idx}")
        vac_cell.number_format = fmt_currency
        
        # TCPI = (BAC - EV)/(BAC - AC)
        tcpi_cell = ws2.cell(row=r_idx, column=13, value=f"=(C{r_idx}-E{r_idx})/(C{r_idx}-F{r_idx})")
        tcpi_cell.number_format = fmt_decimal
        
        # Status formula
        status_cell = ws2.cell(row=r_idx, column=14, value=f'=IF(OR(G{r_idx}<0.85, H{r_idx}<0.85, L{r_idx}<-1000000), "CRITICAL", IF(OR(G{r_idx}<0.95, H{r_idx}<0.95), "WARNING", "ON TRACK"))')
        
        # Alignments & Borders
        for c in range(1, 15):
            cell = ws2.cell(row=r_idx, column=c)
            cell.border = thin_bottom
            if c in (1, 14):
                cell.alignment = Alignment(horizontal='center')
            elif c >= 3:
                cell.alignment = Alignment(horizontal='right')
                
        # Status highlights
        if p_id in ("UM-ENG-03", "UM-FPV-01"):
            status_cell.fill = critical_fill
            status_cell.font = critical_font
        else:
            status_cell.fill = ontrack_fill
            status_cell.font = ontrack_font

    # Portfolio Summary Row
    tot_row = 8
    ws2.cell(row=tot_row, column=1, value="SUM PORTEFØLJE").font = bold_font
    ws2.cell(row=tot_row, column=3, value="=SUM(C5:C7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=4, value="=SUM(D5:D7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=5, value="=SUM(E5:E7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=6, value="=SUM(F5:F7)").number_format = fmt_currency
    
    ws2.cell(row=tot_row, column=7, value="=E8/F8").number_format = fmt_decimal # Portfolio CPI
    ws2.cell(row=tot_row, column=8, value="=E8/D8").number_format = fmt_decimal # Portfolio SPI
    
    ws2.cell(row=tot_row, column=9, value="=SUM(I5:I7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=10, value="=SUM(J5:J7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=11, value="=SUM(K5:K7)").number_format = fmt_currency
    ws2.cell(row=tot_row, column=12, value="=C8-I8").number_format = fmt_currency
    ws2.cell(row=tot_row, column=13, value="=(C8-E8)/(C8-F8)").number_format = fmt_decimal
    
    for c in range(1, 15):
        cell = ws2.cell(row=tot_row, column=c)
        cell.font = bold_font
        cell.border = double_bottom
        cell.fill = total_row_fill
        if c >= 3 and c != 14:
            cell.alignment = Alignment(horizontal='right')

    # =========================================================================
    # TAB 3: STATLIG DRIFTSAVSETNING (F-05-20)
    # =========================================================================
    ws3 = wb.create_sheet(title="3. Statlig Avsetning (F-05-20)")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["A1"] = "Statlig Avsetningskontroll — Kunnskapsdepartementets 5,0 % Tak"
    ws3["A1"].font = title_font
    ws3["A2"] = "Regelverk: Finansdepartementets og Kunnskapsdepartementets rundskriv F-05-20"
    ws3["A2"].font = subtitle_font
    
    res_headers = ["Budsjettpost / Parametersammenstilling", "Beløp (NOK)", "Andel av Bevilgning", "Status & Kommentar"]
    for col_idx, text in enumerate(res_headers, 1):
        cell = ws3.cell(row=4, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        
    res_rows = [
        ("Statlig Rammebevilgning (Kap. 260, post 50)", 1200000000, "=B5/B5", "Årlig tildeling over statsbudsjettet"),
        ("Maksimalt Tillatt Driftsavsetning (5.0 %)", "=B5*0.05", "=B6/B5", "Maksimal automatisk overføring til neste år"),
        ("Reell Akkumulert Driftsavsetning (2026-M10)", 72000000, "=B7/B5", "Akkumulert ubrukt bevilgning"),
        ("Overskridelse / Søknadsbeløp til KD", "=MAX(0, B7-B6)", "=B8/B5", "DISPENSASJON PÅKREVD (Risiko for inndragning)")
    ]
    
    for r_idx, (label, val, pct_formula, note) in enumerate(res_rows, 5):
        c1 = ws3.cell(row=r_idx, column=1, value=label)
        c2 = ws3.cell(row=r_idx, column=2, value=val)
        c3 = ws3.cell(row=r_idx, column=3, value=pct_formula)
        c4 = ws3.cell(row=r_idx, column=4, value=note)
        
        c1.font = bold_font
        c2.font = critical_font if r_idx == 8 else bold_font
        c3.font = bold_font
        c4.font = regular_font
        
        c2.number_format = fmt_currency
        c3.number_format = fmt_percent
        c2.alignment = Alignment(horizontal='right')
        c3.alignment = Alignment(horizontal='right')
        
        for c in (c1, c2, c3, c4):
            c.border = thin_bottom
            if r_idx == 8:
                c.fill = critical_fill

    # =========================================================================
    # TAB 4: DFØ REISEREGNING AUDIT
    # =========================================================================
    ws4 = wb.create_sheet(title="4. DFØ Reiseregning Audit")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4["A1"] = "DFØ Internkontroll — Flaggede Reiseregninger & Bilagsavvik"
    ws4["A1"].font = title_font
    ws4["A2"] = "Automatisert atestasjons- og regulativskann for 15 reiseregninger"
    ws4["A2"].font = subtitle_font
    
    audit_headers = ["Reise-ID", "Ansatt / Enhet", "Beløp (NOK)", "Regelbrudd Beskrivelse", "Sperret i Unit4?", "Handlingsregel"]
    for col_idx, text in enumerate(audit_headers, 1):
        cell = ws4.cell(row=4, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        
    audit_data = [
        ("REISE-2026-004", "K. Hansen (Handelshøyskolen)", 6400, "Egengodkjenning (Attektasjon brudd / UiA fullmakt)", "JA", "Omdiriger til instituttleder"),
        ("REISE-2026-014", "M. Olsen (Fakultetsdirektør)", 4800, "Egengodkjenning (Manglende 4-øyne kontroll)", "JA", "Omdiriger til dekan"),
        ("REISE-2026-002", "J. Berg (Institutt for økonomi)", 3100, "Manglende måltidsfradrag (Dekket middag på konferanse)", "NEI", "Korriger diettbeløp"),
        ("REISE-2026-005", "A. Lie (Forskning)", 2200, "Manglende måltidsfradrag (Lunsj inkludert i hotell)", "NEI", "Korriger diettbeløp"),
        ("REISE-2026-007", "E. Strand (Prosjekt admin)", 1450, "Manglende kvittering over 100 NOK (Drosje uten bilag)", "NEI", "Etterspør bilag"),
        ("REISE-2026-011", "P. Nygård (Doktorgradsstipendiat)", 1020, "Manglende originalkvittering (Bankutskrift leveres ikke)", "NEI", "Etterspør bilag"),
        ("REISE-2026-006", "S. Foss (Gjesteforeleser)", 450, "Mangler kjørerutebeskrivelse i kilometergodtgjørelse", "NEI", "Innfordre kjørebok")
    ]
    
    for r_idx, (r_id, emp, val, breach, is_blocked, action) in enumerate(audit_data, 5):
        c1 = ws4.cell(row=r_idx, column=1, value=r_id)
        c2 = ws4.cell(row=r_idx, column=2, value=emp)
        c3 = ws4.cell(row=r_idx, column=3, value=val)
        c4 = ws4.cell(row=r_idx, column=4, value=breach)
        c5 = ws4.cell(row=r_idx, column=5, value=is_blocked)
        c6 = ws4.cell(row=r_idx, column=6, value=action)
        
        c1.font = mono_font
        c2.font = regular_font
        c3.font = bold_font
        c3.number_format = fmt_currency
        c3.alignment = Alignment(horizontal='right')
        c4.font = critical_font if is_blocked == "JA" else warning_font
        c5.font = critical_font if is_blocked == "JA" else bold_font
        c5.alignment = Alignment(horizontal='center')
        c6.font = regular_font
        
        for c in (c1, c2, c3, c4, c5, c6):
            c.border = thin_bottom
            if is_blocked == "JA":
                c.fill = critical_fill
            else:
                c.fill = warning_fill

    # Total Row for Audit
    aud_tot_row = 12
    ws4.cell(row=aud_tot_row, column=1, value="TOTALT AVVIK").font = bold_font
    ws4.cell(row=aud_tot_row, column=3, value="=SUM(C5:C11)").number_format = fmt_currency
    ws4.cell(row=aud_tot_row, column=3).font = critical_font
    ws4.cell(row=aud_tot_row, column=3).alignment = Alignment(horizontal='right')
    
    for c in range(1, 7):
        cell = ws4.cell(row=aud_tot_row, column=c)
        cell.border = double_bottom
        cell.fill = total_row_fill

    # Auto-adjust column widths across all sheets
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
            
    # Save workbook
    wb.save(OUTPUT_FILE)
    
    print(f"Executive Excel report generated successfully:")
    print(f" - Report Path: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_excel_report()
