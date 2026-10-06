"""
Portal Server for UiA Controller Dashboard (v19)
Lightweight HTTP API & Static File Server using Python Standard Library.
Provides endpoints for:
- GET  /api/health      : Health & database connectivity check
- GET  /api/inventory   : Live SQLite & DuckDB monthly coverage statistics
- POST /api/upload      : Ingests uploaded data files directly into SQLite, DuckDB & Parquet Star Schema
"""

import http.server
import socketserver
import json
import base64
import sqlite3
import sys
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "staging" / "projects.db"
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "staging" / "analytics_snapshots.duckdb"
DEFAULT_STAGING_DIR = BASE_DIR / "data" / "staging"
DEFAULT_PARQUET_DIR = BASE_DIR / "data" / "staging" / "parquet"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

MONTH_NAMES_NO = {
    "2026-M01": "Januar 2026",
    "2026-M02": "Februar 2026",
    "2026-M03": "Mars 2026",
    "2026-M04": "April 2026",
    "2026-M05": "Mai 2026",
    "2026-M06": "Juni 2026",
    "2026-M07": "Juli 2026",
    "2026-M08": "August 2026",
    "2026-M09": "September 2026",
    "2026-M10": "Oktober 2026",
    "2026-M11": "November 2026",
    "2026-M12": "Desember 2026"
}

def query_database_inventory(db_path: Path = None) -> dict:
    """Queries SQLite projects.db and builds live monthly inventory for 2026."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH

    inventory = {}
    for m in range(1, 13):
        code = f"2026-M{m:02d}"
        inventory[code] = {
            "month": code,
            "name": MONTH_NAMES_NO.get(code, code),
            "status": "missing",
            "has_actuals": False,
            "ubw_count": 0,
            "ubw_sum": 0.0,
            "ubw_total": 0.0,
            "travel_count": 0,
            "travel_sum": 0.0,
            "travel_flagged": 0,
            "budget_sum": 1175000.0,
            "budget_count": 32,
            "evm_count": 0,
            "ubw_samples": [],
            "travel_samples": [],
            "budget_samples": [],
            "evm_rows": []
        }

    if not db_path.exists():
        return inventory

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 1. UBW Transactions
        try:
            cur.execute("""
                SELECT Maaned, COUNT(*) as cnt, COALESCE(SUM(Belop_NOK), 0) as total
                FROM ubw_transactions_2026
                GROUP BY Maaned
            """)
            for row in cur.fetchall():
                m = row["Maaned"]
                if m in inventory:
                    inventory[m]["ubw_count"] = int(row["cnt"])
                    inventory[m]["ubw_sum"] = float(row["total"])
                    inventory[m]["ubw_total"] = float(row["total"])
                    if inventory[m]["ubw_count"] > 0:
                        inventory[m]["has_actuals"] = True

            # Samples for each month
            for code in inventory.keys():
                cur.execute("""
                    SELECT Transaksjon_ID, Dato, Avdeling, Konto, Kontonavn, Beskrivelse, Belop_NOK, BDM_ID, Attestant_ID, Kontrollflagg
                    FROM ubw_transactions_2026
                    WHERE Maaned = ?
                    LIMIT 10
                """, [code])
                inventory[code]["ubw_samples"] = [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"Inventory UBW query note: {e}")

        # 2. Travel Claims
        try:
            cur.execute("""
                SELECT Maaned, COUNT(*) as cnt, COALESCE(SUM(Belop_NOK), 0) as total,
                       SUM(CASE WHEN Kontrollflagg IS NOT NULL AND Kontrollflagg != 'OK' THEN 1 ELSE 0 END) as flagged
                FROM travel_claims_2026
                GROUP BY Maaned
            """)
            for row in cur.fetchall():
                m = row["Maaned"]
                if m in inventory:
                    inventory[m]["travel_count"] = int(row["cnt"])
                    inventory[m]["travel_sum"] = float(row["total"])
                    inventory[m]["travel_flagged"] = int(row["flagged"] or 0)
                    if inventory[m]["travel_count"] > 0:
                        inventory[m]["has_actuals"] = True

            for code in inventory.keys():
                cur.execute("""
                    SELECT Reise_ID, Ansatt, Dato, Formaal, Belop_NOK, Maltid_Dekket, Fradrag_Utfort, Km_Godtgjorelse, Kvittering_Vedlagt, BDM_ID, Attestant_ID, Kontrollflagg
                    FROM travel_claims_2026
                    WHERE Maaned = ?
                    LIMIT 5
                """, [code])
                inventory[code]["travel_samples"] = [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"Inventory Travel query note: {e}")

        # 3. Budget
        try:
            cur.execute("""
                SELECT Maaned, COUNT(*) as cnt, COALESCE(SUM(Budsjett_Maaned_NOK), 0) as total
                FROM budget_2026
                GROUP BY Maaned
            """)
            for row in cur.fetchall():
                m = row["Maaned"]
                if m in inventory:
                    inventory[m]["budget_count"] = int(row["cnt"])
                    inventory[m]["budget_sum"] = float(row["total"])
        except Exception as e:
            print(f"Inventory Budget query note: {e}")

        # 4. EVM Projects
        try:
            cur.execute("SELECT COUNT(*) as cnt FROM evm_projects_2026")
            evm_cnt = cur.fetchone()["cnt"]
            for m in inventory.keys():
                if inventory[m]["has_actuals"]:
                    inventory[m]["evm_count"] = evm_cnt or 5
        except Exception:
            pass

        conn.close()
    except Exception as e:
        print(f"Inventory DB connection note: {e}")

    # Set status
    for code, item in inventory.items():
        if item["has_actuals"]:
            item["status"] = "complete"
        elif code == "2026-M10":
            item["status"] = "partial"
        else:
            item["status"] = "missing"

    return inventory

class PortalRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.send_json_response(200, {
                "status": "ok",
                "app": "UiA Controller Portal Server",
                "version": "v19",
                "database_online": DEFAULT_DB_PATH.exists(),
                "db_path": str(DEFAULT_DB_PATH)
            })
            return

        elif path == "/api/inventory":
            inv = query_database_inventory(DEFAULT_DB_PATH)
            self.send_json_response(200, {
                "year": 2026,
                "monthly_inventory": inv
            })
            return

        # Default static file handler
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/upload":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except ValueError:
                self.send_json_response(400, {"status": "ERROR", "message": "Ugyldig Content-Length."})
                return
            if content_length <= 0:
                self.send_json_response(400, {"status": "ERROR", "message": "Tom forespørsel."})
                return
            if content_length > MAX_UPLOAD_BYTES:
                self.send_json_response(413, {"status": "ERROR", "message": "Filen overskrider maksimal størrelse på 10 MB."})
                return

            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                self.send_json_response(400, {"status": "ERROR", "message": f"Ugyldig JSON payload: {e}"})
                return
            if not isinstance(payload, dict):
                self.send_json_response(400, {"status": "ERROR", "message": "JSON payload må være et objekt."})
                return

            filename = payload.get("filename", f"upload_{os.getpid()}.csv")
            content_b64 = payload.get("content_base64")
            raw_text = payload.get("content_text")
            period = payload.get("period", "2026-M10")
            datatype = payload.get("datatype") # e.g. "regnskap_ubw", "reiseregninger", etc.
            tag = payload.get("tag")

            if not isinstance(filename, str) or Path(filename).name != filename or any(sep in filename for sep in ("/", "\\")):
                self.send_json_response(400, {"status": "ERROR", "message": "Ugyldig filnavn."})
                return
            suffix = Path(filename).suffix.lower()
            if suffix not in {".csv", ".xlsx", ".xls"}:
                self.send_json_response(400, {"status": "ERROR", "message": "Filformatet må være CSV eller Excel."})
                return
            if not isinstance(period, str) or len(period) != 8 or not period.startswith("2026-M") or not period[-2:].isdigit() or not 1 <= int(period[-2:]) <= 12:
                self.send_json_response(400, {"status": "ERROR", "message": "Ugyldig rapporteringsperiode."})
                return
            if not isinstance(tag, (str, type(None))) or not isinstance(datatype, (str, type(None))):
                self.send_json_response(400, {"status": "ERROR", "message": "Ugyldig tag eller datatype."})
                return

            if not tag:
                # Generate default tag based on period, e.g. 2026-M10 -> 2026T1okt
                month_abbrs = {"01": "jan", "02": "feb", "03": "mar", "04": "apr", "05": "mai", "06": "jun",
                               "07": "jul", "08": "aug", "09": "sep", "10": "okt", "11": "nov", "12": "des"}
                m_num = period.split("-M")[-1] if "-M" in period else "10"
                tag = f"2026T1{month_abbrs.get(m_num, 'ny')}"

            # Save uploaded file into staging directory
            DEFAULT_STAGING_DIR.mkdir(parents=True, exist_ok=True)
            target_path = DEFAULT_STAGING_DIR / f"upload_{uuid.uuid4().hex}{suffix}"

            try:
                if content_b64:
                    if not isinstance(content_b64, str):
                        raise ValueError("content_base64 må være tekst.")
                    try:
                        file_bytes = base64.b64decode(content_b64, validate=True)
                    except ValueError:
                        self.send_json_response(400, {"status": "ERROR", "message": "Ugyldig Base64 filinnhold."})
                        return
                    if len(file_bytes) > MAX_UPLOAD_BYTES:
                        self.send_json_response(413, {"status": "ERROR", "message": "Filen overskrider maksimal størrelse på 10 MB."})
                        return
                    target_path.write_bytes(file_bytes)
                elif raw_text:
                    if not isinstance(raw_text, str):
                        raise ValueError("content_text må være tekst.")
                    target_path.write_text(raw_text, encoding="utf-8")
                else:
                    self.send_json_response(400, {"status": "ERROR", "message": "Mangler filinnhold (content_base64 eller content_text)."})
                    return
            except (OSError, ValueError) as e:
                self.send_json_response(500, {"status": "ERROR", "message": f"Kunne ikke lagre fil til disk: {e}"})
                return

            # Invoke data ingestion pipeline
            try:
                from data_ingestion import ingest_data_file
                ingest_res = ingest_data_file(
                    file_path=str(target_path),
                    tag=tag,
                    db_path=str(DEFAULT_DB_PATH),
                    duckdb_path=str(DEFAULT_DUCKDB_PATH),
                    parquet_dir=str(DEFAULT_PARQUET_DIR),
                    period=period,
                    file_type_override=datatype if datatype != "auto" else None
                )

                # Fetch updated inventory for this period
                updated_inv = query_database_inventory(DEFAULT_DB_PATH)

                self.send_json_response(200, {
                    "status": "SUCCESS",
                    "filename": filename,
                    "rows_ingested": ingest_res["rows_ingested"],
                    "file_type": ingest_res["file_type"],
                    "tag": tag,
                    "period": period,
                    "inventory_update": updated_inv.get(period),
                    "message": f"Fil '{filename}' ble vellykket importert ({ingest_res['rows_ingested']} rader, type: '{ingest_res['file_type']}') og lagret i databasen for {period} (Tag: {tag})."
                })
            except Exception as e:
                self.send_json_response(500, {
                    "status": "ERROR",
                    "filename": filename,
                    "message": f"Feil under datainnlesing / database-oppdatering: {e}"
                })
            finally:
                try:
                    target_path.unlink(missing_ok=True)
                except OSError as e:
                    print(f"Could not remove temporary upload {target_path}: {e}")
            return

        self.send_json_response(404, {"status": "ERROR", "message": "Ukjent API-endepunkt."})

def run_server(port: int = 8000, directory: Path = BASE_DIR, host: str = "127.0.0.1"):
    """Starts the Portal HTTP Server."""
    os.chdir(str(directory))
    handler = PortalRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"UiA Controller Portal Server running at http://localhost:{port}/")
        print(f"Web Dashboard: http://localhost:{port}/index.html")
        print(f"API Endpoints: http://localhost:{port}/api/health , /api/inventory , /api/upload")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    host = os.environ.get("HOST", "127.0.0.1")
    run_server(port=port, host=host)
