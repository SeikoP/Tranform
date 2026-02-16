"""
Lazy loading utilities for large datasets
"""
import pandas as pd
from typing import Iterator, Optional
from config.constants import PREVIEW_ROWS


class LazyDataLoader:
    """Lazy loader for large datasets"""
    
    def __init__(self, file_path: str, chunk_size: int = 10000):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self._total_rows: Optional[int] = None
        self._columns: Optional[list] = None
    
    def get_preview(self, n_rows: int = PREVIEW_ROWS) -> pd.DataFrame:
        """Get preview of first n rows"""
        return pd.read_csv(self.file_path, nrows=n_rows)
    
    def get_chunks(self) -> Iterator[pd.DataFrame]:
        """Get data in chunks"""
        return pd.read_csv(self.file_path, chunksize=self.chunk_size)
    
    def get_total_rows(self) -> int:
        """Get total number of rows (cached)"""
        if self._total_rows is None:
            self._total_rows = sum(1 for _ in open(self.file_path)) - 1
        return self._total_rows
    
    def get_columns(self) -> list:
        """Get column names (cached)"""
        if self._columns is None:
            self._columns = pd.read_csv(self.file_path, nrows=0).columns.tolist()
        return self._columns
    
    def get_page(self, page: int, page_size: int = 100) -> pd.DataFrame:
        """Get specific page of data"""
        skip_rows = page * page_size
        return pd.read_csv(
            self.file_path,
            skiprows=range(1, skip_rows + 1),
            nrows=page_size
        )


class VirtualScrollModel:
    """Model for virtual scrolling in UI"""
    
    def __init__(self, loader: LazyDataLoader, visible_rows: int = 20):
        self.loader = loader
        self.visible_rows = visible_rows
        self._cache = {}
        self._current_page = 0
    
    def get_visible_data(self, start_index: int) -> pd.DataFrame:
        """Get data for visible rows"""
        page = start_index // self.visible_rows
        
        if page not in self._cache:
            self._cache[page] = self.loader.get_page(page, self.visible_rows)
        
        return self._cache[page]
    
    def clear_cache(self):
        """Clear cached data"""
        self._cache.clear()
