# Tests

This directory contains all test files for the LNA Bot project.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for complete workflows  
- `fixtures/` - Test data and configuration files

## Running Tests

To run all tests:
```bash
python -m pytest tests/
```

To run specific test categories:
```bash
# Integration tests only
python tests/integration/test_simple.py

# Installation tests
python tests/integration/test_installation.py
```

## Test Coverage

The tests cover:
- ✅ Business logic validation
- ✅ Data processing and validation
- ✅ CSV file analysis
- ✅ Configuration loading
- ✅ Error handling
- ✅ Export functionality