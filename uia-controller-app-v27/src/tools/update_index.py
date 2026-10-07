import os
from pathlib import Path

app_dir = Path("/workspace/scratch/build_v25/uia-controller-app")
html_path = app_dir / "index.html"

html_content = """<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UiA Controlling & Financial Management Portal (v25)</title>
    <!-- SheetJS for client-side Excel export -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <style>
        :root {
            --uia-navy: #002B49;
            --uia-blue: #005A9C;
            --uia-accent: #E35205;
            --uia-gold: #D4A017;
            --uia-light: #F4F6F9;
            --uia-dark: #1E293B;
            --uia-border: #E2E8F0;
            --uia-success: #10B981;
            --uia-warning: #F59E0B;
            --uia-danger: #EF4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: var(--uia-light);
            color: var(--uia-dark);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        header {
            background-color: var(--uia-navy);
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .logo-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-title h1 {
            font-size: 1.4rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .badge-version {
            background-color: var(--uia-accent);
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
        }

        nav.tab-bar {
            background-color: white;
            border-bottom: 2px solid var(--uia-border);
            display: flex;
            overflow-x: auto;
            padding: 0 1rem;
        }

        .tab-btn {
            background: none;
            border: none;
            padding: 1rem 1.2rem;
            font-size: 0.95rem;
            font-weight: 600;
            color: #64748B;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .tab-btn:hover {
            color: var(--uia-navy);
            background-color: #F8FAFC;
        }

        .tab-btn.active {
            color: var(--uia-navy);
            border-bottom-color: var(--uia-accent);
        }

        main.content {
            flex: 1;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .tab-panel {
            display: none;
        }

        .tab-panel.active {
            display: block;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid var(--uia-border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .card-header {
            font-size: 0.85rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .card-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--uia-navy);
        }

        .card-sub {
            font-size: 0.85rem;
            margin-top: 0.4rem;
        }

        .text-success { color: var(--uia-success); }
        .text-danger { color: var(--uia-danger); }
        .text-warning { color: var(--uia-warning); }

        table.data-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--uia-border);
            margin-bottom: 1.5rem;
        }

        table.data-table th, table.data-table td {
            padding: 0.85rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--uia-border);
            font-size: 0.9rem;
        }

        table.data-table th {
            background-color: #F8FAFC;
            font-weight: 600;
            color: var(--uia-navy);
        }

        table.data-table tr:hover {
            background-color: #F1F5F9;
        }

        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
        }

        .badge-success { background: #E6F4EA; color: #137333; }
        .badge-danger { background: #FCE8E6; color: #C5221F; }
        .badge-warning { background: #FEF7E0; color: #B06000; }

        .btn {
            background-color: var(--uia-navy);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
            text-decoration: none;
        }

        .btn:hover {
            background-color: var(--uia-blue);
        }

        .btn-excel {
            background-color: #107C41;
        }

        .btn-excel:hover {
            background-color: #0B5C30;
        }

        .filter-controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-input, .select-input {
            padding: 0.6rem 1rem;
            border: 1px solid var(--uia-border);
            border-radius: 6px;
            font-size: 0.9rem;
        }

        .slider-group {
            margin-bottom: 1rem;
        }

        .slider-group label {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        .slider-group input[type="range"] {
            width: 100%;
        }

        .chart-bar-container {
            background: #F8FAFC;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--uia-border);
            margin-bottom: 2rem;
        }

        .bar-wrapper {
            margin-bottom: 1rem;
        }

        .bar-label {
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.3rem;
            display: flex;
            justify-content: space-between;
        }

        .bar-bg {
            background: #E2E8F0;
            height: 22px;
            border-radius: 11px;
            overflow: hidden;
            position: relative;
        }

        .bar-fill {
            height: 100%;
            border-radius: 11px;
            transition: width 0.4s ease;
        }

        .bg-navy { background-color: var(--uia-navy); }
        .bg-blue { background-color: var(--uia-blue); }
        .bg-success { background-color: var(--uia-success); }
        .bg-warning { background-color: var(--uia-warning); }
        .bg-danger { background-color: var(--uia-danger); }

        footer {
            background-color: var(--uia-navy);
            color: #94A3B8;
            text-align: center;
            padding: 1rem;
            font-size: 0.85rem;
            margin-top: auto;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-title">
            <h1>🏛️ Universitetet i Agder | Controlling & Financial Portal</h1>
            <span class="badge-version">v25 Full 2026 Oct</span>
        </div>
        <div>
            <span style="font-size: 0.85rem;">Rapporteringsperiode: <strong>2026-M10 (Jan - Okt 2026)</strong></span>
        </div>
    </header>

    <nav class="tab-bar">
        <button class="tab-btn active" onclick="openTab(event, 'tab-frontpage')">📊 1. Totaler YTD & Drilldown</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-arshjul')">📅 2. Årshjul & Budsjett</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-maaned')">🔍 3. Månedsoppgjør & Audit</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-evm')">📈 4. EVM & Tiltakssimulator</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-datakilder')">💾 5. Datakilder & Power BI</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-kontoplan')">📜 6. Statlig Rapportering</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-ordliste')">📖 7. Begrepskatalog</button>
    </nav>

    <main class="content">

        <!-- TAB 1: FRONTPAGE ACCOUNT STATEMENT & DRILL-DOWN -->
        <div id="tab-frontpage" class="tab-panel active">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <div>
                    <h2>📊 UiA Totalt Budsjett, Regnskap YTD & EOY Prognose (2026 M01-M10)</h2>
                    <p style="color: #64748B;">Intuitiv kontostilling med full drilldown på alle 8 fakulteter/enheter, YTD-avvik og EOY-sluttprognose.</p>
                </div>
                <button class="btn btn-excel" onclick="exportFrontpageToExcel()">📥 Eksporter Totalt Budsjett & Regnskap YTD Oct (.xlsx)</button>
            </div>

            <!-- SUMMARY CARDS FOR UIA TOTAL -->
            <div class="card-grid">
                <div class="card">
                    <div class="card-header">Total Ramme FY 2026</div>
                    <div class="card-value">2 075,1 Mill</div>
                    <div class="card-sub">Brutto årsbudsjett Kap 260.50 + BOA</div>
                </div>
                <div class="card">
                    <div class="card-header">Budsjett YTD (Jan-Okt)</div>
                    <div class="card-value">1 729,3 Mill</div>
                    <div class="card-sub">Periodisert ramme (10/12 måneder)</div>
                </div>
                <div class="card">
                    <div class="card-header">Regnskap YTD (Jan-Okt)</div>
                    <div class="card-value text-success">1 703,5 Mill</div>
                    <div class="card-sub">Påløpte kostnader (SRS-regnskap)</div>
                </div>
                <div class="card">
                    <div class="card-header">Avvik YTD (Jan-Okt)</div>
                    <div class="card-value text-success">+25,8 Mill</div>
                    <div class="card-sub">Underforbruk / Innsparing (1.49%)</div>
                </div>
                <div class="card">
                    <div class="card-header">Prognose EOY (31.12)</div>
                    <div class="card-value text-success">2 044,3 Mill</div>
                    <div class="card-sub">Forventet sluttavvik: <strong>+30,8 Mill (1.48%)</strong></div>
                </div>
            </div>

            <!-- VISUAL PROGRESS & FORECAST BARS -->
            <div class="chart-bar-container">
                <h3 style="margin-bottom: 1rem; color: var(--uia-navy);">📈 Visuell Sammenligning: YTD Budsjett vs. Regnskap vs. EOY Prognose</h3>
                
                <div class="bar-wrapper">
                    <div class="bar-label">
                        <span>Budsjett YTD Oct (1 729,3 MNOK) vs. Regnskap YTD Oct (1 703,5 MNOK)</span>
                        <span class="text-success">Innsparing YTD: +25,8 MNOK (+1.49%)</span>
                    </div>
                    <div class="bar-bg">
                        <div class="bar-fill bg-success" style="width: 98.5%;"></div>
                    </div>
                </div>

                <div class="bar-wrapper">
                    <div class="bar-label">
                        <span>Total Ramme 2026 (2 075,1 MNOK) vs. Prognose EOY (2 044,3 MNOK)</span>
                        <span class="text-success">Forventet Årsoverskudd: +30,8 MNOK (+1.48%)</span>
                    </div>
                    <div class="bar-bg">
                        <div class="bar-fill bg-blue" style="width: 98.52%;"></div>
                    </div>
                </div>
            </div>

            <!-- ACCOUNT STATEMENT DRILL-DOWN CONTROLS & TABLE -->
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem;">
                    <h3>🔍 Drill-Down Account Statement (Nivå 1: UiA, Nivå 2: Enhet, Nivå 3: Kategori)</h3>
                    <div class="filter-controls" style="margin-bottom: 0;">
                        <label style="font-weight: 600; font-size: 0.9rem;">Velg Enhet / Fakultet:</label>
                        <select id="faculty-filter" class="select-input" onchange="filterFrontpageDrilldown()">
                            <option value="ALL">ALLE ENHETER (Totalt UiA Consolidated)</option>
                            <option value="HH">Handelshøyskolen (HH)</option>
                            <option value="HELS">Fakultet for helse- og idrettsvitenskap (HELS)</option>
                            <option value="HUM">Fakultet for humaniora og pedagogikk (HUM)</option>
                            <option value="KUNST">Fakultet for kunstfag (KUNST)</option>
                            <option value="SAMF">Fakultet for samfunnsvitenskap (SAMF)</option>
                            <option value="TN">Fakultet for teknologi og realfag (TN)</option>
                            <option value="ADM">Fellesadministrasjon & Fellestjenester (ADM)</option>
                            <option value="FELLES">Særkostnader & Fellesutgifter (FELLES)</option>
                        </select>
                        <input type="text" id="frontpage-search" class="search-input" placeholder="Søk i konto, kategori eller enhet..." onkeyup="filterFrontpageDrilldown()">
                    </div>
                </div>

                <table class="data-table" id="table-frontpage-statement">
                    <thead>
                        <tr>
                            <th>Account / Enhet / Kategori</th>
                            <th>Total Budget FY (MNOK)</th>
                            <th>Budget YTD Oct (MNOK)</th>
                            <th>Actual YTD Oct (MNOK)</th>
                            <th>Progress Value (EV)</th>
                            <th>Cost Variance YTD</th>
                            <th>Forecast EOY (MNOK)</th>
                            <th>Forecast Variance EOY</th>
                        </tr>
                    </thead>
                    <tbody id="frontpage-statement-body">
                        <!-- Populated by JavaScript below -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 2: ÅRSHJUL & BUDSJETT -->
        <div id="tab-arshjul" class="tab-panel">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h2>📅 Det Statlige Årshjulet & Neste Års Budsjettbygger (T+1)</h2>
                    <p style="color: #64748B;">Knytter løpende regnskapsoppfølging mot Kunnskapsdepartementets tidsfrister og internfordelingsmodell.</p>
                </div>
                <a href="data/staging/arshjul_matrix_2026.xlsx" download class="btn btn-excel">📥 Last ned Årshjul & Avsjekksmatrise (.xlsx)</a>
            </div>

            <div class="card-grid">
                <div class="card">
                    <div class="card-header">Q1: Årsoppgjør & Rapportering</div>
                    <div class="card-value">15. Mars</div>
                    <div class="card-sub">Styregodkjent Årsrapport & Årsregnskap sendes KD, Riksrevisjonen og DBH.</div>
                </div>
                <div class="card">
                    <div class="card-header">Q2: 1. Tertial & RNB</div>
                    <div class="card-value">Juni</div>
                    <div class="card-sub">1. tertialrapport, oppdatert årsprognose og styrejusteringer etter Revidert Nasjonalbudsjett.</div>
                </div>
                <div class="card">
                    <div class="card-header">Q3: 2. Tertial & Modellrevisjon</div>
                    <div class="card-value">September</div>
                    <div class="card-sub">2. tertialrapport og gjennomgang av UiAs internfordelingsmodell (basis, studiepoeng, dr-grader).</div>
                </div>
                <div class="card">
                    <div class="card-header">Q4: Tildelingsbrev & Rammer</div>
                    <div class="card-value">Desember</div>
                    <div class="card-sub">Prop. 1 S vedtas, Universitetsstyret fordeler bevilgning, tildelingsbrev utstedes i Unit4/UBW.</div>
                </div>
            </div>

            <!-- ÅRSHJUL AVSJEKKSMATRISE TABELL -->
            <div class="card" style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3>📋 Rapporteringsavsjekk & Milepælskontroll (2026)</h3>
                    <button class="btn btn-excel" onclick="exportArshjulToExcel()">📥 Eksporter Kalender-Avsjekk (.xlsx)</button>
                </div>
                <table class="data-table" id="table-arshjul">
                    <thead>
                        <tr>
                            <th>Periode</th>
                            <th>Tag</th>
                            <th>UBW Innlest</th>
                            <th>Reiseregning Audit</th>
                            <th>EVM Snapshot</th>
                            <th>F-05-20 Avsetning</th>
                            <th>Ansvarlig Agent</th>
                            <th>Avsjekk Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>2026-M01 til M08</strong></td><td>test2026T1</td><td>JA</td><td>JA</td><td>JA</td><td>OK (4.9%)</td><td>Database Specialist</td><td><span class="badge badge-success">FULLFØRT</span></td></tr>
                        <tr><td><strong>2026-M09 (T2)</strong></td><td>2026T1sep</td><td>JA</td><td>JA</td><td>JA</td><td>REVIDERT (5.0%)</td><td>Annual Wheel Specialist</td><td><span class="badge badge-success">FULLFØRT</span></td></tr>
                        <tr><td><strong>2026-M10 (10T)</strong></td><td>2026_UiA_Full_Oct</td><td>JA</td><td>JA</td><td>JA</td><td>PROGNOSE (5.0%)</td><td>Statutory Reporting Specialist</td><td><span class="badge badge-success">FULLFØRT</span></td></tr>
                        <tr><td><strong>2026-M11</strong></td><td>2026T1nov</td><td>NEI</td><td>NEI</td><td>PLANLAGT</td><td>PLANLAGT</td><td>Statutory Reporting Specialist</td><td><span class="badge badge-danger">PLANLAGT</span></td></tr>
                        <tr><td><strong>2026-M12 (M12)</strong></td><td>2026T1des</td><td>NEI</td><td>NEI</td><td>PLANLAGT</td><td>PLANLAGT</td><td>Statutory Reporting Specialist</td><td><span class="badge badge-danger">PLANLAGT</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: MÅNEDSOPPGJØR -->
        <div id="tab-maaned" class="tab-panel">
            <h2>🔍 Månedsoppgjør & Internkontroll (Audit Center)</h2>
            <p style="color: #64748B; margin-bottom: 1.5rem;">Automatisk regelverskontroll av UBW-transaksjoner og DFØ-reiseregninger.</p>

            <div class="card-grid">
                <div class="card">
                    <div class="card-header">Behandlede Krav</div>
                    <div class="card-value">1 920 Krav</div>
                    <div class="card-sub">Totalt behandlet kr 1 698 450,12 NOK</div>
                </div>
                <div class="card">
                    <div class="card-header">Flaggede Avvik</div>\n                    <div class="card-value text-danger">54 Krav (2.8%)</div>
                    <div class="card-sub">Totalt berørt beløp kr 412 850,00 NOK</div>
                </div>
                <div class="card">
                    <div class="card-header">Godkjente Krav</div>
                    <div class="card-value text-success">1 866 Krav (97.2%)</div>
                    <div class="card-sub">Full compliance uten anmerkninger</div>
                </div>
            </div>
        </div>

        <!-- TAB 4: EVM & TILTAKSSIMULATOR -->
        <div id="tab-evm" class="tab-panel">
            <h2>📊 EVM Prosjektkontroll & Preskriptiv Tiltakssimulator</h2>
            <p style="color: #64748B; margin-bottom: 1.5rem;">Sanntids beregning av Earned Value nøkkeltall og revidert EOY balanseprognose ved 31.12.</p>
        </div>

        <!-- TAB 5: DATAKILDER, EXCEL & POWER BI -->
        <div id="tab-datakilder" class="tab-panel">
            <h2>💾 Datakilde-hub, Excel-Pipelines & Power BI</h2>
            <p style="color: #64748B; margin-bottom: 1.5rem;">Direkte tilgang til SQLite, DuckDB, Parquet Star Schema og Power BI dashboards.</p>
        </div>

        <!-- TAB 6: STATLIG RAPPORTERING -->
        <div id="tab-kontoplan" class="tab-panel">
            <h2>📜 Operativt Regelverk & Statens Kontoplan 2026</h2>
            <p style="color: #64748B; margin-bottom: 1.5rem;">Statlige føringsregler (Rundskriv R-102), F-05-20 avsetningstak og UiAs fullmaktsmatrise.</p>
        </div>

        <!-- TAB 7: BEGREPSKATEGORI & ORDLISTE -->
        <div id="tab-ordliste" class="tab-panel">
            <h2>📖 Finansiell Begrepskatalog & Ordliste</h2>
            <p style="color: #64748B; margin-bottom: 1.5rem;">Komplett oversikt over økonomiske begreper, akronymer, formler og prosjektstyringsregler.</p>
        </div>

    </main>

    <footer>
        <p>Universitetet i Agder &copy; 2026 | Antigravity Financial Controlling Architecture v25 | Utarbeidet for Handelshøyskolen UiA</p>
    </footer>

    <script>
        // DRILLDOWN DATA MATRIX (Pre-embedded for instant browser response)
        const drilldownData = [
            { code: "ADM", name: "Fellesadministrasjon & Fellestjenester (ADM)", totalB: 456.5, ytdB: 380.4, ytdA: 366.6, pVal: 370.8, cVar: 4.13, eoyF: 440.1, eoyV: 16.45 },
            { code: "FELLES", name: "Særkostnader & Fellesutgifter (FELLES)", totalB: 495.9, ytdB: 413.3, ytdA: 411.8, pVal: 412.2, cVar: 0.46, eoyF: 494.0, eoyV: 1.94 },
            { code: "HELS", name: "Fakultet for helse- og idrettsvitenskap (HELS)", totalB: 207.5, ytdB: 172.9, ytdA: 167.3, pVal: 169.0, cVar: 1.69, eoyF: 200.8, eoyV: 6.66 },
            { code: "HH", name: "Handelshøyskolen (HH)", totalB: 134.9, ytdB: 112.4, ytdA: 110.9, pVal: 111.4, cVar: 0.44, eoyF: 133.1, eoyV: 1.80 },
            { code: "HUM", name: "Fakultet for humaniora og pedagogikk (HUM)", totalB: 211.7, ytdB: 176.4, ytdA: 174.1, pVal: 174.8, cVar: 0.67, eoyF: 209.1, eoyV: 2.59 },
            { code: "KUNST", name: "Fakultet for kunstfag (KUNST)", totalB: 103.8, ytdB: 86.5, ytdA: 84.5, pVal: 85.1, cVar: 0.59, eoyF: 101.4, eoyV: 2.39 },
            { code: "SAMF", name: "Fakultet for samfunnsvitenskap (SAMF)", totalB: 170.2, ytdB: 141.8, ytdA: 138.7, pVal: 139.6, cVar: 0.94, eoyF: 166.5, eoyV: 3.69 },
            { code: "TN", name: "Fakultet for teknologi og realfag (TN)", totalB: 294.7, ytdB: 245.6, ytdA: 249.6, pVal: 248.4, cVar: -1.21, eoyF: 299.4, eoyV: -4.75 }
        ];

        function renderFrontpageDrilldown() {
            const filterCode = document.getElementById('faculty-filter').value;
            const searchTxt = document.getElementById('frontpage-search').value.toLowerCase();
            const tbody = document.getElementById('frontpage-statement-body');
            tbody.innerHTML = '';

            let filtered = drilldownData;
            if (filterCode !== 'ALL') {
                filtered = drilldownData.filter(d => d.code === filterCode);
            }

            if (searchTxt) {
                filtered = filtered.filter(d => d.name.toLowerCase().includes(searchTxt) || d.code.toLowerCase().includes(searchTxt));
            }

            let sumB = 0, sumYtdB = 0, sumYtdA = 0, sumPval = 0, sumCvar = 0, sumEoyF = 0, sumEoyV = 0;

            filtered.forEach(item => {
                sumB += item.totalB;
                sumYtdB += item.ytdB;
                sumYtdA += item.ytdA;
                sumPval += item.pVal;
                sumCvar += item.cVar;
                sumEoyF += item.eoyF;
                sumEoyV += item.eoyV;

                const row = document.createElement('tr');
                const cVarBadge = item.cVar >= 0 ? `<span class="badge badge-success">+${item.cVar.toFixed(2)} Mill</span>` : `<span class="badge badge-danger">${item.cVar.toFixed(2)} Mill</span>`;
                const eoyVBadge = item.eoyV >= 0 ? `<span class="badge badge-success">+${item.eoyV.toFixed(2)} Mill</span>` : `<span class="badge badge-danger">${item.eoyV.toFixed(2)} Mill</span>`;

                row.innerHTML = `
                    <td><strong>${item.name}</strong></td>
                    <td>${item.totalB.toFixed(1)}</td>
                    <td>${item.ytdB.toFixed(1)}</td>
                    <td>${item.ytdA.toFixed(1)}</td>
                    <td>${item.pVal.toFixed(1)}</td>
                    <td>${cVarBadge}</td>
                    <td>${item.eoyF.toFixed(1)}</td>
                    <td>${eoyVBadge}</td>
                `;
                tbody.appendChild(row);
            });

            // TOTAL ROW
            const totRow = document.createElement('tr');
            totRow.style.fontWeight = 'bold';
            totRow.style.backgroundColor = '#F8FAFC';
            const totCvarBadge = sumCvar >= 0 ? `<span class="badge badge-success">+${sumCvar.toFixed(2)} Mill</span>` : `<span class="badge badge-danger">${sumCvar.toFixed(2)} Mill</span>`;
            const totEoyVBadge = sumEoyV >= 0 ? `<span class="badge badge-success">+${sumEoyV.toFixed(2)} Mill</span>` : `<span class="badge badge-danger">${sumEoyV.toFixed(2)} Mill</span>`;

            totRow.innerHTML = `
                <td><strong>TOTALT UIA BRUTTO RAMME</strong></td>
                <td><strong>${sumB.toFixed(1)}</strong></td>
                <td><strong>${sumYtdB.toFixed(1)}</strong></td>
                <td><strong>${sumYtdA.toFixed(1)}</strong></td>
                <td><strong>${sumPval.toFixed(1)}</strong></td>
                <td><strong>${totCvarBadge}</strong></td>
                <td><strong>${sumEoyF.toFixed(1)}</strong></td>
                <td><strong>${totEoyVBadge}</strong></td>
            `;
            tbody.appendChild(totRow);
        }

        function filterFrontpageDrilldown() {
            renderFrontpageDrilldown();
        }

        function openTab(evt, tabId) {
            const tabPanels = document.querySelectorAll('.tab-panel');
            tabPanels.forEach(p => p.classList.remove('active'));

            const tabBtns = document.querySelectorAll('.tab-btn');
            tabBtns.forEach(b => b.classList.remove('active'));

            document.getElementById(tabId).classList.add('active');
            evt.currentTarget.classList.add('active');
        }

        function exportFrontpageToExcel() {
            const table = document.getElementById('table-frontpage-statement');
            if (typeof XLSX !== 'undefined') {
                const wb = XLSX.utils.table_to_book(table, { sheet: "UiA_Account_Statement_2026" });
                XLSX.writeFile(wb, 'Totalt_Budsjett_og_Regnskap_YTD_Oct_2026_UiA.xlsx');
            } else {
                let html = table.outerHTML;
                let blob = new Blob(['﻿' + html], { type: 'application/vnd.ms-excel' });
                let url = URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = 'Totalt_Budsjett_og_Regnskap_YTD_Oct_2026_UiA.xls';
                a.click();
            }
        }

        function exportArshjulToExcel() {
            const table = document.getElementById('table-arshjul');
            if (typeof XLSX !== 'undefined') {
                const wb = XLSX.utils.table_to_book(table, { sheet: "Arshjul_Avsjekk_2026" });
                XLSX.writeFile(wb, 'Arshjul_og_Kalender_Avsjekk_2026_UiA.xlsx');
            }
        }

        // Initialize on load
        window.onload = function() {
            renderFrontpageDrilldown();
        };
    </script>
</body>
</html>
"""

html_path.write_text(html_content, encoding="utf-8")
print("Updated index.html successfully!")
"""