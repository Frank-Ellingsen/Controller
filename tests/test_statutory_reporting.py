"""
Unit tests for Statutory & State Reporting Engine (statutory_reporting_engine.py)
Verifies KD F-05-20 reserve compliance, DBH metrics, and Riksrevisjonen audit checks.
"""

import sys
from pathlib import Path
import pytest

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

# Also support v22 inner path if needed
V22_TOOLS = Path(__file__).resolve().parent.parent / "uia-controller-app-v22" / "uia-controller-app" / "src" / "tools"
if V22_TOOLS.exists():
    sys.path.append(str(V22_TOOLS))

from statutory_reporting_engine import (
    get_dbh_reporting_metrics,
    verify_kd_statutory_compliance,
    format_statutory_report_summary
)

def test_dbh_reporting_metrics():
    dbh = get_dbh_reporting_metrics()
    assert isinstance(dbh, dict)
    assert dbh["rapporteringsar"] == 2026
    assert "studiepoeng_stp_produksjon" in dbh
    assert dbh["studiepoeng_stp_produksjon"]["totalt_stp"] == 278500
    assert dbh["studiepoeng_stp_produksjon"]["mål_oppnåelse_pct"] == 102.4
    assert dbh["uteksaminerte_kandidater"]["phd_avlagte_grader"] == 42
    assert dbh["forskning_nvi_poeng"]["samlet_nvi_poeng"] == 895.4

def test_verify_kd_statutory_compliance_compliant():
    # Test reserve <= 5% (e.g. 50M out of 1.2B -> 4.17%)
    res = verify_kd_statutory_compliance(
        rammebevilgning_nok=1200000000.0,
        akkumulert_avsetning_nok=50000000.0
    )
    assert res["f0520_avsetning_pct"] == 4.17
    assert res["f0520_overskridelse_nok"] == 0.0
    assert res["f0520_status"] == "COMPLIANT"

def test_verify_kd_statutory_compliance_non_compliant():
    # Test reserve > 5% (e.g. 72M out of 1.2B -> 6.0%)
    res = verify_kd_statutory_compliance(
        rammebevilgning_nok=1200000000.0,
        akkumulert_avsetning_nok=72000000.0
    )
    assert res["f0520_avsetning_pct"] == 6.0
    assert res["f0520_overskridelse_nok"] == 12000000.0
    assert res["f0520_status"] == "NON_COMPLIANT_DISPENSATION_NEEDED"
    assert len(res["sjekkliste_statlig_rapportering"]) == 5

def test_format_statutory_report_summary():
    report = format_statutory_report_summary()
    assert isinstance(report, str)
    assert "# Lovpålagt Rapportering til Stat og Universitet" in report
    assert "Kunnskapsdepartementet" in report
    assert "DBH / HK-dir" in report
    assert "278 500 STP" in report
