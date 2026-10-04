"""
Power BI Project Builder & Data Manifest Generator
Consolidates Star Schema data export and generates Power BI configuration files.
"""

import os
import sys
from pathlib import Path

# Add src/tools to path
BASE_DIR = Path(__file__).resolve().parent.parent
APP_TOOLS = BASE_DIR / "src" / "tools"
sys.path.append(str(APP_TOOLS))

from powerbi_exporter import export_powerbi_data_model

def build_powerbi_project():
    print("=== START: Building Power BI Star Schema & Data Artifacts ===")
    
    # 1. Export Parquet & CSV Data Model
    output_dir = BASE_DIR / "data" / "staging" / "parquet"
    exported_files = export_powerbi_data_model(output_dir=str(output_dir))
    
    # 2. Write Manifest Summary
    manifest_path = BASE_DIR / "powerbi" / "manifest.json"
    import json
    
    manifest_data = {
        "project": "UiA Controller Power BI Model",
        "version": "12.0",
        "exported_tables": list(exported_files.keys()),
        "output_directory": str(output_dir),
        "dax_measures_file": str(BASE_DIR / "powerbi" / "dax_measures.dax"),
        "m_scripts_file": str(BASE_DIR / "powerbi" / "power_query_m_code.m"),
        "spec_file": str(BASE_DIR / "powerbi" / "UiA_Controller_DataModel_Spec.md")
    }
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"\nManifest successfully created at: {manifest_path}")
    print("=== SLUTT: Power BI Prosjekt Bygging Fullført ===")

if __name__ == "__main__":
    build_powerbi_project()
