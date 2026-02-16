"""
ETL Engine - Core transformation and data quality module
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import json
import re


class TransformRule:
    """Represents a single transformation rule"""
    
    def __init__(self, name: str, rule_type: str, config: Dict[str, Any]):
        self.name = name
        self.rule_type = rule_type
        self.config = config
        self.enabled = True
    
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformation rule to DataFrame"""
        if not self.enabled:
            return df
        
        try:
            if self.rule_type == "remove_duplicates":
                return self._remove_duplicates(df)
            elif self.rule_type == "fill_missing":
                return self._fill_missing(df)
            elif self.rule_type == "drop_missing":
                return self._drop_missing(df)
            elif self.rule_type == "convert_type":
                return self._convert_type(df)
            elif self.rule_type == "rename_column":
                return self._rename_column(df)
            elif self.rule_type == "filter_rows":
                return self._filter_rows(df)
            elif self.rule_type == "trim_strings":
                return self._trim_strings(df)
            elif self.rule_type == "replace_values":
                return self._replace_values(df)
            elif self.rule_type == "normalize_text":
                return self._normalize_text(df)
            elif self.rule_type == "extract_pattern":
                return self._extract_pattern(df)
            else:
                return df
        except Exception as e:
            print(f"Error applying rule {self.name}: {e}")
            return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        subset = self.config.get('columns', None)
        keep = self.config.get('keep', 'first')
        return df.drop_duplicates(subset=subset, keep=keep)
    
    def _fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.config.get('columns', df.columns)
        method = self.config.get('method', 'constant')
        value = self.config.get('value', '')
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if method == 'constant':
                df[col] = df[col].fillna(value)
            elif method == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif method == 'median':
                df[col] = df[col].fillna(df[col].median())
            elif method == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else value)
            elif method == 'forward':
                df[col] = df[col].fillna(method='ffill')
            elif method == 'backward':
                df[col] = df[col].fillna(method='bfill')
        
        return df
    
    def _drop_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.config.get('columns', None)
        how = self.config.get('how', 'any')
        threshold = self.config.get('threshold', None)
        
        return df.dropna(subset=columns, how=how, thresh=threshold)
    
    def _convert_type(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.config.get('columns', [])
        target_type = self.config.get('target_type', 'string')
        
        for col in columns:
            if col not in df.columns:
                continue
            
            try:
                if target_type == 'string':
                    df[col] = df[col].astype(str)
                elif target_type == 'integer':
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                elif target_type == 'float':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif target_type == 'datetime':
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                elif target_type == 'boolean':
                    df[col] = df[col].astype(bool)
            except Exception as e:
                print(f"Error converting {col} to {target_type}: {e}")
        
        return df
    
    def _rename_column(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = self.config.get('mapping', {})
        return df.rename(columns=mapping)
    
    def _filter_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        column = self.config.get('column')
        operator = self.config.get('operator', '==')
        value = self.config.get('value')
        
        if column not in df.columns:
            return df
        
        if operator == '==':
            return df[df[column] == value]
        elif operator == '!=':
            return df[df[column] != value]
        elif operator == '>':
            return df[df[column] > value]
        elif operator == '<':
            return df[df[column] < value]
        elif operator == '>=':
            return df[df[column] >= value]
        elif operator == '<=':
            return df[df[column] <= value]
        elif operator == 'contains':
            return df[df[column].astype(str).str.contains(str(value), na=False)]
        elif operator == 'not_contains':
            return df[~df[column].astype(str).str.contains(str(value), na=False)]
        
        return df
    
    def _trim_strings(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.config.get('columns', df.select_dtypes(include=['object']).columns)
        
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def _replace_values(self, df: pd.DataFrame) -> pd.DataFrame:
        column = self.config.get('column')
        mapping = self.config.get('mapping', {})
        
        if column in df.columns:
            df[column] = df[column].replace(mapping)
        
        return df
    
    def _normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.config.get('columns', [])
        case = self.config.get('case', 'lower')
        
        for col in columns:
            if col in df.columns:
                if case == 'lower':
                    df[col] = df[col].astype(str).str.lower()
                elif case == 'upper':
                    df[col] = df[col].astype(str).str.upper()
                elif case == 'title':
                    df[col] = df[col].astype(str).str.title()
        
        return df
    
    def _extract_pattern(self, df: pd.DataFrame) -> pd.DataFrame:
        column = self.config.get('column')
        pattern = self.config.get('pattern')
        new_column = self.config.get('new_column')
        
        if column in df.columns and pattern and new_column:
            df[new_column] = df[column].astype(str).str.extract(pattern, expand=False)
        
        return df


class DataQualityChecker:
    """Data quality profiling and validation"""
    
    @staticmethod
    def profile_data(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data quality profile"""
        profile = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'columns': {}
        }
        
        for col in df.columns:
            col_profile = {
                'dtype': str(df[col].dtype),
                'missing_count': int(df[col].isna().sum()),
                'missing_percent': float(df[col].isna().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'unique_percent': float(df[col].nunique() / len(df) * 100),
            }
            
            # Numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_profile.update({
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None,
                })
            
            # String columns
            elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
                col_profile.update({
                    'avg_length': float(df[col].astype(str).str.len().mean()),
                    'max_length': int(df[col].astype(str).str.len().max()),
                    'min_length': int(df[col].astype(str).str.len().min()),
                })
            
            profile['columns'][col] = col_profile
        
        return profile
    
    @staticmethod
    def detect_anomalies(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Detect data quality issues"""
        issues = {
            'high_missing': [],
            'low_variance': [],
            'potential_duplicates': [],
            'outliers': [],
            'inconsistent_types': []
        }
        
        for col in df.columns:
            # High missing values
            missing_pct = df[col].isna().sum() / len(df) * 100
            if missing_pct > 50:
                issues['high_missing'].append(f"{col} ({missing_pct:.1f}% missing)")
            
            # Low variance (potential constant columns)
            if df[col].nunique() == 1:
                issues['low_variance'].append(f"{col} (constant value)")
            
            # Numeric outliers using IQR
            if pd.api.types.is_numeric_dtype(df[col]):
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                if len(outliers) > 0:
                    issues['outliers'].append(f"{col} ({len(outliers)} outliers)")
        
        # Check for duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues['potential_duplicates'].append(f"{dup_count} duplicate rows found")
        
        return issues


class ETLPipeline:
    """ETL Pipeline orchestrator"""
    
    def __init__(self, name: str):
        self.name = name
        self.rules: List[TransformRule] = []
        self.created_at = datetime.now()
        self.last_run = None
        self.execution_log = []
    
    def add_rule(self, rule: TransformRule):
        """Add transformation rule to pipeline"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_name: str):
        """Remove rule by name"""
        self.rules = [r for r in self.rules if r.name != rule_name]
    
    def execute(self, df: pd.DataFrame) -> tuple[pd.DataFrame, Dict[str, Any]]:
        """Execute pipeline on DataFrame"""
        result_df = df.copy()
        execution_stats = {
            'start_time': datetime.now(),
            'rules_applied': [],
            'errors': [],
            'initial_rows': len(df),
            'initial_columns': len(df.columns)
        }
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            try:
                before_rows = len(result_df)
                result_df = rule.apply(result_df)
                after_rows = len(result_df)
                
                execution_stats['rules_applied'].append({
                    'rule': rule.name,
                    'type': rule.rule_type,
                    'rows_before': before_rows,
                    'rows_after': after_rows,
                    'rows_changed': after_rows - before_rows
                })
            except Exception as e:
                execution_stats['errors'].append({
                    'rule': rule.name,
                    'error': str(e)
                })
        
        execution_stats['end_time'] = datetime.now()
        execution_stats['final_rows'] = len(result_df)
        execution_stats['final_columns'] = len(result_df.columns)
        execution_stats['duration'] = (execution_stats['end_time'] - execution_stats['start_time']).total_seconds()
        
        self.last_run = execution_stats['end_time']
        self.execution_log.append(execution_stats)
        
        return result_df, execution_stats
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize pipeline to dictionary"""
        return {
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'rules': [
                {
                    'name': r.name,
                    'type': r.rule_type,
                    'config': r.config,
                    'enabled': r.enabled
                }
                for r in self.rules
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ETLPipeline':
        """Deserialize pipeline from dictionary"""
        pipeline = cls(data['name'])
        pipeline.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('last_run'):
            pipeline.last_run = datetime.fromisoformat(data['last_run'])
        
        for rule_data in data.get('rules', []):
            rule = TransformRule(
                rule_data['name'],
                rule_data['type'],
                rule_data['config']
            )
            rule.enabled = rule_data.get('enabled', True)
            pipeline.add_rule(rule)
        
        return pipeline


class PipelineManager:
    """Manage multiple ETL pipelines"""
    
    def __init__(self, config_file: str = "etl_pipelines.json"):
        self.config_file = config_file
        self.pipelines: Dict[str, ETLPipeline] = {}
        self.load_pipelines()
    
    def load_pipelines(self):
        """Load pipelines from config file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pipeline_data in data.get('pipelines', []):
                    pipeline = ETLPipeline.from_dict(pipeline_data)
                    self.pipelines[pipeline.name] = pipeline
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading pipelines: {e}")
    
    def save_pipelines(self):
        """Save pipelines to config file"""
        try:
            data = {
                'pipelines': [p.to_dict() for p in self.pipelines.values()]
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving pipelines: {e}")
    
    def create_pipeline(self, name: str) -> ETLPipeline:
        """Create new pipeline"""
        pipeline = ETLPipeline(name)
        self.pipelines[name] = pipeline
        self.save_pipelines()
        return pipeline
    
    def get_pipeline(self, name: str) -> Optional[ETLPipeline]:
        """Get pipeline by name"""
        return self.pipelines.get(name)
    
    def delete_pipeline(self, name: str):
        """Delete pipeline"""
        if name in self.pipelines:
            del self.pipelines[name]
            self.save_pipelines()
    
    def list_pipelines(self) -> List[str]:
        """List all pipeline names"""
        return list(self.pipelines.keys())
