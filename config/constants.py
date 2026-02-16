"""
Application constants and configuration
"""

# Application Info
APP_NAME = "Transform 3NF"
APP_VERSION = "3.0.0"

# UI Constants
PREVIEW_ROWS = 15
DEFAULT_GRID_SIZE = 20

# File Extensions
SUPPORTED_CSV_EXTENSIONS = [".csv"]
SUPPORTED_EXCEL_EXTENSIONS = [".xlsx", ".xls"]
SUPPORTED_JSON_EXTENSIONS = [".json"]
SUPPORTED_DB_EXTENSIONS = [".db", ".sqlite"]

# Database Types
DB_TYPE_SQLITE = "sqlite"
DB_TYPE_MYSQL = "mysql"
DB_TYPE_POSTGRESQL = "postgresql"

# Export Formats
EXPORT_FORMAT_CSV = "csv"
EXPORT_FORMAT_EXCEL = "excel"
EXPORT_FORMAT_JSON = "json"
EXPORT_FORMAT_SQL = "sql"
EXPORT_FORMAT_SQLITE = "sqlite"

# Status Messages
STATUS_READY = "Sẵn sàng"
STATUS_LOADING = "Đang tải..."
STATUS_PROCESSING = "Đang xử lý..."
STATUS_SUCCESS = "Thành công"
STATUS_ERROR = "Lỗi"

# Status Colors
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_WARNING = "orange"
COLOR_INFO = "blue"

# Table Types
TABLE_TYPE_DIM = "Dim"
TABLE_TYPE_FACT = "Fact"

# ETL Pipeline
DEFAULT_PIPELINE_NAME = "default_pipeline"
PIPELINE_STORAGE_FILE = ".pipelines.json"

# Connection Manager
CONNECTIONS_STORAGE_FILE = ".connections.json"
