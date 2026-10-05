---
name: controller-manual-guidelines
description: Operativ controllerhåndbok for statlig UH-sektor: Rolledeling, regelverkshierarki, internkontroll, attestasjonskontroll, BOA/TDI, SRS 9/10, koordinatoroppgjør, tapsavsetning (786), SRS 3 korreksjon og risikostyring.
---

# Controllerhåndbok for Statlig UH-Sektor: Operativ Agent-Ferdighet

Denne ferdighetsfilen koder retningslinjene fra **Controllerhåndboken for Statlig UH-Sektor** for automatisk og konsistent oppfølging av økonomistyring, internkontroll og prosjektkontroll ved Universitetet i Agder (UiA).

---

## 1. Controllerens Trepartrolle og Rolledeling

Agentene skal i sine analyser og kontroller opprettholde den faste trepartrollen:

1. **Rådgiver (Pre-Award & Avtaleinngåelse):**
   - Bistå prosjektleder (PL) med å sette opp **TDI-kalkyler** med korrekte indirekte kostnader (overhead) og direkte personellkostnader.
   - Vurdere frikjøpskapasitet og synliggjøre eventuell finansiell underdekning / egenandel for BDM-holder (dekan/instituttleder).
2. **Analytiker (Løpende Oppfølging & Prognose):**
   - Månedlig og tertialvis prosjekt- og driftsgjennomgang.
   - Analysere avvik mellom periodisert budsjett og faktisk regnskap, utarbeide **Estimate at Completion (EAC)** og avdekke tids- og kostnadsavvik.
3. **Kontrollør (Attestasjon & Etterlevelse):**
   - Utføre regnskapsmessig og faglig attestasjonskontroll i tråd med Statens Kontoplan (R-102).
   - Håndheve to-manns-prinsippet, egenattestasjonssperrer og habilitetsregler.

### Rolledelingsmatrise (Ufravikelige Prinsipper)
- **Linjeledelse (BDM-holder):** Innehar skriftlig delegert Budsjettdisponeringsmyndighet (dekan/instituttleder). Bærer juridisk og økonomisk ansvar.
- **Prosjektleder (PL):** Faglig og fremdriftsmessig ansvarlig for det enkelte prosjekt.
- **Controller:** Uavhengig faglig rådgiver og kontrollør på vegne av institusjonen (eier verken budsjettmidler eller faglig innhold).

---

## 2. Statlig Regelverkshierarki & Internkontrollens 5 Byggebrikker

Alle kontroller skal forankres i gjeldende regelverkshierarki:
1. **Lov om universiteter og høyskoler (UHL)** & **Lov om offentlige anskaffelser (LOA)**
2. **Reglement for økonomistyring i staten** & **Bestemmelser om økonomistyring** (Finansdepartementet, sist endret 2026)
3. **Virksomhets- og økonomiinstruks for statlige universiteter og høyskoler** (Kunnskapsdepartementet)
4. **Statlige RegnskapsStandarder (SRS)** (Pålagt full innføring innen 1. jan 2027)
5. **Årlig Tildelingsbrev fra Kunnskapsdepartementet** (Kap. 260 post 50)
6. **UiAs Interne Hovedregler & Fullmaktsmatrise**

### ERP-integrasjon av Internkontrollens 5 Byggebrikker
- **Kontrollmiljø:** Tilgangsstyring i ERP (Unit4/UBW) basert på skriftlig BDM-delegasjon.
- **Risikovurdering:** Automatiske varsler i økonomisystemet ved budsjettavvik, forsinkelser eller manglende timeregistrering.
- **Kontrollaktiviteter:** Maskinell sperre der BDM og attestasjon tvinges til å utføres av to ulike personer (`BDM_ID != Attestant_ID`).
- **Informasjon & Kommunikasjon:** Automatisk logging av bruker-ID, dato og klokkeslett for alle regnskapstransaksjoner.
- **Oppfølging & Revisjon:** Systemgenerert endringslogg og ubrytelig revisjonsspor (*audit trail*) fra primærbilag til overordnet rapportering.

---

## 3. Funksjonsskille, Habilitet og Attestasjonsrutiner

### Transaksjonsrekkevisjon (To-manns-prinsippet)
```plaintext
 ┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
 │ BESTILLING/BDM │ ──► │   VAREMOTTAK   │ ──► │  ATTESTASJON   │ ──► │ BOKFØRING &    │
 │ (Forpliktelse) │     │ (Mottakskontr.)│     │ (Faglig/Regnk.)│     │ UTBETALINGSBO. │
 └────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
```
- **Hovedregel:** BDM og Attestasjon må KUN utføres av to ulike personer (`BDM_ID != Attestant_ID`).
- **Unntak:** Småbeløp under **kr 5 000 NOK** (bagatellmessige kjøp/overtid) kan godkjennes og attesteres av samme BDM-haver.
- **Egenattestasjonssperre:** Ingen kan godkjenne eller attestere reiser, timelister eller utlegg til seg selv, overordnet eller nærstående.
- **Bankkonto- og Betalingssperre:** Endring av bankkontonummer og bankautorisasjon skal kun utføres av personell uten BDM.

### Attestasjons-Sjekkliste for Utgiftsbilag
- [ ] **Fakturainnhold:** Rett juridisk enhet (UiA/Fakultet), leverandøradresse, org.nr. og KID.
- [ ] **Avtale- og Priskontroll:** Pris og kvantum stemmer med inngått kontrakt/bestilling.
- [ ] **Varemottak:** Elektronisk registrert i ERP; uoverensstemmelser sperrer utbetaling.
- [ ] **R-102 Kontering:** Korrekt artskonto i Statens Kontoplan (klasser 1–8), kostnadssted og prosjekt.
- [ ] **MVA & Utlandskjøp:** Nettoføringsordning eller pliktig snudd avregning (*reverse charge*) ved kjøp av tjenester fra utlandet (Mval. § 11-3).

---

## 4. Prosjektøkonomi (BOA – Bidrags- og Oppdragsforskning)

### A. TDI-Modellen (Totalkostnad)
$$\text{Total Prosjektkostnad (TDI)} = \text{Direkte Lønn \& Drift} + \text{Indirekte Kostnader (TDI Overhead)}$$
- Enhver underdekning i TDI-overhead eller krav om udekket egenandel tapper instituttets ordinære bevilgningsbudsjett direkte. Skriftlig forhåndsgodkjenning fra BDM-holder kreves før søknadssending.

### B. Klassifisering: SRS 10 (Bidrag) vs. SRS 9 (Oppdrag)
- **SRS 10 (Bidragsforskning - NFR, EU, KD):** Inntekt resultatføres i takt med at godkjente kostnader påløper (motsatt sammenstilling). Ubenyttede forskudd balanseføres på **konto 218/290** (ikke-inntektsført tilskudd).
- **SRS 9 (Oppdragsforskning - Næringsliv, kommersielle kunder):** Resultatføres etter fullføringsgrad. Lovpålagt krav om full kostnadsdekning + fortjenestemargin for å unngå ulovlig statsstøtte (EØS art. 61).

### C. Koordinatorprosjekter (Konsortiummidler)
- Midler mottatt på vegne av eksterne konsortiumpartnere er **IKKE** universitetets inntekt eller kostnad.
- **Regel:** Mottak og viderebetaling av partnerandeler skal i sin helhet føres **via balansen (mellomværendekontoer)** – ALDRI resultatføres i kontoklasse 3, 6 eller 7!

### D. Tapsavsetning på Prosjektnivå (Konto 786)
- Ved forventet framtidig prosjektunderskudd skal det samlede forventede sluttapet resultatføres **umiddelbart**:
  - **Debet:** Konto 786 – *Avsetning for tap på BOA-prosjekter* (Resultat)
  - **Kredit:** Konto 28X – *Avsetning for forpliktelser/tap på prosjekt* (Balanse)
- Reverseres mot balansen ved prosjektslutt.

---

## 5. Avviksanalyse, Risikomatrise & Korreksjonsposteringer (SRS 3)

### Skille mellom Tidsavvik og Varige Kostnadsavvik
- **Tidsavvik (Periodiseringsavvik):** Forskyvning i tid (f.eks. forsinket rekruttering eller feltsamling). Tiltak: Justere prognoseprofil, evt. søke *no-cost extension*.
- **Varige Kostnadsavvik:** Permanente merforbruk eller prissvikt. Tiltak: Omdisponere rammer, kaste om på arbeidspakker, eller foreta tapsavsetning over **konto 786**.

### Operativ BOA-Risikomatrise (R1–R7)
- **R1 (🔴 12):** Feil i TDI-kalkyle / underdekning av overhead -> Krav om controller-sjekk og BDM-godkjenning pre-award.
- **R2 (🟡 8):** Feilklassifisering SRS 9 vs SRS 10 -> Kontraktsklassifiseringssjekk.
- **R3 (🔴 10):** Brudd på funksjonsskille / egengodkjenning -> Maskinell sperre i ERP (`BDM != Attestant`).
- **R4 (🔴 12):** Manglende/forsinket timeregistrering -> Månedlig sperre og eskalering til instituttleder.
- **R5 (🔴 12):** Uidentifisert prosjektunderskudd -> Tapsavsetning over konto 786 ved tertialslutt.
- **R6 (🟡 6):** Feil føring av koordinatormidler -> Streng føring via balansen.
- **R7 (🟡 8):** Mangelfull arkivering / kontrollspor -> 10 års lagring, sperre mot makulering før Riksrevisjonens Dokument 1 er behandlet i Stortinget.

### SRS 3 Bokføringsregler for Retting og Reversering
- **Absolutt forbud** mot sletting eller overskriving i hovedboken.
- **Retting ved stordering:**
  1. Fullstendig reversering (stordering) av opprinnelig feilpostering.
  2. Riktig ny bokføring med oppdatert kontering og prosjekt.
  3. Eksplisitt kryssreferanse til opprinnelig bilags-ID og skriftlig begrunnelse.
