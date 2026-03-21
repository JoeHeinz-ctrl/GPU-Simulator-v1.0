"""
Workload Generator for GPU Parallel Floating-Point Simulator
Generates floating-point datasets for computational operations
"""

import numpy as np
from typing import Tuple, List
from datetime import datetime
import math

from .models import Dataset


class WorkloadGenerator:
    """
    Generates floating-point datasets for parallel computing simulations.
    
    This class creates datasets that simulate real-world computational workloads
    for educational purposes, helping students understand how data size affects
    parallel processing performance.
    """
    
    # Supported dataset sizes for educational demonstration
    SUPPORTED_SIZES = [10000, 50000, 100000, 500000]
    
    def __init__(self, random_seed: int = None):
        """
        Initialize the workload generator.
        
        Args:
            random_seed: Optional seed for reproducible random number generation
        """
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def generate_dataset(self, size: int, operation_type: str = "vector_add") -> Dataset:
        """
        Generate a floating-point dataset of specified size.
        
        Creates random float64 values in the range [0.0, 1.0] to ensure
        numerical stability and consistent performance characteristics.
        
        Args:
            size: Number of elements to generate (must be in SUPPORTED_SIZES)
            operation_type: Type of operation the dataset will be used for
            
        Returns:
            Dataset object containing the generated data and metadata
            
        Raises:
            ValueError: If size is not supported or invalid
        """
        if size not in self.SUPPORTED_SIZES:
            raise ValueError(f"Dataset size {size} not supported. Use one of: {self.SUPPORTED_SIZES}")
        
        if size <= 0:
            raise ValueError("Dataset size must be positive")
        
        # Generate random floating-point data in [0.0, 1.0] range
        # Using float64 for educational precision without performance overhead
        data = np.random.random(size).astype(np.float64)
        
        return Dataset(
            size=size,
            data=data,
            created_at=datetime.now(),
            operation_type=operation_type
        )
    
    def generate_vector_pair(self, size: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a pair of vectors for binary operations (addition, multiplication, dot product).
        
        Args:
            size: Number of elements in each vector
            
        Returns:
            Tuple of two numpy arrays with random float64 values
        """
        if size not in self.SUPPORTED_SIZES:
            raise ValueError(f"Dataset size {size} not supported. Use one of: {self.SUPPORTED_SIZES}")
        
        vector_a = np.random.random(size).astype(np.float64)
        vector_b = np.random.random(size).astype(np.float64)
        
        return vector_a, vector_b
    
    def generate_matrix_pair(self, size: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a pair of square matrices for matrix multiplication.
        
        For educational purposes, we create square matrices where the total
        number of elements approximates the requested size. This helps
        demonstrate how matrix operations scale with data size.
        
        Args:
            size: Approximate total number of elements (will be adjusted for square matrices)
            
        Returns:
            Tuple of two square numpy arrays with random float64 values
        """
        if size not in self.SUPPORTED_SIZES:
            raise ValueError(f"Dataset size {size} not supported. Use one of: {self.SUPPORTED_SIZES}")
        
        # Calculate matrix dimension to approximate the requested size
        # For a square matrix: dimension^2 ≈ size
        dimension = int(math.sqrt(size))
        
        # Ensure minimum dimension for meaningful computation
        dimension = max(dimension, 10)
        
        matrix_a = np.random.random((dimension, dimension)).astype(np.float64)
        matrix_b = np.random.random((dimension, dimension)).astype(np.float64)
        
        return matrix_a, matrix_b
    
    def get_supported_sizes(self) -> List[int]:
        """
        Get list of supported dataset sizes.
        
        Returns:
            List of supported dataset sizes for the simulator
        """
        return self.SUPPORTED_SIZES.copy()
    
    def estimate_memory_usage(self, size: int) -> float:
        """
        Estimate memory usage in MB for a dataset of given size.
        
        Helps users understand memory requirements for different dataset sizes.
        Assumes float64 (8 bytes per element) for calculations.
        
        Args:
            size: Dataset size in elements
            
        Returns:
            Estimated memory usage in megabytes
        """
        bytes_per_element = 8  # float64
        total_bytes = size * bytes_per_element
        megabytes = total_bytes / (1024 * 1024)
        return megabytes
    
    def validate_generation_time(self, size: int, max_time_seconds: float = 5.0) -> bool:
        """
        Validate that dataset generation will complete within time limit.
        
        Educational requirement: all dataset generation should complete within 5 seconds.
        
        Args:
            size: Dataset size to validate
            max_time_seconds: Maximum allowed generation time
            
        Returns:
            True if generation is expected to complete within time limit
        """
        # Empirical estimation: modern systems can generate ~10M float64/second
        estimated_time = size / 10_000_000
        return estimated_time <= max_time_seconds