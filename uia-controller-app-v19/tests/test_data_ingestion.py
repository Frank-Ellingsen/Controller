import pytest
import sys
import sqlite3
import pandas as pd
import duckdb
from pathlib import Path

# Add src/tools to path
tools_dir = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.insert(0, str(tools_dir))

from data_ingestion import detect_file_type, ensure_columns_exist, ingest_data_file

def test_detect_file_type():
    # Reiseregninger
    df_travel = pd.DataFrame({"Reise_ID": ["R-01"], "Belop_NOK": [1500]})
    assert detect_file_type(df_travel, "reiseregninger.csv") == "reiseregninger"
    
    # EVM
    df_evm = pd.DataFrame({"Project_ID": ["P-01"], "PV_Sep_NOK": [1000], "EV_Sep_NOK": [1100]})
    assert detect_file_type(df_evm, "evm_prosjekter.csv") == "evm_prosjekter"
    
    # Budsjett
    df_bud = pd.DataFrame({"Budsjett_ID": ["B-01"], "Budsjett_Maaned_NOK": [50000]})
    assert detect_file_type(df_bud, "budsjett_2026.csv") == "budsjett"
    
    # Regnskap / UBW
    df_ubw = pd.DataFrame({"Transaksjon_ID": ["TX-01"], "Konto": [5000], "Belop_NOK": [12000]})
    assert detect_file_type(df_ubw, "regnskap_2026.csv") == "regnskap_ubw"

def test_ensure_columns_exist(tmp_path):
    db_file = tmp_path / "test_schema.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, col_a TEXT)")
    conn.commit()
    
    # DataFrame with new columns
    df = pd.DataFrame({
        "col_a": ["val1"],
        "col_b": [42.5],
        "col_c": ["new_text"]
    })
    
    ensure_columns_exist(conn, "test_table", df)
    
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(test_table)")
    cols = [r[1] for r in cur.fetchall()]
    conn.close()
    
    assert "col_a" in cols
    assert "col_b" in cols
    assert "col_c" in cols

def test_ingest_data_file_evm(tmp_path):
    csv_file = tmp_path / "evm_test_2026T1sep.csv"
    df_evm = pd.DataFrame({
        "Project_ID": ["PRJ-01", "PRJ-02"],
        "Project_Name": ["Test Prosjekt 1", "Test Prosjekt 2"],
        "Avdeling": ["Handelshøyskolen", "Teknologi"],
        "BAC_NOK": [10_000_000.0, 5_000_000.0],
        "PV_Sep_NOK": [6_000_000.0, 3_000_000.0],
        "EV_Sep_NOK": [6_200_000.0, 2_800_000.0],
        "AC_Sep_NOK": [5_900_000.0, 3_100_000.0],
        "Maaned": ["2026-M09", "2026-M09"],
        "Status": ["ON TRACK", "NEEDS ATTENTION"]
    })
    df_evm.to_csv(csv_file, index=False)
    
    db_path = tmp_path / "test_projects.db"
    duck_path = tmp_path / "test_analytics.duckdb"
    parquet_dir = tmp_path / "parquet"
    parquet_dir.mkdir()
    
    # Pre-create evm_projects_2026 in SQLite
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE evm_projects_2026 (Project_ID TEXT, Project_Name TEXT, Tag TEXT)")
    conn.commit()
    conn.close()
    
    res = ingest_data_file(
        file_path=str(csv_file),
        tag="2026T1sep",
        db_path=str(db_path),
        duckdb_path=str(duck_path),
        parquet_dir=str(parquet_dir)
    )
    
    assert res["status"].upper() == "SUCCESS"
    assert res["file_type"] == "evm_prosjekter"
    assert res["rows_ingested"] == 2
    assert res["tag"] == "2026T1sep"
    
    # Verify SQLite rows
    conn = sqlite3.connect(str(db_path))
    df_res = pd.read_sql_query("SELECT * FROM evm_projects_2026 WHERE Tag = '2026T1sep'", conn)
    conn.close()
    assert len(df_res) == 2
    assert "PRJ-01" in df_res["Project_ID"].values
    
    # Verify DuckDB rows
    con_duck = duckdb.connect(str(duck_path))
    duck_count = con_duck.execute("SELECT count(*) FROM evm_snapshots WHERE tag = '2026T1sep'").fetchone()[0]
    con_duck.close()
    assert duck_count == 2

def test_ingest_data_file_missing_file():
    with pytest.raises(FileNotFoundError):
        ingest_data_file("non_existent_file.csv")

def test_ingest_data_file_unsupported_format(tmp_path):
    bad_file = tmp_path / "test.json"
    bad_file.write_text('{"key": "value"}')
    with pytest.raises(ValueError, match="støttes ikke"):
        ingest_data_file(str(bad_file))
