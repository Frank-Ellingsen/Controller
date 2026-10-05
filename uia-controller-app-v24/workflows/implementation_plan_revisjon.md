# Implementation Plan: Internkontroll av Reiseregninger

## Mål
Gjennomføre en automatisert etterlevelseskontroll av **15 innsendte reiseregninger** i mappen `data/staging/reiseregninger_15_stk.csv` mot regelverket i `.agents/skills/dfo_reiseregning.md`.

## Agent-konfigurasjon og sikkerhet
- **Security Preset:** Default
- **Artifact Review Policy:** Always Ask (krever godkjenning fra brukersiden før filendringer utføres)

## Gjennomføringssteg
1. **Lesing og validering av stagingdata (`Ledger Analyst`):**
   - Hente ut alle 15 transaksjonsrader fra `data/staging/reiseregninger_15_stk.csv`.
   - Eksekvere `src/tools/audit_travel_expenses.py` i Python for å unngå skjønnsmessige/tekstbaserte regnefeil.
2. **Regel-evaluering (`Compliance Auditor`):**
   - **Måltidsfradrag:** Sjekke at fradrag (20% frokost, 30% lunsj, 50% middag) er aktivert når måltider var inkludert.
   - **Bilagskontroll:** Verifisere at utlegg over **100 NOK** har gyldig kvittering.
   - **Fire-øyne-prinsipp:** Sjekke at BDM_ID != Attestant_ID.
   - **Kilometergodtgjørelse:** Bekrefte at reiserute og formål er spesifisert.
3. **Generering av Walkthrough og Revisjonsrapport (`Lead Controller`):**
   - Opprette `walkthrough_revisjon.md` med oppsummering, tabell over godkjente vs. avvikende saker og spesifikke tiltak per sak.

---
*Godkjent for utførelse:* [x] Ja
