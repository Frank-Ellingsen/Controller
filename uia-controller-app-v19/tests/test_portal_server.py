"""
Unit & Integration Tests for UiA Controller Portal Server (portal_server.py)
Tests HTTP API endpoints: /api/health, /api/inventory, /api/upload
and verifies database persistence in SQLite & DuckDB.
"""

import sys
import json
import base64
import threading
import socket
import socketserver
import http.client
from pathlib import Path
from urllib.request import urlopen, Request
import pytest
import sqlite3
import pandas as pd

tools_dir = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.insert(0, str(tools_dir))

from portal_server import query_database_inventory, PortalRequestHandler, DEFAULT_DB_PATH

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def test_query_database_inventory():
    inv = query_database_inventory()
    assert len(inv) == 12, "Should return 12 months for 2026"
    assert "2026-M09" in inv
    assert "2026-M10" in inv
    assert "2026-M11" in inv

    # Check known baseline state
    assert inv["2026-M09"]["status"] == "complete"
    assert inv["2026-M09"]["has_actuals"] is True
    assert inv["2026-M09"]["ubw_count"] >= 50

    # November initially missing
    assert inv["2026-M11"]["status"] == "missing"

@pytest.fixture(scope="module")
def portal_test_server():
    port = get_free_port()
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), PortalRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()
    httpd.server_close()

def test_api_health(portal_test_server):
    url = f"{portal_test_server}/api/health"
    with urlopen(url, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["version"] == "v19"
        assert "database_online" in data

def test_api_inventory(portal_test_server):
    url = f"{portal_test_server}/api/inventory"
    with urlopen(url, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["year"] == 2026
        assert "monthly_inventory" in data
        assert "2026-M09" in data["monthly_inventory"]
        assert data["monthly_inventory"]["2026-M09"]["status"] == "complete"

def test_api_upload_flow(portal_test_server):
    # Test uploading a new UBW transaction batch for 2026-M10
    csv_content = (
        "Transaksjon_ID,Dato,Avdeling,Konto,Kontonavn,Beskrivelse,Belop_NOK,BDM_ID,Attestant_ID,Kvittering_Vedlagt,Formaal\n"
        "TX-TEST-901,2026-10-05,Handelshøyskolen,5000,Fast Lønn,Oktober Lønnskjøring,45000.0,EMP-102,EMP-201,1,Lønn oktober\n"
        "TX-TEST-902,2026-10-12,Handelshøyskolen,6800,Kontorrekvisita,Fagbøker,3200.0,EMP-102,EMP-202,1,Pensum\n"
    )
    b64_content = base64.b64encode(csv_content.encode("utf-8")).decode("utf-8")

    payload = {
        "filename": "test_upload_oktober_2026.csv",
        "period": "2026-M10",
        "datatype": "regnskap_ubw",
        "tag": "2026T1test_okt",
        "content_base64": b64_content
    }

    url = f"{portal_test_server}/api/upload"
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urlopen(req, timeout=10) as resp:
        assert resp.status == 200
        result = json.loads(resp.read().decode("utf-8"))
        assert result["status"] == "SUCCESS"
        assert result["rows_ingested"] == 2
        assert result["period"] == "2026-M10"
        assert result["tag"] == "2026T1test_okt"

    # Verify rows in database
    conn = sqlite3.connect(str(DEFAULT_DB_PATH))
    df_check = pd.read_sql_query("SELECT * FROM ubw_transactions_2026 WHERE Tag = '2026T1test_okt'", conn)
    assert len(df_check) == 2
    assert "TX-TEST-901" in df_check["Transaksjon_ID"].values

    # Clean up test rows and staging file
    conn.execute("DELETE FROM ubw_transactions_2026 WHERE Tag = '2026T1test_okt'")
    conn.commit()
    conn.close()

    test_staging_file = DEFAULT_DB_PATH.parent / "test_upload_oktober_2026.csv"
    if test_staging_file.exists():
        test_staging_file.unlink()
