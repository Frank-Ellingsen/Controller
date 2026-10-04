import sys
from pathlib import Path
import pytest
import os
import openpyxl

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from powerbi_exporter import export_powerbi_data_model
from generate_excel_report import create_excel_report

def test_powerbi_parquet_exporter(tmp_path):
    exported = export_powerbi_data_model(output_dir=str(tmp_path))
    assert isinstance(exported, dict)
    assert "Fact_EVM_Snapshots" in exported
    assert "Dim_Project" in exported
    assert "Fact_Travel_Audit" in exported
    
    for table_name, filepath in exported.items():
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0

def test_excel_reporter_generation():
    create_excel_report()
    report_file = Path(__file__).resolve().parent.parent / "data" / "reports" / "UiA_Controller_Maanedsoppgjoer_2026-M10.xlsx"
    assert report_file.exists()
    assert report_file.stat().st_size > 0
    
    wb = openpyxl.load_workbook(report_file, data_only=False)
    sheet_names = wb.sheetnames
    assert "1. Sammendrag & Status" in sheet_names
    assert "2. EVM Prosjektkontroll" in sheet_names
    assert "3. Statlig Avsetning (F-05-20)" in sheet_names
    assert "4. DFØ Reiseregning Audit" in sheet_names
    
    ws2 = wb["2. EVM Prosjektkontroll"]
    assert str(ws2["G5"].value).startswith("=")  # Formel for CPI
