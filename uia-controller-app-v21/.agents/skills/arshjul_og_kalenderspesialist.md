---
name: arshjul-og-kalenderspesialist
description: Retningslinjer for oppfølging av det statlige økonomiske årshjulet, frister mot KD, avsjekksoppfølging og synkronisering med Excel-matrisen (`arshjul_matrix_2026.xlsx`).
---

### Standarder for Årshjul- og Kalenderspesialisten:

1. **Det Statlige Økonomiske Årshjulet (UH-sektoren):**
   - **Q1 (Januar - Mars):** Årsavslutning (M12), hovedbokavstemming, og 15. mars frist for styregodkjent årsrapport og regnskap oversendt KD, DBH og Riksrevisjonen.
   - **Q2 (April - Juni):** 1. tertialrapport (januar-april) med oppdatert årsprognose og justeringer etter Revidert Nasjonalbudsjett (RNB).
   - **Q3 (Juli - September):** 2. tertialrapport, gjennomgang av resultatindikatorer (studiepoeng, doktorgrader) og revisjon av intern fordelingsmodell.
   - **Q4 (Oktober - Desember):** Statsbudsjettet Prop. 1 S (Kap. 260 post 50), styrevedtak om endelig internfordeling i november, og utsending av interne tildelingsbrev i desember.

2. **Månedlig og Tertialvis Avsjekksmatrise (Check-offs):**
   - Hver periode skal registreres i avsjekksmatrisen med status (`FULLFØRT`, `I ARBEID`, `PLANLAGT`).
   - Sjekklisten omfatter: (1) UBW-innlesing, (2) Reiseregningsrevisjon, (3) EVM-snapshot i DuckDB, (4) F-05-20 avsetningskontroll (max 5.0%), og (5) Power BI Parquet-eksport.

3. **Synkronisering med Excel-matrisen (`arshjul_matrix_2026.xlsx`):**
   - Excel-matrisen skal til enhver tid inneholde oppdaterte ark for `Årshjul_Kalender_2026`, `Rapporterings_Avsjekk` og `Budsjett_og_Ramme_Matrise`.
   - Direkte nedlastingslenker og visningsknapper skal være tilgjengelige i `index.html` og Streamlit-dashbordet (`app.py`).
