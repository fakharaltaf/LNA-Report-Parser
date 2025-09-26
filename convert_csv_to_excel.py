#!/usr/bin/env python3
"""
Convert CSV test files to Excel format for testing Excel support.
"""

import pandas as pd
from pathlib import Path
import sys

def convert_csv_to_excel(csv_path: Path, excel_path: Path, sheet_name: str = "LNA_Data"):
    """Convert a CSV file to Excel format."""
    try:
        # Read CSV
        print(f"Reading CSV: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Write to Excel
        print(f"Writing Excel: {excel_path}")
        df.to_excel(excel_path, sheet_name=sheet_name, index=False)
        
        print(f"✅ Successfully converted {csv_path.name} to {excel_path.name}")
        print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
        
    except Exception as e:
        print(f"❌ Error converting {csv_path}: {e}")

def main():
    # Base paths
    data_dir = Path("data/test_datasets")
    
    # Check if openpyxl is available
    try:
        import openpyxl
        print("✅ openpyxl is available")
    except ImportError:
        print("❌ openpyxl not found. Please install with: pip install openpyxl")
        return
    
    # Find CSV files
    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Convert a few sample files to Excel
    sample_files = [
        "lna_report_2024_q1.csv",
        "lna_report_fintech_banking.csv", 
        "lna_report_edge_cases_errors.csv"
    ]
    
    for csv_name in sample_files:
        csv_path = data_dir / csv_name
        if csv_path.exists():
            # Create Excel version
            excel_name = csv_name.replace('.csv', '.xlsx')
            excel_path = data_dir / excel_name
            
            convert_csv_to_excel(csv_path, excel_path)
        else:
            print(f"⚠️  CSV file not found: {csv_path}")
    
    # Create a multi-sheet Excel file for testing
    multi_sheet_path = data_dir / "lna_multi_sheet_test.xlsx"
    print(f"\nCreating multi-sheet Excel file: {multi_sheet_path}")
    
    try:
        with pd.ExcelWriter(multi_sheet_path, engine='openpyxl') as writer:
            # Add multiple sheets with different data
            for i, csv_name in enumerate(sample_files[:3]):
                csv_path = data_dir / csv_name
                if csv_path.exists():
                    df = pd.read_csv(csv_path)
                    sheet_name = f"Sheet{i+1}_{csv_name.replace('lna_report_', '').replace('.csv', '')}"
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"   Added sheet: {sheet_name}")
        
        print("✅ Multi-sheet Excel file created successfully")
        
    except Exception as e:
        print(f"❌ Error creating multi-sheet file: {e}")

if __name__ == "__main__":
    main()