# Finance & Project Controls Account Statement Report

**Organisasjon:** Universitetet i Agder (UiA) / Prosjektstyring
**Dato:** 5. oktober 2026
**Modell:** Intuitiv Kontostilling (Project Controls & Financial Accounting)

---

## 1. Project Controls Account Statement (Engineering, Procurement, Construction)

Denne kontostillingsoppstillingen kobler tradisjonelt finansielt regnskap med Earned Value Prosjektstyring for å gi en umiddelbar og intuitiv forståelse av budsjett, regnskap YTD, fremdriftsverdi, kostnadsavvik og sluttprognose (EAC).

| Account | Total Budget | Budget YTD | Actual YTD | Progress Value (EV) | Cost Variance (CV) | Forecast (EAC) | Forecast Variance (VAC) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Engineering** | 20.0 | 12.0 | 11.0 | 10.5 | -0.5 | 21.0 | -1.0 |
| **Procurement** | 45.0 | 25.0 | 21.0 | 18.0 | -3.0 | 49.0 | -4.0 |
| **Construction** | 35.0 | 13.0 | 8.0 | 6.5 | -1.5 | 39.0 | -4.0 |
| **TOTAL** | **100.0** | **50.0** | **40.0** | **35.0** | **-5.0** | **109.0** | **-9.0** |

---

## 2. UiA Departmental Account Statement (Fakulteter & Infrastruktur)

Tilsvarende oppstilling beregnet for UiAs institusjonelle rammer og avdelinger (tall i MNOK):

| Account / Fakultet | Total Budget | Budget YTD | Actual YTD | Progress Value | Cost Variance | Forecast (EOY) | Forecast Variance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Teknologi og Realfag (TN)** | 22.5 | 15.0 | 14.8 | 14.2 | -0.6 | 23.4 | -0.9 |
| **Handelshøyskolen (HH)** | 18.0 | 12.0 | 11.4 | 11.8 | +0.4 | 17.4 | +0.6 |
| **Helse- og Idrettsvitenskap (HELS)** | 15.0 | 10.0 | 9.6 | 9.8 | +0.2 | 14.7 | +0.3 |
| **Fellesadministrasjon & Infrastruktur** | 15.0 | 10.0 | 10.2 | 9.7 | -0.5 | 15.8 | -0.8 |
| **TOTAL UIA RAMME** | **70.5** | **47.0** | **46.0** | **45.5** | **-0.5** | **71.3** | **-0.8** |

---

## 3. Forklaring av Kolonnene & Formler

* **Total Budget (BAC):** Den samlede vedtatte økonomiske rammen for kontoen/prosjektet.
* **Budget YTD (PV):** Planlagt budsjettforbruk fram til gjeldende periode.
* **Actual YTD (AC):** Faktisk påløpte regnskapsførte kostnader i hovedboken YTD.
* **Progress Value (EV):** Opptjent verdi / fremdriftsverdi calculated as $\text{Progress \%} \times \text{Total Budget}$.
* **Cost Variance (CV):** Kostnadsavvik beregnet som $\text{Progress Value} - \text{Actual YTD}$ ($\text{EV} - \text{AC}$). Negativt tall indikerer overskridelse mot utført arbeid.
* **Forecast (EAC):** Estimert sluttkostnad ved ferdigstillelse basert på historisk kostnadseffektivitet ($\text{CPI} = \frac{\text{EV}}{\text{AC}}$).
* **Forecast Variance (VAC):** Forventet sluttavvik ved ferdigstillelse beregnet som $\text{Total Budget} - \text{Forecast}$ ($\text{BAC} - \text{EAC}$).
