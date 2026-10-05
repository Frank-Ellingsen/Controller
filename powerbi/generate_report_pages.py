"""
Generates complete Power BI Report Pages and Visual Containers in PBIP format
for 'powerbi/Controller project.Report' conforming to Microsoft Fabric PBIP standards.
"""

import os
import sys
import json
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "powerbi" / "Controller project.Report"
PAGES_DIR = REPORT_DIR / "definition" / "pages"

PAGES_SPEC = [
    {
        "id": "page_01_account_statement",
        "displayName": "📊 Account Statement & Balanse",
        "visuals": [
            {
                "name": "title_card",
                "position": {"x": 40, "y": 30, "width": 1840, "height": 80},
                "type": "textbox",
                "title": "Finance & Project Controls Account Statement (UiA 2026)",
                "subtitle": "8-kolonnes kontostilling: Budsjett, YTD Regnskap, Fremdriftsverdi (EV), Kostnadsavvik (CV) og EAC-prognose"
            },
            {
                "name": "kpi_bac",
                "position": {"x": 40, "y": 130, "width": 280, "height": 130},
                "type": "card",
                "title": "Total Budget (BAC)",
                "measure": "[Total BAC]"
            },
            {
                "name": "kpi_pv",
                "position": {"x": 340, "y": 130, "width": 280, "height": 130},
                "type": "card",
                "title": "Budget YTD (PV)",
                "measure": "[Total PV]"
            },
            {
                "name": "kpi_ev",
                "position": {"x": 640, "y": 130, "width": 280, "height": 130},
                "type": "card",
                "title": "Progress Value (EV)",
                "measure": "[Total EV]"
            },
            {
                "name": "kpi_ac",
                "position": {"x": 940, "y": 130, "width": 280, "height": 130},
                "type": "card",
                "title": "Actual YTD (AC)",
                "measure": "[Total AC]"
            },
            {
                "name": "kpi_cv",
                "position": {"x": 1240, "y": 130, "width": 280, "height": 130},
                "type": "card",
                "title": "Cost Variance (CV)",
                "measure": "[Cost Variance NOK]"
            },
            {
                "name": "kpi_eac",
                "position": {"x": 1540, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Forecast (EAC)",
                "measure": "[EAC Typical CPI]"
            },
            {
                "name": "table_account_statement",
                "position": {"x": 40, "y": 280, "width": 1840, "height": 740},
                "type": "tableEx",
                "title": "Kontostilling Per Prosjekt og Avdeling",
                "columns": ["Dim_Project[project_id]", "Dim_Project[project_name]", "Dim_Project[bac]", "Dim_Project[pv]", "Dim_Project[ev]", "Dim_Project[ac]", "Dim_Project[status]"]
            }
        ]
    },
    {
        "id": "page_02_evm_forecasting",
        "displayName": "📈 EVM Prosjektstyring & EAC",
        "visuals": [
            {
                "name": "title_card",
                "position": {"x": 40, "y": 30, "width": 1840, "height": 80},
                "type": "textbox",
                "title": "EVM Capital Project Controlling & Multi-Model EAC Forecast",
                "subtitle": "Earned Value Analysis, CPI/SPI Indikatorer & Interaktiv Modellvelger"
            },
            {
                "name": "kpi_cpi",
                "position": {"x": 40, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Portfolio CPI",
                "measure": "[Portfolio CPI]"
            },
            {
                "name": "kpi_spi",
                "position": {"x": 400, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Portfolio SPI",
                "measure": "[Portfolio SPI]"
            },
            {
                "name": "kpi_selected_eac",
                "position": {"x": 760, "y": 130, "width": 360, "height": 130},
                "type": "card",
                "title": "Valgt EAC Modell",
                "measure": "[EAC Selected Model]"
            },
            {
                "name": "kpi_vac",
                "position": {"x": 1140, "y": 130, "width": 360, "height": 130},
                "type": "card",
                "title": "Sluttavvik (VAC)",
                "measure": "[VAC Selected Model]"
            },
            {
                "name": "kpi_tcpi",
                "position": {"x": 1520, "y": 130, "width": 360, "height": 130},
                "type": "card",
                "title": "Påkrevd TCPI (BAC)",
                "measure": "[TCPI Target BAC]"
            },
            {
                "name": "slicer_model_parameter",
                "position": {"x": 40, "y": 280, "width": 400, "height": 740},
                "type": "slicer",
                "title": "Velg EAC Prognosemodell",
                "column": "Dim_Model_Parameter[ModelName]"
            },
            {
                "name": "table_evm_details",
                "position": {"x": 460, "y": 280, "width": 1420, "height": 740},
                "type": "tableEx",
                "title": "EVM Prosjektportefølje & Tidsrekke Snapshots",
                "columns": ["Fact_EVM_Snapshots[project_id]", "Fact_EVM_Snapshots[reporting_period]", "Fact_EVM_Snapshots[bac]", "Fact_EVM_Snapshots[ac]", "Fact_EVM_Snapshots[cpi]", "Fact_EVM_Snapshots[spi]", "Fact_EVM_Snapshots[eac_cpi]", "Fact_EVM_Snapshots[eac_composite]", "Fact_EVM_Snapshots[status]"]
            }
        ]
    },
    {
        "id": "page_03_f0520_compliance",
        "displayName": "⚖️ F-05-20 Avsetningskontroll",
        "visuals": [
            {
                "name": "title_card",
                "position": {"x": 40, "y": 30, "width": 1840, "height": 80},
                "type": "textbox",
                "title": "Statlig Rapportering & Kunnskapsdepartementet Rundskriv F-05-20",
                "subtitle": "Driftsavsetningskontroll (Maks 5,0% overføringstak ved 31.12.2026)"
            },
            {
                "name": "kpi_ramme",
                "position": {"x": 40, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Rammebevilgning (Kap 260 p 50)",
                "measure": "[Statlig Rammebevilgning NOK]"
            },
            {
                "name": "kpi_avsetning",
                "position": {"x": 400, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Reell Akkumulert Avsetning",
                "measure": "[Reell Driftsavsetning NOK]"
            },
            {
                "name": "kpi_share_pct",
                "position": {"x": 760, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Avsetningsandel (%)",
                "measure": "[Reserve Share Pct]"
            },
            {
                "name": "kpi_limit_nok",
                "position": {"x": 1120, "y": 130, "width": 340, "height": 130},
                "type": "card",
                "title": "Lovlig 5.0% Grense (NOK)",
                "measure": "[Reserve Cap 5% Limit NOK]"
            },
            {
                "name": "kpi_excess_nok",
                "position": {"x": 1480, "y": 130, "width": 400, "height": 130},
                "type": "card",
                "title": "Overskridelse / Inndragingsrisiko",
                "measure": "[Reserve Cap Excess NOK]"
            },
            {
                "name": "compliance_status_banner",
                "position": {"x": 40, "y": 280, "width": 1840, "height": 740},
                "type": "textbox",
                "title": "Status F-05-20 Overføringsrapport",
                "subtitle": "KRAV OM UOPPFORDRET DISPENSJONSSØKNAD TIL KD PER M10 (REEL AVSETNING 6,0% > 5,0% CAP)"
            }
        ]
    },
    {
        "id": "page_04_travel_audit",
        "displayName": "🔍 Internkontroll Reiseregninger",
        "visuals": [
            {
                "name": "title_card",
                "position": {"x": 40, "y": 30, "width": 1840, "height": 80},
                "type": "textbox",
                "title": "DFØ Reiseregninger & Utlegg Internkontroll",
                "subtitle": "Automatisert etterlevelseskontroll mot Statens reiseregulativ & To-personerskontroll"
            },
            {
                "name": "kpi_total_claims",
                "position": {"x": 40, "y": 130, "width": 420, "height": 130},
                "type": "card",
                "title": "Totalt Skannede Krav",
                "measure": "[Total Scanned Claims Count]"
            },
            {
                "name": "kpi_flagged_claims",
                "position": {"x": 480, "y": 130, "width": 420, "height": 130},
                "type": "card",
                "title": "Flaggede Krav (Avvik)",
                "measure": "[Flagged Claims Count]"
            },
            {
                "name": "kpi_flagged_amount",
                "position": {"x": 920, "y": 130, "width": 480, "height": 130},
                "type": "card",
                "title": "Berørt Beløp med Avvik (NOK)",
                "measure": "[Total Flagged Amount NOK]"
            },
            {
                "name": "kpi_self_approval_breach",
                "position": {"x": 1420, "y": 130, "width": 460, "height": 130},
                "type": "card",
                "title": "Egengodkjente Krav (Brudd)",
                "measure": "[Self-Approval Breach Amount NOK]"
            },
            {
                "name": "table_travel_audit",
                "position": {"x": 40, "y": 280, "width": 1840, "height": 740},
                "type": "tableEx",
                "title": "Reiseregninger Transaksjons- og Avviksliste",
                "columns": ["Fact_Travel_Audit[Reise_ID]", "Fact_Travel_Audit[Ansatt]", "Fact_Travel_Audit[Dato]", "Fact_Travel_Audit[Formaal]", "Fact_Travel_Audit[Belop_NOK]", "Fact_Travel_Audit[BDM_ID]", "Fact_Travel_Audit[Attestant_ID]", "Fact_Travel_Audit[Avvik_Beskrivelse]", "Fact_Travel_Audit[Status]"]
            }
        ]
    },
    {
        "id": "page_05_ubw_audit",
        "displayName": "📜 UBW Hovedbok & Audit",
        "visuals": [
            {
                "name": "title_card",
                "position": {"x": 40, "y": 30, "width": 1840, "height": 80},
                "type": "textbox",
                "title": "Unit4 / UBW Hovedbok & Transaksjonsrevisjon",
                "subtitle": "Fire-Øyne Attestasjonskontroll & Bilagssjekk iht. Reglement for økonomistyring i staten § 14"
            },
            {
                "name": "kpi_ubw_trans_count",
                "position": {"x": 40, "y": 130, "width": 560, "height": 130},
                "type": "card",
                "title": "Totalt Antall UBW Transaksjoner",
                "measure": "[Total UBW Transactions Count]"
            },
            {
                "name": "kpi_ubw_trans_amount",
                "position": {"x": 620, "y": 130, "width": 640, "height": 130},
                "type": "card",
                "title": "Samlet Transaksjonsvolum (NOK)",
                "measure": "[Total UBW Amount NOK]"
            },
            {
                "name": "kpi_ubw_flagged_count",
                "position": {"x": 1280, "y": 130, "width": 600, "height": 130},
                "type": "card",
                "title": "Flaggede Hovedboksposter",
                "measure": "[Flagged UBW Transactions Count]"
            },
            {
                "name": "table_ubw_audit",
                "position": {"x": 40, "y": 280, "width": 1840, "height": 740},
                "type": "tableEx",
                "title": "UBW Journalføring & Segregation of Duties Audit",
                "columns": ["Fact_UBW_Audit[transaksjon_id]", "Fact_UBW_Audit[konto]", "Fact_UBW_Audit[beskrivelse]", "Fact_UBW_Audit[belop_nok]", "Fact_UBW_Audit[bdm_id]", "Fact_UBW_Audit[attestant_id]", "Fact_UBW_Audit[formaal]", "Fact_UBW_Audit[Kontrollflagg]"]
            }
        ]
    }
]

def build_visual_json(v, page_name):
    v_name = v["name"]
    v_type = v["type"]
    pos = v["position"]
    
    vis_obj = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
        "name": v_name,
        "position": {
            "x": pos["x"],
            "y": pos["y"],
            "width": pos["width"],
            "height": pos["height"],
            "z": 1
        },
        "visual": {
            "visualType": v_type,
            "query": {},
            "objects": {}
        }
    }
    
    if v_type == "textbox":
        vis_obj["visual"]["objects"]["general"] = [
            {
                "properties": {
                    "paragraphs": [
                        {
                            "textRuns": [
                                {
                                    "value": v.get("title", ""),
                                    "textStyle": {"fontWeight": "bold", "fontSize": "16pt", "color": "#F8FAFC"}
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    return vis_obj

def generate_powerbi_reports():
    print("=== START: Generating Power BI Report Pages & Visual Containers ===")
    
    # 1. Clean existing pages directory except base files
    if PAGES_DIR.exists():
        shutil.rmtree(PAGES_DIR)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    page_order = []
    
    for page in PAGES_SPEC:
        p_id = page["id"]
        p_title = page["displayName"]
        page_order.append(p_id)
        
        p_dir = PAGES_DIR / p_id
        p_dir.mkdir(parents=True, exist_ok=True)
        
        # Write page.json
        page_json_content = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": p_id,
            "displayName": p_title,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }
        
        with open(p_dir / "page.json", "w", encoding="utf-8") as f:
            json.dump(page_json_content, f, indent=2)
            
        # Write visuals subfolder
        vis_dir = p_dir / "visuals"
        vis_dir.mkdir(parents=True, exist_ok=True)
        
        for v in page["visuals"]:
            v_id = v["name"]
            v_sub = vis_dir / v_id
            v_sub.mkdir(parents=True, exist_ok=True)
            
            v_json = build_visual_json(v, p_id)
            with open(v_sub / "visual.json", "w", encoding="utf-8") as f:
                json.dump(v_json, f, indent=2)
                
        print(f"  + Generated Report Page: {p_title} ({p_id}) with {len(page['visuals'])} visuals")
        
    # Write pages.json metadata
    pages_meta = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": page_order,
        "activePageName": page_order[0]
    }
    
    with open(PAGES_DIR / "pages.json", "w", encoding="utf-8") as f:
        json.dump(pages_meta, f, indent=2)
        
    print(f"\nReport Pages metadata updated at: {PAGES_DIR / 'pages.json'}")
    print("=== SLUTT: Power BI Rapportpopulering Fullført ===")

if __name__ == "__main__":
    generate_powerbi_reports()
