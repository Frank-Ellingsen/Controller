import sys
from pathlib import Path
import pytest

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from action_engine import calculate_baseline_status, simulate_action_plan, format_action_plan_report

def test_baseline_status_calculation():
    baseline = calculate_baseline_status()
    assert isinstance(baseline, dict)
    assert baseline["rammebevilgning"] == 1200000000.0
    assert baseline["baseline_avsetning"] == 72000000.0
    assert baseline["grense_5_pct"] == 60000000.0
    assert baseline["baseline_overskridelse"] == 12000000.0
    assert "projects" in baseline
    assert "travel" in baseline
    assert "UM-ENG-03" in baseline["projects"]

def test_simulate_action_plan_defaults():
    sim = simulate_action_plan(
        descoping_pct=20.0,
        investments_activated_nok=12000000.0,
        travel_enforcement_pct=100.0,
        kd_application=True
    )
    assert isinstance(sim, dict)
    assert "savings" in sim
    assert "revised_eoy_balance" in sim
    assert "revised_projects" in sim

    # Check F-05-20 compliance achieved via 12M investment activation
    eoy = sim["revised_eoy_balance"]
    assert eoy["revised_avsetning"] == 60000000.0
    assert eoy["revised_avsetning_pct"] == 5.0
    assert eoy["revised_overskridelse"] == 0.0
    assert "COMPLIANT" in eoy["f0520_status"]

    # Check EVM descoping savings
    savings = sim["savings"]
    assert savings["evm_eng_savings"] > 0
    assert savings["evm_fpv_savings"] > 0
    assert savings["total_evm_savings"] > 6000000.0
    assert savings["travel_savings"] == 5300.0

def test_format_action_plan_report():
    sim = simulate_action_plan(descoping_pct=20.0, investments_activated_nok=12000000.0)
    report = format_action_plan_report(sim)
    assert isinstance(report, str)
    assert "# Tiltaksplan og Revidert Årsprognose" in report
    assert "F-05-20 Driftsavsetning" in report
    assert "COMPLIANT" in report
    assert "UM-ENG-03" in report
