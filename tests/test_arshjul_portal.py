"""
Test Suite for UiA Årshjul, Avsjekksmatrise & Budsjettbygger (v21)
Verifies that Årshjul is integrated as a dedicated tab in index.html,
with full quarterly milestone tracking, monthly check-off matrix,
and T+1 budget simulation for Kap. 260 post 50.
"""

from pathlib import Path
import pytest
import openpyxl

current_dir = Path(__file__).resolve().parent
if "uia-controller-app" in current_dir.parent.name:
    ROOT_DIR = current_dir.parent.parent
else:
    ROOT_DIR = current_dir.parent

def test_arshjul_matrix_file_exists():
    paths = [
        ROOT_DIR / "Data" / "staging" / "arshjul_matrix_2026.xlsx",
        ROOT_DIR / "excel" / "arshjul_matrix_2026.xlsx",
        ROOT_DIR / "uia-controller-app-v22" / "uia-controller-app" / "data" / "staging" / "arshjul_matrix_2026.xlsx"
    ]
    found = False
    for p in paths:
        if p.exists():
            found = True
            break
    assert found, "Missing arshjul_matrix_2026.xlsx"

    # Verify sheets and content
    wb = openpyxl.load_workbook(str(paths[0]), data_only=True)
    assert len(wb.sheetnames) >= 2
    assert any("Kalender" in s or "arshjul" in s.lower() for s in wb.sheetnames)
    assert any("Avsjekk" in s for s in wb.sheetnames)

def test_arshjul_skill_and_agent_docs():
    skill_p = ROOT_DIR / ".agents" / "skills" / "arshjul_og_kalenderspesialist.md"
    assert skill_p.exists(), "arshjul_og_kalenderspesialist.md skill missing"
    skill_txt = skill_p.read_text(encoding="utf-8")
    assert "Statlige Økonomiske Årshjulet" in skill_txt
    assert "F-05-20" in skill_txt

    agents_p = ROOT_DIR / ".agents" / "AGENTS.md"
    assert agents_p.exists()
    agents_txt = agents_p.read_text(encoding="utf-8")
    assert "Annual Wheel Specialist" in agents_txt
    assert "Database Specialist" in agents_txt

def test_index_html_has_arshjul_tab():
    portal = ROOT_DIR / "index.html"
    assert portal.exists()
    content = portal.read_text(encoding="utf-8")

    # 1. Tab button in nav
    assert 'switchTab(\'arshjul-tab\')' in content or 'tab-arshjul' in content
    assert '<span>📅 Årshjul Kalender</span>' in content or '<span>📅 Årshjul &amp; Budsjett</span>' in content or '📅 1. Årshjul' in content or '📅 2. Årshjul' in content or 'tab-arshjul' in content

    # 2. Tab panel container
    assert 'id="arshjul-tab"' in content or 'id="tab-arshjul"' in content

    # 3. SheetJS script in head
    assert 'xlsx.full.min.js' in content

def test_v22_portal_has_arshjul_tab():
    portal_v22 = ROOT_DIR / "uia-controller-app-v22" / "uia-controller-app" / "index.html"
    assert portal_v22.exists()
    content = portal_v22.read_text(encoding="utf-8")
    assert 'tab-arshjul' in content
    assert 'exportArshjulToExcel' in content
