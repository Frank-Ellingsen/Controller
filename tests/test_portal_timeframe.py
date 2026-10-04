"""
Test Suite for UiA Controller Web Portal (index.html) Timeframe & Database Integrity
Verifies Year & Period selection, monthly coverage inventory, and missing data warning logic.
"""

from pathlib import Path
import re
import pytest

current_dir = Path(__file__).resolve().parent
if current_dir.parent.name == "uia-controller-app-v19":
    ROOT_DIR = current_dir.parent.parent
else:
    ROOT_DIR = current_dir.parent

PORTAL_FILE = ROOT_DIR / "index.html"
PORTAL_V19_FILE = ROOT_DIR / "uia-controller-app-v19" / "index.html"

def test_portal_html_exists():
    assert PORTAL_FILE.exists(), "Root index.html missing"
    assert PORTAL_V19_FILE.exists(), "v19 index.html missing"
    assert PORTAL_FILE.stat().st_size > 50_000

def test_portal_timeframe_controls_present():
    content = PORTAL_FILE.read_text(encoding="utf-8")
    
    # Check selectors
    assert 'id="selectYear"' in content, "Missing selectYear element"
    assert 'id="selectPeriod"' in content, "Missing selectPeriod element"
    assert 'timeframe-picker-bar' in content, "Missing timeframe-picker-bar"
    
    # Check alert and inspector containers
    assert 'id="timeframeAlertContainer"' in content, "Missing timeframeAlertContainer"
    assert 'id="timelineGrid"' in content, "Missing timelineGrid"
    assert 'timeframe-inspector-card' in content, "Missing timeframe-inspector-card"
    assert 'covUbwVal' in content, "Missing covUbwVal"
    assert 'covTravelVal' in content, "Missing covTravelVal"
    assert 'covEvmVal' in content, "Missing covEvmVal"
    assert 'covBudVal' in content, "Missing covBudVal"

def test_portal_javascript_inventory_and_functions():
    content = PORTAL_FILE.read_text(encoding="utf-8")
    
    # Check JS inventory definition
    assert "const monthlyDatabaseInventory =" in content
    assert "evaluateTimeframeIntegrity(" in content
    assert "renderTimelineTrack(" in content
    assert "handleTimeframeChange(" in content
    assert "selectPeriod(" in content
    assert "viewSelectedPeriodData(" in content

    # Check that all 12 months are in inventory
    for m in range(1, 13):
        code = f"2026-M{m:02d}"
        assert f'"{code}":' in content, f"Month {code} missing in database inventory"

def test_v19_portal_synced():
    v19_content = PORTAL_V19_FILE.read_text(encoding="utf-8")
    assert 'id="selectYear"' in v19_content
    assert 'id="selectPeriod"' in v19_content
    assert 'id="timeframeAlertContainer"' in v19_content
    assert "const monthlyDatabaseInventory =" in v19_content

def test_portal_upload_menu_and_modal_present():
    content = PORTAL_FILE.read_text(encoding="utf-8")
    
    # Check upload modal HTML elements
    assert 'id="uploadModal"' in content, "Missing uploadModal element"
    assert 'id="modalUploadPeriod"' in content, "Missing modalUploadPeriod selector"
    assert 'id="modalUploadType"' in content, "Missing modalUploadType selector"
    assert 'id="modalUploadTag"' in content, "Missing modalUploadTag input"
    assert 'id="modalDropzone"' in content, "Missing modalDropzone dropzone"
    assert 'id="modalFileInput"' in content, "Missing modalFileInput file input"
    assert 'id="btnModalUpload"' in content, "Missing btnModalUpload button"
    assert 'id="modalServerStatus"' in content, "Missing modalServerStatus indicator"

    # Check upload JavaScript functions
    assert "function openUploadModal(" in content
    assert "function closeUploadModal(" in content
    assert "function autoSuggestUploadTag(" in content
    assert "function executeUploadToDatabase(" in content
    assert "function checkPortalServerStatus(" in content
    assert "function initModalDropzone(" in content
    assert "openUploadModal()" in content

