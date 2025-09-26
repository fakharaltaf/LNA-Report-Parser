# Export Functionality Guide

## Overview
The LNA Bot now supports exporting analysis results in multiple formats: JSON, CSV, and Excel. Each format provides different levels of detail and analysis capabilities.

## Export Formats

### 1. JSON Export (Detailed Structure)
**File Extension**: `.json`
**Best For**: Integration with other systems, detailed analysis, programmatic access

**Features**:
- Complete data structure with metadata
- All analysis results with full details
- Summary statistics included
- Machine-readable format
- Preserves all data types and relationships

**Structure**:
```json
{
  "metadata": {
    "total_records": 20,
    "analysis_timestamp": "2025-09-27T02:22:28.817557",
    "bot_version": "1.0.0"
  },
  "summary": { ... },
  "results": [ ... ]
}
```

### 2. CSV Export (Tabular Format)
**File Extension**: `.csv`
**Best For**: Spreadsheet applications, data analysis, reporting

**Features**:
- Flat tabular structure
- Easy to import into Excel, Google Sheets, or other tools
- Human-readable format
- 16 columns of analysis data
- Associated skills converted to semicolon-separated text

**Columns**:
- `id`: Record identifier
- `submission`: Submission date
- `priority`: Priority level (High/Medium/Low)
- `competency`: Target competency
- `estimated_trainees`: Number of trainees
- `expected_training_type`: Recommended training type
- `reasoning`: Explanation for recommendation
- `demand_score`: Calculated demand score
- `competency_classification`: Niche or common classification
- `associated_skills`: Related skills (semicolon-separated)
- `job_families`: Job categories
- `targeted_audience`: Target audience
- `division`: Organizational division
- `department`: Department
- `section`: Section/team
- `analysis_timestamp`: When analysis was performed

### 3. Excel Export (Multi-Sheet Analysis)
**File Extension**: `.xlsx`
**Best For**: Advanced analysis, presentations, stakeholder reports

**Features**:
- Multiple worksheets with different views
- Built-in analysis and breakdowns
- Professional formatting
- Ready for presentations

**Worksheets**:

#### Sheet 1: Analysis Results
- Complete analysis data (same as CSV)
- All 16 columns with full details
- One row per analyzed record

#### Sheet 2: Summary
- Key metrics and statistics
- Training type distribution
- Priority distribution
- Competency classification distribution
- Total entries and trainees
- Average trainees per entry

#### Sheet 3: Training Type Breakdown
- Records count by training type
- Total trainees by training type
- Average demand score by training type
- Summary statistics

#### Sheet 4: Competency Analysis
- Analysis by individual competency
- Record count per competency
- Total trainees per competency
- Average demand score per competency
- Most common training type recommendation

## How to Use

### Through Interactive Menu

1. **During Analysis** (Option 1):
   ```
   Export results? (y/n): y
   Select export format:
   1. JSON (detailed structure)
   2. CSV (tabular format)  
   3. Excel (multi-sheet with analysis)
   Choose format (1-3): [your choice]
   ```

2. **Dedicated Export Function** (Option 5):
   ```
   Select export formats (you can choose multiple):
   1. JSON (detailed structure)
   2. CSV (tabular format)
   3. Excel (multi-sheet with analysis)
   4. All formats
   Choose format(s) (1-4): [your choice]
   ```

### Programmatic Usage

```python
from lna_bot import LNABot
from pathlib import Path

bot = LNABot()
results, summary = bot.analyze_csv_file(Path('data.csv'))

# Export to specific format
bot.export_results_to_json(results, summary, Path('output.json'))
bot.export_results_to_csv(results, summary, Path('output.csv'))
bot.export_results_to_excel(results, summary, Path('output.xlsx'))

# Universal export method
bot.export_results(results, summary, Path('output.xlsx'), 'excel')
```

## File Locations

All exports are saved in organized directories:
```
outputs/
├── analysis_results/           # Main analysis files
│   ├── analysis_results_YYYYMMDD_HHMMSS.json
│   ├── analysis_results_YYYYMMDD_HHMMSS.csv
│   ├── analysis_results_YYYYMMDD_HHMMSS.xlsx
│   └── lna_analysis_YYYYMMDD_HHMMSS.* (from export function)
└── reports/                    # Summary reports
    └── lna_summary_YYYYMMDD_HHMMSS.txt
```

## Use Cases

### For Data Analysts
- **CSV**: Import into Python/R for statistical analysis
- **Excel**: Use pivot tables and charts for insights
- **JSON**: Integrate with custom analysis tools

### For Management Reports
- **Excel**: Professional multi-sheet reports with breakdowns
- **CSV**: Quick overview in spreadsheet applications

### For System Integration
- **JSON**: Feed data into other applications
- **CSV**: Import into databases or data warehouses

### For Presentations
- **Excel**: Ready-made analysis sheets with summaries
- Charts and breakdowns already calculated

## Best Practices

1. **Use Excel** for stakeholder presentations and detailed analysis
2. **Use CSV** for data manipulation and further analysis
3. **Use JSON** for system integration and API consumption
4. **Use "All formats"** when you need flexibility for different audiences
5. Files are timestamped to prevent overwrites
6. Always check the `outputs/` directory for your exported files

## Error Handling

The export functions include robust error handling:
- Missing openpyxl dependency for Excel export (with helpful error message)
- File permission issues
- Invalid data format issues
- Clear error messages with suggested solutions

All export functions maintain data integrity and provide detailed logging for troubleshooting.