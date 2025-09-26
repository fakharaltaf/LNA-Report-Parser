# LNA Bot - Simplified Terminal Version

## Quick Start

The LNA Bot is now simplified for direct terminal testing without CLI dependencies.

### Test the Application

```bash
# Run the simple demo
python demo_simple.py

# Run comprehensive tests
python test_simple.py

# Test installation
python test_installation.py
```

### Programmatic Usage

```python
from src.lna_bot import LNABot
from pathlib import Path

# Initialize bot
bot = LNABot()

# Analyze CSV file
results, summary = bot.analyze_csv_file(Path("Testing/TestData/lna_report_2024_q1.csv"))

# Get single recommendation
recommendation = bot.get_training_recommendation(
    estimated_trainees=25,
    competency="Patient Safety"
)

# Export results
bot.export_results_to_json(results, summary, Path("output.json"))
```

### Available Test Data

- `Testing/TestData/lna_report_2024_q1.csv` (20 records)
- `Testing/TestData/lna_report_2024_q2.csv` (20 records) 
- `Testing/TestData/lna_report_2024_q3.csv` (20 records)
- `Testing/TestData/lna_report_2024_q4_2025_preview.csv` (20 records)

### Core Features

✅ Individual record analysis  
✅ Batch CSV processing  
✅ Business rule implementation  
✅ JSON export  
✅ Error handling  
✅ Data validation  

The application is fully functional and ready for your testing!