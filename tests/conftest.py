"""
Shared pytest fixtures and configuration for all tests.

This module provides common fixtures used across unit, property-based,
and integration tests for the 3NF normalization system.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pandas as pd
import pytest
from hypothesis import settings, Verbosity
from PySide6.QtWidgets import QApplication

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ============================================================================
# Hypothesis Configuration
# ============================================================================

# Default profile for most tests
settings.register_profile("default", max_examples=100, deadline=None)

# Fast profile for quick testing during development
settings.register_profile("fast", max_examples=10, deadline=None)

# Thorough profile for CI/CD
settings.register_profile("ci", max_examples=1000, deadline=None, verbosity=Verbosity.verbose)

# Load profile from environment or use default
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))


# ============================================================================
# Qt Application Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def qapp() -> Generator[QApplication, None, None]:
    """
    Provide a QApplication instance for the entire test session.
    
    This fixture ensures that Qt widgets can be created and tested.
    It's session-scoped to avoid creating multiple QApplication instances.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # QApplication cleanup happens automatically


# ============================================================================
# File System Fixtures
# ============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Provide a temporary directory for test file operations.
    
    The directory is automatically cleaned up after the test completes.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_csv_file(temp_dir: Path) -> Path:
    """
    Create a temporary CSV file with sample data.
    
    Returns the path to the created CSV file.
    """
    csv_path = temp_dir / "test_data.csv"
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "city": ["New York", "London", "Paris", "Tokyo", "Sydney"]
    })
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def large_csv_file(temp_dir: Path) -> Path:
    """
    Create a large CSV file (>100MB) for performance testing.
    
    Returns the path to the created CSV file.
    """
    csv_path = temp_dir / "large_data.csv"
    # Create approximately 2 million rows to exceed 100MB
    num_rows = 2_000_000
    df = pd.DataFrame({
        "id": range(num_rows),
        "value": [f"data_{i}" for i in range(num_rows)],
        "number": range(num_rows)
    })
    df.to_csv(csv_path, index=False)
    return csv_path


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """
    Provide a sample DataFrame for testing data operations.
    """
    return pd.DataFrame({
        "student_id": [1, 2, 3, 4, 5],
        "student_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "course_id": [101, 102, 101, 103, 102],
        "course_name": ["Math", "Physics", "Math", "Chemistry", "Physics"],
        "grade": ["A", "B", "A", "C", "B"]
    })


@pytest.fixture
def normalized_dataframe() -> dict:
    """
    Provide a sample normalized dataset (3NF) for testing.
    
    Returns a dictionary with table names as keys and DataFrames as values.
    """
    students = pd.DataFrame({
        "student_id": [1, 2, 3, 4, 5],
        "student_name": ["Alice", "Bob", "Charlie", "David", "Eve"]
    })
    
    courses = pd.DataFrame({
        "course_id": [101, 102, 103],
        "course_name": ["Math", "Physics", "Chemistry"]
    })
    
    enrollments = pd.DataFrame({
        "student_id": [1, 2, 3, 4, 5],
        "course_id": [101, 102, 101, 103, 102],
        "grade": ["A", "B", "A", "C", "B"]
    })
    
    return {
        "students": students,
        "courses": courses,
        "enrollments": enrollments
    }


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def test_config() -> dict:
    """
    Provide test configuration settings.
    """
    return {
        "chunk_size_mb": 10,
        "max_workers": 4,
        "memory_threshold": 0.8,
        "log_level": "DEBUG",
        "enable_performance_tracking": True
    }


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_progress_callback():
    """
    Provide a mock progress callback function for testing.
    
    Tracks all progress updates received.
    """
    class ProgressTracker:
        def __init__(self):
            self.updates = []
        
        def __call__(self, progress: float):
            self.updates.append(progress)
        
        def get_updates(self):
            return self.updates
        
        def reset(self):
            self.updates = []
    
    return ProgressTracker()


# ============================================================================
# Cleanup Hooks
# ============================================================================

@pytest.fixture(autouse=True)
def reset_environment():
    """
    Reset environment variables and state before each test.
    
    This fixture runs automatically for every test.
    """
    # Store original environment
    original_env = os.environ.copy()
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    """
    config.addinivalue_line(
        "markers", "requires_qt: mark test as requiring Qt application"
    )
    config.addinivalue_line(
        "markers", "requires_large_memory: mark test as requiring significant memory"
    )
