import os
import pandas as pd
from PySide6.QtCore import QObject, Signal, Slot, Property
from utils.data_analysis import AdvancedNormalizer, analyze_dependencies
from utils.file_utils import get_data # Note: Might need adjustment for QML

class DataBridge(QObject):
    dataChanged = Signal()
    statsChanged = Signal()
    erdChanged = Signal()
    statusChanged = Signal(str, str) # message, color

    def __init__(self):
        super().__init__()
        self._df = None
        self._file_path = ""
        self._stats = {"records": 0, "columns": 0, "dim": 0, "fact": 0}
        self._tables = {} # Normalized tables structure
        self._preview_data = [] # List of dicts for QML TableView

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
