#!/bin/bash
echo "Starting analysis..."
python3 scripts/etl/process.py
jupyter nbconvert --to html --execute notebooks/01_quickstart.ipynb
echo "Analysis complete."
