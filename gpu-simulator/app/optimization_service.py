"""
Optimization Service for GPU Quantum Compute Simulator
"""

import multiprocessing
import psutil
from typing import Dict, Any


class OptimizationService:
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.available_memory_gb = self._get_available_memory()
    
    def _get_available_memory(self) -> float:
        """Get available memory in GB"""
        try:
            memory = psutil.virtual_memory()
            return memory.available / (1024 ** 3)
        except:
            return 8.0
    
    def get_optimization_suggestions(self) -> Dict[str, Any]:
        """Get optimization suggestions"""
        recommended_processes = max(1, int(self.cpu_count * 0.75))
        
        available_memory_bytes = self.available_memory_gb * (1024 ** 3) * 0.5
        max_dataset_size = int(available_memory_bytes / 8)
        
        supported_sizes = [10000, 50000, 100000, 500000]
        valid_sizes = [s for s in supported_sizes if s <= max_dataset_size]
        recommended_dataset_size = max(valid_sizes) if valid_sizes else min(supported_sizes)
        
        rationale = {
            "processes": f"Using {recommended_processes} of {self.cpu_count} CPU cores (75%) for optimal performance",
            "dataset_size": f"Recommended {recommended_dataset_size:,} elements based on {self.available_memory_gb:.1f}GB available memory",
            "memory": f"Each element uses ~8 bytes. Total usage: ~{(recommended_dataset_size * 8) / (1024**2):.1f}MB"
        }
        
        return {
            "recommended_processes": recommended_processes,
            "recommended_dataset_size": recommended_dataset_size,
            "cpu_cores": self.cpu_count,
            "available_memory_gb": round(self.available_memory_gb, 2),
            "rationale": rationale
        }
