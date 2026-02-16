"""
Base transformer class for ETL operations
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Optional


class BaseTransformer(ABC):
    """Abstract base class for data transformers"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = True
        self.last_error: Optional[str] = None
    
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply transformation to DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: Transformed DataFrame
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate transformer configuration
        
        Returns:
            bool: True if config is valid, False otherwise
        """
        pass
    
    def get_description(self) -> str:
        """Get human-readable description of transformation"""
        return f"{self.name}: {self.__class__.__name__}"
    
    def enable(self):
        """Enable this transformer"""
        self.enabled = True
    
    def disable(self):
        """Disable this transformer"""
        self.enabled = False
    
    def get_last_error(self) -> Optional[str]:
        """Get the last error message"""
        return self.last_error


class ColumnTransformer(BaseTransformer):
    """Base class for column-level transformations"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.columns = config.get('columns', [])
    
    def validate_config(self) -> bool:
        """Validate that columns are specified"""
        if not self.columns:
            self.last_error = "No columns specified"
            return False
        return True
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        """Check if specified columns exist in DataFrame"""
        missing = [col for col in self.columns if col not in df.columns]
        if missing:
            self.last_error = f"Columns not found: {missing}"
            return False
        return True


class RowTransformer(BaseTransformer):
    """Base class for row-level transformations"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.condition = config.get('condition', None)
    
    def validate_config(self) -> bool:
        """Validate row transformer configuration"""
        return True
