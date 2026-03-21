"""
GPU Parallel Simulation Engine for GPU Parallel Floating-Point Simulator
Simulates GPU-style parallel execution using Python multiprocessing
"""

import numpy as np
import time
import multiprocessing as mp
from typing import Tuple, List, Dict, Any
from datetime import datetime
import math

from .models import SimulationResult, ThreadBlockInfo


def _worker_vector_add(args):
    """Worker function for parallel vector addition"""
    chunk_a, chunk_b, chunk_id = args
    return chunk_id, chunk_a + chunk_b


def _worker_vector_multiply(args):
    """Worker function for parallel vector multiplication"""
    chunk_a, chunk_b, chunk_id = args
    return chunk_id, chunk_a * chunk_b


def _worker_dot_product(args):
    """Worker function for parallel dot product (partial sum)"""
    chunk_a, chunk_b, chunk_id = args
    partial_sum = np.sum(chunk_a * chunk_b)
    return chunk_id, partial_sum


def _worker_matrix_multiply_row(args):
    """Worker function for parallel matrix multiplication (row-wise)"""
    row_a, matrix_b, row_id = args
    result_row = np.dot(row_a, matrix_b)
    return row_id, result_row


class GPUSimulator:
    """
    Simulates GPU-style parallel execution using Python multiprocessing.
    
    This class demonstrates how GPUs process data by dividing work into
    thread blocks (simulated as worker processes) that execute in parallel.
    Each worker process handles a chunk of data, mimicking how GPU cores
    work together to accelerate floating-point computations.
    """
    
    def __init__(self, num_processes: int = None):
        """
        Initialize the GPU simulator.
        
        Args:
            num_processes: Number of worker processes (thread blocks).
                          If None, uses CPU count for optimal performance.
        """
        if num_processes is None:
            # Use CPU count as default, simulating GPU cores
            self.num_processes = mp.cpu_count()
        else:
            self.num_processes = max(1, min(num_processes, mp.cpu_count() * 2))
        
        self.execution_history = []
    
    def vector_add_parallel(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform parallel vector addition using multiprocessing.
        
        Simulates how GPUs divide vector operations across thread blocks.
        Each worker process (thread block) handles a chunk of the vectors,
        performing element-wise addition in parallel.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (result_vector, execution_time_seconds)
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        start_time = time.perf_counter()
        
        # Divide data into chunks (thread blocks)
        chunks_a, chunks_b = self._create_vector_chunks(a, b)
        
        # Create work items for each thread block
        work_items = [
            (chunks_a[i], chunks_b[i], i) 
            for i in range(len(chunks_a))
        ]
        
        # Execute in parallel using multiprocessing Pool
        with mp.Pool(processes=self.num_processes) as pool:
            results = pool.map(_worker_vector_add, work_items)
        
        # Combine results from all thread blocks
        result = self._combine_vector_results(results, len(a))
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("vector_add_parallel", len(a), execution_time)
        
        return result, execution_time
    
    def vector_multiply_parallel(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform parallel vector multiplication using multiprocessing.
        
        Demonstrates element-wise multiplication across thread blocks,
        showing how embarrassingly parallel operations benefit from
        GPU-style parallel processing.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (result_vector, execution_time_seconds)
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        start_time = time.perf_counter()
        
        chunks_a, chunks_b = self._create_vector_chunks(a, b)
        work_items = [
            (chunks_a[i], chunks_b[i], i) 
            for i in range(len(chunks_a))
        ]
        
        with mp.Pool(processes=self.num_processes) as pool:
            results = pool.map(_worker_vector_multiply, work_items)
        
        result = self._combine_vector_results(results, len(a))
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("vector_multiply_parallel", len(a), execution_time)
        
        return result, execution_time
    
    def dot_product_parallel(self, a: np.ndarray, b: np.ndarray) -> Tuple[float, float]:
        """
        Perform parallel dot product using reduction across thread blocks.
        
        Demonstrates how reduction operations work in parallel processing:
        1. Each thread block computes partial sums
        2. Main thread combines partial sums into final result
        
        This shows both parallel computation and the reduction pattern
        common in GPU programming.
        
        Args:
            a: First input vector (numpy array)
            b: Second input vector (numpy array)
            
        Returns:
            Tuple of (dot_product_result, execution_time_seconds)
        """
        if a.shape != b.shape:
            raise ValueError(f"Vector shapes must match: {a.shape} vs {b.shape}")
        
        start_time = time.perf_counter()
        
        chunks_a, chunks_b = self._create_vector_chunks(a, b)
        work_items = [
            (chunks_a[i], chunks_b[i], i) 
            for i in range(len(chunks_a))
        ]
        
        with mp.Pool(processes=self.num_processes) as pool:
            results = pool.map(_worker_dot_product, work_items)
        
        # Reduction: sum all partial results
        total_sum = sum(partial_sum for _, partial_sum in results)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self._record_execution("dot_product_parallel", len(a), execution_time)
        
        return total_sum, execution_time
    
    def matrix_multiply_parallel(self, a: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Perform parallel matrix multiplication using row-wise distribution.
        
        Simulates GPU matrix multiplication by distributing rows of the first
        matrix across thread blocks. Each thread block computes one or more
        rows of the result matrix independently.
        
        Args:
            a: First input matrix (2D numpy array)
            b: Second input matrix (2D numpy array)
            
        Returns:
            Tuple of (result_matrix, execution_time_seconds)
        """
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"Matrix dimensions incompatible: {a.shape} x {b.shape}")
        
        start_time = time.perf_counter()
        
        rows_a = a.shape[0]
        
        # Distribute rows across thread blocks
        work_items = [(a[i], b, i) for i in range(rows_a)]
        
        with mp.Pool(processes=self.num_processes) as pool:
            results = pool.map(_worker_matrix_multiply_row, work_items)
        
        # Combine results maintaining row order
        results.sort(key=lambda x: x[0])  # Sort by row_id
        result_matrix = np.array([row_result for _, row_result in results])
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Record total operations for comparison
        total_ops = a.shape[0] * a.shape[1] * b.shape[1]
        self._record_execution("matrix_multiply_parallel", total_ops, execution_time)
        
        return result_matrix, execution_time
    
    def get_thread_block_info(self, dataset_size: int) -> ThreadBlockInfo:
        """
        Get information about thread block distribution for visualization.
        
        Args:
            dataset_size: Size of the dataset being processed
            
        Returns:
            ThreadBlockInfo object with block distribution details
        """
        block_size = math.ceil(dataset_size / self.num_processes)
        actual_blocks = math.ceil(dataset_size / block_size)
        
        # Calculate how many elements each process will handle
        process_distribution = []
        for i in range(actual_blocks):
            start_idx = i * block_size
            end_idx = min(start_idx + block_size, dataset_size)
            elements_in_block = end_idx - start_idx
            process_distribution.append(elements_in_block)
        
        return ThreadBlockInfo(
            num_blocks=actual_blocks,
            block_size=block_size,
            total_elements=dataset_size,
            process_distribution=process_distribution
        )
    
    def _create_vector_chunks(self, a: np.ndarray, b: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Divide vectors into chunks for parallel processing.
        
        Simulates how GPU memory controllers distribute data across
        thread blocks for parallel execution.
        
        Args:
            a: First vector to chunk
            b: Second vector to chunk
            
        Returns:
            Tuple of (chunks_a, chunks_b) lists
        """
        chunk_size = math.ceil(len(a) / self.num_processes)
        
        chunks_a = []
        chunks_b = []
        
        for i in range(0, len(a), chunk_size):
            end_idx = min(i + chunk_size, len(a))
            chunks_a.append(a[i:end_idx])
            chunks_b.append(b[i:end_idx])
        
        return chunks_a, chunks_b
    
    def _combine_vector_results(self, results: List[Tuple[int, np.ndarray]], total_size: int) -> np.ndarray:
        """
        Combine results from parallel workers into final vector.
        
        Args:
            results: List of (chunk_id, result_chunk) tuples
            total_size: Expected size of final result
            
        Returns:
            Combined result vector
        """
        # Sort results by chunk_id to maintain order
        results.sort(key=lambda x: x[0])
        
        # Concatenate all result chunks
        combined = np.concatenate([result_chunk for _, result_chunk in results])
        
        return combined
    
    def get_execution_history(self) -> List[SimulationResult]:
        """Get history of all GPU simulation executions."""
        return self.execution_history.copy()
    
    def clear_execution_history(self):
        """Clear the execution history."""
        self.execution_history.clear()
    
    def _record_execution(self, operation: str, dataset_size: int, execution_time: float):
        """Record execution details for performance tracking."""
        record = SimulationResult(
            operation=operation,
            dataset_size=dataset_size,
            execution_time=execution_time,
            result_data=None,  # Don't store large result arrays
            timestamp=datetime.now(),
            engine_type="gpu"
        )
        self.execution_history.append(record)
    
    def get_optimal_process_count(self, dataset_size: int) -> int:
        """
        Determine optimal number of processes for a given dataset size.
        
        Educational heuristic: balance parallelism with overhead.
        Too many processes can hurt performance due to overhead.
        
        Args:
            dataset_size: Size of dataset to process
            
        Returns:
            Recommended number of processes
        """
        # Heuristic: at least 1000 elements per process to justify overhead
        min_elements_per_process = 1000
        max_useful_processes = dataset_size // min_elements_per_process
        
        # Don't exceed available CPU cores
        return min(max_useful_processes, self.num_processes, mp.cpu_count())
    
    def estimate_speedup(self, dataset_size: int, cpu_time: float) -> float:
        """
        Estimate expected speedup for parallel execution.
        
        Educational estimation based on Amdahl's Law and overhead considerations.
        
        Args:
            dataset_size: Size of dataset
            cpu_time: Sequential execution time
            
        Returns:
            Estimated speedup ratio
        """
        # Simple model: speedup limited by number of processes and overhead
        theoretical_speedup = min(self.num_processes, dataset_size / 1000)
        
        # Account for multiprocessing overhead (empirical factor)
        overhead_factor = 0.8  # 20% overhead
        practical_speedup = theoretical_speedup * overhead_factor
        
        return max(1.0, practical_speedup)  # Never slower than 1x