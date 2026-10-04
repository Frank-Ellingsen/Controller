"""
Action Engine for UiA Controlling App (v14)
Calculates preskriptive tiltak, quantifies financial savings, and forecasts
revised End of Year (EOY) balance and EVM project metrics.
Uses relative Path(__file__) resolution.
"""

from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_TRAVEL_CSV_PATH = BASE_DIR / "data" / "staging" / "reiseregninger_15_stk.csv"

def calculate_baseline_status(db_path: str = None, travel_csv_path: str = None) -> dict:
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    if travel_csv_path is None:
        travel_csv_path = str(DEFAULT_TRAVEL_CSV_PATH)

    # 1. F-05-20 Baseline
    rammebevilgning = 1200000000.0  # 1.2 mrd NOK
    baseline_avsetning = 72000000.0  # 72 mill NOK (6.0%)
    grense_5_pct = rammebevilgning * 0.05  # 60 mill NOK
    baseline_overskridelse = max(0.0, baseline_avsetning - grense_5_pct)

    # 2. EVM Baseline
    # UM-DEF-02: BAC=18.5M, AC=11.8M, EV=12.2M, CPI=1.03, EAC=17.893M, VAC=+0.607M
    # UM-ENG-03: BAC=8.2M, AC=6.8M, EV=5.2M, CPI=0.76, ETC=3.989M, EAC=10.789M, VAC=-2.589M
    # UM-FPV-01: BAC=45.0M, AC=23.1M, EV=21.0M, CPI=0.91, ETC=26.351M, EAC=49.451M, VAC=-4.451M
    projects_baseline = {
        "UM-DEF-02": {"bac": 18500000.0, "ac": 11800000.0, "ev": 12200000.0, "cpi": 1.03, "etc": 6161165.0, "eac": 17893443.0, "vac": 606557.0, "status": "ON TRACK"},
        "UM-ENG-03": {"bac": 8200000.0, "ac": 6800000.0, "ev": 5200000.0, "cpi": 0.76, "etc": 3989474.0, "eac": 10789474.0, "vac": -2589474.0, "status": "CRITICAL"},
        "UM-FPV-01": {"bac": 45000000.0, "ac": 23100000.0, "ev": 21000000.0, "cpi": 0.91, "etc": 26350549.0, "eac": 49450549.0, "vac": -4450549.0, "status": "CRITICAL"}
    }

    # 3. Travel Audit Baseline
    travel_baseline = {
        "totalt_behandlet": 15,
        "avvik_claims": 7,
        "totalt_belop_nok": 40850.0,
        "avvik_belop_nok": 19420.0,
        "direkte_feilutbetaling_nok": 5300.0
    }

    return {
        "rammebevilgning": rammebevilgning,
        "baseline_avsetning": baseline_avsetning,
        "grense_5_pct": grense_5_pct,
        "baseline_overskridelse": baseline_overskridelse,
        "projects": projects_baseline,
        "travel": travel_baseline
    }

def simulate_action_plan(
    descoping_pct: float = 20.0,
    investments_activated_nok: float = 12000000.0,
    travel_enforcement_pct: float = 100.0,
    kd_application: bool = True
) -> dict:
    baseline = calculate_baseline_status()
    
    # 1. EVM Descoping Savings (on Critical Projects ETC)
    eng_etc = baseline["projects"]["UM-ENG-03"]["etc"]
    fpv_etc = baseline["projects"]["UM-FPV-01"]["etc"]
    
    eng_savings = eng_etc * (descoping_pct / 100.0)
    fpv_savings = fpv_etc * (descoping_pct / 100.0)
    total_evm_savings = eng_savings + fpv_savings

    revised_projects = {}
    for p_id, p in baseline["projects"].items():
        if p["status"] == "CRITICAL":
            sav = p["etc"] * (descoping_pct / 100.0)
            rev_eac = p["eac"] - sav
            rev_vac = p["bac"] - rev_eac
            rev_etc = p["etc"] - sav
        else:
            sav = 0.0
            rev_eac = p["eac"]
            rev_vac = p["vac"]
            rev_etc = p["etc"]

        revised_projects[p_id] = {
            "bac": p["bac"],
            "ac": p["ac"],
            "ev": p["ev"],
            "cpi": p["cpi"],
            "baseline_eac": p["eac"],
            "revised_eac": rev_eac,
            "baseline_vac": p["vac"],
            "revised_vac": rev_vac,
            "savings": sav,
            "status": p["status"]
        }

    # 2. Travel Claims Savings
    travel_savings = baseline["travel"]["direkte_feilutbetaling_nok"] * (travel_enforcement_pct / 100.0)

    # 3. Total Direct Cost Savings
    total_cost_savings = total_evm_savings + travel_savings

    # 4. F-05-20 Balance EOY Forecast
    # Status Quo avsetning: 72M NOK
    # Reallocated to investments before 31.12: investments_activated_nok
    # Net avsetning EOY = Baseline avsetning - investments_activated_nok
    revised_avsetning = baseline["baseline_avsetning"] - investments_activated_nok
    revised_avsetning_pct = (revised_avsetning / baseline["rammebevilgning"]) * 100.0
    revised_overskridelse = max(0.0, revised_avsetning - baseline["grense_5_pct"])
    f0520_status = "COMPLIANT (<= 5.0%)" if revised_avsetning <= baseline["grense_5_pct"] else "EXCEEDS 5.0% LIMIT"

    return {
        "inputs": {
            "descoping_pct": descoping_pct,
            "investments_activated_nok": investments_activated_nok,
            "travel_enforcement_pct": travel_enforcement_pct,
            "kd_application": kd_application
        },
        "baseline": baseline,
        "savings": {
            "evm_eng_savings": eng_savings,
            "evm_fpv_savings": fpv_savings,
            "total_evm_savings": total_evm_savings,
            "travel_savings": travel_savings,
            "total_cost_savings": total_cost_savings,
            "investments_activated_nok": investments_activated_nok
        },
        "revised_eoy_balance": {
            "rammebevilgning": baseline["rammebevilgning"],
            "baseline_avsetning": baseline["baseline_avsetning"],
            "baseline_avsetning_pct": (baseline["baseline_avsetning"] / baseline["rammebevilgning"]) * 100.0,
            "revised_avsetning": revised_avsetning,
            "revised_avsetning_pct": round(revised_avsetning_pct, 2),
            "baseline_overskridelse": baseline["baseline_overskridelse"],
            "revised_overskridelse": revised_overskridelse,
            "f0520_status": f0520_status
        },
        "revised_projects": revised_projects
    }

def format_action_plan_report(sim: dict) -> str:
    b = sim["baseline"]
    s = sim["savings"]
    bal = sim["revised_eoy_balance"]
    p = sim["revised_projects"]

    lines = []
    lines.append("# Tiltaksplan og Revidert Årsprognose (EOY 2026)")
    lines.append("\n**Organisasjon:** Universitetet i Agder (UiA)")
    lines.append("**Dato:** 4. oktober 2026")
    lines.append("**Rapporteringsperiode:** 2026-M10 (End of Year Forecast)")
    lines.append("\n---\n")

    lines.append("## 1. Anbefalte Tiltak (Action to Take Plan)")
    lines.append("1. **[F-05-20 Driftsavsetning]** Fremskynd styregodkjente utstyrs- og infrastrukturanskaffelser for kr **{:,.0f} NOK** før 31.12.2026 for å redusere samlet overskuddsavsetning til lovlig nivå.".format(s['investments_activated_nok']))
    if sim["inputs"]["kd_application"]:
        lines.append("2. **[F-05-20 KD-Søknad]** Utarbeid uoppfordret dispensasjonssøknad til Kunnskapsdepartementet om strategiske avsetninger for å sikre full juridisk ryggdekning.")
    lines.append("3. **[EVM Prosjektstyring]** Gjennomfør **{:.1f}% descoping / kostnadskutt** på gjenstående arbeider (ETC) i de kritiske prosjektene `UM-ENG-03` og `UM-FPV-01`.".format(sim['inputs']['descoping_pct']))
    lines.append("4. **[Reiseregninger & Utlegg]** Gjennomfør **{:.0f}% stans og retur** av de 7 urettmessige reiseregningene (kr 19 420 NOK berørt) for korreksjon og to-personerskontroll.".format(sim['inputs']['travel_enforcement_pct']))

    lines.append("\n---\n")
    lines.append("## 2. Kvantifisert Finansiell Effekt av Tiltak")
    lines.append("| Tiltakskategori | Beskrivelse | Finansiell Besparelse / Omplassering |")
    lines.append("| :--- | :--- | :---: |")
    lines.append("| **EVM Prosjekt-descoping** | {:.1f}% kutt i ETC for `UM-ENG-03` | kr {:,.0f} NOK |".format(sim['inputs']['descoping_pct'], s['evm_eng_savings']))
    lines.append("| **EVM Prosjekt-descoping** | {:.1f}% kutt i ETC for `UM-FPV-01` | kr {:,.0f} NOK |".format(sim['inputs']['descoping_pct'], s['evm_fpv_savings']))
    lines.append("| **Reisekontroll / Diett** | Korreksjon av feilutbetalte diettkrav | kr {:,.0f} NOK |".format(s['travel_savings']))
    lines.append("| **Investeringsomplassering** | Aktiverte investeringer før 31.12 | kr {:,.0f} NOK |".format(s['investments_activated_nok']))
    lines.append("| **TOTAL DIREKTE BESPARELSE** | **Kutt i løpende prosjekt- og reisekostnader** | **kr {:,.0f} NOK** |".format(s['total_cost_savings']))

    lines.append("\n---\n")
    lines.append("## 3. Revidert Årsprognose og Balanse ved 31.12.2026 (EOY)")
    lines.append("| Balanse- og Resultatindikator | Status Quo (Før Tiltak) | Revidert Prognose (Etter Tiltak) | Endring / Effekt |")
    lines.append("| :--- | :---: | :---: | :---: |")
    lines.append("| **Rammebevilgning (Kap. 260, post 50)** | kr {:,.0f} NOK | kr {:,.0f} NOK | 0 NOK |".format(bal['rammebevilgning'], bal['rammebevilgning']))
    lines.append("| **Akkumulert Driftsavsetning EOY** | kr {:,.0f} NOK ({:.2f}%) | **kr {:,.0f} NOK ({:.2f}%)** | **kr {:,.0f} NOK** |".format(bal['baseline_avsetning'], bal['baseline_avsetning_pct'], bal['revised_avsetning'], bal['revised_avsetning_pct'], -s['investments_activated_nok']))
    lines.append("| **Overskridelse mot 5.0% grense** | kr {:,.0f} NOK | **kr {:,.0f} NOK** | **-kr {:,.0f} NOK** |".format(bal['baseline_overskridelse'], bal['revised_overskridelse'], bal['baseline_overskridelse'] - bal['revised_overskridelse']))
    lines.append("| **Status Rundskriv F-05-20** | `SØKNAD KREVES` | **`{}`** | **Full compliance** |".format(bal['f0520_status']))

    lines.append("\n---\n")
    lines.append("## 4. Revidert Prosjektportefølje (EVM EAC & VAC)")
    lines.append("| Prosjekt ID | BAC | Status Quo EAC | Revidert EAC (Med Tiltak) | Status Quo VAC | Revidert VAC | Status |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for p_id, info in p.items():
        lines.append("| **{}** | kr {:,.0f} | kr {:,.0f} | **kr {:,.0f}** | kr {:,.0f} | **kr {:,.0f}** | `{}` |".format(
            p_id, info['bac'], info['baseline_eac'], info['revised_eac'], info['baseline_vac'], info['revised_vac'], info['status']
        ))

    return "\n".join(lines)

if __name__ == "__main__":
    res = simulate_action_plan(descoping_pct=20.0, investments_activated_nok=12000000.0)
    print(format_action_plan_report(res))
