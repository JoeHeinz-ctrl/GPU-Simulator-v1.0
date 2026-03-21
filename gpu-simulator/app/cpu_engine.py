"""
CPU Sequential Execution Engine for GPU Parallel Floating-Point Simulator
Implements sequential floating-point operations for baseline performance measurement
"""

import numpy as np
import time
from typing import Tuple, Union
from datetime import datetime

from .models import SimulationResult


class CPUEngine:
    """
    Sequential CPU execution engine for floating-point operations.
    
    This class implements traditional sequential processing to establish
    baseline performance metrics for comparison with parallel GPU simulation.
    All operations use standard loops and NumPy functions to demonstrate
    how sequential processing scales with data size.
    """
    
    def __init__(self):
        """Initialize the CPU execution engine."""
        self.execution_history = []
    
    def vector_add(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform sequential vector addition: result[i] = a[i] + b[i]
        
        Educational demonstration of element-wise addition using sequential processing.
        This operation shows how CPU handles parallel-friendly computations sequentially.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (result_vector, execution_time_seconds)
            
        Raises:
            ValueError: If input vectors have different shapes
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        # Measure execution time with microsecond precision
        start_time = time.perf_counter()
        
        # Sequential implementation for educational purposes
        # In practice, NumPy's vectorized operations are highly optimized
        result = np.zeros_like(a)
        for i in range(len(a)):
            result[i] = a[i] + b[i]
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Store execution record
        self._record_execution("vector_add", len(a), execution_time)
        
        return result, execution_time
    
    def vector_multiply(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform sequential vector multiplication: result[i] = a[i] * b[i]
        
        Element-wise multiplication demonstrates how floating-point arithmetic
        operations scale with dataset size in sequential processing.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (result_vector, execution_time_seconds)
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        start_time = time.perf_counter()
        
        # Sequential multiplication loop
        result = np.zeros_like(a)
        for i in range(len(a)):
            result[i] = a[i] * b[i]
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("vector_multiply", len(a), execution_time)
        
        return result, execution_time
    
    def dot_product(self, a: np.ndarray, b: np.ndarray) -> Tuple[float, float]:
        """
        Perform sequential dot product: result = sum(a[i] * b[i])
        
        Demonstrates reduction operations where all elements contribute
        to a single result. Shows how sequential processing handles
        operations that require accumulation.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (dot_product_result, execution_time_seconds)
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        start_time = time.perf_counter()
        
        # Sequential dot product calculation
        result = 0.0
        for i in range(len(a)):
            result += a[i] * b[i]
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("dot_product", len(a), execution_time)
        
        return result, execution_time
    
    def matrix_multiply(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform sequential matrix multiplication using triple nested loops.
        
        Demonstrates the O(n³) complexity of matrix multiplication in sequential
        processing. This operation shows the most dramatic performance differences
        between sequential and parallel execution.
        
        Args:
            a: First input matrix (2D numpy array)
            b: Second input matrix (2D numpy array)
            
        Returns:
            Tuple of (result_matrix, execution_time_seconds)
        """
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"Matrix dimensions incompatible: {a.shape} x {b.shape}")
        
        start_time = time.perf_counter()
        
        # Sequential matrix multiplication with triple nested loops
        # This is intentionally naive to demonstrate sequential processing
        rows_a, cols_a = a.shape
        rows_b, cols_b = b.shape
        result = np.zeros((rows_a, cols_b))
        
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i, j] += a[i, k] * b[k, j]
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Record total elements processed (approximation for comparison)
        total_elements = rows_a * cols_b * cols_a
        self._record_execution("matrix_multiply", total_elements, execution_time)
        
        return result, execution_time
    
    def vector_fused_multiply_add(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform fused multiply-add: result[i] = a[i] * b[i] + c[i]
        
        Demonstrates a common floating-point operation that combines
        multiplication and addition. Useful for showing how complex
        operations can benefit from parallelization.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)  
            c: Third input vector (numpy array)
            
        Returns:
            Tuple of (result_vector, execution_time_seconds)
        """
        if not (a.shape == b.shape == c.shape):
            raise ValueError("All vectors must have the same shape")
        
        start_time = time.perf_counter()
        
        # Sequential fused multiply-add
        result = np.zeros_like(a)
        for i in range(len(a)):
            result[i] = a[i] * b[i] + c[i]
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("fused_multiply_add", len(a), execution_time)
        
        return result, execution_time
    
    def get_execution_history(self) -> list:
        """
        Get history of all CPU executions for performance analysis.
        
        Returns:
            List of execution records with operation, size, and timing data
        """
        return self.execution_history.copy()
    
    def clear_execution_history(self):
        """Clear the execution history."""
        self.execution_history.clear()
    
    def _record_execution(self, operation: str, dataset_size: int, execution_time: float):
        """
        Record execution details for performance tracking.
        
        Args:
            operation: Name of the operation performed
            dataset_size: Size of the dataset processed
            execution_time: Time taken for execution in seconds
        """
        record = SimulationResult(
            operation=operation,
            dataset_size=dataset_size,
            execution_time=execution_time,
            result_data=None,  # Don't store large result arrays
            timestamp=datetime.now(),
            engine_type="cpu"
        )
        self.execution_history.append(record)
    
    def estimate_performance(self, operation: str, dataset_size: int) -> float:
        """
        Estimate execution time for an operation based on historical data.
        
        Uses linear scaling assumption for educational purposes.
        
        Args:
            operation: Operation type to estimate
            dataset_size: Size of dataset to process
            
        Returns:
            Estimated execution time in seconds
        """
        # Find similar operations in history
        similar_ops = [
            record for record in self.execution_history 
            if record.operation == operation
        ]
        
        if not similar_ops:
            # No historical data, return rough estimate
            base_time_per_element = {
                "vector_add": 1e-8,
                "vector_multiply": 1e-8, 
                "dot_product": 1e-8,
                "matrix_multiply": 1e-6,  # Much slower due to O(n³)
                "fused_multiply_add": 1.5e-8
            }
            return base_time_per_element.get(operation, 1e-8) * dataset_size
        
        # Use most recent similar operation for scaling
        recent_op = max(similar_ops, key=lambda x: x.timestamp)
        scaling_factor = dataset_size / recent_op.dataset_size
        return recent_op.execution_time * scaling_factor