# LNA Bot - AI-Powered Training Recommendations

An intelligent command-line tool that analyzes Learning Need Analysis (LNA) reports and provides automated recommendations for training delivery methods.

## Features

🤖 **AI-Powered Analysis**: Intelligent decision engine for training recommendations  
📊 **CSV Processing**: Batch analysis of LNA reports in CSV format  
🎯 **Smart Classification**: Automatic competency classification (niche vs common)  
📈 **Comprehensive Reporting**: Detailed analysis summaries and export capabilities  
🖥️ **CLI Interface**: User-friendly command-line interface with rich formatting  
⚡ **Interactive Mode**: Real-time single record analysis  
🔧 **Configurable**: Flexible business rules and skills mapping

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

### 1. Prepare Your Data

Ensure your LNA CSV file contains these columns:
- `id`: Unique identifier
- `competency`: Competency name
- `estimated_trainees`: Number of trainees
- `priority`: Priority level (High/Medium/Low)
- `department`: Department name
- `justification`: Analysis justification

### 2. Run Analysis

```bash
# Analyze a CSV file
lna-bot analyze data/lna_report.csv

# Export detailed results
lna-bot analyze data/lna_report.csv --export-detailed -o results.json

# Show summary only
lna-bot analyze data/lna_report.csv --summary-only
```

### 3. Interactive Mode

```bash
# Start interactive analysis
lna-bot interactive
```

## Usage Examples

### Basic Analysis

```bash
# Analyze LNA file with default settings
lna-bot analyze Testing/LNA_Sample_Data/lna_healthcare_data.csv
```

### Advanced Analysis

```bash
# Custom configuration directory and detailed export
lna-bot -c ./custom_config analyze data.csv -d -o detailed_results.json
```

### Configuration Management

```bash
# View current configuration
lna-bot config

# Check skills for a competency
lna-bot skills "Patient Safety"
```

## Configuration

### Business Rules Configuration

Create `Testing/Configuration/business_rules.json`:

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

Create `Testing/Configuration/skills_mapping.json`:

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
lna-bot/
├── src/lna_bot/
│   ├── __init__.py          # Main LNABot class
│   ├── cli.py               # CLI interface
│   ├── models/              # Data models
│   ├── core/                # Business logic
│   └── utils/               # Utilities
├── Testing/
│   ├── Configuration/       # Config files
│   └── LNA_Sample_Data/     # Test data
├── requirements.txt
├── setup.py
└── README.md
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
ls Testing/Configuration/
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

The application logs to both console and `lna_bot.log` file:

```bash
# Enable verbose logging
lna-bot -v analyze data.csv

# Check log file
tail -f lna_bot.log
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

### Version 1.0.0
- Initial release
- Core decision engine implementation
- CLI interface with rich formatting
- Configuration management
- Comprehensive test suite
- JSON export functionality
- Interactive mode