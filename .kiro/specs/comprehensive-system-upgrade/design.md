# Design Document: Comprehensive System Upgrade

## Overview

Tài liệu này mô tả thiết kế chi tiết cho việc nâng cấp toàn diện hệ thống chuẩn hóa dữ liệu 3NF. Hệ thống hiện tại sử dụng kiến trúc PySide6/QML với Python backend và QML frontend. Việc nâng cấp tập trung vào 10 khía cạnh chính: performance optimization, data versioning, UI/UX enhancement, collaboration features, visual ETL builder, advanced validation, AI suggestions, logging/monitoring, security, và comprehensive testing.

### Design Goals

1. **Performance**: Xử lý datasets lớn (>100MB) hiệu quả với chunk processing và multi-threading
2. **Reliability**: Version control và rollback capabilities để đảm bảo data safety
3. **Usability**: Modern UI/UX với dark mode, responsive design, và visual pipeline builder
4. **Collaboration**: Export/import projects để hỗ trợ team workflows
5. **Quality**: Advanced validation rules và AI-powered suggestions
6. **Observability**: Comprehensive logging và monitoring
7. **Security**: Encrypted credentials và secure database connections
8. **Maintainability**: High test coverage với unit và property-based tests

## Architecture

### Current Architecture

```
┌─────────────────────────────────────────────────┐
│              QML Frontend (UI)                  │
│  - Main.qml (entry point)                       │
│  - Component-based UI structure                 │
└─────────────────┬───────────────────────────────┘
                  │ Qt Signals/Slots
┌─────────────────▼───────────────────────────────┐
│           DataBridge (Python-QML Bridge)        │
│  - Exposes Python methods to QML                │
│  - Manages signals for UI updates               │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Business Logic Layer               │
│  ┌──────────────────────────────────────────┐   │
│  │ utils/data_analysis.py                   │   │
│  │ - AdvancedNormalizer                     │   │
│  │ - analyze_dependencies()                 │   │
│  ├──────────────────────────────────────────┤   │
│  │ utils/data_connectors.py                 │   │
│  │ - DataConnector                          │   │
│  │ - ConnectionManager                      │   │
│  ├──────────────────────────────────────────┤   │
│  │ utils/etl_engine.py                      │   │
│  │ - ETLPipeline                            │   │
│  │ - PipelineManager                        │   │
│  │ - TransformRule                          │   │
│  │ - DataQualityChecker                     │   │
│  ├──────────────────────────────────────────┤   │
│  │ utils/file_utils.py                      │   │
│  │ - get_data()                             │   │
│  ├──────────────────────────────────────────┤   │
│  │ utils/sql_generator.py                   │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Enhanced Architecture


Kiến trúc nâng cấp sẽ thêm các modules mới và cải thiện các modules hiện có:

```
┌─────────────────────────────────────────────────────────────┐
│                   QML Frontend (Enhanced)                   │
│  - Dark mode support                                        │
│  - Responsive layouts                                       │
│  - Visual pipeline builder canvas                           │
│  - Version history viewer                                   │
│  - Data quality dashboard                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ Qt Signals/Slots + Progress Updates
┌─────────────────▼───────────────────────────────────────────┐
│           Enhanced DataBridge                               │
│  - Async operation support                                  │
│  - Progress tracking                                        │
│  - Cancellation support                                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Enhanced Business Logic Layer                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │ NEW: utils/performance_optimizer.py                │     │
│  │ - ChunkProcessor (streaming data processing)       │     │
│  │ - MultiThreadExecutor (parallel operations)        │     │
│  │ - MemoryMonitor (adaptive processing mode)         │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/version_controller.py                   │     │
│  │ - VersionManager (snapshot management)             │     │
│  │ - DiffEngine (differential storage)                │     │
│  │ - VersionComparator (diff visualization)           │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/ui_manager.py                           │     │
│  │ - ThemeManager (dark/light mode)                   │     │
│  │ - LayoutManager (responsive design)                │     │
│  │ - PreferenceStore (settings persistence)           │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/project_manager.py                      │     │
│  │ - ProjectSerializer (export/import)                │     │
│  │ - ProjectValidator (compatibility checks)          │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ ENHANCED: utils/etl_engine.py                      │     │
│  │ - VisualPipelineBuilder (graph-based UI)          │     │
│  │ - NodeRegistry (transformation catalog)            │     │
│  │ - SchemaValidator (connection validation)          │     │
│  │ - PipelineSerializer (save/load pipelines)         │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/validation_engine.py                    │     │
│  │ - RuleEngine (validation rule execution)           │     │
│  │ - RuleBuilder (custom rule creation)               │     │
│  │ - ValidationReporter (quality reports)             │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/ai_suggester.py                         │     │
│  │ - DependencyAnalyzer (functional dependencies)     │     │
│  │ - PrimaryKeyDetector (ML-based PK suggestion)      │     │
│  │ - TransformationRecommender (next-step hints)      │     │
│  │ - DataQualityAnalyzer (issue detection)            │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/logger.py                               │     │
│  │ - StructuredLogger (comprehensive logging)         │     │
│  │ - LogRotator (automatic rotation)                  │     │
│  │ - MetricsCollector (performance tracking)          │     │
│  │ - NotificationService (alerts)                     │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ NEW: utils/security_manager.py                     │     │
│  │ - CredentialEncryptor (AES-256 encryption)         │     │
│  │ - SecureConnectionManager (SSL/TLS support)        │     │
│  │ - SecretStore (secure credential storage)          │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Separation of Concerns**: Mỗi module mới có trách nhiệm rõ ràng và độc lập
2. **Backward Compatibility**: Các modules hiện có được enhance chứ không rewrite hoàn toàn
3. **Async Operations**: Sử dụng QThread cho long-running operations để không block UI
4. **Plugin Architecture**: ETL nodes và validation rules có thể extend dễ dàng
5. **Event-Driven**: Sử dụng Qt Signals/Slots cho loose coupling giữa components

## Components and Interfaces



### 1. Performance Optimizer Module

**ChunkProcessor**
```python
class ChunkProcessor:
    def __init__(self, chunk_size_mb: int = 10):
        self.chunk_size = chunk_size_mb * 1024 * 1024
        
    def process_file_in_chunks(self, file_path: str, 
                               processor_func: Callable,
                               progress_callback: Optional[Callable] = None) -> pd.DataFrame:
        """Process large files in chunks to avoid memory overflow"""
        pass
        
    def estimate_chunk_count(self, file_path: str) -> int:
        """Estimate number of chunks for progress tracking"""
        pass
```

**MultiThreadExecutor**
```python
class MultiThreadExecutor:
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or os.cpu_count()
        
    def execute_parallel(self, tasks: List[Callable], 
                        cancellation_token: Optional[CancellationToken] = None) -> List[Any]:
        """Execute independent tasks in parallel"""
        pass
        
    def map_parallel(self, func: Callable, items: List[Any]) -> List[Any]:
        """Apply function to items in parallel"""
        pass
```

**MemoryMonitor**
```python
class MemoryMonitor:
    def __init__(self, threshold_percent: float = 0.8):
        self.threshold = threshold_percent
        
    def get_memory_usage(self) -> float:
        """Get current memory usage as percentage"""
        pass
        
    def should_use_disk_mode(self) -> bool:
        """Check if should switch to disk-based processing"""
        pass
        
    def start_monitoring(self, callback: Callable):
        """Start background memory monitoring"""
        pass
```

### 2. Version Controller Module

**VersionManager**
```python
class Version:
    id: str
    timestamp: datetime
    description: str
    data_hash: str
    metadata: Dict[str, Any]

class VersionManager:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.versions: List[Version] = []
        
    def create_snapshot(self, data: pd.DataFrame, 
                       description: str = "") -> Version:
        """Create new version snapshot"""
        pass
        
    def restore_version(self, version_id: str) -> pd.DataFrame:
        """Restore data to specific version"""
        pass
        
    def list_versions(self) -> List[Version]:
        """Get all versions with metadata"""
        pass
        
    def delete_version(self, version_id: str):
        """Delete specific version"""
        pass
```

**DiffEngine**
```python
class DiffEngine:
    def compute_diff(self, old_data: pd.DataFrame, 
                    new_data: pd.DataFrame) -> Dict[str, Any]:
        """Compute differential changes between versions"""
        pass
        
    def apply_diff(self, base_data: pd.DataFrame, 
                   diff: Dict[str, Any]) -> pd.DataFrame:
        """Apply diff to reconstruct version"""
        pass
        
    def estimate_storage_size(self, diff: Dict[str, Any]) -> int:
        """Estimate storage size for diff"""
        pass
```

**VersionComparator**
```python
class VersionComparator:
    def compare_versions(self, version1_id: str, 
                        version2_id: str) -> ComparisonResult:
        """Compare two versions and highlight differences"""
        pass
        
    def get_schema_changes(self, v1: pd.DataFrame, 
                          v2: pd.DataFrame) -> List[SchemaChange]:
        """Detect schema changes between versions"""
        pass
        
    def get_data_changes(self, v1: pd.DataFrame, 
                        v2: pd.DataFrame) -> DataChangeSummary:
        """Summarize data content changes"""
        pass
```

### 3. UI Manager Module

**ThemeManager**
```python
class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager(QObject):
    themeChanged = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = Theme.LIGHT
        
    def set_theme(self, theme: Theme):
        """Switch application theme"""
        pass
        
    def get_theme(self) -> Theme:
        """Get current theme"""
        pass
        
    def apply_theme_to_qml(self, engine: QQmlApplicationEngine):
        """Apply theme colors to QML context"""
        pass
```

**PreferenceStore**
```python
class PreferenceStore:
    def __init__(self, config_path: str = "~/.3nf_normalizer/preferences.json"):
        self.config_path = Path(config_path).expanduser()
        
    def save_preference(self, key: str, value: Any):
        """Save user preference"""
        pass
        
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        pass
        
    def save_layout(self, layout_config: Dict[str, Any]):
        """Save window layout configuration"""
        pass
        
    def load_layout(self) -> Dict[str, Any]:
        """Load saved layout configuration"""
        pass
```

### 4. Project Manager Module

**ProjectSerializer**
```python
class Project:
    name: str
    version: str
    created_at: datetime
    data_sources: List[DataSource]
    erd_design: Dict[str, Any]
    etl_pipelines: List[ETLPipeline]
    transform_rules: List[TransformRule]
    validation_rules: List[ValidationRule]
    metadata: Dict[str, Any]

class ProjectSerializer:
    def export_project(self, project: Project, 
                      output_path: str,
                      include_data: bool = True):
        """Export project to portable file"""
        pass
        
    def import_project(self, file_path: str) -> Project:
        """Import project from file"""
        pass
        
    def export_selective(self, project: Project,
                        components: List[str],
                        output_path: str):
        """Export selected project components"""
        pass
```

**ProjectValidator**
```python
class ProjectValidator:
    def validate_project_file(self, file_path: str) -> ValidationResult:
        """Validate project file format and structure"""
        pass
        
    def check_version_compatibility(self, project_version: str) -> bool:
        """Check if project version is compatible"""
        pass
        
    def detect_conflicts(self, project: Project) -> List[Conflict]:
        """Detect conflicts in imported project"""
        pass
```

### 5. Enhanced ETL Engine

**VisualPipelineBuilder**
```python
class PipelineNode:
    id: str
    type: str
    position: Tuple[float, float]
    config: Dict[str, Any]
    input_schema: Optional[Schema]
    output_schema: Optional[Schema]

class PipelineConnection:
    source_node_id: str
    target_node_id: str
    source_port: str
    target_port: str

class VisualPipelineBuilder(QObject):
    nodeAdded = Signal(str)
    nodeRemoved = Signal(str)
    connectionAdded = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.nodes: Dict[str, PipelineNode] = {}
        self.connections: List[PipelineConnection] = []
        
    def add_node(self, node_type: str, position: Tuple[float, float]) -> PipelineNode:
        """Add transformation node to canvas"""
        pass
        
    def remove_node(self, node_id: str):
        """Remove node from canvas"""
        pass
        
    def connect_nodes(self, source_id: str, target_id: str) -> bool:
        """Connect two nodes with validation"""
        pass
        
    def validate_connection(self, source: PipelineNode, 
                          target: PipelineNode) -> bool:
        """Validate schema compatibility"""
        pass
        
    def execute_pipeline(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """Execute pipeline in topological order"""
        pass
        
    def serialize_pipeline(self) -> Dict[str, Any]:
        """Serialize pipeline to JSON"""
        pass
```

**NodeRegistry**
```python
class TransformationNode:
    name: str
    category: str
    description: str
    input_schema_requirements: List[str]
    output_schema_template: Callable
    execute: Callable

class NodeRegistry:
    def __init__(self):
        self.nodes: Dict[str, TransformationNode] = {}
        self._register_builtin_nodes()
        
    def register_node(self, node: TransformationNode):
        """Register custom transformation node"""
        pass
        
    def get_node(self, node_type: str) -> TransformationNode:
        """Get node definition"""
        pass
        
    def list_nodes_by_category(self) -> Dict[str, List[str]]:
        """List available nodes grouped by category"""
        pass
```

### 6. Validation Engine Module

**RuleEngine**
```python
class ValidationRule:
    name: str
    rule_type: str  # range, pattern, unique, referential, custom
    config: Dict[str, Any]
    enabled: bool

class ValidationResult:
    passed: bool
    violations: List[Violation]
    statistics: Dict[str, Any]

class RuleEngine:
    def __init__(self):
        self.rules: List[ValidationRule] = []
        
    def add_rule(self, rule: ValidationRule):
        """Add validation rule"""
        pass
        
    def validate_dataset(self, data: pd.DataFrame) -> ValidationResult:
        """Apply all rules to dataset"""
        pass
        
    def validate_row(self, row: pd.Series, 
                    rules: List[ValidationRule]) -> List[Violation]:
        """Validate single row"""
        pass
```

**RuleBuilder**
```python
class RuleBuilder:
    def create_range_rule(self, column: str, 
                         min_val: Any, max_val: Any) -> ValidationRule:
        """Create range check rule"""
        pass
        
    def create_pattern_rule(self, column: str, 
                          pattern: str) -> ValidationRule:
        """Create regex pattern rule"""
        pass
        
    def create_unique_rule(self, columns: List[str]) -> ValidationRule:
        """Create uniqueness constraint"""
        pass
        
    def create_custom_rule(self, name: str, 
                          expression: str) -> ValidationRule:
        """Create custom Python/SQL rule"""
        pass
        
    def create_cross_column_rule(self, columns: List[str],
                                constraint: str) -> ValidationRule:
        """Create cross-column constraint"""
        pass
```

### 7. AI Suggester Module

**DependencyAnalyzer**
```python
class DependencyAnalyzer:
    def analyze_functional_dependencies(self, 
                                       data: pd.DataFrame) -> List[Dependency]:
        """Detect functional dependencies in data"""
        pass
        
    def suggest_normalization_steps(self, 
                                   dependencies: List[Dependency]) -> List[NormalizationStep]:
        """Recommend steps to achieve 3NF"""
        pass
```

**PrimaryKeyDetector**
```python
class PrimaryKeyDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.model = self._load_model(model_path)
        
    def suggest_primary_keys(self, data: pd.DataFrame) -> List[PKSuggestion]:
        """Suggest potential primary key columns"""
        pass
        
    def calculate_confidence(self, column: pd.Series) -> float:
        """Calculate confidence score for PK candidate"""
        pass
```

**TransformationRecommender**
```python
class TransformationRecommender:
    def recommend_next_steps(self, current_data: pd.DataFrame,
                            pipeline_history: List[str]) -> List[Recommendation]:
        """Recommend next transformation steps"""
        pass
        
    def explain_recommendation(self, recommendation: Recommendation) -> str:
        """Provide explanation for recommendation"""
        pass
```

### 8. Logger Module

**StructuredLogger**
```python
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StructuredLogger:
    def __init__(self, log_dir: str = "~/.3nf_normalizer/logs"):
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
    def log(self, level: LogLevel, message: str, 
           context: Optional[Dict[str, Any]] = None):
        """Log structured message"""
        pass
        
    def log_operation(self, operation: str, user: str, 
                     outcome: str, duration: float):
        """Log operation with metadata"""
        pass
        
    def log_error(self, error: Exception, context: Dict[str, Any]):
        """Log error with full context"""
        pass
```

**MetricsCollector**
```python
class MetricsCollector:
    def record_operation_duration(self, operation: str, duration: float):
        """Record operation timing"""
        pass
        
    def record_memory_usage(self, operation: str, memory_mb: float):
        """Record memory consumption"""
        pass
        
    def record_cpu_usage(self, operation: str, cpu_percent: float):
        """Record CPU utilization"""
        pass
        
    def get_metrics_summary(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Get aggregated metrics"""
        pass
```

### 9. Security Manager Module

**CredentialEncryptor**
```python
class CredentialEncryptor:
    def __init__(self, key_path: str = "~/.3nf_normalizer/.key"):
        self.key_path = Path(key_path).expanduser()
        self.key = self._load_or_generate_key()
        
    def encrypt(self, plaintext: str) -> str:
        """Encrypt credential using AES-256"""
        pass
        
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt credential"""
        pass
```

**SecureConnectionManager**
```python
class SecureConnectionManager:
    def __init__(self, encryptor: CredentialEncryptor):
        self.encryptor = encryptor
        
    def create_connection(self, conn_config: Dict[str, Any],
                         use_ssl: bool = True) -> Connection:
        """Create secure database connection"""
        pass
        
    def save_connection_config(self, name: str, config: Dict[str, Any]):
        """Save connection with encrypted credentials"""
        pass
        
    def load_connection_config(self, name: str) -> Dict[str, Any]:
        """Load connection with decrypted credentials"""
        pass
```

## Data Models



### Version Model
```python
@dataclass
class Version:
    id: str  # UUID
    timestamp: datetime
    description: str
    data_hash: str  # SHA-256 hash of data
    diff_path: Optional[str]  # Path to diff file
    metadata: Dict[str, Any]  # Additional metadata
    parent_version_id: Optional[str]  # For version chain
```

### Project Model
```python
@dataclass
class DataSource:
    type: str  # csv, excel, json, sqlite, mysql, postgresql
    path: str
    config: Dict[str, Any]

@dataclass
class Project:
    name: str
    version: str  # Project format version
    created_at: datetime
    modified_at: datetime
    data_sources: List[DataSource]
    erd_design: Dict[str, Any]  # Table definitions
    etl_pipelines: List[Dict[str, Any]]  # Serialized pipelines
    transform_rules: List[Dict[str, Any]]
    validation_rules: List[Dict[str, Any]]
    metadata: Dict[str, Any]
```

### Pipeline Models
```python
@dataclass
class Schema:
    columns: List[str]
    types: Dict[str, str]
    constraints: List[str]

@dataclass
class PipelineNode:
    id: str
    type: str  # filter, map, join, aggregate, pivot, custom_sql
    position: Tuple[float, float]  # Canvas position
    config: Dict[str, Any]
    input_schema: Optional[Schema]
    output_schema: Optional[Schema]

@dataclass
class PipelineConnection:
    source_node_id: str
    target_node_id: str
    source_port: str = "output"
    target_port: str = "input"
```

### Validation Models
```python
@dataclass
class ValidationRule:
    name: str
    rule_type: str  # range, pattern, unique, referential, custom
    target_columns: List[str]
    config: Dict[str, Any]
    enabled: bool = True
    severity: str = "error"  # error, warning, info

@dataclass
class Violation:
    rule_name: str
    row_number: int
    column: str
    value: Any
    message: str
    severity: str

@dataclass
class ValidationResult:
    passed: bool
    total_rows: int
    violations: List[Violation]
    statistics: Dict[str, Any]
```

### AI Suggestion Models
```python
@dataclass
class Dependency:
    determinant: List[str]  # Left side of dependency
    dependent: List[str]    # Right side of dependency
    confidence: float

@dataclass
class PKSuggestion:
    columns: List[str]
    confidence: float
    reasoning: str

@dataclass
class Recommendation:
    type: str  # transformation, validation, normalization
    action: str
    confidence: float
    explanation: str
    parameters: Dict[str, Any]
```

### Log Models
```python
@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    operation: str
    user: str
    message: str
    context: Dict[str, Any]
    duration: Optional[float]
    outcome: str  # success, failure, partial

@dataclass
class MetricEntry:
    timestamp: datetime
    operation: str
    metric_type: str  # duration, memory, cpu
    value: float
    unit: str
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Performance Properties

**Property 1: Chunk Processing for Large Files**
*For any* CSV file larger than 100MB, when loaded by the Data_Processor, the system should process it using chunk-based streaming and memory usage should remain below the configured threshold.
**Validates: Requirements 1.1**

**Property 2: Progress Tracking Completeness**
*For any* long-running data processing operation, the system should emit progress updates that monotonically increase from 0% to 100% and the final progress value should equal 100%.
**Validates: Requirements 1.2**

**Property 3: Processing Performance Bounds**
*For any* dataset being normalized to 3NF, the processing time should be at most 5 seconds per 10MB of data size (linear time complexity).
**Validates: Requirements 1.3**

**Property 4: Multi-threading Utilization**
*For any* data processing operation with independent sub-tasks, the system should utilize multiple threads and the number of active threads should be greater than 1 during processing.
**Validates: Requirements 1.4**

**Property 5: Cancellation Responsiveness**
*For any* cancellable operation, when a user requests cancellation, the operation should terminate within 2 seconds and all allocated resources should be released.
**Validates: Requirements 1.6**

### Version Control Properties

**Property 6: Automatic Snapshot Creation**
*For any* data transformation operation, the Version_Controller should automatically create a version snapshot before applying the transformation.
**Validates: Requirements 2.1**

**Property 7: Version Information Completeness**
*For any* version in the version history, the system should provide timestamp, description, and change summary information.
**Validates: Requirements 2.2, 2.5**

**Property 8: Version Restore Round-Trip**
*For any* dataset state, creating a version snapshot, making arbitrary changes, then restoring that version should produce a dataset equivalent to the original state.
**Validates: Requirements 2.3**

**Property 9: Differential Storage Efficiency**
*For any* sequence of versions, the total storage size using differential storage should be less than storing each version as a complete copy.
**Validates: Requirements 2.4**

### UI/UX Properties

**Property 10: Theme Switching Performance**
*For any* theme toggle operation, the UI should complete the theme switch within 200ms.
**Validates: Requirements 3.1**

**Property 11: Responsive Layout Adaptation**
*For any* window resize operation, all UI components should remain visible and usable without overlapping or clipping.
**Validates: Requirements 3.2**

**Property 12: Navigation Animation Performance**
*For any* screen navigation, the transition animation should complete within 300ms.
**Validates: Requirements 3.3**

**Property 13: Configuration Persistence Round-Trip**
*For any* user preference or layout configuration, saving the configuration, restarting the application, then loading should restore the exact same configuration.
**Validates: Requirements 3.4, 3.7**

**Property 14: Virtual Scrolling for Large Tables**
*For any* data table with more than 1000 rows, the UI should use virtual scrolling and only render visible rows plus a small buffer.
**Validates: Requirements 3.5**

**Property 15: Tooltip Availability**
*For any* interactive UI element, hovering over it should display a contextual tooltip explaining its functionality.
**Validates: Requirements 3.6**

### Project Collaboration Properties

**Property 16: Project Export Completeness**
*For any* project export operation, the exported file should contain all data sources, transformation rules, ERD designs, ETL pipelines, and validation rules from the original project.
**Validates: Requirements 4.1, 4.3**

**Property 17: Project Import Validation**
*For any* project file being imported, the system should validate file format and version compatibility before attempting to load any components.
**Validates: Requirements 4.2**

**Property 18: Selective Export Functionality**
*For any* subset of project components selected for export, the exported file should contain exactly those components and no others.
**Validates: Requirements 4.5**

### ETL Pipeline Properties

**Property 19: Node Creation and Configuration**
*For any* transformation node type dragged onto the canvas, the system should create an instance with configurable properties specific to that node type.
**Validates: Requirements 5.2**

**Property 20: Schema Validation on Connection**
*For any* attempt to connect two pipeline nodes, the connection should only succeed if the output schema of the source node is compatible with the input requirements of the target node.
**Validates: Requirements 5.3**

**Property 21: Topological Execution Order**
*For any* pipeline graph, when executed, nodes should be processed in topological order such that all dependencies of a node are processed before that node.
**Validates: Requirements 5.4**

**Property 22: Error Highlighting on Failure**
*For any* pipeline execution that fails at a specific node, the system should highlight that node and display the error message.
**Validates: Requirements 5.5**

**Property 23: Pipeline Serialization Round-Trip**
*For any* pipeline, saving it to disk then loading it back should produce an equivalent pipeline with the same nodes, connections, and configurations.
**Validates: Requirements 5.6**

**Property 24: Transformation Type Support**
*For any* of the transformation types (filter, map, join, aggregate, pivot, custom SQL), the system should provide a corresponding node type that can be added to pipelines.
**Validates: Requirements 5.7**

### Validation Properties

**Property 25: Validation Rule Type Support**
*For any* of the rule types (range checks, pattern matching, uniqueness, referential integrity), the Validation_Engine should support creating and applying rules of that type.
**Validates: Requirements 6.1**

**Property 26: Violation Reporting Completeness**
*For any* validation rule applied to a dataset, all violations should be reported with row numbers and specific error messages.
**Validates: Requirements 6.2, 6.7**

**Property 27: Validation Failure Handling Options**
*For any* validation failure, the system should provide options to reject invalid rows, auto-correct, or manually review.
**Validates: Requirements 6.3**

**Property 28: Custom Rule Execution**
*For any* custom validation rule defined using Python expressions or SQL queries, the Validation_Engine should be able to execute it against datasets.
**Validates: Requirements 6.4**

**Property 29: Cross-Column Constraint Validation**
*For any* cross-column constraint defined on multiple columns, the Validation_Engine should validate the relationship between those columns for all rows.
**Validates: Requirements 6.5**

**Property 30: Rule Persistence and Association**
*For any* validation rule saved with a table or dataset association, loading that table or dataset should automatically load and apply the associated rules.
**Validates: Requirements 6.6**

### AI Suggestion Properties

**Property 31: Primary Key Suggestion**
*For any* dataset loaded, the AI_Suggester should analyze the data structure and suggest at least one potential primary key column or combination.
**Validates: Requirements 7.1**

**Property 32: Functional Dependency Detection**
*For any* dataset with functional dependencies, the AI_Suggester should detect those dependencies and recommend normalization steps to achieve 3NF.
**Validates: Requirements 7.2**

**Property 33: Data Quality Issue Detection with Confidence**
*For any* data quality issue detected, the AI_Suggester should propose cleaning transformations with confidence scores between 0 and 1.
**Validates: Requirements 7.4**

**Property 34: Suggestion Explanation Completeness**
*For any* suggestion provided by the AI_Suggester, an explanation should be included describing why the suggestion is relevant.
**Validates: Requirements 7.6**

**Property 35: Suggestion Undo Capability**
*For any* AI suggestion that is accepted and applied, the user should be able to undo the transformation and restore the previous data state.
**Validates: Requirements 7.7**

### Logging Properties

**Property 36: Operation Logging Completeness**
*For any* operation performed in the system, the Logger should record the operation type, timestamp, user, and outcome.
**Validates: Requirements 8.1**

**Property 37: Error Logging with Context**
*For any* error that occurs, the Logger should capture the full stack trace, context data, and system state.
**Validates: Requirements 8.2**

**Property 38: Log Level Support**
*For any* of the log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), the Logger should support logging at that level and filtering by that level.
**Validates: Requirements 8.3**

**Property 39: Automatic Log Rotation**
*For any* log file that exceeds 100MB, the Logger should automatically rotate the log and compress the old file.
**Validates: Requirements 8.4**

**Property 40: Log Filtering Functionality**
*For any* log viewing operation, the system should support filtering logs by date range, log level, and operation type.
**Validates: Requirements 8.5**

**Property 41: Performance Metrics Collection**
*For any* operation executed, the system should track and record performance metrics including operation duration, memory usage, and CPU utilization.
**Validates: Requirements 8.6**

**Property 42: Critical Error Notifications**
*For any* critical error when notifications are configured, the system should send notifications to the configured email addresses or webhooks.
**Validates: Requirements 8.7**

### Security Properties

**Property 43: Credential Encryption**
*For any* database credentials saved by the user, the Security_Manager should encrypt them using AES-256 encryption before storage.
**Validates: Requirements 9.1**

**Property 44: SSL/TLS Connection Encryption**
*For any* database connection established, the Connection_Manager should use SSL/TLS encryption for all network communication.
**Validates: Requirements 9.2**

**Property 45: No Plain Text Password Storage**
*For any* connection string or credential stored in the system, passwords should never be stored in plain text.
**Validates: Requirements 9.3**

**Property 46: Authentication Method Support**
*For any* of the authentication methods (username/password, SSH keys, OAuth tokens), the system should support that authentication method for database connections.
**Validates: Requirements 9.4**

**Property 47: Credential Exclusion from Error Messages**
*For any* connection failure due to authentication, the error message should not expose credential details.
**Validates: Requirements 9.5**

**Property 48: Credential Exclusion from Project Export**
*For any* project export operation, the exported file should not contain sensitive credentials and should prompt for re-entry on import.
**Validates: Requirements 9.6**

**Property 49: Connection Retry with Exponential Backoff**
*For any* failed database connection, the system should retry with exponential backoff up to the configured timeout.
**Validates: Requirements 9.7**

## Error Handling



### Error Categories

1. **User Input Errors**: Invalid file formats, malformed data, incorrect configurations
2. **System Errors**: Memory overflow, disk space issues, permission errors
3. **Network Errors**: Connection timeouts, authentication failures, SSL errors
4. **Data Errors**: Schema mismatches, validation failures, constraint violations
5. **Operation Errors**: Cancellation, timeout, resource exhaustion

### Error Handling Strategies

**Graceful Degradation**
- When memory is insufficient, switch to disk-based processing
- When network is slow, increase timeout and show progress
- When AI suggestions fail, fall back to rule-based analysis

**User-Friendly Error Messages**
```python
class ErrorHandler:
    def format_error_message(self, error: Exception, context: Dict[str, Any]) -> str:
        """
        Convert technical errors to user-friendly messages
        - Avoid exposing stack traces to users
        - Provide actionable suggestions
        - Include relevant context
        """
        pass
        
    def suggest_resolution(self, error: Exception) -> List[str]:
        """Suggest possible resolutions for common errors"""
        pass
```

**Error Recovery**
```python
class RecoveryManager:
    def auto_save_on_error(self, data: pd.DataFrame, error: Exception):
        """Automatically save data when critical error occurs"""
        pass
        
    def restore_from_auto_save(self) -> Optional[pd.DataFrame]:
        """Restore data from auto-save"""
        pass
```

**Retry Logic**
```python
class RetryPolicy:
    def __init__(self, max_retries: int = 3, 
                 backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
    def execute_with_retry(self, func: Callable, 
                          *args, **kwargs) -> Any:
        """Execute function with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except RetryableError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = self.backoff_factor ** attempt
                time.sleep(wait_time)
```

### Error Logging

All errors should be logged with:
- Full stack trace
- Operation context (what was being attempted)
- User context (who triggered the operation)
- System state (memory, CPU, disk usage)
- Timestamp and error ID for tracking

### User Notifications

**Error Severity Levels**
- **Critical**: System cannot continue, requires immediate action
- **Error**: Operation failed, user action needed
- **Warning**: Operation succeeded with issues, user should review
- **Info**: Operation completed successfully with notes

**Notification Channels**
- In-app toast notifications for immediate feedback
- Status bar messages for ongoing operations
- Dialog boxes for critical errors requiring user decision
- Log file for detailed error tracking
- Optional email/webhook for critical errors

## Testing Strategy

### Dual Testing Approach

The system will employ both unit testing and property-based testing as complementary strategies:

**Unit Tests**: Focus on specific examples, edge cases, and error conditions
- Test specific scenarios with known inputs and expected outputs
- Verify integration points between components
- Test error handling with specific error conditions
- Validate UI interactions with specific user actions

**Property-Based Tests**: Verify universal properties across all inputs
- Test correctness properties that should hold for all valid inputs
- Use randomized input generation to discover edge cases
- Validate invariants and round-trip properties
- Ensure comprehensive input coverage

Together, unit tests catch concrete bugs while property tests verify general correctness.

### Testing Framework Selection

**Python Testing Stack**:
- **pytest**: Main testing framework for unit and integration tests
- **Hypothesis**: Property-based testing library for Python
- **pytest-qt**: Testing utilities for PySide6/Qt applications
- **pytest-cov**: Code coverage measurement
- **pytest-mock**: Mocking utilities

### Property-Based Testing Configuration

Each property test will:
- Run minimum 100 iterations (due to randomization)
- Reference its corresponding design document property
- Use tag format: **Feature: comprehensive-system-upgrade, Property {number}: {property_text}**
- Each correctness property will be implemented by a SINGLE property-based test

### Test Organization

```
tests/
├── unit/
│   ├── test_performance_optimizer.py
│   ├── test_version_controller.py
│   ├── test_ui_manager.py
│   ├── test_project_manager.py
│   ├── test_etl_engine.py
│   ├── test_validation_engine.py
│   ├── test_ai_suggester.py
│   ├── test_logger.py
│   └── test_security_manager.py
├── property/
│   ├── test_performance_properties.py
│   ├── test_version_properties.py
│   ├── test_ui_properties.py
│   ├── test_project_properties.py
│   ├── test_etl_properties.py
│   ├── test_validation_properties.py
│   ├── test_ai_properties.py
│   ├── test_logging_properties.py
│   └── test_security_properties.py
├── integration/
│   ├── test_end_to_end_workflows.py
│   ├── test_data_pipeline_integration.py
│   └── test_ui_integration.py
└── conftest.py  # Shared fixtures and configuration
```

### Example Property Test

```python
from hypothesis import given, strategies as st
import pytest

# Feature: comprehensive-system-upgrade, Property 8: Version Restore Round-Trip
@given(
    data=st.data_frames(
        columns=[
            st.column('id', dtype=int),
            st.column('name', dtype=str),
            st.column('value', dtype=float)
        ],
        rows=st.tuples(
            st.integers(min_value=1, max_value=1000),
            st.text(min_size=1, max_size=50),
            st.floats(allow_nan=False, allow_infinity=False)
        )
    )
)
@pytest.mark.property_test
def test_version_restore_round_trip(data):
    """
    For any dataset state, creating a version snapshot, making arbitrary 
    changes, then restoring that version should produce a dataset 
    equivalent to the original state.
    """
    version_manager = VersionManager(storage_path="test_versions")
    
    # Create snapshot
    version = version_manager.create_snapshot(data, "test snapshot")
    
    # Make arbitrary changes
    modified_data = data.copy()
    modified_data['value'] = modified_data['value'] * 2
    
    # Restore version
    restored_data = version_manager.restore_version(version.id)
    
    # Verify equivalence
    pd.testing.assert_frame_equal(data, restored_data)
```

### Test Coverage Goals

- **Unit Test Coverage**: Minimum 80% of business logic code
- **Property Test Coverage**: All 49 correctness properties implemented
- **Integration Test Coverage**: All critical user workflows
- **UI Test Coverage**: All user interactions and state transitions

### Continuous Testing

- All tests run automatically on code changes
- Property tests run with 100 iterations in CI/CD
- Performance tests run nightly to track regressions
- Coverage reports generated and tracked over time

### Test Data Management

**Fixtures for Common Test Data**:
```python
@pytest.fixture
def sample_csv_data():
    """Small CSV dataset for quick tests"""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10.5, 20.3, 30.7]
    })

@pytest.fixture
def large_csv_data():
    """Large dataset for performance tests (>100MB)"""
    return generate_large_dataset(rows=1_000_000, cols=50)

@pytest.fixture
def sample_pipeline():
    """Sample ETL pipeline for testing"""
    pipeline = VisualPipelineBuilder()
    filter_node = pipeline.add_node('filter', (0, 0))
    map_node = pipeline.add_node('map', (100, 0))
    pipeline.connect_nodes(filter_node.id, map_node.id)
    return pipeline
```

### Performance Testing

**Benchmarks**:
- Data loading: <5 seconds per 10MB
- Normalization: <5 seconds per 10MB
- Theme switching: <200ms
- Navigation: <300ms
- Cancellation: <2 seconds

**Performance Test Example**:
```python
import time

def test_normalization_performance_benchmark():
    """Verify normalization meets performance requirements"""
    data = generate_test_data(size_mb=10)
    
    start_time = time.time()
    normalizer = AdvancedNormalizer(data)
    result = normalizer.normalize_to_3nf()
    duration = time.time() - start_time
    
    assert duration < 5.0, f"Normalization took {duration}s, expected <5s"
```

### Mock and Stub Strategy

**External Dependencies to Mock**:
- Database connections (MySQL, PostgreSQL)
- File system operations (for deterministic tests)
- Network requests (for AI service calls)
- System resources (memory, CPU monitoring)

**Example Mock**:
```python
from unittest.mock import Mock, patch

def test_secure_connection_with_ssl():
    """Test that database connections use SSL"""
    with patch('psycopg2.connect') as mock_connect:
        conn_manager = SecureConnectionManager(encryptor)
        conn_manager.create_connection({
            'host': 'localhost',
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_pass'
        }, use_ssl=True)
        
        # Verify SSL was enabled in connection params
        call_args = mock_connect.call_args
        assert call_args[1]['sslmode'] == 'require'
```

---

## Implementation Notes

### Technology Stack

**Core Technologies**:
- Python 3.8+
- PySide6 (Qt for Python)
- QML for UI
- pandas for data processing
- scikit-learn for ML features

**New Dependencies**:
- cryptography (for AES-256 encryption)
- hypothesis (for property-based testing)
- psutil (for system monitoring)
- watchdog (for file monitoring)
- joblib (for parallel processing)

### Migration Strategy

The upgrade will be implemented incrementally:

1. **Phase 1**: Core infrastructure (performance, logging, security)
2. **Phase 2**: Data features (versioning, validation)
3. **Phase 3**: UI enhancements (dark mode, responsive design)
4. **Phase 4**: Advanced features (visual pipeline, AI suggestions)
5. **Phase 5**: Collaboration features (project export/import)

Each phase will be fully tested before moving to the next.

### Backward Compatibility

- Existing ERD files will be automatically migrated to new format
- Old project files will be supported with conversion utility
- Configuration files will use versioned schema
- Database connections will maintain compatibility with existing configs

### Performance Considerations

- Use lazy loading for large datasets
- Implement caching for frequently accessed data
- Use connection pooling for database connections
- Optimize QML rendering with virtual scrolling
- Profile and optimize hot paths identified during testing

### Security Considerations

- Never log sensitive information (passwords, tokens)
- Use secure random number generation for encryption keys
- Implement rate limiting for AI API calls
- Validate all user inputs to prevent injection attacks
- Use parameterized queries for SQL generation
