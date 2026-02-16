# Test Suite Documentation

This directory contains the comprehensive test suite for the 3NF Data Normalization System.

## Directory Structure

```
tests/
├── unit/               # Unit tests for individual components
├── property/           # Property-based tests using Hypothesis
├── integration/        # Integration tests for end-to-end workflows
├── conftest.py         # Shared fixtures and pytest configuration
└── README.md          # This file
```

## Test Categories

### Unit Tests (`tests/unit/`)
Unit tests verify individual functions, classes, and methods in isolation. These tests should be:
- Fast (< 1 second each)
- Focused on a single unit of functionality
- Independent of external systems

### Property-Based Tests (`tests/property/`)
Property-based tests use Hypothesis to verify universal properties across many generated inputs. These tests:
- Validate correctness properties from the design document
- Run 100+ iterations with diverse inputs
- Help discover edge cases automatically

### Integration Tests (`tests/integration/`)
Integration tests verify end-to-end workflows and component interactions. These tests:
- May be slower (several seconds)
- Test complete user workflows
- Verify system behavior with real data

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
pytest tests/unit/              # Unit tests only
pytest tests/property/          # Property tests only
pytest tests/integration/       # Integration tests only
```

### Run with markers
```bash
pytest -m unit                  # All unit tests
pytest -m property              # All property-based tests
pytest -m integration           # All integration tests
pytest -m "not slow"            # Skip slow tests
```

### Run with coverage
```bash
pytest --cov=utils --cov=ui --cov-report=html
```

### Run in parallel
```bash
pytest -n auto                  # Use all CPU cores
pytest -n 4                     # Use 4 workers
```

## Hypothesis Profiles

Configure Hypothesis behavior with environment variables:

```bash
# Default profile (100 examples)
pytest

# Fast profile for development (10 examples)
HYPOTHESIS_PROFILE=fast pytest

# Thorough profile for CI (1000 examples)
HYPOTHESIS_PROFILE=ci pytest
```

## Coverage Requirements

The test suite aims for:
- **80%+ overall code coverage** (enforced by pytest.ini)
- **100% coverage** for critical business logic
- **Branch coverage** enabled to catch untested code paths

View coverage report:
```bash
pytest --cov=utils --cov=ui --cov-report=html
# Open htmlcov/index.html in browser
```

## Writing Tests

### Unit Test Example
```python
import pytest

def test_function_behavior():
    result = my_function(input_data)
    assert result == expected_output
```

### Property-Based Test Example
```python
from hypothesis import given, strategies as st

@given(st.integers())
def test_property(n):
    result = my_function(n)
    assert result >= 0  # Universal property
```

### Integration Test Example
```python
@pytest.mark.integration
def test_end_to_end_workflow(temp_csv_file):
    # Load data
    data = load_csv(temp_csv_file)
    
    # Transform
    normalized = normalize_to_3nf(data)
    
    # Verify
    assert validate_3nf(normalized)
```

## Fixtures

Common fixtures are defined in `conftest.py`:

- `qapp`: QApplication instance for Qt tests
- `temp_dir`: Temporary directory for file operations
- `temp_csv_file`: Sample CSV file
- `large_csv_file`: Large CSV file (>100MB) for performance tests
- `sample_dataframe`: Sample pandas DataFrame
- `normalized_dataframe`: Sample normalized dataset
- `test_config`: Test configuration dictionary
- `mock_progress_callback`: Mock callback for progress tracking

## Continuous Integration

Tests run automatically on:
- Every commit (fast profile)
- Pull requests (default profile)
- Main branch (thorough CI profile)

## Troubleshooting

### Qt tests fail
Ensure `pytest-qt` is installed and `QT_API` environment variable is set:
```bash
pip install pytest-qt
export QT_API=pyside6
```

### Hypothesis tests are slow
Use the fast profile during development:
```bash
HYPOTHESIS_PROFILE=fast pytest
```

### Coverage is below 80%
Identify untested code:
```bash
pytest --cov=utils --cov=ui --cov-report=term-missing
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-qt documentation](https://pytest-qt.readthedocs.io/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
