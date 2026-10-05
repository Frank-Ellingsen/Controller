---
name: tiltaksplan-og-arsprognose
description: Regler, formler og prosedyrer for utarbeidelse av tiltaksplan, finansiell effektsimulering og revidert EOY-balanseprognose ved 31.12.
---

### Kontroll- og beregningsregler for Tiltaksplan & Revidert EOY-balanse:

1. **Utdrag av Avvik og Triggere:**
   - **F-05-20 Driftsavsetninger:** Dersom akkumulert avsetning overskrider 5,0 % av rammebevilgningen (Kap. 260, post 50), må tiltak for investeringsaktivering eller KD-dispensasjonssøknad utløses.
   - **EVM Kritiske Prosjekter:** Prosjekter med $CPI < 0.85$ eller $TCPI > 1.10$ krever umiddelbar descoping / kostnadskutt i gjenstående estimerte arbeider (ETC).
   - **Reiseregninger:** Urettmessige utbetalinger stanses og omrutes for to-personerskontroll.

2. **Formler for Kvantifisering av Finansiell Effekt:**
   - **Innsparing fra Prosjekt-descoping ($\Delta ETC$):**
     $$\Delta \text{Cost}_{\text{EVM}} = \text{ETC}_{\text{opprinnelig}} \times \left(\frac{\text{Descoping \%}}{100}\right)$$
   - **Revidert Estimat ved Ferdigstillelse ($\text{EAC}_{\text{revidert}}$):**
     $$\text{EAC}_{\text{revidert}} = \text{EAC}_{\text{opprinnelig}} - \Delta \text{Cost}_{\text{EVM}}$$
   - **Revidert Driftsavsetning End of Year ($\text{Avsetning}_{\text{EOY, revidert}}$):**
     $$\text{Avsetning}_{\text{EOY, revidert}} = \text{Avsetning}_{\text{Status Quo}} - \text{Investeringer Aktivert før 31.12}$$
   - **Reell Avsetningsprosent EOY:**
     $$\text{Avsetningsprosent}_{\text{EOY}} = \left(\frac{\text{Avsetning}_{\text{EOY, revidert}}}{\text{Rammebevilgning}}\right) \times 100$$

3. **Gjennomføring i Applikasjonen:**
   - Kjøres deterministisk via `action_engine.py` i backend eller interaktivt via Streamlit (`src/tools/app.py`).
