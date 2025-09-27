# LNA Bot - AI-Powered Training Recommendations

An intelligent web application that analyzes Learning Need Analysis (LNA) reports and provides automated recommendations for training delivery methods through an intuitive Streamlit interface.

## Features

🤖 **AI-Powered Analysis**: Intelligent decision engine for training recommendations  
📊 **File Processing**: Support for CSV and Excel files with multi-sheet capability  
🎯 **Smart Classification**: Automatic competency classification (niche vs common)  
📈 **Interactive Visualizations**: Charts, graphs, and comprehensive dashboards  
💾 **Advanced Export**: Results in CSV, JSON, and professionally formatted Excel (.xlsx)  
🎯 **Sample Datasets**: Pre-configured test scenarios for quick evaluation  
🔧 **Configurable**: Flexible business rules and skills mapping  
⚡ **Real-time Analysis**: Single record analysis with instant recommendations

## Business Logic

The LNA Bot uses intelligent business rules to determine training delivery methods:

- **External Training** (≤10 trainees): Cost-effective for small groups
- **Special Development Program (SDP)** (11-50 trainees): Balanced approach for medium groups
- **In-house Training** (>50 trainees): Efficient for large groups
- **Niche Competency Override**: SDP recommended for specialized skills regardless of group size

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/lna-bot.git
cd lna-bot

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Launch the Application

**Easy Launch (Recommended):**
```bash
# Using the launcher script
python start_app.py

# Or on Windows, double-click:
start_app.bat
```

**Manual Launch:**
```bash
# Start the Streamlit web interface directly
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

### 2. Choose Your Data Source

**Option A: Upload Your Own File**
- Click on "Upload Your File" tab
- Drag & drop or browse for your CSV/Excel file
- Click "Analyze File" to process

**Option B: Try Sample Datasets**
- Click on "Sample Datasets" tab
- Choose from 7 pre-configured test scenarios
- Load instantly with one click

**Option C: Single Record Analysis**
- Switch to "Single Record Analysis" tab
- Enter training details manually
- Get instant recommendations

### 3. Expected File Format

Your CSV/Excel file should contain these columns:
- `ID`: Unique identifier
- `Targeted competencies`: Competency name
- `Estimated trainees`: Number of trainees  
- `Priority`: Priority level (High/Medium/Low)
- `Department`: Department name
- `Division`: Division name
- `Submission`: Date of request
lna-bot interactive
```

## Usage Examples

### Basic Analysis

```bash
# Run the main application
python main.py

### 4. Sample Datasets Available

The application includes 7 comprehensive test datasets:

- **🏢 Multi-Industry Comprehensive** (25 records): Mixed scenarios across industries
- **🚀 Niche Competencies** (25 records): Specialized skills testing SDP override
- **🏭 Large-Scale Training** (25 records): Enterprise programs (55-500 trainees)
- **👥 Small Group Edge Cases** (25 records): Individual/small group training (1-4 trainees)
- **💼 Business Competencies Mix** (25 records): Realistic business scenarios
- **⚠️ Error Handling Test** (25 records): Data validation and error recovery
- **📊 Excel Multi-Sheet** (75 records): Excel workbook with 3 sheets

## Configuration

### Business Rules Configuration

Configuration files are located in `config/business_rules.json`:

```json
{
  "external_threshold": 10,
  "in_house_threshold": 50,
  "priority_weights": {
    "High": 3,
    "Medium": 2,
    "Low": 1
  },
  "niche_competencies": [
    "Advanced Clinical Research",
    "Specialized Surgery Techniques"
  ],
  "common_competencies": [
    "Patient Safety",
    "Communication Skills"
  ]
}
```

### Skills Mapping Configuration

Located in `config/skills_mapping.json`:

```json
{
  "competency_skills": {
    "Patient Safety": [
      "Risk Assessment",
      "Safety Protocols",
      "Incident Reporting"
    ],
    "Communication Skills": [
      "Active Listening",
      "Empathy",
      "Clear Documentation"
    ]
  }
}
```

## CLI Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `analyze` | Analyze LNA CSV file |
| `interactive` | Start interactive mode |
| `config` | Show configuration |
| `skills` | Show skills for competency |

### Global Options

| Option | Description |
|--------|-------------|
| `-c, --config-dir` | Configuration directory |
| `-v, --verbose` | Enable verbose logging |
| `--help` | Show help message |

### Analyze Command Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output JSON file path |
| `-s, --summary-only` | Show only summary |
| `-d, --export-detailed` | Export detailed results |

## Output Formats

### Console Output

The tool provides rich console output with:
- Color-coded training type recommendations
- Summary tables with statistics
- Progress indicators
- Interactive prompts

### JSON Export

Detailed results are exported in structured JSON format:

```json
{
  "metadata": {
    "total_records": 80,
    "analysis_timestamp": "2024-01-15T10:30:00",
    "bot_version": "1.0.0"
  },
  "summary": {
    "total_records": 80,
    "in_house_count": 25,
    "sdp_count": 35,
    "external_count": 20
  },
  "results": [
    {
      "record_id": "LNA001",
      "competency": "Patient Safety",
      "training_type": "SDP",
      "reasoning": "Medium group size with high priority"
    }
  ]
}
```

## Architecture

### Project Structure

```
v4_cli/
├── src/                    # Source code
│   └── lna_bot/           # Main package
│       ├── __init__.py    # Package initialization & main LNABot class
│       ├── decision_engine.py  # Core business logic
│       ├── data_processor.py   # Data processing & validation
│       └── lna_bot.py     # LNA Bot implementation
├── tests/                 # Test suite
│   ├── integration/       # Integration tests
│   └── unit/             # Unit tests (future)
├── examples/             # Usage examples and demos
├── docs/                 # Documentation
├── config/               # Configuration files
│   ├── business_rules.json
│   └── skills_mapping.json
├── data/                 # Data files and datasets
│   └── test_datasets/    # Test CSV files
├── outputs/              # Generated outputs
├── logs/                 # Application logs
├── scripts/              # Utility scripts
├── main.py              # Main entry point
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Key Components

- **LNABot**: Main application orchestrator
- **DecisionEngine**: Core business logic for recommendations
- **DataProcessor**: Data conversion and validation
- **ConfigurationLoader**: Loads business rules and mappings
- **CLI**: Rich command-line interface

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/lna-bot.git
cd lna-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate     # Windows

# Install in development mode
pip install -e .[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lna_bot

# Run specific test file
pytest tests/test_decision_engine.py
```

### Code Quality

```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

## Testing Data

The project includes comprehensive test data:

### Sample Data Files

- `lna_healthcare_data.csv`: 20 healthcare competency records
- `lna_it_data.csv`: 20 IT competency records  
- `lna_management_data.csv`: 20 management competency records
- `lna_mixed_data.csv`: 20 mixed competency records

### Expected Results

All test data includes corresponding expected results in JSON format for validation.

## Troubleshooting

### Common Issues

**Configuration Not Found**
```bash
# Ensure configuration directory exists
ls config/
```

**Import Errors**
```bash
# Install in development mode
pip install -e .
```

**CSV Format Issues**
- Ensure all required columns are present
- Check for proper encoding (UTF-8)
- Verify numeric fields contain valid numbers

### Logging

The application logs to `logs/lna_bot.log` file:

```bash
# Check log file (Windows)
Get-Content logs\lna_bot.log -Tail 10 -Wait

# Check log file (Linux/Mac)
tail -f logs/lna_bot.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test data for examples

## Changelog

### Version 4.0.0 (Current)
- 🏗️ **Major Project Reorganization**: Professional Python package structure
- 📁 **Improved Directory Structure**: Separated concerns with dedicated directories
- ✅ **Enhanced Testing Framework**: Organized integration and unit test structure  
- 📚 **Comprehensive Documentation**: README files for each directory
- 🔧 **Better Configuration Management**: Centralized config directory
- 📊 **Organized Data Management**: Structured data and outputs directories
- 🛡️ **Security Improvements**: .gitignore and proper file organization

### Version 1.0.0
- Initial release
- Core decision engine implementation
- CLI interface with rich formatting
- Configuration management
- Comprehensive test suite
- JSON export functionality
- Interactive mode