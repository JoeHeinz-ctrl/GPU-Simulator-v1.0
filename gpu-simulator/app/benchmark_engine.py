"""
Benchmark Engine for GPU Quantum Compute Simulator
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

from .workload_generator import WorkloadGenerator
from .cpu_engine import CPUEngine
from .parallel_engine import GPUSimulator


@dataclass
class BenchmarkProgress:
    current_test: int
    total_tests: int
    current_operation: str
    current_size: int
    completed_tests: List
    status: str


class BenchmarkEngine:
    def __init__(self):
        self.workload_generator = WorkloadGenerator()
        self.cpu_engine = CPUEngine()
        self.gpu_simulator = GPUSimulator()
        self.current_progress: Optional[BenchmarkProgress] = None
        self.is_cancelled = False
    
    async def run_benchmark_suite(
        self,
        operations: List[str],
        dataset_sizes: List[int],
        num_processes: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run benchmark suite"""
        self.is_cancelled = False
        results = []
        total_tests = len(operations) * len(dataset_sizes)
        current_test = 0
        
        self.current_progress = BenchmarkProgress(
            current_test=0,
            total_tests=total_tests,
            current_operation='',
            current_size=0,
            completed_tests=[],
            status='running'
        )
        
        start_time = time.perf_counter()
        
        for operation in operations:
            for dataset_size in dataset_sizes:
                if self.is_cancelled:
                    break
                
                current_test += 1
                self.current_progress.current_test = current_test
                self.current_progress.current_operation = operation
                self.current_progress.current_size = dataset_size
                
                result = await self.run_single_benchmark(operation, dataset_size, num_processes)
                if result:
                    results.append(result)
                
                await asyncio.sleep(0.1)
            
            if self.is_cancelled:
                break
        
        total_duration = time.perf_counter() - start_time
        speedups = [r['speedup'] for r in results]
        
        return {
            'results': results,
            'total_tests': len(results),
            'average_speedup': sum(speedups) / len(speedups) if speedups else 0,
            'best_speedup': max(speedups) if speedups else 0,
            'worst_speedup': min(speedups) if speedups else 0,
            'total_duration': total_duration,
            'completed': not self.is_cancelled
        }
    
    async def run_single_benchmark(self, operation: str, dataset_size: int, num_processes: Optional[int]) -> Optional[Dict]:
        """Run single benchmark"""
        try:
            dataset = self.workload_generator.generate_dataset(dataset_size, operation)
            
            if operation == "matrix_multiply":
                matrix_a, matrix_b = self.workload_generator.generate_matrix_pair(dataset_size)
                data_a, data_b = matrix_a, matrix_b
            else:
                vector_a, vector_b = self.workload_generator.generate_vector_pair(dataset_size)
                data_a, data_b = vector_a, vector_b
            
            # CPU
            if operation == "vector_add":
                _, cpu_time = self.cpu_engine.vector_add(data_a, data_b)
            elif operation == "vector_multiply":
                _, cpu_time = self.cpu_engine.vector_multiply(data_a, data_b)
            elif operation == "dot_product":
                _, cpu_time = self.cpu_engine.dot_product(data_a, data_b)
            elif operation == "matrix_multiply":
                _, cpu_time = self.cpu_engine.matrix_multiply(data_a, data_b)
            else:
                return None
            
            # GPU
            gpu_sim = GPUSimulator(num_processes) if num_processes else self.gpu_simulator
            
            if operation == "vector_add":
                _, gpu_time = gpu_sim.vector_add_parallel(data_a, data_b)
            elif operation == "vector_multiply":
                _, gpu_time = gpu_sim.vector_multiply_parallel(data_a, data_b)
            elif operation == "dot_product":
                _, gpu_time = gpu_sim.dot_product_parallel(data_a, data_b)
            elif operation == "matrix_multiply":
                _, gpu_time = gpu_sim.matrix_multiply_parallel(data_a, data_b)
            else:
                return None
            
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            
            return {
                'operation': operation,
                'dataset_size': dataset_size,
                'cpu_time': cpu_time,
                'gpu_time': gpu_time,
                'speedup': speedup,
                'timestamp': datetime.now().isoformat()
            }
        except:
            return None
    
    def cancel_benchmark(self):
        """Cancel benchmark"""
        self.is_cancelled = True
    
    def get_progress(self) -> Optional[BenchmarkProgress]:
        """Get progress"""
        return self.current_progress
