---
name: evm-prosjektkontroll
description: Retningslinjer og terskelverdier for Earned Value Management (EVM) prosjektkontroll ved UiA.
---

### Kontroll- og beregningsregler for EVM:
1. **Beregninger:**
   - **CPI (Cost Performance Index):** EV / AC (Verdi over 1,00 indikerer underbudskostnad; under 1,00 indikerer kostnadsoverskridelse).
   - **SPI (Schedule Performance Index):** EV / PV (Verdi over 1,00 indikerer foran skjema; under 1,00 indikerer forsinkelse).
   - **CV (Cost Variance):** EV - AC (Positiv = under budsjett, Negativ = over budsjett).
   - **SV (Schedule Variance):** EV - PV (Positiv = foran skjema, Negativ = bak skjema).
   - **EAC (Estimate at Completion):** BAC / CPI (Estimert totalkostnad ved ferdigstillelse basert på gjeldende CPI).
   - **VAC (Variance at Completion):** BAC - EAC (Positiv = innsparing, Negativ = overskridelse).
   - **ETC (Estimate to Complete):** EAC - AC (Forventet gjenstående kapitalbehov).
   - **TCPI (To-Complete Performance Index):** (BAC - EV) / (BAC - AC) (Påkrevd CPI for gjenstående arbeid for å nå BAC).

2. **Eskalerings- og varslingsgrenser:**
   - **CRITICAL:** Dersom CPI < 0.85, SPI < 0.85, eller VAC < -1 000 000 NOK.
   - **ACTION:** Skriftlig avviksrapport med tiltaksplan sendes til prosjekteier og fakultetsdirektør innen 5 virkedager.
