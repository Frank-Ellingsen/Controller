import sys
from pathlib import Path
import pytest

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from audit_travel_expenses import audit_travel_claims

def test_travel_claim_audit():
    result = audit_travel_claims()
    assert isinstance(result, dict)
    assert "summary" in result
    assert "findings" in result
    
    summary = result["summary"]
    assert summary["totalt_behandlet"] == 15
    assert summary["avvik_claims"] == 7
    assert summary["belop_med_avvik_nok"] == 19420.0
    
    # Verify self-approval findings (Rule 2)
    self_approval_findings = [f for f in result["findings"] if any("FIRE_OYNE" in v for v in f["Avvik"])]
    assert len(self_approval_findings) == 2
    for item in self_approval_findings:
        assert item["Reise_ID"] in ["REISE-2026-004", "REISE-2026-014"]
