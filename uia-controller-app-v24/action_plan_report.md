# Tiltaksplan, Kvantifiserte Effekter og Revidert Årsprognose (EOY 2026)

**Mottaker:** Dekan og Fakultetsstyret, Handelshøyskolen UiA  
**Fra:** Lead Controller & Analyst Team  
**Dato:** 4. oktober 2026  
**Rapporteringsperiode:** 2026-M10 (End of Year Forecast)

---

## 1. Executive Summary

Basert på den konsoliderte månedskjøringen for oktober 2026 er det identifisert tre kritiske avviksområder:
1. **Rundskriv F-05-20 (Driftsavsetninger):** Akkumulert overskudd utgjør kr 72,00 mill. NOK (6,00 % av rammebevilgningen), noe som overskrider den lovlige grensen på 5,00 % med **kr 12,00 mill. NOK**.
2. **Kritiske EVM-prosjekter:** Prosjektene `UM-ENG-03` ($CPI = 0,76$, $TCPI = 2,14$) og `UM-FPV-01` ($CPI = 0,91$, $TCPI = 1,10$) utviser samlede forventede overskridelser ($VAC$) på kr **-7,04 mill. NOK**.
3. **Reiseregninger & Internkontroll:** 7 av 15 skannede reiseregninger har alvorlige bilags- eller fullmaktsavvik, berørende kr 19 420 NOK.

For å unngå statlig inndragning av avsetningsmidler og gjenopprette økonomisk balanse har controller-teamet simulert en preskriptiv tiltaksplan via **`src/tools/action_engine.py`** og Streamlit-dashbordet (`src/tools/app.py`).

---

## 2. Anbefalt Tiltaksplan (Action to Take Plan)

1. **[F-05-20 Driftsavsetninger] Investeringsfremskyndelse:**
   * Fremskynd og aktiver styregodkjente utstyrs- og IT-infrastrukturinvesteringer for kr **12 000 000 NOK** før 31.12.2026 for å redusere akkumulert overskuddsavsetning til lovlig nivå (5,00 %).
2. **[F-05-20 Dispensasjon] Søknad til Kunnskapsdepartementet:**
   * Utarbeid uoppfordret dispensasjonssøknad til KD for strategiske campusavsetninger for å sikre full juridisk ryggdekning.
3. **[EVM Prosjektstyring] Portefølje-descoping (20,0 % kutt i ETC):**
   * Gjennomfør 20,0 % descoping på gjenstående estimerte arbeider (ETC) i `UM-ENG-03` og `UM-FPV-01`.
4. **[Reiseregninger & Utlegg] Utbetalingssperre og Retur:**
   * Gjennomfør 100 % stans og retur av de 7 urettmessige reiseregningene for korreksjon og to-personerskontroll.

---

## 3. Kvantifisert Finansiell Effekt av Tiltak

| Tiltakskategori | Beskrivelse | Finansiell Besparelse / Omplassering |
| :--- | :--- | :---: |
| **EVM Prosjekt-descoping** | 20,0 % kutt i ETC for `UM-ENG-03` | kr 797 895 NOK |
| **EVM Prosjekt-descoping** | 20,0 % kutt i ETC for `UM-FPV-01` | kr 5 270 110 NOK |
| **Reisekontroll / Diett** | Korreksjon av feilutbetalte diettkrav | kr 5 300 NOK |
| **Investeringsomplassering** | Aktiverte investeringer før 31.12 | kr 12 000 000 NOK |
| **TOTAL DIREKTE BESPARELSE** | **Kutt i løpende prosjekt- og reisekostnader** | **kr 6 073 305 NOK** |

---

## 4. Revidert Årsprognose og Balanse End of Year (31.12.2026)

| Balanse- og Resultatindikator | Status Quo (Før Tiltak) | Revidert Prognose (Etter Tiltak) | Endring / Effekt |
| :--- | :---: | :---: | :---: |
| **Rammebevilgning (Kap. 260, post 50)** | kr 1 200 000 000 NOK | kr 1 200 000 000 NOK | 0 NOK |
| **Akkumulert Driftsavsetning EOY** | kr 72 000 000 NOK (6,00 %) | **kr 60 000 000 NOK (5,00 %)** | **kr -12 000 000 NOK** |
| **Overskridelse mot 5,0 % grense** | kr 12 000 000 NOK | **kr 0 NOK** | **-kr 12 000 000 NOK** |
| **Status Rundskriv F-05-20** | `SØKNAD KREVES` | **`COMPLIANT (<= 5,0 %)`** | **Full compliance** |

---

## 5. Revidert Prosjektportefølje (EVM EAC & VAC)

| Prosjekt ID | BAC | Status Quo EAC | Revidert EAC (Med Tiltak) | Status Quo VAC | Revidert VAC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **UM-DEF-02** | kr 18 500 000 | kr 17 893 443 | **kr 17 893 443** | kr 606 557 | **kr 606 557** | `ON TRACK` |
| **UM-ENG-03** | kr 8 200 000 | kr 10 789 474 | **kr 9 991 579** | kr -2 589 474 | **kr -1 791 579** | `CRITICAL` |
| **UM-FPV-01** | kr 45 000 000 | kr 49 450 549 | **kr 44 180 439** | kr -4 450 549 | **kr 819 561** | `CRITICAL` |
