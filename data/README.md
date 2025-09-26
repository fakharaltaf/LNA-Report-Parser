# Data Directory

This directory contains all data files used by the LNA Bot application.

## Structure

### `test_datasets/`
CSV files used for testing and development:
- `test_data.csv` - Sample learning data
- `test_data_advanced.csv` - Complex scenarios
- `test_data_edge_cases.csv` - Edge case testing
- `test_data_large.csv` - Performance testing data

### `models/` (Future)
Machine learning models and weights:
- Trained model files
- Model configurations
- Feature encoders

### `reference/` (Future)
Reference data and lookup tables:
- Category mappings
- Validation rules
- Static configuration data

## File Formats

### CSV Files
Standard format for test datasets:
- UTF-8 encoding
- Comma-separated values
- Header row required
- Consistent column naming

### Expected Columns
Test CSV files should include:
- `student_id` - Unique identifier
- `learning_objective` - What the student wants to learn
- `current_knowledge` - Current skill level
- `preferred_style` - Learning style preference
- Additional context columns as needed

## Usage Guidelines

### Adding New Test Data
1. Follow existing naming conventions
2. Include representative samples
3. Document data sources and formats
4. Ensure data privacy compliance

### Data Quality
- Validate data integrity before use
- Remove personally identifiable information
- Use consistent formatting
- Include edge cases for robust testing

## Security Notes

- No sensitive data should be stored here
- Use synthetic or anonymized data for testing
- Regular cleanup of temporary data files
- Backup important datasets