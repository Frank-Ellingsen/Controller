import sys
from pathlib import Path
import pytest
import pandas as pd

APP_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from duckdb_analytics import snapshot_evm_data, query_eac_forecasting_models

def test_duckdb_snapshotting(tmp_path):
    duckdb_path = str(tmp_path / "analytics.duckdb")
    res_df = snapshot_evm_data(duckdb_path=duckdb_path, period="2026-M10")
    assert isinstance(res_df, pd.DataFrame)
    assert not res_df.empty
    assert len(res_df) == 3
    
    assert "eac_cpi" in res_df.columns
    assert "eac_composite" in res_df.columns
    assert "eac_weighted" in res_df.columns

def test_duckdb_query_forecasting_models(tmp_path):
    # Pre-populate snapshot
    duckdb_path = str(tmp_path / "analytics.duckdb")
    snapshot_evm_data(duckdb_path=duckdb_path, period="2026-M10")
    df_models = query_eac_forecasting_models(duckdb_path=duckdb_path)
    assert isinstance(df_models, pd.DataFrame)
    assert not df_models.empty
    assert "eac_typical_cpi" in df_models.columns
    assert "eac_cpi_spi" in df_models.columns
    assert "eac_weighted_80_20" in df_models.columns
