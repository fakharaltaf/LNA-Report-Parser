#!/usr/bin/env python3
"""
LNA Bot Application Launcher

Simple launcher script for the LNA Bot Streamlit application.
This script handles environment setup and launches the web interface.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Launch the LNA Bot Streamlit application."""
    
    print("🤖 LNA Bot - AI-Powered Training Recommendations")
    print("=" * 50)
    
    # Check if we're in the right directory
    app_file = Path("streamlit_app.py")
    if not app_file.exists():
        print("❌ Error: streamlit_app.py not found in current directory")
        print("Please run this script from the LNA Bot project root directory")
        return 1
    
    # Check if required dependencies are available
    try:
        import streamlit
        import plotly
        import pandas
        print(f"✅ Dependencies verified (Streamlit {streamlit.__version__})")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return 1
    
    # Check if sample datasets exist
    datasets_dir = Path("data/test_datasets")
    if datasets_dir.exists():
        dataset_count = len(list(datasets_dir.glob("*.csv"))) + len(list(datasets_dir.glob("*.xlsx")))
        print(f"✅ Found {dataset_count} sample datasets")
    else:
        print("⚠️  Sample datasets directory not found")
    
    print("\n🚀 Starting LNA Bot Web Interface...")
    print("📍 Application will open at: http://localhost:8501")
    print("💡 Press Ctrl+C to stop the application\n")
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n👋 LNA Bot application stopped")
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())