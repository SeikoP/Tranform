"""
Multi-source data connectors for import/export operations
Supports: CSV, Excel, JSON, SQL Databases, APIs
"""
import pandas as pd
import json
import os
from typing import Optional, Dict, Any, List
import sqlite3


class DataConnector:
    """Base class for data connectors"""
    
    @staticmethod
    def import_csv(file_path: str, **kwargs) -> pd.DataFrame:
        """Import data from CSV file"""
        encoding = kwargs.get('encoding', 'utf-8')
        delimiter = kwargs.get('delimiter', ',')
        return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
    
    @staticmethod
    def import_excel(file_path: str, **kwargs) -> pd.DataFrame:
        """Import data from Excel file"""
        sheet_name = kwargs.get('sheet_name', 0)
        return pd.read_excel(file_path, sheet_name=sheet_name)
    
    @staticmethod
    def import_json(file_path: str, **kwargs) -> pd.DataFrame:
        """Import data from JSON file"""
        orient = kwargs.get('orient', 'records')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        else:
            raise ValueError("Unsupported JSON format")
    
    @staticmethod
    def import_sqlite(db_path: str, table_name: str, **kwargs) -> pd.DataFrame:
        """Import data from SQLite database"""
        query = kwargs.get('query', f"SELECT * FROM {table_name}")
        conn = sqlite3.connect(db_path)
        try:
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
    
    @staticmethod
    def import_sql_server(connection_string: str, query: str, **kwargs) -> pd.DataFrame:
        """Import data from SQL Server (requires pyodbc)"""
        try:
            import pyodbc
            conn = pyodbc.connect(connection_string)
            try:
                return pd.read_sql_query(query, conn)
            finally:
                conn.close()
        except ImportError:
            raise ImportError("pyodbc is required for SQL Server connections")
    
    @staticmethod
    def import_mysql(host: str, user: str, password: str, database: str, 
                     table_name: str, **kwargs) -> pd.DataFrame:
        """Import data from MySQL (requires pymysql)"""
        try:
            import pymysql
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            try:
                query = kwargs.get('query', f"SELECT * FROM {table_name}")
                return pd.read_sql_query(query, conn)
            finally:
                conn.close()
        except ImportError:
            raise ImportError("pymysql is required for MySQL connections")
    
    @staticmethod
    def import_postgresql(host: str, user: str, password: str, database: str,
                          table_name: str, **kwargs) -> pd.DataFrame:
        """Import data from PostgreSQL (requires psycopg2)"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            try:
                query = kwargs.get('query', f"SELECT * FROM {table_name}")
                return pd.read_sql_query(query, conn)
            finally:
                conn.close()
        except ImportError:
            raise ImportError("psycopg2 is required for PostgreSQL connections")
    
    @staticmethod
    def export_csv(df: pd.DataFrame, file_path: str, **kwargs) -> bool:
        """Export DataFrame to CSV"""
        try:
            encoding = kwargs.get('encoding', 'utf-8')
            index = kwargs.get('index', False)
            df.to_csv(file_path, encoding=encoding, index=index)
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False
    
    @staticmethod
    def export_excel(df: pd.DataFrame, file_path: str, **kwargs) -> bool:
        """Export DataFrame to Excel"""
        try:
            sheet_name = kwargs.get('sheet_name', 'Sheet1')
            index = kwargs.get('index', False)
            df.to_excel(file_path, sheet_name=sheet_name, index=index)
            return True
        except Exception as e:
            print(f"Error exporting Excel: {e}")
            return False
    
    @staticmethod
    def export_json(df: pd.DataFrame, file_path: str, **kwargs) -> bool:
        """Export DataFrame to JSON"""
        try:
            orient = kwargs.get('orient', 'records')
            indent = kwargs.get('indent', 2)
            df.to_json(file_path, orient=orient, indent=indent, force_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False
    
    @staticmethod
    def export_sqlite(df: pd.DataFrame, db_path: str, table_name: str, **kwargs) -> bool:
        """Export DataFrame to SQLite database"""
        try:
            if_exists = kwargs.get('if_exists', 'replace')
            conn = sqlite3.connect(db_path)
            try:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
                return True
            finally:
                conn.close()
        except Exception as e:
            print(f"Error exporting to SQLite: {e}")
            return False
    
    @staticmethod
    def export_sql_script(tables: Dict[str, pd.DataFrame], output_path: str, 
                          dialect: str = 'sqlite') -> bool:
        """Generate SQL script for creating tables and inserting data"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for table_name, df in tables.items():
                    # Create table statement
                    f.write(f"-- Table: {table_name}\n")
                    f.write(f"DROP TABLE IF EXISTS {table_name};\n")
                    f.write(f"CREATE TABLE {table_name} (\n")
                    
                    # Column definitions
                    col_defs = []
                    for col in df.columns:
                        dtype = df[col].dtype
                        if pd.api.types.is_integer_dtype(dtype):
                            sql_type = "INTEGER"
                        elif pd.api.types.is_float_dtype(dtype):
                            sql_type = "REAL"
                        elif pd.api.types.is_datetime64_any_dtype(dtype):
                            sql_type = "DATETIME"
                        else:
                            sql_type = "TEXT"
                        col_defs.append(f"    {col} {sql_type}")
                    
                    f.write(",\n".join(col_defs))
                    f.write("\n);\n\n")
                    
                    # Insert statements
                    for _, row in df.iterrows():
                        values = []
                        for val in row:
                            if pd.isna(val):
                                values.append("NULL")
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            else:
                                # Escape single quotes
                                escaped = str(val).replace("'", "''")
                                values.append(f"'{escaped}'")
                        
                        f.write(f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n")
                    
                    f.write("\n\n")
            
            return True
        except Exception as e:
            print(f"Error generating SQL script: {e}")
            return False


class ConnectionManager:
    """Manage database connections and configurations"""
    
    def __init__(self):
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.config_file = "connections.json"
        self.load_connections()
    
    def load_connections(self):
        """Load saved connections from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.connections = json.load(f)
            except Exception as e:
                print(f"Error loading connections: {e}")
    
    def save_connections(self):
        """Save connections to config file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.connections, f, indent=2)
        except Exception as e:
            print(f"Error saving connections: {e}")
    
    def add_connection(self, name: str, conn_type: str, config: Dict[str, Any]):
        """Add a new connection configuration"""
        self.connections[name] = {
            "type": conn_type,
            "config": config
        }
        self.save_connections()
    
    def remove_connection(self, name: str):
        """Remove a connection configuration"""
        if name in self.connections:
            del self.connections[name]
            self.save_connections()
    
    def get_connection(self, name: str) -> Optional[Dict[str, Any]]:
        """Get connection configuration by name"""
        return self.connections.get(name)
    
    def list_connections(self) -> List[str]:
        """List all saved connection names"""
        return list(self.connections.keys())
