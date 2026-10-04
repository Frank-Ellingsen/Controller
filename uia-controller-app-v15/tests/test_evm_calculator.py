import sys
from pathlib import Path
import pytest
import pandas as pd

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from evm_calculator import calculate_evm_from_db, generate_evm_report

def test_evm_calculation_execution():
    df = calculate_evm_from_db()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 3

def test_evm_metrics_columns():
    df = calculate_evm_from_db()
    expected_cols = ["project_id", "bac", "pv", "ev", "ac", "CPI", "SPI", "CV", "SV", "EAC", "VAC", "ETC", "TCPI", "Status"]
    for col in expected_cols:
        assert col in df.columns

def test_evm_formula_accuracy():
    df = calculate_evm_from_db()
    # Check UM-DEF-02 row
    row_def = df[df["project_id"] == "UM-DEF-02"].iloc[0]
    # CPI = EV / AC = 12200000 / 11800000 = 1.0338 -> rounded 1.03
    assert row_def["CPI"] == 1.03
    # SPI = EV / PV = 12200000 / 12000000 = 1.0166 -> rounded 1.02
    assert row_def["SPI"] == 1.02
    assert row_def["Status"] == "ON TRACK"

def test_evm_critical_status():
    df = calculate_evm_from_db()
    row_eng = df[df["project_id"] == "UM-ENG-03"].iloc[0]
    assert row_eng["Status"] == "CRITICAL"
    assert row_eng["TCPI"] > 2.0

def test_evm_report_string_generation():
    report = generate_evm_report()
    assert "PROJECT CONTROLLER MONTHLY PERFORMANCE REVIEW" in report
    assert "UM-DEF-02" in report
    assert "CRITICAL" in report
