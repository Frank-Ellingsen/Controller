import pytest
import sys
from pathlib import Path

# Add src/tools to path
tools_dir = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.insert(0, str(tools_dir))

from budget_engine import get_annual_wheel_calendar, build_next_year_budget, calculate_tdi_project_budget, get_2026_budget_vs_actuals_ytd

def test_annual_wheel_calendar():
    df = get_annual_wheel_calendar()
    assert not df.empty
    assert len(df) == 7
    assert "Frist/Milepæl" in df.columns
    assert "Ansvarlig" in df.columns
    assert "Status" in df.columns
    assert "Budget Specialist" in df["Ansvarlig"].values

def test_build_next_year_budget_calculations():
    res = build_next_year_budget(
        current_ramme_nok=1_000_000_000.0,
        price_inflation_pct=3.0,
        result_adjustment_nok=10_000_000.0,
        strategic_reserve_pct=2.0
    )
    assert res["grunnlag_inneværende_år_nok"] == 1_000_000_000.0
    assert res["pris_og_lonnsjustering_nok"] == 30_000_000.0
    assert res["ny_brutto_ramme_nok"] == 1_040_000_000.0
    assert res["strategisk_avsetning_styret_nok"] == 20_800_000.0
    assert res["netto_fordelt_fakultetene_nok"] == 1_019_200_000.0
    
    # Check department allocation sum
    dept_sum = sum(res["fakultetsfordeling"].values())
    assert abs(dept_sum - res["netto_fordelt_fakultetene_nok"]) < 10.0  # roundoff tolerance

def test_calculate_tdi_project_budget():
    tdi = calculate_tdi_project_budget(
        direct_salary_nok=1_000_000.0,
        direct_operating_nok=200_000.0,
        overhead_pct=45.0
    )
    assert tdi["direkte_lonn_nok"] == 1_000_000.0
    assert tdi["direkte_drift_nok"] == 200_000.0
    assert tdi["indirekte_kostnader_tdi_nok"] == 540_000.0
    assert tdi["totalkostnad_tdi_nok"] == 1_740_000.0
    assert tdi["overhead_prosent"] == 45.0

def test_get_2026_budget_vs_actuals_ytd():
    df = get_2026_budget_vs_actuals_ytd(tag="test2026T1")
    assert not df.empty
    assert "Avdeling" in df.columns
    assert "Budsjett_2026_FY_NOK" in df.columns
    assert "Budsjett_YTD_Aug_NOK" in df.columns
    assert "Regnskap_YTD_Aug_NOK" in df.columns
    assert "Avvik_YTD_NOK" in df.columns
    assert "Avvik_YTD_Pct" in df.columns
    assert "Prognose_2026_EOY_NOK" in df.columns
    assert "Tag" in df.columns
    assert len(df) == 4
    assert "Handelshøyskolen" in df["Avdeling"].values

