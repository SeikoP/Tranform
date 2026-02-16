"""
Performance Optimizer Module

This module provides utilities for optimizing performance when processing
large datasets, including chunk processing, multi-threading, and memory monitoring.

Requirements: 1.1, 1.2, 1.4, 1.5, 1.6
"""

import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List, Optional, Any, Dict
from dataclasses import dataclass

import pandas as pd
import psutil


# ============================================================================
# Cancellation Support
# ============================================================================

class CancellationToken:
    """Token for cancelling long-running operations."""
    
    def __init__(self):
        self._cancelled = False
        self._lock = threading.Lock()
    
    def cancel(self):
        """Request cancellation of the operation."""
        with self._lock:
            self._cancelled = True
    
    def is_cancelled(self) -> bool:
        """Check if cancellation has been requested."""
        with self._lock:
            return self._cancelled


# ============================================================================
# Chunk Processor
# ============================================================================

class ChunkProcessor:
    """
    Process large files in chunks to avoid memory overflow.
    
    Requirements: 1.1, 1.2
    """
    
    def __init__(self, chunk_size_mb: int = 10):
        """
        Initialize ChunkProcessor.
        
        Args:
            chunk_size_mb: Size of each chunk in megabytes (default: 10MB)
        """
        self.chunk_size = chunk_size_mb * 1024 * 1024  # Convert to bytes
    
    def process_file_in_chunks(
        self,
        file_path: str,
        processor_func: Callable[[pd.DataFrame], pd.DataFrame],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> pd.DataFrame:
        """
        Process large files in chunks to avoid memory overflow.
        
        Args:
            file_path: Path to the file to process
            processor_func: Function to apply to each chunk
            progress_callback: Optional callback for progress updates (0.0 to 1.0)
        
        Returns:
            Processed DataFrame
        
        Requirements: 1.1, 1.2
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Estimate number of chunks for progress tracking
        total_chunks = self.estimate_chunk_count(str(file_path))
        
        # Determine file type and read in chunks
        file_extension = file_path.suffix.lower()
        
        processed_chunks = []
        chunk_index = 0
        
        if file_extension == '.csv':
            # Process CSV in chunks
            for chunk in pd.read_csv(file_path, chunksize=self._calculate_row_chunksize(file_path)):
                processed_chunk = processor_func(chunk)
                processed_chunks.append(processed_chunk)
                
                chunk_index += 1
                if progress_callback:
                    progress = chunk_index / total_chunks
                    progress_callback(progress)
        
        elif file_extension in ['.xlsx', '.xls']:
            # Excel files - read entire file but process in chunks
            df = pd.read_excel(file_path)
            row_chunksize = self._calculate_row_chunksize(file_path)
            
            for i in range(0, len(df), row_chunksize):
                chunk = df.iloc[i:i + row_chunksize]
                processed_chunk = processor_func(chunk)
                processed_chunks.append(processed_chunk)
                
                chunk_index += 1
                if progress_callback:
                    progress = chunk_index / total_chunks
                    progress_callback(progress)
        
        elif file_extension == '.json':
            # JSON files - read and process in chunks
            df = pd.read_json(file_path)
            row_chunksize = self._calculate_row_chunksize(file_path)
            
            for i in range(0, len(df), row_chunksize):
                chunk = df.iloc[i:i + row_chunksize]
                processed_chunk = processor_func(chunk)
                processed_chunks.append(processed_chunk)
                
                chunk_index += 1
                if progress_callback:
                    progress = chunk_index / total_chunks
                    progress_callback(progress)
        
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Combine all processed chunks
        if processed_chunks:
            result = pd.concat(processed_chunks, ignore_index=True)
            
            # Final progress update
            if progress_callback:
                progress_callback(1.0)
            
            return result
        else:
            return pd.DataFrame()
    
    def estimate_chunk_count(self, file_path: str) -> int:
        """
        Estimate number of chunks for progress tracking.
        
        Args:
            file_path: Path to the file
        
        Returns:
            Estimated number of chunks
        
        Requirements: 1.2
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return 0
        
        file_size = file_path.stat().st_size
        
        # Estimate chunks based on file size
        estimated_chunks = max(1, (file_size + self.chunk_size - 1) // self.chunk_size)
        
        return estimated_chunks
    
    def _calculate_row_chunksize(self, file_path: Path) -> int:
        """
        Calculate appropriate row chunksize based on file size and chunk_size.
        
        Args:
            file_path: Path to the file
        
        Returns:
            Number of rows per chunk
        """
        file_size = file_path.stat().st_size
        
        # Estimate rows based on file size and chunk size
        # Assume average row size is file_size / estimated_rows
        # For simplicity, use a heuristic: 10000 rows per 10MB
        rows_per_mb = 10000 / 10
        chunk_size_mb = self.chunk_size / (1024 * 1024)
        
        return max(1000, int(rows_per_mb * chunk_size_mb))


# ============================================================================
# Multi-Thread Executor
# ============================================================================

class MultiThreadExecutor:
    """
    Execute tasks in parallel using multiple threads.
    
    Requirements: 1.4, 1.6
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        """
        Initialize MultiThreadExecutor.
        
        Args:
            max_workers: Maximum number of worker threads (default: CPU count)
        """
        self.max_workers = max_workers or os.cpu_count() or 4
    
    def execute_parallel(
        self,
        tasks: List[Callable[[], Any]],
        cancellation_token: Optional[CancellationToken] = None
    ) -> List[Any]:
        """
        Execute independent tasks in parallel.
        
        Args:
            tasks: List of callable tasks to execute
            cancellation_token: Optional token for cancelling execution
        
        Returns:
            List of results from each task
        
        Requirements: 1.4, 1.6
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {executor.submit(task): i for i, task in enumerate(tasks)}
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                # Check for cancellation
                if cancellation_token and cancellation_token.is_cancelled():
                    # Cancel remaining futures
                    for f in future_to_task:
                        f.cancel()
                    break
                
                try:
                    result = future.result()
                    task_index = future_to_task[future]
                    results.append((task_index, result))
                except Exception as e:
                    task_index = future_to_task[future]
                    results.append((task_index, e))
        
        # Sort results by original task order
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]
    
    def map_parallel(
        self,
        func: Callable[[Any], Any],
        items: List[Any],
        cancellation_token: Optional[CancellationToken] = None
    ) -> List[Any]:
        """
        Apply function to items in parallel.
        
        Args:
            func: Function to apply to each item
            items: List of items to process
            cancellation_token: Optional token for cancelling execution
        
        Returns:
            List of results
        
        Requirements: 1.4, 1.6
        """
        # Create tasks from items
        tasks = [lambda item=item: func(item) for item in items]
        return self.execute_parallel(tasks, cancellation_token)


# ============================================================================
# Memory Monitor
# ============================================================================

class MemoryMonitor:
    """
    Monitor system memory usage and recommend processing modes.
    
    Requirements: 1.5
    """
    
    def __init__(self, threshold_percent: float = 0.8):
        """
        Initialize MemoryMonitor.
        
        Args:
            threshold_percent: Memory usage threshold (0.0 to 1.0)
        """
        self.threshold = threshold_percent
        self._monitoring = False
        self._monitor_thread = None
        self._callback = None
    
    def get_memory_usage(self) -> float:
        """
        Get current memory usage as percentage.
        
        Returns:
            Memory usage as a float between 0.0 and 1.0
        
        Requirements: 1.5
        """
        memory = psutil.virtual_memory()
        return memory.percent / 100.0
    
    def should_use_disk_mode(self) -> bool:
        """
        Check if should switch to disk-based processing.
        
        Returns:
            True if memory usage exceeds threshold
        
        Requirements: 1.5
        """
        return self.get_memory_usage() >= self.threshold
    
    def start_monitoring(self, callback: Callable[[float], None], interval: float = 1.0):
        """
        Start background memory monitoring.
        
        Args:
            callback: Function to call with memory usage updates
            interval: Monitoring interval in seconds
        
        Requirements: 1.5
        """
        if self._monitoring:
            return
        
        self._monitoring = True
        self._callback = callback
        
        def monitor_loop():
            while self._monitoring:
                memory_usage = self.get_memory_usage()
                if self._callback:
                    self._callback(memory_usage)
                time.sleep(interval)
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop background memory monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
            self._monitor_thread = None
