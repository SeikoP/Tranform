import pandas as pd
import numpy as np
from typing import Dict, List, Any
from sklearn.preprocessing import LabelEncoder

class AdvancedNormalizer:
    def __init__(self, df: pd.DataFrame):
        self.original_df = df
        self.analysis_result = {}
        self.normalized_tables = {}
        self.error_log = []
    
    def preprocess_data(self) -> pd.DataFrame:
        df = self.original_df.copy()
        for col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                else:
                    df[col] = df[col].fillna('').astype(str)
            except Exception as e:
                self.error_log.append(f"Error preprocessing column {col}: {str(e)}")
        return df
    
    def detect_dependencies(self, threshold: float = 0.95) -> Dict[str, List[str]]:
        dependencies = {}
        df = self.preprocess_data()
        for col_x in df.columns:
            col_deps = []
            for col_y in df.columns:
                if col_x != col_y:
                    try:
                        categorical_dep = self._check_categorical_dependency(df, col_x, col_y)
                        correlation_dep = self._check_correlation(df, col_x, col_y)
                        if categorical_dep or correlation_dep:
                            col_deps.append(col_y)
                    except Exception as e:
                        self.error_log.append(f"Error checking dependency between {col_x} and {col_y}: {str(e)}")
            if col_deps:
                dependencies[col_x] = col_deps
        return dependencies
    
    def _check_categorical_dependency(self, df: pd.DataFrame, col_x: str, col_y: str, max_unique_ratio: float = 0.1) -> bool:
        try:
            le = LabelEncoder()
            x_data = df[col_x].fillna('').astype(str)
            y_data = df[col_y].fillna('').astype(str)
            
            x_encoded = le.fit_transform(x_data)
            y_encoded = le.fit_transform(y_data)
            
            unique_x = len(np.unique(x_encoded))
            unique_y = len(np.unique(y_encoded))
            return unique_x / len(df) <= max_unique_ratio and unique_y > unique_x
        except Exception as e:
            self.error_log.append(f"Error in categorical dependency check for columns {col_x} and {col_y}: {str(e)}")
            return False
    
    def _check_correlation(self, df: pd.DataFrame, col_x: str, col_y: str, threshold: float = 0.8) -> bool:
        try:
            if pd.api.types.is_numeric_dtype(df[col_x]) and pd.api.types.is_numeric_dtype(df[col_y]):
                data = df[[col_x, col_y]].dropna()
                if len(data) < 2:
                    return False
                correlation = np.abs(data[col_x].corr(data[col_y], method='pearson'))
                return correlation >= threshold
            return False
        except Exception as e:
            self.error_log.append(f"Error checking correlation between {col_x} and {col_y}: {str(e)}")
            return False
    
    def normalize_to_3nf(self) -> Dict[str, pd.DataFrame]:
        try:
            dependencies = self.detect_dependencies()
            for source, targets in dependencies.items():
                for target in targets:
                    transitive_targets = [t for t in dependencies.get(target, []) if t not in targets]
                    if transitive_targets:
                        dim_table = self.original_df[[source, target] + transitive_targets].drop_duplicates()
                        table_name = f"Dim_{source}_{target}"
                        self.normalized_tables[table_name] = dim_table
        
            fact_columns = [col for col in self.original_df.columns 
                           if col not in [col for table in self.normalized_tables.values() for col in table.columns]]
            self.normalized_tables["Fact_Main"] = self.original_df[fact_columns]
            return self.normalized_tables
        except Exception as e:
            self.error_log.append(f"Error during 3NF normalization: {str(e)}")
            return {}

def analyze_dependencies(df):
    unique_counts = {col: df[col].nunique() for col in df.columns}
    dim_cols = [col for col, count in unique_counts.items() if count < len(df) * 0.1]
    fact_cols = [col for col in df.columns if col not in dim_cols]
    return {"Dim": dim_cols, "Fact": fact_cols}