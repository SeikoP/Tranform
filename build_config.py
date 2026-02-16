"""
Build configuration for Transform 3NF application
Supports: PyInstaller (EXE), Docker, and Runtime options
"""

# PyInstaller Configuration
PYINSTALLER_CONFIG = {
    'name': 'Transform3NF',
    'icon': 'assets/normalization.ico',
    'onefile': True,  # Single EXE file
    'windowed': True,  # No console window
    'add_data': [
        ('qml', 'qml'),
        ('assets', 'assets'),
    ],
    'hidden_imports': [
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'pandas',
        'numpy',
        'sklearn',
        'openpyxl',
    ],
    'exclude_modules': [
        'matplotlib',
        'scipy',
        'PIL',
        'tkinter',
    ],
}

# Docker Configuration
DOCKER_CONFIG = {
    'base_image': 'python:3.11-slim',
    'expose_port': 8080,
    'volumes': [
        '/app/data',
        '/app/exports',
    ],
}

# Runtime Configuration
RUNTIME_CONFIG = {
    'python_version': '3.11+',
    'required_packages': [
        'PySide6>=6.7.0',
        'pandas>=2.2.1',
        'numpy>=1.26.4',
        'scikit-learn>=1.4.1',
        'openpyxl>=3.1.2',
    ],
    'optional_packages': {
        'mysql': 'pymysql>=1.1.0',
        'postgresql': 'psycopg2-binary>=2.9.9',
        'sqlserver': 'pyodbc>=5.0.0',
    },
}
