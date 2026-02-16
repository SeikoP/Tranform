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
