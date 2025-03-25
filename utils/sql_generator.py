import os
import pandas as pd
import re
from typing import Dict, List, Any, Optional

def create_script_sql(erd: Dict[str, List[Dict[str, Any]]], df: Optional[pd.DataFrame] = None, 
                      database_type: str = 'mysql', 
                      max_varchar_length: int = 255,
                      strict_schema: bool = False) -> str:
    if not isinstance(erd, dict) or not erd:
        raise ValueError("ERD must be a non-empty dictionary")

    def advanced_type_inference(column_name: str, 
                                sample_value: Optional[Any] = None, 
                                df_col: Optional[pd.Series] = None) -> Dict[str, str]:
        column_name = column_name.lower()
        
        type_strategies = [
            lambda: _infer_from_dataframe(column_name, df_col),
            lambda: _infer_from_sample_value(column_name, sample_value),
            lambda: _infer_from_column_name(column_name),
            lambda: {'mysql': 'VARCHAR(100)', 'postgresql': 'VARCHAR(100)', 'sqlite': 'TEXT'}
        ]
        
        for strategy in type_strategies:
            result = strategy()
            if result:
                return result
        
        return {'mysql': 'VARCHAR(100)', 'postgresql': 'VARCHAR(100)', 'sqlite': 'TEXT'}

    def _infer_from_dataframe(column_name: str, df_col: Optional[pd.Series]) -> Optional[Dict[str, str]]:
        if df_col is None:
            return None
        
        dtype = df_col.dtype
        unique_count = df_col.nunique()
        total_count = len(df_col)
        
        type_mapping = {
            'mysql': {
                'integer': 'INT',
                'float': 'DECIMAL(10, 2)',
                'bool': 'BOOLEAN',
                'datetime': 'DATETIME',
                'string': lambda length: f'VARCHAR({min(length, max_varchar_length)})'
            },
            'postgresql': {
                'integer': 'INTEGER',
                'float': 'NUMERIC(10, 2)',
                'bool': 'BOOLEAN',
                'datetime': 'TIMESTAMP',
                'string': lambda length: f'VARCHAR({min(length, max_varchar_length)})'
            },
            'sqlite': {
                'integer': 'INTEGER',
                'float': 'REAL',
                'bool': 'INTEGER',
                'datetime': 'TEXT',
                'string': 'TEXT'
            }
        }
        
        if pd.api.types.is_integer_dtype(dtype):
            return {db: type_mapping[db]['integer'] for db in type_mapping}
        elif pd.api.types.is_float_dtype(dtype):
            return {db: type_mapping[db]['float'] for db in type_mapping}
        elif pd.api.types.is_bool_dtype(dtype):
            return {db: type_mapping[db]['bool'] for db in type_mapping}
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return {db: type_mapping[db]['datetime'] for db in type_mapping}
        elif pd.api.types.is_string_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            max_length = int(df_col.str.len().max() * 1.5) if df_col.dtype == 'object' else 100
            return {db: type_mapping[db]['string'](max_length) for db in type_mapping}
        
        return None

    def _infer_from_sample_value(column_name: str, sample_value: Optional[Any]) -> Optional[Dict[str, str]]:
        if sample_value is None:
            return None
        
        type_mapping = {
            'mysql': {
                bool: 'BOOLEAN',
                int: 'INT',
                float: 'DECIMAL(10, 2)',
                str: lambda v: f'VARCHAR({min(len(v) * 2, max_varchar_length)})'
            },
            'postgresql': {
                bool: 'BOOLEAN',
                int: 'INTEGER',
                float: 'NUMERIC(10, 2)',
                str: lambda v: f'VARCHAR({min(len(v) * 2, max_varchar_length)})'
            },
            'sqlite': {
                bool: 'INTEGER',
                int: 'INTEGER',
                float: 'REAL',
                str: 'TEXT'
            }
        }
        
        for python_type, db_type in type_mapping['mysql'].items():
            if isinstance(sample_value, python_type):
                if callable(db_type):
                    return {db: db_type(sample_value) for db in type_mapping}
                return {db: db_type for db in type_mapping}
        
        return None

    def _infer_from_column_name(column_name: str) -> Dict[str, str]:
        type_patterns = [
            (r'(id|key)$', {'mysql': 'INT', 'postgresql': 'INTEGER', 'sqlite': 'INTEGER'}),
            (r'^is_', {'mysql': 'BOOLEAN', 'postgresql': 'BOOLEAN', 'sqlite': 'INTEGER'}),
            (r'(date|time|datetime)', {'mysql': 'DATETIME', 'postgresql': 'TIMESTAMP', 'sqlite': 'TEXT'}),
            (r'(count|number|total|quantity)', {'mysql': 'INT', 'postgresql': 'INTEGER', 'sqlite': 'INTEGER'}),
            (r'(price|cost|amount|salary|revenue)', {'mysql': 'DECIMAL(10, 2)', 'postgresql': 'NUMERIC(10, 2)', 'sqlite': 'REAL'}),
            (r'(email|phone|address|description)', {'mysql': f'VARCHAR({max_varchar_length})', 'postgresql': f'VARCHAR({max_varchar_length})', 'sqlite': 'TEXT'})
        ]
        
        for pattern, data_type in type_patterns:
            if re.search(pattern, column_name):
                return data_type
        
        return {'mysql': 'VARCHAR(100)', 'postgresql': 'VARCHAR(100)', 'sqlite': 'TEXT'}

    def sanitize_identifier(name: str, max_length: int = 64) -> str:
        sanitized = re.sub(r'[^\w\s]', '', name)
        sanitized = sanitized.replace(' ', '_')
        sanitized = sanitized.lower()
        return sanitized.strip()[:max_length]

    database_name = sanitize_identifier(erd.get('database_name', 'generated_database'))
    sql_script = [
        f"-- Auto-generated SQL Script for {database_type.upper()}",
        f"-- Database: {database_name}"
    ]
    
    if database_type == 'mysql':
        sql_script.extend([f"CREATE DATABASE IF NOT EXISTS {database_name};", f"USE {database_name};\n"])
    elif database_type == 'postgresql':
        sql_script.extend([f"CREATE DATABASE {database_name};", f"\\c {database_name};\n"])
    
    dim_tables = {k: v for k, v in erd.items() if k.startswith("Dim_")}
    for table_name, columns in dim_tables.items():
        safe_table_name = sanitize_identifier(table_name)
        table_script = [f"-- Dimension Table: {safe_table_name}"]
        table_script.append(f"CREATE TABLE {safe_table_name} (")
        
        primary_keys = [col['name'] for col in columns if col.get('is_primary', False)]
        if not primary_keys and columns:
            primary_keys = [columns[0]['name']]
        
        column_definitions = []
        for col in columns:
            col_name = sanitize_identifier(col['name'])
            df_col = df[col_name] if df is not None and col_name in df.columns else None
            
            type_info = advanced_type_inference(col_name, col.get('sample'), df_col)
            data_type = type_info[database_type]
            
            nullable = " NOT NULL" if col.get('required', False) or col.get('is_primary', False) else ""
            
            column_definitions.append(f"    {col_name} {data_type}{nullable}")
        
        if primary_keys:
            column_definitions.append(f"    PRIMARY KEY ({', '.join(sanitize_identifier(pk) for pk in primary_keys)})")
        
        table_script.extend(column_definitions)
        table_script.append(");\n")
        
        if primary_keys and database_type != 'sqlite':
            table_script.append(f"CREATE INDEX idx_{safe_table_name}_pk ON {safe_table_name} ({', '.join(sanitize_identifier(pk) for pk in primary_keys)});\n")
        
        sql_script.extend(table_script)
    
    fact_tables = {k: v for k, v in erd.items() if k.startswith("Fact_")}
    for table_name, columns in fact_tables.items():
        safe_table_name = sanitize_identifier(table_name)
        table_script = [f"-- Fact Table: {safe_table_name}"]
        table_script.append(f"CREATE TABLE {safe_table_name} (")
        
        column_definitions = []
        foreign_keys = []
        for col in columns:
            col_name = sanitize_identifier(col['name'])
            df_col = df[col_name] if df is not None and col_name in df.columns else None
            
            type_info = advanced_type_inference(col_name, col.get('sample'), df_col)
            data_type = type_info[database_type]
            
            nullable = " NOT NULL" if col.get('required', False) else ""
            
            column_definitions.append(f"    {col_name} {data_type}{nullable}")
            
            if col.get('ref_table') and col.get('ref_column'):
                ref_table = sanitize_identifier(col['ref_table'])
                ref_column = sanitize_identifier(col['ref_column'])
                foreign_keys.append(f"    FOREIGN KEY ({col_name}) REFERENCES {ref_table} ({ref_column})")
        
        column_definitions.extend(foreign_keys)
        table_script.extend(column_definitions)
        table_script.append(");\n")
        
        sql_script.extend(table_script)
    
    data_path = os.path.join(os.getcwd(), "generated_scripts")
    os.makedirs(data_path, exist_ok=True)
    sql_file_path = os.path.join(data_path, f'{database_name}_{database_type}_create.sql')
    
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_script))
    
    return sql_file_path