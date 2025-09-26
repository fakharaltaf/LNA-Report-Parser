#!/usr/bin/env python3
"""
Entry point for the LNA Bot CLI application.

This script serves as the main entry point for running the LNA Bot
from the command line.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    from lna_bot.cli import cli
    cli()