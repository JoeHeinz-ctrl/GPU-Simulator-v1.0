"""
Performance Analysis Component for GPU Parallel Floating-Point Simulator
Analyzes and compares performance between CPU and GPU execution modes
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import statistics

from .models import PerformanceMetrics, SimulationResult


class PerformanceAnalyzer:
    """
    Analyzes performance characteristics of CPU vs GPU simulation execution.
    
    This class provides comprehensive performance analysis for educational
    purposes, helping students understand speedup, efficiency, and the
    factors that influence parallel processing performance.
    """
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.performance_history: List[PerformanceMetrics] = []
        self.analysis_cache: Dict[str, Any] = {}
    
    def calculate_speedup(self, cpu_time: float, gpu_time: float) -> float:
        """
        Calculate speedup ratio between CPU and GPU execution.
        
        Speedup = CPU_time / GPU_time
        - Speedup > 1.0: GPU is faster
        - Speedup < 1.0: CPU is faster  
        - Speedup = 1.0: Equal performance
        
        Args:
            cpu_time: CPU execution time in seconds
            gpu_time: GPU execution time in seconds
            
        Returns:
            Speedup ratio with proper handling of edge cases
        """
        # Handle edge cases for educational robustness
        if cpu_time <= 0:
            raise ValueError("CPU time must be positive")
        
        if gpu_time <= 0:
            # If GPU time is zero or negative, assume minimal measurable time
            gpu_time = 1e-6  # 1 microsecond
        
        # Handle near-zero GPU times (measurement precision issues)
        if gpu_time < 1e-6:
            gpu_time = 1e-6
        
        speedup = cpu_time / gpu_time
        
        # Round to 2 decimal places for educational display
        return round(speedup, 2)
    
    def analyze_results(self, cpu_result: Tuple[Any, float], gpu_result: Tuple[Any, float], 
                       operation: str, dataset_size: int, num_processes: int = None) -> Dict[str, Any]:
        """
        Comprehensive analysis of CPU vs GPU execution results.
        
        Args:
            cpu_result: Tuple of (result_data, execution_time) from CPU
            gpu_result: Tuple of (result_data, execution_time) from GPU
            operation: Name of the operation performed
            dataset_size: Size of the dataset processed
            num_processes: Number of processes used in GPU simulation
            
        Returns:
            Dictionary containing comprehensive performance analysis
        """
        cpu_data, cpu_time = cpu_result
        gpu_data, gpu_time = gpu_result
        
        # Calculate core metrics
        speedup = self.calculate_speedup(cpu_time, gpu_time)
        efficiency = self._calculate_efficiency(speedup, num_processes or 1)
        
        # Verify result consistency (educational validation)
        results_match = self._verify_result_consistency(cpu_data, gpu_data, operation)
        
        # Create performance metrics record
        metrics = PerformanceMetrics(
            cpu_time=round(cpu_time, 3),
            gpu_time=round(gpu_time, 3),
            speedup_ratio=speedup,
            dataset_size=dataset_size,
            operation=operation,
            num_processes=num_processes or 1,
            timestamp=datetime.now()
        )
        
        # Add to history
        self.performance_history.append(metrics)
        
        # Comprehensive analysis
        analysis = {
            "speedup": speedup,
            "efficiency": efficiency,
            "cpu_time": round(cpu_time, 3),
            "gpu_time": round(gpu_time, 3),
            "results_consistent": results_match,
            "performance_category": self._categorize_performance(speedup),
            "throughput_improvement": self._calculate_throughput_improvement(cpu_time, gpu_time),
            "elements_per_second_cpu": round(dataset_size / cpu_time, 0),
            "elements_per_second_gpu": round(dataset_size / gpu_time, 0),
            "overhead_analysis": self._analyze_overhead(speedup, num_processes or 1),
            "educational_insights": self._generate_educational_insights(speedup, operation, dataset_size)
        }
        
        return analysis
    
    def get_performance_history(self) -> List[Dict[str, Any]]:
        """
        Get performance history formatted for visualization and analysis.
        
        Returns:
            List of performance records with additional computed metrics
        """
        history = []
        for metrics in self.performance_history:
            record = {
                "timestamp": metrics.timestamp.isoformat(),
                "operation": metrics.operation,
                "dataset_size": metrics.dataset_size,
                "cpu_time": metrics.cpu_time,
                "gpu_time": metrics.gpu_time,
                "speedup": metrics.speedup_ratio,
                "efficiency": self._calculate_efficiency(metrics.speedup_ratio, metrics.num_processes),
                "num_processes": metrics.num_processes
            }
            history.append(record)
        
        return history
    
    def get_summary_statistics(self) -> Dict[str, float]:
        """
        Calculate summary statistics across all performance measurements.
        
        Returns:
            Dictionary with statistical summaries for educational analysis
        """
        if not self.performance_history:
            return {}
        
        speedups = [m.speedup_ratio for m in self.performance_history]
        cpu_times = [m.cpu_time for m in self.performance_history]
        gpu_times = [m.gpu_time for m in self.performance_history]
        
        return {
            "avg_speedup": round(statistics.mean(speedups), 2),
            "max_speedup": round(max(speedups), 2),
            "min_speedup": round(min(speedups), 2),
            "median_speedup": round(statistics.median(speedups), 2),
            "speedup_std_dev": round(statistics.stdev(speedups) if len(speedups) > 1 else 0, 2),
            "avg_cpu_time": round(statistics.mean(cpu_times), 3),
            "avg_gpu_time": round(statistics.mean(gpu_times), 3),
            "total_measurements": len(self.performance_history),
            "operations_tested": len(set(m.operation for m in self.performance_history))
        }
    
    def analyze_scaling_behavior(self, operation: str) -> Dict[str, Any]:
        """
        Analyze how performance scales with dataset size for a specific operation.
        
        Args:
            operation: Operation to analyze scaling for
            
        Returns:
            Scaling analysis results
        """
        # Filter history for specific operation
        op_history = [m for m in self.performance_history if m.operation == operation]
        
        if len(op_history) < 2:
            return {"error": "Insufficient data for scaling analysis"}
        
        # Sort by dataset size
        op_history.sort(key=lambda x: x.dataset_size)
        
        sizes = [m.dataset_size for m in op_history]
        speedups = [m.speedup_ratio for m in op_history]
        
        # Calculate scaling efficiency
        scaling_analysis = {
            "operation": operation,
            "data_points": len(op_history),
            "size_range": {"min": min(sizes), "max": max(sizes)},
            "speedup_range": {"min": min(speedups), "max": max(speedups)},
            "scaling_trend": self._analyze_scaling_trend(sizes, speedups),
            "optimal_size": self._find_optimal_dataset_size(op_history)
        }
        
        return scaling_analysis
    
    def _calculate_efficiency(self, speedup: float, num_processes: int) -> float:
        """
        Calculate parallel efficiency: speedup / num_processes
        
        Perfect efficiency = 1.0 (linear speedup)
        Efficiency < 1.0 indicates overhead or non-parallelizable work
        """
        if num_processes <= 0:
            return 0.0
        
        efficiency = speedup / num_processes
        return round(efficiency, 3)
    
    def _verify_result_consistency(self, cpu_result: Any, gpu_result: Any, operation: str) -> bool:
        """
        Verify that CPU and GPU results are mathematically consistent.
        
        Educational validation to ensure simulation correctness.
        """
        try:
            if operation == "dot_product":
                # Single float values
                return abs(cpu_result - gpu_result) < 1e-10
            else:
                # Array results
                if not isinstance(cpu_result, np.ndarray) or not isinstance(gpu_result, np.ndarray):
                    return False
                
                if cpu_result.shape != gpu_result.shape:
                    return False
                
                # Check element-wise differences within floating-point precision
                return np.allclose(cpu_result, gpu_result, rtol=1e-10, atol=1e-10)
        
        except Exception:
            return False
    
    def _categorize_performance(self, speedup: float) -> str:
        """Categorize performance for educational understanding."""
        if speedup >= 4.0:
            return "Excellent"
        elif speedup >= 2.0:
            return "Good"
        elif speedup >= 1.2:
            return "Moderate"
        elif speedup >= 0.8:
            return "Comparable"
        else:
            return "Poor"
    
    def _calculate_throughput_improvement(self, cpu_time: float, gpu_time: float) -> float:
        """Calculate throughput improvement percentage."""
        if cpu_time <= 0:
            return 0.0
        
        improvement = ((cpu_time - gpu_time) / cpu_time) * 100
        return round(improvement, 1)
    
    def _analyze_overhead(self, speedup: float, num_processes: int) -> Dict[str, Any]:
        """Analyze multiprocessing overhead for educational insights."""
        theoretical_max = num_processes
        efficiency = speedup / theoretical_max
        overhead_factor = 1.0 - efficiency
        
        return {
            "theoretical_max_speedup": theoretical_max,
            "actual_speedup": speedup,
            "efficiency": round(efficiency, 3),
            "overhead_factor": round(overhead_factor, 3),
            "overhead_percentage": round(overhead_factor * 100, 1)
        }
    
    def _generate_educational_insights(self, speedup: float, operation: str, dataset_size: int) -> List[str]:
        """Generate educational insights about the performance results."""
        insights = []
        
        if speedup > 1.0:
            insights.append(f"Parallel processing achieved {speedup:.1f}x speedup!")
        else:
            insights.append("Sequential processing was faster due to overhead.")
        
        if operation == "matrix_multiply" and speedup > 2.0:
            insights.append("Matrix multiplication benefits greatly from parallelization.")
        
        if dataset_size < 10000 and speedup < 1.5:
            insights.append("Small datasets may not justify parallel processing overhead.")
        
        if dataset_size >= 100000 and speedup > 3.0:
            insights.append("Large datasets show excellent parallel scaling.")
        
        return insights
    
    def _analyze_scaling_trend(self, sizes: List[int], speedups: List[float]) -> str:
        """Analyze the trend in speedup as dataset size increases."""
        if len(sizes) < 2:
            return "Insufficient data"
        
        # Simple trend analysis
        first_half_avg = statistics.mean(speedups[:len(speedups)//2])
        second_half_avg = statistics.mean(speedups[len(speedups)//2:])
        
        if second_half_avg > first_half_avg * 1.1:
            return "Improving"
        elif second_half_avg < first_half_avg * 0.9:
            return "Declining"
        else:
            return "Stable"
    
    def _find_optimal_dataset_size(self, history: List[PerformanceMetrics]) -> Optional[int]:
        """Find the dataset size with the best speedup."""
        if not history:
            return None
        
        best_metric = max(history, key=lambda x: x.speedup_ratio)
        return best_metric.dataset_size
    
    def clear_history(self):
        """Clear performance history and cache."""
        self.performance_history.clear()
        self.analysis_cache.clear()
    
    def export_results(self, format_type: str = "dict") -> Any:
        """
        Export performance results in various formats for further analysis.
        
        Args:
            format_type: Export format ("dict", "csv_data")
            
        Returns:
            Exported data in requested format
        """
        if format_type == "dict":
            return {
                "performance_history": self.get_performance_history(),
                "summary_statistics": self.get_summary_statistics(),
                "export_timestamp": datetime.now().isoformat()
            }
        elif format_type == "csv_data":
            # Return data suitable for CSV export
            return [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "operation": m.operation,
                    "dataset_size": m.dataset_size,
                    "cpu_time": m.cpu_time,
                    "gpu_time": m.gpu_time,
                    "speedup": m.speedup_ratio,
                    "num_processes": m.num_processes
                }
                for m in self.performance_history
            ]
        else:
            raise ValueError(f"Unsupported export format: {format_type}")