import pandas as pd
import numpy as np
from typing import Dict, List, Any, Set
from sklearn.preprocessing import LabelEncoder

class AdvancedNormalizer:
    def __init__(self, df: pd.DataFrame):
        self.original_df = df
        self.analysis_result = {}
        self.normalized_tables = {}
        self.error_log = []
        self.dependencies: Dict[str, Set[str]] = {}
    
    def preprocess_data(self) -> pd.DataFrame:
        """Chuẩn hóa dữ liệu trước khi phân tích"""
        df = self.original_df.copy()
        for col in df.columns:
            try:
                # Ép kiểu dữ liệu nếu có thể
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    pass
                else:
                    df[col] = df[col].fillna('').astype(str).str.strip()
            except Exception as e:
                self.error_log.append(f"Lỗi tiền xử lý cột {col}: {str(e)}")
        return df
    
    def detect_functional_dependencies(self, sample_size: int = 1000) -> Dict[str, Set[str]]:
        """
        Tìm các phụ thuộc hàm (A -> B).
        A -> B nếu với mỗi giá trị của A Duy Nhất chỉ có duy nhất một giá trị của B tương ứng.
        """
        df = self.preprocess_data()
        if len(df) > sample_size:
            df_sample = df.sample(sample_size, random_state=42)
        else:
            df_sample = df

        columns = df_sample.columns
        for i, col_a in enumerate(columns):
            for j, col_b in enumerate(columns):
                if i == j: continue
                
                # Kiểm tra if col_a -> col_b
                # Tính số lượng cặp (a, b) duy nhất và so sánh với số lượng a duy nhất
                unique_a = df_sample[col_a].nunique()
                unique_pairs = df_sample.groupby(col_a)[col_b].nunique().max()
                
                # Nếu max các giá trị b cho mỗi a là 1, thì a -> b
                if unique_pairs == 1:
                    if col_a not in self.dependencies:
                        self.dependencies[col_a] = set()
                    self.dependencies[col_a].add(col_b)
        
        return self.dependencies

    def normalize_to_3nf(self) -> Dict[str, pd.DataFrame]:
        """
        Phân tách các bảng dựa trên phụ thuộc hàm để đạt chuẩn 3NF.
        """
        try:
            self.detect_functional_dependencies()
            df = self.original_df
            
            # 1. Xác định các tập thuộc tính tạo thành bảng Dimension
            # Nếu A -> {B, C, D}, ta tạo bảng Dim_A với các cột {A, B, C, D}
            processed_cols = set()
            
            # Sắp xếp các dependency theo số lượng vế phải giảm dần để ưu tiên bảng lớn
            sorted_deps = sorted(self.dependencies.items(), key=lambda x: len(x[1]), reverse=True)
            
            for determinant, dependents in sorted_deps:
                # Nếu determinant có nhiều hơn 1 phụ thuộc và chưa bị xử lý hoàn toàn
                useful_dependents = [d for d in dependents if d not in processed_cols]
                
                if len(useful_dependents) >= 1:
                    table_name = f"Dim_{determinant}"
                    cols_to_extract = [determinant] + useful_dependents
                    self.normalized_tables[table_name] = df[cols_to_extract].drop_duplicates().reset_index(drop=True)
                    processed_cols.update(useful_dependents)
            
            # 2. Bảng Fact chứa các cột còn lại và các foreign keys (determinants)
            fact_cols = [col for col in df.columns if col not in processed_cols]
            if fact_cols:
                self.normalized_tables["Fact_Main"] = df[fact_cols]
                
            return self.normalized_tables
        except Exception as e:
            self.error_log.append(f"Lỗi trong quá trình chuẩn hóa 3NF: {str(e)}")
            import traceback
            self.error_log.append(traceback.format_exc())
            return {}

def analyze_dependencies(df):
    """Hàm wrapper cho UI cũ sử dụng"""
    unique_counts = {col: df[col].nunique() for col in df.columns}
    total_rows = len(df)
    
    # Gợi ý Dim nếu số lượng giá trị duy nhất ít (<15% tổng số dòng)
    dim_cols = [col for col, count in unique_counts.items() if count < total_rows * 0.15 or count < 50]
    fact_cols = [col for col in df.columns if col not in dim_cols]
    
    return {"Dim": dim_cols, "Fact": fact_cols}
