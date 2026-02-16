"""
Unit tests for Performance Optimizer module.

Tests specific functionality of ChunkProcessor, MultiThreadExecutor,
MemoryMonitor, and CancellationToken classes.
"""

import os
import time
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from utils.performance_optimizer import (
    ChunkProcessor,
    MultiThreadExecutor,
    MemoryMonitor,
    CancellationToken
)


class TestChunkProcessor:
    """Unit tests for ChunkProcessor class."""
    
    def test_chunk_processor_initialization(self):
        """Test ChunkProcessor can be initialized with default and custom chunk sizes."""
        processor_default = ChunkProcessor()
        assert processor_default.chunk_size == 10 * 1024 * 1024  # 10MB in bytes
        
        processor_custom = ChunkProcessor(chunk_size_mb=20)
        assert processor_custom.chunk_size == 20 * 1024 * 1024  # 20MB in bytes
    
    def test_process_small_csv_file(self, temp_dir):
        """Test processing a small CSV file."""
        # Create a small CSV file
        csv_path = temp_dir / "small_test.csv"
        df = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "value": [10.5, 20.3, 30.7, 40.2, 50.9]
        })
        df.to_csv(csv_path, index=False)
        
        # Process file
        processor = ChunkProcessor(chunk_size_mb=1)
        
        def identity_processor(chunk: pd.DataFrame) -> pd.DataFrame:
            return chunk
        
        result = processor.process_file_in_chunks(
            str(csv_path),
            identity_processor
        )
        
        # Verify result
        assert len(result) == 5
        assert list(result.columns) == ["id", "name", "value"]
        pd.testing.assert_frame_equal(result, df)
    
    def test_process_file_with_progress_callback(self, temp_dir):
        """Test that progress callback is called during processing."""
        # Create a CSV file
        csv_path = temp_dir / "test.csv"
        df = pd.DataFrame({
            "col1": range(1000),
            "col2": range(1000, 2000)
        })
        df.to_csv(csv_path, index=False)
        
        # Track progress updates
        progress_updates = []
        
        def progress_callback(progress: float):
            progress_updates.append(progress)
        
        # Process file
        processor = ChunkProcessor(chunk_size_mb=1)
        
        def identity_processor(chunk: pd.DataFrame) -> pd.DataFrame:
            return chunk
        
        result = processor.process_file_in_chunks(
            str(csv_path),
            identity_processor,
            progress_callback=progress_callback
        )
        
        # Verify progress updates
        assert len(progress_updates) > 0, "Progress callback should be called"
        assert progress_updates[-1] == 1.0, "Final progress should be 1.0"
        
        # Verify progress is monotonically increasing
        for i in range(1, len(progress_updates)):
            assert progress_updates[i] >= progress_updates[i-1], "Progress should increase"
    
    def test_estimate_chunk_count(self, temp_dir):
        """Test chunk count estimation."""
        # Create a file
        csv_path = temp_dir / "test.csv"
        df = pd.DataFrame({"col": range(10000)})
        df.to_csv(csv_path, index=False)
        
        processor = ChunkProcessor(chunk_size_mb=1)
        chunk_count = processor.estimate_chunk_count(str(csv_path))
        
        assert chunk_count >= 1, "Should estimate at least 1 chunk"
    
    def test_process_nonexistent_file(self):
        """Test that processing a nonexistent file raises FileNotFoundError."""
        processor = ChunkProcessor()
        
        def identity_processor(chunk: pd.DataFrame) -> pd.DataFrame:
            return chunk
        
        with pytest.raises(FileNotFoundError):
            processor.process_file_in_chunks(
                "nonexistent_file.csv",
                identity_processor
            )


class TestMultiThreadExecutor:
    """Unit tests for MultiThreadExecutor class."""
    
    def test_executor_initialization(self):
        """Test MultiThreadExecutor initialization."""
        executor_default = MultiThreadExecutor()
        assert executor_default.max_workers >= 1
        
        executor_custom = MultiThreadExecutor(max_workers=4)
        assert executor_custom.max_workers == 4
    
    def test_execute_parallel_tasks(self):
        """Test executing multiple tasks in parallel."""
        executor = MultiThreadExecutor(max_workers=4)
        
        def task1():
            return 1
        
        def task2():
            return 2
        
        def task3():
            return 3
        
        tasks = [task1, task2, task3]
        results = executor.execute_parallel(tasks)
        
        assert len(results) == 3
        assert set(results) == {1, 2, 3}
    
    def test_map_parallel(self):
        """Test mapping a function over items in parallel."""
        executor = MultiThreadExecutor(max_workers=4)
        
        def square(x):
            return x * x
        
        items = [1, 2, 3, 4, 5]
        results = executor.map_parallel(square, items)
        
        assert results == [1, 4, 9, 16, 25]
    
    def test_cancellation_support(self):
        """Test that operations can be cancelled."""
        executor = MultiThreadExecutor(max_workers=2)
        cancellation_token = CancellationToken()
        
        def slow_task():
            time.sleep(0.5)
            return "completed"
        
        # Start tasks
        tasks = [slow_task for _ in range(10)]
        
        # Cancel after a short delay
        def cancel_after_delay():
            time.sleep(0.1)
            cancellation_token.cancel()
        
        import threading
        cancel_thread = threading.Thread(target=cancel_after_delay)
        cancel_thread.start()
        
        start_time = time.time()
        results = executor.execute_parallel(tasks, cancellation_token)
        duration = time.time() - start_time
        
        cancel_thread.join()
        
        # Should complete faster than running all tasks
        assert duration < 2.0, "Cancellation should stop execution early"


class TestMemoryMonitor:
    """Unit tests for MemoryMonitor class."""
    
    def test_memory_monitor_initialization(self):
        """Test MemoryMonitor initialization."""
        monitor_default = MemoryMonitor()
        assert monitor_default.threshold == 0.8
        
        monitor_custom = MemoryMonitor(threshold_percent=0.9)
        assert monitor_custom.threshold == 0.9
    
    def test_get_memory_usage(self):
        """Test getting current memory usage."""
        monitor = MemoryMonitor()
        usage = monitor.get_memory_usage()
        
        assert 0.0 <= usage <= 1.0, "Memory usage should be between 0 and 1"
    
    def test_should_use_disk_mode(self):
        """Test disk mode recommendation."""
        # Use a very high threshold so it returns False
        monitor = MemoryMonitor(threshold_percent=0.99)
        assert monitor.should_use_disk_mode() == False
        
        # Use a very low threshold so it returns True
        monitor_low = MemoryMonitor(threshold_percent=0.01)
        assert monitor_low.should_use_disk_mode() == True
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping background monitoring."""
        monitor = MemoryMonitor()
        updates = []
        
        def callback(usage):
            updates.append(usage)
        
        # Start monitoring
        monitor.start_monitoring(callback, interval=0.1)
        time.sleep(0.5)
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        # Should have received some updates
        assert len(updates) > 0, "Should receive memory updates"
        
        # All updates should be valid
        for usage in updates:
            assert 0.0 <= usage <= 1.0


class TestCancellationToken:
    """Unit tests for CancellationToken class."""
    
    def test_cancellation_token_initialization(self):
        """Test CancellationToken initialization."""
        token = CancellationToken()
        assert token.is_cancelled() == False
    
    def test_cancel_token(self):
        """Test cancelling a token."""
        token = CancellationToken()
        assert token.is_cancelled() == False
        
        token.cancel()
        assert token.is_cancelled() == True
    
    def test_thread_safety(self):
        """Test that CancellationToken is thread-safe."""
        token = CancellationToken()
        
        def cancel_from_thread():
            time.sleep(0.1)
            token.cancel()
        
        import threading
        thread = threading.Thread(target=cancel_from_thread)
        thread.start()
        
        # Check status before cancellation
        assert token.is_cancelled() == False
        
        # Wait for cancellation
        thread.join()
        
        # Check status after cancellation
        assert token.is_cancelled() == True
