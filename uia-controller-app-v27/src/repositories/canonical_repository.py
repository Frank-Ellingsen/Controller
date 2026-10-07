"""
Canonical Repository & Data Access Layer for UiA Controlling App (v27)
Decouples database and storage layers from business logic and hydrates domain models.
"""

from pathlib import Path
import sys
import sqlite3
import pandas as pd
import yaml
import json
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

CONFIG_PATH = BASE_DIR / "data" / "config" / "system_config.yaml"
DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
CSV_DRILLDOWN = BASE_DIR / "data" / "staging" / "fakultet_drilldown_statement_2026.csv"
OUTPUT_STATE_JSON = BASE_DIR / "data" / "staging" / "master_state.json"

from src.models.canonical import (
    MasterState,
    RegulationRules,
    DepartmentConfig,
    CanonicalProject,
    AccountStatementRow,
    SCurvePoint
)

class CanonicalRepository:
    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config_path = config_path
        self.raw_config = self._load_config()

    def _load_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get_regulations(self) -> RegulationRules:
        reg = self.raw_config.get("regulations", {})
        return RegulationRules(
            f0520_max_reserve_pct=reg.get("f0520_max_reserve_pct", 0.05),
            receipt_requirement_threshold_nok=reg.get("receipt_requirement_threshold_nok", 100.0),
            small_purchase_exception_limit_nok=reg.get("small_purchase_exception_limit_nok", 5000.0),
            storage_retention_years_standard=reg.get("storage_retention_years_standard", 10)
        )

    def get_departments(self) -> Dict[str, DepartmentConfig]:
        depts = self.raw_config.get("departments", {})
        res = {}
        for code, data in depts.items():
            if isinstance(data, dict):
                res[code] = DepartmentConfig(
                    code=code,
                    name=data.get("name", code),
                    share_pct=data.get("share_pct", 0.0)
                )
            else:
                res[code] = DepartmentConfig(code=code, name=str(data), share_pct=0.1)
        return res

    def get_projects(self, db_path: Path = DB_PATH) -> List[CanonicalProject]:
        if not db_path.exists():
            return []
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM evm_projects", conn)
        conn.close()

        projects = []
        for _, r in df.iterrows():
            projects.append(CanonicalProject(
                project_id=str(r.get('project_id', r.get('Project_ID', ''))),
                project_name=str(r.get('project_name', r.get('Project_Name', ''))),
                department_code=str(r.get('avdeling', r.get('Avdeling', 'TN'))),
                bac_nok=float(r.get('bac', r.get('BAC_NOK', 0.0))),
                pv_nok=float(r.get('pv', r.get('PV_NOK', 0.0))),
                ev_nok=float(r.get('ev', r.get('EV_NOK', 0.0))),
                ac_nok=float(r.get('ac', r.get('AC_NOK', 0.0))),
                tag=str(r.get('tag', '2026_Canonical'))
            ))
        return projects

    def get_department_statements(self) -> List[AccountStatementRow]:
        if not CSV_DRILLDOWN.exists():
            return []
        df_raw = pd.read_csv(CSV_DRILLDOWN)
        df_costs = df_raw[df_raw["Kategori"].isin(["5xxx Lønn", "6xxx Drift", "7xxx Reiser"])]
        
        unit_grp = df_costs.groupby(["Avdeling_Kode", "Avdeling"]).agg({
            "Total_Budget_FY_NOK": "sum",
            "Budget_YTD_Oct_NOK": "sum",
            "Actual_YTD_Oct_NOK": "sum",
            "Progress_Value_Oct_NOK": "sum"
        }).reset_index()

        rows = []
        for _, r in unit_grp.iterrows():
            rows.append(AccountStatementRow(
                unit_code=r["Avdeling_Kode"],
                account_name=r["Avdeling"],
                total_budget_fy_nok=round(r["Total_Budget_FY_NOK"], 2),
                budget_ytd_nok=round(r["Budget_YTD_Oct_NOK"], 2),
                actual_ytd_nok=round(r["Actual_YTD_Oct_NOK"], 2),
                progress_value_nok=round(r["Progress_Value_Oct_NOK"], 2)
            ))
        return rows

    def get_scurve_time_series(self) -> List[SCurvePoint]:
        months = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"]
        labels = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
        
        base_pv = 172.92
        time_series = []
        for i in range(12):
            m = months[i]
            lbl = labels[i]
            cum_pv = round(base_pv * (i + 1), 1)
            
            if i <= 9: # Up to M10
                cum_ev = round(base_pv * (i + 1) * 0.99, 1)
                cum_ac = round(base_pv * (i + 1) * 0.985, 1)
                eac_f = None
                is_f = False
            else: # M11, M12
                cum_ev = round(base_pv * (i + 1) * 0.99, 1)
                cum_ac = round(base_pv * (i + 1) * 0.985, 1)
                eac_f = round(1703.5 + (base_pv * (i - 9) * 0.985), 1)
                is_f = True
                
            time_series.append(SCurvePoint(
                month=m,
                month_label=lbl,
                cum_pv_mnok=cum_pv,
                cum_ev_mnok=cum_ev,
                cum_ac_mnok=cum_ac,
                eac_forecast_mnok=eac_f,
                is_forecast=is_f
            ))
        return time_series

    def build_master_state(self) -> MasterState:
        return MasterState(
            organization_name="Universitetet i Agder (UiA)",
            reporting_period="2026-M10",
            regulations=self.get_regulations(),
            departments=self.get_departments(),
            department_statements=self.get_department_statements(),
            projects=self.get_projects(),
            scurve_time_series=self.get_scurve_time_series()
        )

    def export_master_state_json(self, output_path: Path = OUTPUT_STATE_JSON) -> Path:
        state = self.build_master_state()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        state_dict = state.model_dump()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(state_dict, f, indent=2, ensure_ascii=False)
            
        return output_path

if __name__ == "__main__":
    repo = CanonicalRepository()
    json_path = repo.export_master_state_json()
    print(f"Canonical Master State successfully exported to: {json_path}")
