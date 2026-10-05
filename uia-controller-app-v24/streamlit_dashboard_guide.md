# Streamlit Web Dashboard & Preskriptiv Tiltakssimulator (Guide)

**Applikasjon:** `uia-controller-app` (v14)  
**Filplassering:** `src/tools/app.py`  
**Kjørekommando:** `uv run streamlit run src/tools/app.py`

---

## 1. Oversikt over Streamlit-dashbordet

Streamlit-dashbordet leverer et interaktivt webgrensesnitt for ledelsen og økonomicontrollere ved Universitetet i Agder (UiA). Grensesnittet lar brukerne justere preskriptive tiltaksparametre i sanntid og observere umiddelbar effekt på revidert EOY-balanse, avsetningsprosent og prosjektenes EAC/VAC.

```plaintext
┌──────────────────────────────────────────────┐
│  SIDEBAR: Interaktiv Tiltakssimulator        │
│  - Descoping/Kostnadskutt i ETC (%)          │
│  - Investeringsaktivering før 31.12 (NOK)    │
│  - Stans av urettmessige reisekrav (%)       │
│  - KD-dispensasjonssøknad (Toggle)           │
└──────────────────────┬───────────────────────┘
                       │ (Beregner i sanntid via action_engine.py)
                       ▼
┌──────────────────────────────────────────────┐
│  HOVEDOMRÅDE: 4 Interaktive Faner            │
│  1. 📊 Revidert EOY Balanse & Resultat       │
│  2. 📈 EVM Prosjektstyring & Descoping        │
│  3. ⚖️ F-05-20 Avsetningskontroll             │
│  4. 🔍 Internkontroll & Reiseregninger       │
└──────────────────────────────────────────────┘
```

---

## 2. Funksjonalitet i Fanene

### Fane 1: Revidert EOY Balanse & Resultat
* **Metric Cards:** Viser `Reell Driftsavsetning EOY %` (med fargekodet avvik fra 5,0 %-taket), `Driftsavsetning EOY (NOK)`, `Direkte Kostnadsinnsparing` og `F-05-20 Compliance Status`.
* **Balanse- og Resultattabell:** Sammenligner Status Quo mot Revidert Prognose post-tiltak.
* **Avsetningsdiagram:** Stolpediagram som viser Status Quo (6,0 %) vs. 5,0 % lovlig grense vs. Revidert EOY-prognose.

### Fane 2: EVM Prosjektstyring & Descoping Simulator
* **Porteføljematrise:** Viser BAC, AC, CPI, Baseline EAC, Revidert EAC, Baseline VAC og Revidert VAC for alle prosjekter (`UM-DEF-02`, `UM-ENG-03`, `UM-FPV-01`).
* **Interaktivt Descoping-diagram:** Viser hvordan %-vise kutt i gjenstående arbeider (ETC) reduserer forventet overskridelse ($VAC$).

### Fane 3: F-05-20 Avsetningskontroll
* **Informasjonsboks og Terskelanalyse:** Forklarer regelverket i Rundskriv F-05-20 og viser nøyaktig beløp som må aktiveres som utstyrsinvesteringer for å unngå statlig inndragning.

### Fane 4: Internkontroll & Reiseregninger
* **Revisjonsoversikt:** Tabell over alle 15 skannede reiseregninger med filtrering på regelbrudd (`BRUDD_MALTID`, `BRUDD_FIRE_OYNE`, `BRUDD_KM_RUTE`, `BRUDD_KVITTERING`).

---

## 3. Lokal Oppstart og Installasjon

For å kjøre webgrensesnittet lokalt på din maskin:

```bash
# 1. Naviger til prosjektmappen
cd uia-controller-app

# 2. Synkroniser miljø og avhengigheter
uv sync

# 3. Start Streamlit-applikasjonen
uv run streamlit run src/tools/app.py
```

Når kommandoen kjøres, åpnes dashbordet automatisk i din nettleser på `http://localhost:8501`.
