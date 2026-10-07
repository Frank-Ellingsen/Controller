"""
Canonical Domain Models for UiA Controlling & Financial App (v27)
Encapsulates domain entities and business rules cleanly, eliminating hardcoded values.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class RegulationRules(BaseModel):
    f0520_max_reserve_pct: float = 0.05
    receipt_requirement_threshold_nok: float = 100.0
    small_purchase_exception_limit_nok: float = 5000.0
    storage_retention_years_standard: int = 10

class DepartmentConfig(BaseModel):
    code: str
    name: str
    share_pct: float

class CanonicalProject(BaseModel):
    project_id: str
    project_name: str
    department_code: str
    bac_nok: float
    pv_nok: float
    ev_nok: float
    ac_nok: float
    tag: str = "2026_Canonical"

    @property
    def cpi(self) -> float:
        return round(self.ev_nok / self.ac_nok, 2) if self.ac_nok > 0 else 1.0

    @property
    def spi(self) -> float:
        return round(self.ev_nok / self.pv_nok, 2) if self.pv_nok > 0 else 1.0

    @property
    def cost_variance_nok(self) -> float:
        return round(self.ev_nok - self.ac_nok, 2)

    @property
    def schedule_variance_nok(self) -> float:
        return round(self.ev_nok - self.pv_nok, 2)

    @property
    def eac_typical_nok(self) -> float:
        return round(self.bac_nok / self.cpi, 2) if self.cpi > 0 else self.bac_nok

    @property
    def eac_composite_nok(self) -> float:
        comp_idx = self.cpi * self.spi
        return round(self.ac_nok + (self.bac_nok - self.ev_nok) / comp_idx, 2) if comp_idx > 0 else self.bac_nok

    @property
    def vac_nok(self) -> float:
        return round(self.bac_nok - self.eac_typical_nok, 2)

    @property
    def etc_nok(self) -> float:
        return round(self.eac_typical_nok - self.ac_nok, 2)

    @property
    def tcpi(self) -> float:
        rem_work = self.bac_nok - self.ev_nok
        rem_fund = self.bac_nok - self.ac_nok
        return round(rem_work / rem_fund, 2) if rem_fund > 0 else 9.99

    @property
    def status(self) -> str:
        if self.cpi < 0.85 or self.spi < 0.85 or self.vac_nok < -1000000.0:
            return "CRITICAL"
        elif self.cpi < 0.95 or self.spi < 0.95:
            return "WARNING"
        return "ON TRACK"

class AccountStatementRow(BaseModel):
    unit_code: str
    account_name: str
    total_budget_fy_nok: float
    budget_ytd_nok: float
    actual_ytd_nok: float
    progress_value_nok: float

    @property
    def cost_variance_ytd_nok(self) -> float:
        return round(self.progress_value_nok - self.actual_ytd_nok, 2)

    @property
    def cpi(self) -> float:
        return (self.progress_value_nok / self.actual_ytd_nok) if self.actual_ytd_nok > 0 else 1.0

    @property
    def forecast_eoy_nok(self) -> float:
        return round(self.total_budget_fy_nok / self.cpi, 2) if self.cpi > 0 else self.total_budget_fy_nok

    @property
    def forecast_variance_eoy_nok(self) -> float:
        return round(self.total_budget_fy_nok - self.forecast_eoy_nok, 2)

class SCurvePoint(BaseModel):
    month: str
    month_label: str
    cum_pv_mnok: float
    cum_ev_mnok: float
    cum_ac_mnok: float
    eac_forecast_mnok: Optional[float] = None
    is_forecast: bool = False

class MasterState(BaseModel):
    organization_name: str = "Universitetet i Agder (UiA)"
    reporting_period: str = "2026-M10"
    regulations: RegulationRules = RegulationRules()
    departments: Dict[str, DepartmentConfig] = {}
    department_statements: List[AccountStatementRow] = []
    projects: List[CanonicalProject] = []
    scurve_time_series: List[SCurvePoint] = []
