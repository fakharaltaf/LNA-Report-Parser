#!/usr/bin/env python3
"""
Direct CLI test script that bypasses the main.py entry point.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"  
sys.path.insert(0, str(src_path))

from lna_bot.cli import cli

if __name__ == "__main__":
    cli()