# Statlig og Lovpålagt Rapporteringsguide for Universitetet i Agder (UiA 2026)

**Mottaker:** Universitetsstyret, Dekaner, Lead Controller & Statutory Reporting Specialist  
**Dato:** 4. oktober 2026  
**Hjemmel/Regelverk:** Reglement for økonomistyring i staten, Bevilgningsreglementet, Rundskriv F-05-20, Universitets- og høyskoleloven, Finansdepartementets Rundskriv R-102 (Statens Kontoplan 2026).

---

## 1. Innledning & Formål

Som statlig universitet under Kunnskapsdepartementet (KD) er Universitetet i Agder (UiA) underlagt omfattende lovpålagte rapporteringskrav overfor departementet, DBH/HK-dir, Riksrevisjonen og Skatteetaten.

Denne veiledningen oppsummerer de operative kravene, fristene, beregningsmodellene og kontrollrutinene som **Statutory & State Reporting Specialist** i Antigravity-teamet forvalter.

---

## 2. Kunnskapsdepartementet (KD) - Etatsstyring & Rapportering

### A. Årsrapport & Årsregnskap (Frist: 15. mars - M12)
* **Status & Krav:** Styregodkjent årsrapport og årsregnskap oversendes KD, Riksrevisjonen og DBH.
* **Innhold:**
  1. Ledelseskommentarer og strategisk måloppnåelse (Utviklingsavtale).
  2. Årsregnskap oppstilt iht. **Statlige RegnskapsStandarder (SRS)** og **Statens Kontoplan 2026 (R-102)**.
  3. Rapportering på bevilgnings- og artskonti.
  4. Redegjørelse for internkontroll og risikostyring.

### B. Rundskriv F-05-20 - Reglement for Ubrukte Budsjettmidler (Driftsavsetninger)
* **Hovedregel:** Akkumulerte ubrukte driftsmidler per 31.12 skal **ikke overskride 5,0 %** av årets statlige rammebevilgning (Kap. 260, post 50).
* **Beregning for UiA 2026:**
  $$\text{Reell Avsetningsprosent} = \frac{\text{Akkumulert Driftsavsetning per 31.12}}{\text{Rammebevilgning (Kap. 260 post 50)}} \times 100$$
* **Konsekvens ved overskridelse (> 5,0 %):** Overflytende midler inndras til statskassen dersom skriftlig, begrunnet dispensasjonssøknad med spesifisert investings- og tiltaksplan ikke innvilges av KD.

### C. Utviklingsavtale (2023–2026 / 2027–2030)
* **Krav:** Årlig Rapportering på strategiske målsetninger avtalt mellom KD og Universitetsstyret.
* **Kjerneområder for UiA:** regional samskaping, digital transformasjon, utdanningskvalitet og internasjonalisering.

---

## 3. DBH / HK-dir - Resultat- og Produksjonsrapportering

Rapportering til **Database for statistikk om høgre utdanning (DBH)** forvaltes av HK-dir og danner direkte grunnlag for den resultatbaserte uttellingen i statens finansieringsmodell (T+2).

| Indikator | Frekvens / Frist | Målenhet / Metrikk | Konsekvens for Budsjett (T+2) |
| :--- | :---: | :--- | :--- |
| **Studiepoeng (STP)** | Halvårlig (15. feb / 15. okt) | Beståtte studiepoeng per student | Årlig resultatbasert rammejustering |
| **Kandidater (Gradsgivende)** | Årlig (15. februar) | Antall fullførte Bachelor & Master | Kategoriinnplassert sats per kandidat |
| **Doktorgrader (Ph.d.)** | Årlig (15. februar) | Disputerte kandidater & Nærings-ph.d. | Fast stykkprisbelønning |
| **NVI Publiseringspoeng** | Årlig (15. mars) | Nivå 1 (1 poeng) & Nivå 2 (3 poeng) | Vektet fordelingspot for forskning |
| **Årsverk & Førstekompetanse** | Halvårlig (april / november) | Årsverk, profesjonsandel, professorer | Kvalitetsindikator for NOKUT & KD |

---

## 4. Riksrevisjonen - Compliance & Internkontroll

Riksrevisjonen gjennomfører den årlige eksterne revisjonen av UiAs årsregnskap og økonomistyring:

1. **Fire-øyne-prinsippet (BDM vs. Attestant):**
   * Krav om at enhver forpliktelse og utbetaling skal godkjennes av en BDM-haver og attesteres av en uavhengig saksbehandler (`BDM_ID != Attestant_ID`).
   * BDM-havere kan ikke godkjenne egne utlegg, reiseregninger eller honorarer.
2. **Bilags- og Dokumentasjonskrav:**
   * Bilag over **kr 100 NOK** krever vedlagt originalkvittering med spesifisert MVA.
   * Kilometergodtgjørelse krever fullstendig reiserute og formålsbeskrivelse.
3. **Anskaffelsesregelverk & Fullmaktsgrenser:**
   * Avtaler > kr 10 mill. krever særskilt protokollføring; avtaler > kr 50 mill. / kr 100 mill. krever KDs forhåndsgodkjenning.

---

## 5. Skatteetaten - MVA & BOA (Bidrags- og Oppdragsaktivitet)

* **MVA-skille i UH-Sektoren:**
  * **Utdanning & Egenforskning:** Avgiftsunntatt.
  * **BOA Oppdragsforskning (Salgsinntekt):** MVA-pliktig med 25 % utgående merverdiavgift.
  * **BOA Bidragsforskning (Gave/Tilskudd):** Ikke omssetning; avgiftsfritt, men krever korrekt MVA-kompensasjonsføring.
* **TDI-modellen (Totalkostnad):** Alle BOA-prosjekter skal kalkuleres med fulle direkte kostnader (Timer, Drift) pluss indirekte kostnader/overhead (dekningsgrad for husleie, IT, adm).

---

## 6. Sjekkliste for Statlig Rapportering i Antigravity-Appen

I applikasjonen (`uia-controller-app-v22`) kjøres den automatiske rapporteringskontrollen via:
```bash
uv run python src/tools/antigravity_workflow.py
```
Dette utløser `statutory_reporting_engine.py` som validerer at alle statlige sjekkpunkter er oppfylt før styrebehandling.
