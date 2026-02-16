import os
import pandas as pd
from PySide6.QtCore import QObject, Signal, Slot, Property
from utils.data_analysis import AdvancedNormalizer, analyze_dependencies
from utils.file_utils import get_data
from utils.data_connectors import DataConnector, ConnectionManager
from utils.etl_engine import ETLPipeline, PipelineManager, TransformRule, DataQualityChecker

class DataBridge(QObject):
    dataChanged = Signal()
    statsChanged = Signal()
    erdChanged = Signal()
    statusChanged = Signal(str, str) # message, color

    def __init__(self):
        super().__init__()
        self._df = None
        self._df_transformed = None  # After ETL transformations
        self._file_path = ""
        self._stats = {"records": 0, "columns": 0, "dim": 0, "fact": 0}
        self._tables = {} # Normalized tables structure
        self._preview_data = [] # List of dicts for QML TableView
        self._connector = DataConnector()
        self._connection_manager = ConnectionManager()
        self._saved_connections = []
        self._pipeline_manager = PipelineManager()
        self._current_pipeline = None
        self._data_quality_profile = {}
        self._transform_rules = []
        self._update_connections_list()

    @Property(str, notify=dataChanged)
    def filePath(self):
        return self._file_path

    @Property(list, notify=dataChanged)
    def previewData(self):
        return self._preview_data

    @Property(list, notify=dataChanged)
    def columnNames(self):
        return list(self._df.columns) if self._df is not None else []

    @Property(dict, notify=statsChanged)
    def stats(self):
        return self._stats

    @Property(dict, notify=erdChanged)
    def tables(self):
        return self._tables

    @Slot(str)
    def load_csv(self, file_url):
        # Convert file URL to path if needed
        path = file_url.replace("file:///", "").replace("/", os.sep)
        if not os.path.exists(path):
            self.statusChanged.emit("❌ File không tồn tại", "red")
            return

        try:
            self._df = pd.read_csv(path)
            self._file_path = path
            
            # Update stats
            suggestions = analyze_dependencies(self._df)
            self._stats = {
                "records": len(self._df),
                "columns": len(self._df.columns),
                "dim": len(suggestions['Dim']),
                "fact": len(suggestions['Fact'])
            }
            
            # Prepare preview data (head 15)
            preview_df = self._df.head(15).fillna("")
            self._preview_data = preview_df.to_dict('records')
            
            self.dataChanged.emit()
            self.statsChanged.emit()
            self.statusChanged.emit(f"✅ Đã tải: {os.path.basename(path)}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi: {str(e)}", "red")

    @Slot()
    def suggest_erd(self):
        if self._df is None:
            self.statusChanged.emit("⚠ Vui lòng tải dữ liệu trước", "orange")
            return
            
        try:
            normalizer = AdvancedNormalizer(self._df)
            normalized = normalizer.normalize_to_3nf()
            
            new_tables = {}
            for name, table in normalized.items():
                cols = [{"name": col, "is_primary": i == 0, "ref_table": None} 
                        for i, col in enumerate(table.columns)]
                new_tables[name] = cols
            
            self._tables = new_tables
            self.erdChanged.emit()
            self.statusChanged.emit("✅ Đã đề xuất mô hình ERD", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi phân tích: {str(e)}", "red")

    @Slot(str)
    def add_table(self, name):
        if name and name not in self._tables:
            self._tables[name] = []
            self.erdChanged.emit()
            self.statusChanged.emit(f"✅ Đã thêm bảng: {name}", "green")

    @Slot(str, str, bool, str)
    def add_field(self, table_name, field_name, is_pk, ref_table):
        if table_name in self._tables:
            self._tables[table_name].append({
                "name": field_name,
                "is_primary": is_pk,
                "ref_table": ref_table if ref_table else None
            })
            self.erdChanged.emit()
            self.statusChanged.emit(f"✅ Đã thêm trường: {field_name}", "green")
    
    @Slot(str, str)
    def remove_field(self, table_name, field_name):
        """Remove a field from a table"""
        if table_name in self._tables:
            self._tables[table_name] = [
                col for col in self._tables[table_name] 
                if col['name'] != field_name
            ]
            self.erdChanged.emit()
            self.statusChanged.emit(f"✅ Đã xóa trường: {field_name}", "green")
    
    @Slot(str)
    def remove_table(self, table_name):
        """Remove a table"""
        if table_name in self._tables:
            del self._tables[table_name]
            self.erdChanged.emit()
            self.statusChanged.emit(f"✅ Đã xóa bảng: {table_name}", "green")

    @Property(list, notify=dataChanged)
    def savedConnections(self):
        return self._saved_connections
    
    def _update_connections_list(self):
        """Update the list of saved connections"""
        self._saved_connections = self._connection_manager.list_connections()
        self.dataChanged.emit()
    
    @Slot(str)
    def load_excel(self, file_url):
        """Load data from Excel file"""
        path = file_url.replace("file:///", "").replace("/", os.sep)
        if not os.path.exists(path):
            self.statusChanged.emit("❌ File không tồn tại", "red")
            return
        
        try:
            self._df = self._connector.import_excel(path)
            self._file_path = path
            self._update_stats_and_preview()
            self.statusChanged.emit(f"✅ Đã tải Excel: {os.path.basename(path)}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi: {str(e)}", "red")
    
    @Slot(str)
    def load_json(self, file_url):
        """Load data from JSON file"""
        path = file_url.replace("file:///", "").replace("/", os.sep)
        if not os.path.exists(path):
            self.statusChanged.emit("❌ File không tồn tại", "red")
            return
        
        try:
            self._df = self._connector.import_json(path)
            self._file_path = path
            self._update_stats_and_preview()
            self.statusChanged.emit(f"✅ Đã tải JSON: {os.path.basename(path)}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi: {str(e)}", "red")
    
    @Slot(str, str)
    def load_sqlite(self, file_url, table_name):
        """Load data from SQLite database"""
        path = file_url.replace("file:///", "").replace("/", os.sep)
        if not os.path.exists(path):
            self.statusChanged.emit("❌ Database không tồn tại", "red")
            return
        
        try:
            self._df = self._connector.import_sqlite(path, table_name)
            self._file_path = path
            self._update_stats_and_preview()
            self.statusChanged.emit(f"✅ Đã tải từ SQLite: {table_name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi: {str(e)}", "red")
    
    @Slot(str, str, str, str, str)
    def load_mysql(self, host, user, password, database, table_name):
        """Load data from MySQL database"""
        try:
            self._df = self._connector.import_mysql(host, user, password, database, table_name)
            self._file_path = f"mysql://{host}/{database}/{table_name}"
            self._update_stats_and_preview()
            self.statusChanged.emit(f"✅ Đã kết nối MySQL: {table_name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi MySQL: {str(e)}", "red")
    
    @Slot(str, str, str, str, str)
    def load_postgresql(self, host, user, password, database, table_name):
        """Load data from PostgreSQL database"""
        try:
            self._df = self._connector.import_postgresql(host, user, password, database, table_name)
            self._file_path = f"postgresql://{host}/{database}/{table_name}"
            self._update_stats_and_preview()
            self.statusChanged.emit(f"✅ Đã kết nối PostgreSQL: {table_name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi PostgreSQL: {str(e)}", "red")
    
    def _update_stats_and_preview(self):
        """Update statistics and preview data after loading"""
        if self._df is None:
            return
        
        suggestions = analyze_dependencies(self._df)
        self._stats = {
            "records": len(self._df),
            "columns": len(self._df.columns),
            "dim": len(suggestions['Dim']),
            "fact": len(suggestions['Fact'])
        }
        
        preview_df = self._df.head(15).fillna("")
        self._preview_data = preview_df.to_dict('records')
        
        self.dataChanged.emit()
        self.statsChanged.emit()
    
    @Slot(str, str)
    def export_csv(self, folder_url, filename):
        """Export normalized tables to CSV files"""
        if not self._tables:
            self.statusChanged.emit("⚠ Chưa có dữ liệu để xuất", "orange")
            return
        
        folder = folder_url.replace("file:///", "").replace("/", os.sep)
        try:
            for table_name, columns in self._tables.items():
                col_names = [col['name'] for col in columns]
                if all(col in self._df.columns for col in col_names):
                    table_df = self._df[col_names].drop_duplicates()
                    file_path = os.path.join(folder, f"{filename}_{table_name}.csv")
                    self._connector.export_csv(table_df, file_path)
            
            self.statusChanged.emit(f"✅ Đã xuất CSV tại: {folder}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi xuất CSV: {str(e)}", "red")
    
    @Slot(str, str)
    def export_excel(self, folder_url, filename):
        """Export normalized tables to Excel file with multiple sheets"""
        if not self._tables:
            self.statusChanged.emit("⚠ Chưa có dữ liệu để xuất", "orange")
            return
        
        folder = folder_url.replace("file:///", "").replace("/", os.sep)
        file_path = os.path.join(folder, f"{filename}.xlsx")
        
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for table_name, columns in self._tables.items():
                    col_names = [col['name'] for col in columns]
                    if all(col in self._df.columns for col in col_names):
                        table_df = self._df[col_names].drop_duplicates()
                        sheet_name = table_name[:31]  # Excel sheet name limit
                        table_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            self.statusChanged.emit(f"✅ Đã xuất Excel: {filename}.xlsx", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi xuất Excel: {str(e)}", "red")
    
    @Slot(str, str)
    def export_json(self, folder_url, filename):
        """Export normalized tables to JSON files"""
        if not self._tables:
            self.statusChanged.emit("⚠ Chưa có dữ liệu để xuất", "orange")
            return
        
        folder = folder_url.replace("file:///", "").replace("/", os.sep)
        
        try:
            for table_name, columns in self._tables.items():
                col_names = [col['name'] for col in columns]
                if all(col in self._df.columns for col in col_names):
                    table_df = self._df[col_names].drop_duplicates()
                    file_path = os.path.join(folder, f"{filename}_{table_name}.json")
                    self._connector.export_json(table_df, file_path)
            
            self.statusChanged.emit(f"✅ Đã xuất JSON tại: {folder}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi xuất JSON: {str(e)}", "red")
    
    @Slot(str, str)
    def export_sql_script(self, folder_url, filename):
        """Export normalized tables as SQL script"""
        if not self._tables:
            self.statusChanged.emit("⚠ Chưa có dữ liệu để xuất", "orange")
            return
        
        folder = folder_url.replace("file:///", "").replace("/", os.sep)
        file_path = os.path.join(folder, f"{filename}.sql")
        
        try:
            tables_dict = {}
            for table_name, columns in self._tables.items():
                col_names = [col['name'] for col in columns]
                if all(col in self._df.columns for col in col_names):
                    tables_dict[table_name] = self._df[col_names].drop_duplicates()
            
            self._connector.export_sql_script(tables_dict, file_path)
            self.statusChanged.emit(f"✅ Đã tạo SQL script: {filename}.sql", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi tạo SQL: {str(e)}", "red")
    
    @Slot(str, str)
    def export_sqlite(self, folder_url, filename):
        """Export normalized tables to SQLite database"""
        if not self._tables:
            self.statusChanged.emit("⚠ Chưa có dữ liệu để xuất", "orange")
            return
        
        folder = folder_url.replace("file:///", "").replace("/", os.sep)
        db_path = os.path.join(folder, f"{filename}.db")
        
        try:
            for table_name, columns in self._tables.items():
                col_names = [col['name'] for col in columns]
                if all(col in self._df.columns for col in col_names):
                    table_df = self._df[col_names].drop_duplicates()
                    self._connector.export_sqlite(table_df, db_path, table_name)
            
            self.statusChanged.emit(f"✅ Đã tạo SQLite DB: {filename}.db", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi tạo SQLite: {str(e)}", "red")
    
    @Slot(str, str, str, str)
    def save_connection(self, name, conn_type, host, database):
        """Save a database connection configuration"""
        config = {
            "host": host,
            "database": database
        }
        self._connection_manager.add_connection(name, conn_type, config)
        self._update_connections_list()
        self.statusChanged.emit(f"✅ Đã lưu kết nối: {name}", "green")
    
    @Slot(str)
    def remove_connection(self, name):
        """Remove a saved connection"""
        self._connection_manager.remove_connection(name)
        self._update_connections_list()
        self.statusChanged.emit(f"✅ Đã xóa kết nối: {name}", "green")

    # ETL Pipeline Methods
    
    @Property(list, notify=dataChanged)
    def pipelineNames(self):
        """Get list of available pipeline names"""
        return self._pipeline_manager.list_pipelines()
    
    @Property(list, notify=dataChanged)
    def transformRules(self):
        """Get current transform rules"""
        return self._transform_rules
    
    @Property(dict, notify=dataChanged)
    def dataQualityProfile(self):
        """Get data quality profile"""
        return self._data_quality_profile
    
    @Slot(str)
    def create_pipeline(self, name):
        """Create new ETL pipeline"""
        try:
            pipeline = self._pipeline_manager.create_pipeline(name)
            self._current_pipeline = pipeline
            self.dataChanged.emit()
            self.statusChanged.emit(f"✅ Đã tạo pipeline: {name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi tạo pipeline: {str(e)}", "red")
    
    @Slot(str)
    def load_pipeline(self, name):
        """Load existing pipeline"""
        try:
            pipeline = self._pipeline_manager.get_pipeline(name)
            if pipeline:
                self._current_pipeline = pipeline
                self._update_transform_rules_list()
                self.dataChanged.emit()
                self.statusChanged.emit(f"✅ Đã load pipeline: {name}", "green")
            else:
                self.statusChanged.emit(f"⚠ Pipeline không tồn tại: {name}", "orange")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi load pipeline: {str(e)}", "red")
    
    @Slot(str)
    def delete_pipeline(self, name):
        """Delete pipeline"""
        try:
            self._pipeline_manager.delete_pipeline(name)
            if self._current_pipeline and self._current_pipeline.name == name:
                self._current_pipeline = None
            self.dataChanged.emit()
            self.statusChanged.emit(f"✅ Đã xóa pipeline: {name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi xóa pipeline: {str(e)}", "red")
    
    @Slot(str, str, str)
    def add_transform_rule(self, rule_name, rule_type, config_json):
        """Add transformation rule to current pipeline"""
        if not self._current_pipeline:
            self.statusChanged.emit("⚠ Chưa chọn pipeline", "orange")
            return
        
        try:
            import json
            config = json.loads(config_json)
            rule = TransformRule(rule_name, rule_type, config)
            self._current_pipeline.add_rule(rule)
            self._pipeline_manager.save_pipelines()
            self._update_transform_rules_list()
            self.dataChanged.emit()
            self.statusChanged.emit(f"✅ Đã thêm rule: {rule_name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi thêm rule: {str(e)}", "red")
    
    @Slot(str)
    def remove_transform_rule(self, rule_name):
        """Remove transformation rule"""
        if not self._current_pipeline:
            return
        
        try:
            self._current_pipeline.remove_rule(rule_name)
            self._pipeline_manager.save_pipelines()
            self._update_transform_rules_list()
            self.dataChanged.emit()
            self.statusChanged.emit(f"✅ Đã xóa rule: {rule_name}", "green")
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi xóa rule: {str(e)}", "red")
    
    @Slot()
    def execute_pipeline(self):
        """Execute current pipeline on loaded data"""
        if self._df is None:
            self.statusChanged.emit("⚠ Chưa có dữ liệu", "orange")
            return
        
        if not self._current_pipeline:
            self.statusChanged.emit("⚠ Chưa chọn pipeline", "orange")
            return
        
        try:
            self.statusChanged.emit("⏳ Đang thực thi pipeline...", "blue")
            self._df_transformed, stats = self._current_pipeline.execute(self._df)
            
            # Update preview with transformed data
            preview_df = self._df_transformed.head(15).fillna("")
            self._preview_data = preview_df.to_dict('records')
            
            # Update stats
            self._update_stats_and_preview()
            
            self.dataChanged.emit()
            self.statusChanged.emit(
                f"✅ Pipeline hoàn tất: {stats['final_rows']} rows, {len(stats['rules_applied'])} rules", 
                "green"
            )
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi thực thi: {str(e)}", "red")
    
    @Slot()
    def analyze_data_quality(self):
        """Analyze data quality of current dataset"""
        if self._df is None:
            self.statusChanged.emit("⚠ Chưa có dữ liệu", "orange")
            return
        
        try:
            self.statusChanged.emit("⏳ Đang phân tích chất lượng dữ liệu...", "blue")
            
            # Use transformed data if available, otherwise use original
            df_to_analyze = self._df_transformed if self._df_transformed is not None else self._df
            
            profile = DataQualityChecker.profile_data(df_to_analyze)
            anomalies = DataQualityChecker.detect_anomalies(df_to_analyze)
            
            self._data_quality_profile = {
                'profile': profile,
                'anomalies': anomalies
            }
            
            self.dataChanged.emit()
            
            # Count total issues
            total_issues = sum(len(v) for v in anomalies.values())
            self.statusChanged.emit(
                f"✅ Phân tích hoàn tất: {total_issues} vấn đề phát hiện", 
                "green" if total_issues == 0 else "orange"
            )
        except Exception as e:
            self.statusChanged.emit(f"❌ Lỗi phân tích: {str(e)}", "red")
    
    @Slot()
    def reset_transformations(self):
        """Reset to original data, discard transformations"""
        self._df_transformed = None
        if self._df is not None:
            preview_df = self._df.head(15).fillna("")
            self._preview_data = preview_df.to_dict('records')
            self.dataChanged.emit()
            self.statusChanged.emit("✅ Đã reset về dữ liệu gốc", "green")
    
    @Slot()
    def apply_transformations_permanently(self):
        """Apply transformations permanently (replace original data)"""
        if self._df_transformed is not None:
            self._df = self._df_transformed.copy()
            self._df_transformed = None
            self.statusChanged.emit("✅ Đã áp dụng transformations", "green")
    
    def _update_transform_rules_list(self):
        """Update transform rules list for QML"""
        if self._current_pipeline:
            self._transform_rules = [
                {
                    'name': r.name,
                    'type': r.rule_type,
                    'enabled': r.enabled
                }
                for r in self._current_pipeline.rules
            ]
        else:
            self._transform_rules = []
    
    @Slot(str, str, str)
    def add_quick_rule(self, rule_type, column, value):
        """Quick add common transformation rules"""
        if not self._current_pipeline:
            # Auto-create a pipeline if none exists
            self.create_pipeline("default_pipeline")
        
        import json
        rule_name = f"{rule_type}_{column}_{len(self._current_pipeline.rules)}"
        
        config = {}
        if rule_type == "fill_missing":
            config = {"columns": [column], "method": "constant", "value": value}
        elif rule_type == "convert_type":
            config = {"columns": [column], "target_type": value}
        elif rule_type == "trim_strings":
            config = {"columns": [column]}
        elif rule_type == "normalize_text":
            config = {"columns": [column], "case": value}
        
        self.add_transform_rule(rule_name, rule_type, json.dumps(config))
