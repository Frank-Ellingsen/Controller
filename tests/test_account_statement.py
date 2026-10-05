"""
Test Suite for Finance & Project Controls Account Statement Engine (v23)
Verifies 8-column Account Statement layout, formulas, and export functionality.
"""

from pathlib import Path
import pytest
import pandas as pd
import openpyxl

current_dir = Path(__file__).resolve().parent
if "uia-controller-app" in current_dir.parent.name:
    ROOT_DIR = current_dir.parent.parent
else:
    ROOT_DIR = current_dir.parent

import sys
sys.path.append(str(ROOT_DIR / "src" / "tools"))

from account_statement_engine import (
    get_sample_project_controls_statement,
    generate_uia_department_account_statement,
    export_account_statements
)
from antigravity_workflow import execute_monthly_close_v23

def test_sample_project_controls_statement():
    df = get_sample_project_controls_statement()
    
    # Check columns
    expected_cols = [
        "Account", "Total Budget", "Budget YTD", "Actual YTD", 
        "Progress Value", "Cost Variance", "Forecast", "Forecast Variance"
    ]
    assert list(df.columns) == expected_cols
    
    # Check rows (Engineering, Procurement, Construction, Total)
    assert len(df) == 4
    assert df.iloc[-1]["Account"] == "Total"
    
    # Check Total calculation accuracy
    total_budget = df.iloc[:-1]["Total Budget"].sum()
    assert df.iloc[-1]["Total Budget"] == round(total_budget, 1)

def test_uia_department_account_statement():
    df = generate_uia_department_account_statement()
    
    # Check columns and length
    assert len(df.columns) == 8
    assert len(df) == 5
    assert df.iloc[-1]["Account"] == "Total UiA Ramme"
    
    # Check positive / negative cost variances present
    assert any(df["Cost Variance"] < 0)
    assert any(df["Cost Variance"] > 0)

def test_export_account_statements(tmp_path):
    out_dir = str(tmp_path)
    res = export_account_statements(output_dir=out_dir)
    
    csv_sample = Path(res["sample_statement_csv"])
    csv_uia = Path(res["uia_statement_csv"])
    
    assert csv_sample.exists()
    assert csv_uia.exists()
    assert csv_sample.stat().st_size > 100
    assert csv_uia.stat().st_size > 100

def test_execute_monthly_close_v23(tmp_path):
    # Test v23 pipeline execution
    p_dir = str(tmp_path / "parquet")
    execute_monthly_close_v23(parquet_dir=p_dir)
    
    assert (tmp_path / "parquet" / "Fact_Account_Statement_ProjectControls.parquet").exists()
    assert (tmp_path / "parquet" / "Fact_Account_Statement_UiA.parquet").exists()
