"""
Base connector class for data sources
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any


class BaseConnector(ABC):
    """Abstract base class for data connectors"""
    
    def __init__(self):
        self.connection = None
        self.last_error: Optional[str] = None
    
    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """
        Establish connection to data source
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to data source
        
        Returns:
            bool: True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def read_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read data from source
        
        Returns:
            Optional[pd.DataFrame]: DataFrame if successful, None otherwise
        """
        pass
    
    @abstractmethod
    def write_data(self, df: pd.DataFrame, **kwargs) -> bool:
        """
        Write data to source
        
        Args:
            df: DataFrame to write
            
        Returns:
            bool: True if write successful, False otherwise
        """
        pass
    
    def get_last_error(self) -> Optional[str]:
        """Get the last error message"""
        return self.last_error
    
    def is_connected(self) -> bool:
        """Check if connection is active"""
        return self.connection is not None


class FileConnector(BaseConnector):
    """Base class for file-based connectors"""
    
    def __init__(self):
        super().__init__()
        self.file_path: Optional[str] = None
    
    def connect(self, file_path: str, **kwargs) -> bool:
        """Set file path"""
        self.file_path = file_path
        return True
    
    def disconnect(self) -> bool:
        """Clear file path"""
        self.file_path = None
        return True


class DatabaseConnector(BaseConnector):
    """Base class for database connectors"""
    
    def __init__(self):
        super().__init__()
        self.host: Optional[str] = None
        self.database: Optional[str] = None
        self.user: Optional[str] = None
    
    @abstractmethod
    def get_connection_string(self) -> str:
        """Get database connection string"""
        pass
    
    @abstractmethod
    def list_tables(self) -> list:
        """List all tables in database"""
        pass
