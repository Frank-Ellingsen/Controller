# Walkthrough og Verifiseringslogg: Internkontroll av Reiseregninger

**Mottaker:** Lead Controller / Compliance Auditor  
**Dato:** 3. oktober 2026  
**Ansvarsområde:** Handelshøyskolen UiA  
**Verktøy:** `audit_travel_expenses.py`, `ubw_reader.py`  
**Regelsett:** Statens reiseregulativ (Særavtale for reiser innenlands/utenlands) og UiAs fullmaktsmatrise  

---

## 1. Verifiseringssammendrag

En automatisk etterlevelseskontroll har blitt utført på **15 innsendte reiseregninger** i mappen `data/staging/reiseregninger_15_stk.csv`.

* **Totalt behandlet beløp:** kr 40 850,00 NOK
* **Godkjente reiseregninger uten avvik:** 8 (53,3 %)
* **Reiseregninger med regelbrudd/flagg:** 7 (46,7 %)
* **Totalt beløp berørt av avvik:** kr 19 420,00 NOK

### Kategori-oversikt over avvik
| Avvikskategori | Antall saker | Regelverksreferanse |
| :--- | :---: | :--- |
| **Mangler kvittering (> 100 NOK)** | 2 | DFØ Bilagskrav § 3 |
| **Egengodkjenning (BDM == Attestant)** | 2 | UiA Fullmaktsmatrise § 3 / Fire-øyne-prinsippet |
| **Mangler måltidsfradrag** | 2 | Statens reiseregulativ § 9 (20/30/50 %) |
| **Mangler rutebeskrivelse (Km)** | 1 | Statens reiseregulativ § 6 |

---

## 2. Detaljert avviksmatrise (Saker med flagg)

| Reise-ID | Ansatt | Formål | Beløp (NOK) | Avvikstype | Beskrivelse og påkrevd korreksjon |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **REISE-2026-002** | Kari Hansen | Møte Kunnskapsdepartementet | 2 100,00 | `BRUDD_MALTID` | Middag var inkludert i programmet, men 50 % måltidsfradrag er ikke trukket. Diett må beregnes på nytt. |
| **REISE-2026-004** | Anne Berg | Prosjektmøte EU Horizon | 4 800,00 | `BRUDD_FIRE_OYNE` | Attestant og BDM er identisk (EMP-107). BDM-godkjenning må sendes til overordnet leder for gyldig anvisning. |
| **REISE-2026-005** | Lars Lie | Deltakelse forskningsseminar Trondheim | 3 200,00 | `BRUDD_MALTID` | Frokost, lunsj og middag var dekket (100 % fradrag), men diettutbetaling er krevd fullt ut. Utbetaling stanses. |
| **REISE-2026-006** | Eva Sunde | Kort møte Arendal | 450,00 | `BRUDD_KM_RUTE` | Kilometergodtgjørelse (65 km) mangler spesifisert reiserute. Må suppleres i selvbetjeningsportalen. |
| **REISE-2026-007** | Kjetil Dahl | Taxi til flyplass Kjevik | 620,00 | `BRUDD_KVITTERING` | Bilag over 100 NOK mangler vedlegg. Originalkvittering må lastes opp før BDM kan utbetale. |
| **REISE-2026-011** | Tor Haug | Middagsrepresentasjon eksterne partnere | 1 850,00 | `BRUDD_KVITTERING` | Bilag mangler for utlegg på 1 850 NOK. Utbetaling blokkeres i Unit4 inntil spesifisert kvittering foreligger. |
| **REISE-2026-014** | Hilde Bø | Doktorgradsdisputas Tromsø | 6 400,00 | `BRUDD_FIRE_OYNE` | Egengodkjent bilag (EMP-126). Omrutes til instituttleder/dekan for to-personerskontroll. |

---

## 3. Liste over godkjente reiseregninger (Ingen avvik)

Følgende 8 reiseregninger oppfyller alle krav til bilag, måltidsfradrag, attestering og BDM-godkjenning:
* `REISE-2026-001` (Ola Nordmann - 3 450,00 NOK)
* `REISE-2026-003` (Per Olsen - 850,00 NOK)
* `REISE-2026-008` (Guri Moe - 8 900,00 NOK)
* `REISE-2026-009` (Svein Bakke - 310,00 NOK)
* `REISE-2026-010` (Monika Vik - 2 750,00 NOK)
* `REISE-2026-012` (Ingrid Solberg - 3 900,00 NOK)
* `REISE-2026-013` (Knut Rønning - 420,00 NOK)
* `REISE-2026-015` (Morten Hagen - 850,00 NOK)

---

## 4. Anbefalte strakstiltak for saksbehandling

1. **Sperre utbetalinger i Unit4:** De 7 flaggede reiseregningene sperres for automatisk remittering inntil korreksjon foreligger.
2. **Retur til innsender:** Send `REISE-2026-002`, `005`, `006`, `007` og `011` i retur til de ansatte med krav om supplerende kvitteringer, diettjustering og rutebeskrivelse.
3. **Omruting for BDM-godkjenning:** Re-rut `REISE-2026-004` og `014` til uavhengig BDM-haver for å tilfredsstille statens krav om to-personerskontroll.
