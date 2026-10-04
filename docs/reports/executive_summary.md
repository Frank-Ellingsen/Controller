# Konsolidert Ledelsesrapport: Månedsoppgjør og Prosjektstyring

**Mottaker:** Universitetsdirektør / Dekan / Fakultetsstyret ved Handelshøyskolen UiA  
**Dato:** 3. oktober 2026  
**Rapporteringsperiode:** 2026-M10  
**Utarbeidet av:** Lead Controller (`uia-controller-app v10`)

---

## 1. Hovedkonklusjoner og Risikooversikt

Månedsoppgjøret for periode **2026-M10** viser at virksomheten leverer god faglig aktivitet, men står overfor **to kritiske styringsutfordringer** som krever umiddelbare tiltak fra ledelsen:

1. **Driftsavsetninger overskrider departementets tak (F-05-20):** Akkumulerte driftsavsetninger utgjør **6,0 %** av statlig rammebevilgning, noe som overskrider Kunnskapsdepartementets maksimalgrense på **5,0 %** med **12 000 000 NOK**.
2. **Kritiske kostnadsoverskridelser i prosjektporteføljen:** Porteføljen inneholder to kritiske prosjekter (`UM-ENG-03` og `UM-FPV-01`) med et samlet forventet negativt avvik ved ferdigstillelse (**VAC**) på **-7 039 474 NOK**.

---

## 2. Detaljert Status per Styringsområde

### A. Statlig Økonomistyring og Avsetninger (Rundskriv F-05-20)
* **Rammebevilgning (Kap. 260, post 50):** kr 1 200 000 000 NOK
* **Maksimalt tillatt driftsavsetning (5,0 %):** kr 60 000 000 NOK
* **Reell akkumulert driftsavsetning:** kr 72 000 000 NOK (**6,0 %**)
* **Vurdering:** Uoppfordret skriftlig søknad om dispensasjon og tiltaksplan må sendes til Kunnskapsdepartementet for å unngå inndragning av 12 mill. NOK over statsbudsjettet.

### B. Prosjektstyring og EVM-Analyse (Earned Value Management)
Analyse utført via DuckDB tidsrekkedatabase med tre uavhengige EAC-prognosemodeller:

| Prosjekt-ID | BAC (Budsjett) | AC (Påløpt) | CPI | SPI | EAC (CPI) | EAC (CPI×SPI) | EAC (80/20) | TCPI | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **UM-DEF-02** | 18 500 000 | 11 800 000 | 1,03 | 1,02 | 17 961 165 | 17 796 573 | 17 928 405 | 0,94 | **ON TRACK** |
| **UM-ENG-03** | 8 200 000 | 6 800 000 | 0,76 | 0,80 | 10 789 474 | 11 734 211 | 10 706 250 | 2,14 | **CRITICAL** |
| **UM-FPV-01** | 45 000 000 | 23 100 000 | 0,91 | 0,93 | 49 450 549 | 51 458 738 | 49 358 206 | 1,10 | **CRITICAL** |

* **`UM-ENG-03` (Ingeniørforskning):** Har en svakt kostnadseffektivitet (CPI 0,76) og fremdrift (SPI 0,80). Påkrevd innsats for å hente inn opprinnelig budsjett utgjør en umulig **TCPI på 2,14**. Prosjektet må ombudsjetteres.
* **`UM-FPV-01` (Fornybar lab):** Viser sammensatt avvik på 4,45 mill. NOK. Fremdriftskompositt EAC viser at forsinkelsen vil forsterke overskridelsen opp til **51 458 738 NOK** dersom tiltak ikke iverksettes.

### C. Internkontroll av Reiseregninger og Bilag (DFØ / Fullmakter)
Automatisk gjennomgang av 15 reiseregninger (kr 40 850,00 NOK) avdekket **7 saker med regelbrudd** (kr 19 420,00 NOK):
* **Egengodkjenning (Fire-øyne-brudd):** 2 saker (REISE-2026-004, REISE-2026-014) berører kr 11 200,00 NOK.
* **Manglende kvittering (> 100 NOK):** 2 saker (REISE-2026-007, REISE-2026-011) berører kr 2 470,00 NOK.
* **Manglende måltidsfradrag:** 2 saker (REISE-2026-002, REISE-2026-005) berører kr 5 300,00 NOK.
* **Mangler rutebeskrivelse:** 1 sak (REISE-2026-006) berører kr 450,00 NOK.

---

## 3. Anbefalte Beslutninger og Strakstiltak

1. **KD-Søknad F-05-20:** Få utarbeidet og oversendt formell skriftlig søknad om avsetningsdispensasjon for 12 mill. NOK til Kunnskapsdepartementet innen fristen.
2. **Prosjektrevisjon for `UM-ENG-03`:** Kalle inn prosjekteier til hastemøte for å vurdere omfagskutt eller tilleggsbevilgning, da TCPI 2,14 bekrefter urealistisk innhenting.
3. **Attestasjonsstopp i Unit4:** Sperre utbetaling for de 7 flaggede reiseregningene inntil to-personerskontroll er reetablert og manglende bilag/diettjusteringer er levert.
