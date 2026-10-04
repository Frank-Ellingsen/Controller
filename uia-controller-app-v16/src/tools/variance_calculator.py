"""
Variance Calculator for UiA Controlling App (v7)
Provides budget vs. actual variance calculations and F-05-20 reserve threshold checks.
"""

import pandas as pd

def sjekk_f0520_avsetning(rammebevilgning: float, akkumulert_avsetning: float) -> dict:
    """Sjekker om driftsavsetninger overskrider 5 %-grensen i rundskriv F-05-20."""
    grense = rammebevilgning * 0.05
    prosent = (akkumulert_avsetning / rammebevilgning) * 100
    overskridelse = max(0.0, akkumulert_avsetning - grense)
    
    return {
        "rammebevilgning_nok": rammebevilgning,
        "akkumulert_avsetning_nok": akkumulert_avsetning,
        "maks_driftsavsetning_5_prosent_nok": grense,
        "reell_prosent": round(prosent, 2),
        "krever_soknad_kd": akkumulert_avsetning > grense,
        "overskridelse_nok": overskridelse
    }

def beregn_prosentvis_avvik(df: pd.DataFrame, budsjett_col: str = "Budsjett", regnskap_col: str = "Regnskap") -> pd.DataFrame:
    """Beregner prosentuell og nominelt avvik per linje."""
    df = df.copy()
    df['Avvik_NOK'] = df[regnskap_col] - df[budsjett_col]
    df['Avvik_Prosent'] = ((df['Avvik_NOK'] / df[budsjett_col]) * 100).round(2)
    
    # Flagg vesentlighet: Avvik >= 5% eller >= 100 000 kr
    def flagg_vesentlighet(row):
        grunner = []
        if abs(row['Avvik_Prosent']) >= 5.0:
            grunner.append(f"Prosentavvik ({row['Avvik_Prosent']}%) >= 5.0%")
        if abs(row['Avvik_NOK']) >= 100000:
            grunner.append(f"Beløpsavvik ({row['Avvik_NOK']:,.0f} NOK) >= 100k NOK")
        return "; ".join(grunner) if grunner else "OK"

    df['Avviksgrunn'] = df.apply(flagg_vesentlighet, axis=1)
    return df
