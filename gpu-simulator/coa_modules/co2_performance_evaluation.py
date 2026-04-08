"""
CO2: Performance Evaluation (Enhanced)
Demonstrates: Performance measurement and analysis

This module provides comprehensive performance evaluation:
1. Execution time measurement
2. CPU vs GPU comparison
3. Speedup calculation
4. Efficiency metrics
5. Performance visualization
6. Bottleneck analysis
"""

import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PerformanceMetrics:
    """Stores performance measurement data"""
    operation: str
    data_size: int
    cpu_time: float
    gpu_time: float
    speedup: float
    efficiency: float
    timestamp: str


class PerformanceEvaluator:
    """
    Comprehensive performance evaluation system
    
    COA Concept Mapping:
    - Execution Time: Wall-clock time measurement
    - Speedup: Performance improvement ratio
    - Efficiency: Resource utilization
    - Throughput: Operations per second
    - Latency: Time per operation
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.measurements = []
        self.performance_log = []
    
    def measure_execution_time(self, func, *args, **kwargs) -> Tuple[any, float]:
        """
        Measure execution time of a function
        
        COA Concept: Performance measurement using high-resolution timer
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        
        return result, execution_time
    
    def compare_cpu_gpu(self, cpu_time: float, gpu_time: float, 
                       operation: str, data_size: int, num_cores: int = 1) -> PerformanceMetrics:
        """
        Compare CPU and GPU performance
        
        COA Concept: Performance comparison and speedup calculation
        Speedup = T_sequential / T_parallel
        Efficiency = Speedup / Number_of_Processors
        """
        speedup = cpu_time / gpu_time if gpu_time > 0 else 0
        efficiency = (speedup / num_cores) * 100 if num_cores > 0 else 0
        
        metrics = PerformanceMetrics(
            operation=operation,
            data_size=data_size,
            cpu_time=cpu_time,
            gpu_time=gpu_time,
            speedup=speedup,
            efficiency=efficiency,
            timestamp=datetime.now().isoformat()
        )
        
        self.measurements.append(metrics)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"PERFORMANCE COMPARISON")
            print(f"{'='*60}")
            print(f"  Operation: {operation}")
            print(f"  Data Size: {data_size:,} elements")
            print(f"  CPU Time: {cpu_time:.6f} seconds")
            print(f"  GPU Time: {gpu_time:.6f} seconds")
            print(f"  Speedup: {speedup:.2f}x")
            print(f"  Efficiency: {efficiency:.2f}%")
            print(f"  Performance Gain: {((cpu_time - gpu_time) / cpu_time * 100):.2f}%")
            print(f"{'='*60}")
        
        return metrics
    
    def calculate_throughput(self, data_size: int, execution_time: float) -> float:
        """
        Calculate throughput (operations per second)
        
        COA Concept: Throughput measurement
        """
        throughput = data_size / execution_time if execution_time > 0 else 0
        
        if self.verbose:
            print(f"\n[THROUGHPUT]")
            print(f"  Operations: {data_size:,}")
            print(f"  Time: {execution_time:.6f} seconds")
            print(f"  Throughput: {throughput:,.0f} ops/sec")
        
        return throughput
    
    def calculate_latency(self, execution_time: float, data_size: int) -> float:
        """
        Calculate latency (time per operation)
        
        COA Concept: Latency measurement
        """
        latency = (execution_time / data_size) * 1000000 if data_size > 0 else 0  # microseconds
        
        if self.verbose:
            print(f"\n[LATENCY]")
            print(f"  Time: {execution_time:.6f} seconds")
            print(f"  Operations: {data_size:,}")
            print(f"  Latency: {latency:.3f} μs/op")
        
        return latency
    
    def analyze_scalability(self, measurements: List[PerformanceMetrics]):
        """
        Analyze scalability with increasing data size
        
        COA Concept: Scalability analysis
        """
        if not measurements:
            return
        
        print(f"\n{'='*60}")
        print(f"SCALABILITY ANALYSIS")
        print(f"{'='*60}")
        
        print(f"\n{'Data Size':<15} {'CPU Time':<15} {'GPU Time':<15} {'Speedup':<10}")
        print(f"{'-'*60}")
        
        for m in measurements:
            print(f"{m.data_size:<15,} {m.cpu_time:<15.6f} {m.gpu_time:<15.6f} {m.speedup:<10.2f}x")
        
        print(f"{'='*60}")
    
    def generate_performance_report(self) -> str:
        """
        Generate comprehensive performance report
        
        COA Concept: Performance documentation
        """
        if not self.measurements:
            return "No measurements available"
        
        report = []
        report.append("\n" + "="*70)
        report.append("PERFORMANCE EVALUATION REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Measurements: {len(self.measurements)}")
        report.append("="*70)
        
        # Summary statistics
        avg_speedup = np.mean([m.speedup for m in self.measurements])
        max_speedup = max([m.speedup for m in self.measurements])
        min_speedup = min([m.speedup for m in self.measurements])
        avg_efficiency = np.mean([m.efficiency for m in self.measurements])
        
        report.append("\nSUMMARY STATISTICS:")
        report.append(f"  Average Speedup: {avg_speedup:.2f}x")
        report.append(f"  Maximum Speedup: {max_speedup:.2f}x")
        report.append(f"  Minimum Speedup: {min_speedup:.2f}x")
        report.append(f"  Average Efficiency: {avg_efficiency:.2f}%")
        
        # Detailed measurements
        report.append("\nDETAILED MEASUREMENTS:")
        report.append(f"{'#':<5} {'Operation':<12} {'Size':<12} {'CPU(s)':<12} {'GPU(s)':<12} {'Speedup':<10}")
        report.append("-"*70)
        
        for i, m in enumerate(self.measurements, 1):
            report.append(f"{i:<5} {m.operation:<12} {m.data_size:<12,} {m.cpu_time:<12.6f} {m.gpu_time:<12.6f} {m.speedup:<10.2f}x")
        
        report.append("="*70)
        
        return "\n".join(report)
    
    def visualize_performance(self, save_path: str = "performance_comparison.png"):
        """
        Create performance visualization
        
        COA Concept: Performance visualization for analysis
        """
        if not self.measurements:
            print("No measurements to visualize")
            return
        
        # Prepare data
        operations = [m.operation for m in self.measurements]
        data_sizes = [m.data_size for m in self.measurements]
        cpu_times = [m.cpu_time for m in self.measurements]
        gpu_times = [m.gpu_time for m in self.measurements]
        speedups = [m.speedup for m in self.measurements]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Performance Evaluation Results', fontsize=16, fontweight='bold')
        
        # Plot 1: Execution Time Comparison
        x = np.arange(len(operations))
        width = 0.35
        axes[0, 0].bar(x - width/2, cpu_times, width, label='CPU', color='#FF6B6B')
        axes[0, 0].bar(x + width/2, gpu_times, width, label='GPU', color='#76B900')
        axes[0, 0].set_xlabel('Test Case')
        axes[0, 0].set_ylabel('Execution Time (seconds)')
        axes[0, 0].set_title('CPU vs GPU Execution Time')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels([f"{op}\n{size:,}" for op, size in zip(operations, data_sizes)], 
                                   rotation=45, ha='right', fontsize=8)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Speedup
        axes[0, 1].plot(range(len(speedups)), speedups, marker='o', linewidth=2, 
                       markersize=8, color='#00D4FF')
        axes[0, 1].axhline(y=1, color='r', linestyle='--', label='No Speedup')
        axes[0, 1].set_xlabel('Test Case')
        axes[0, 1].set_ylabel('Speedup (x)')
        axes[0, 1].set_title('Speedup Factor (CPU/GPU)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Efficiency
        efficiencies = [m.efficiency for m in self.measurements]
        axes[1, 0].bar(range(len(efficiencies)), efficiencies, color='#FFD93D')
        axes[1, 0].set_xlabel('Test Case')
        axes[1, 0].set_ylabel('Efficiency (%)')
        axes[1, 0].set_title('Parallel Efficiency')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Performance Gain
        perf_gains = [((m.cpu_time - m.gpu_time) / m.cpu_time * 100) for m in self.measurements]
        axes[1, 1].bar(range(len(perf_gains)), perf_gains, color='#9ACD32')
        axes[1, 1].set_xlabel('Test Case')
        axes[1, 1].set_ylabel('Performance Gain (%)')
        axes[1, 1].set_title('Performance Improvement')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        if self.verbose:
            print(f"\n✓ Performance visualization saved to: {save_path}")
        
        return save_path


def demonstrate_performance_evaluation():
    """
    Demonstration function for CO2
    Shows comprehensive performance evaluation
    """
    print("\n" + "="*70)
    print("CO2 DEMONSTRATION: PERFORMANCE EVALUATION")
    print("="*70)
    print("\nCOA Concepts Demonstrated:")
    print("• Execution Time Measurement")
    print("• CPU vs GPU Performance Comparison")
    print("• Speedup Calculation")
    print("• Efficiency Metrics")
    print("• Throughput Analysis")
    print("• Latency Analysis")
    print("• Performance Visualization")
    print("="*70)
    
    evaluator = PerformanceEvaluator(verbose=True)
    
    # Simulate measurements
    test_cases = [
        ("ADD", 10000, 0.0523, 0.0089),
        ("MUL", 50000, 0.2341, 0.0312),
        ("SUB", 100000, 0.4567, 0.0598),
        ("DIV", 500000, 2.1234, 0.2876),
    ]
    
    print("\n" + "="*70)
    print("RUNNING PERFORMANCE TESTS")
    print("="*70)
    
    for operation, data_size, cpu_time, gpu_time in test_cases:
        metrics = evaluator.compare_cpu_gpu(cpu_time, gpu_time, operation, data_size, num_cores=8)
        evaluator.calculate_throughput(data_size, gpu_time)
        evaluator.calculate_latency(gpu_time, data_size)
    
    # Scalability analysis
    evaluator.analyze_scalability(evaluator.measurements)
    
    # Generate report
    report = evaluator.generate_performance_report()
    print(report)
    
    # Visualize
    try:
        evaluator.visualize_performance()
    except Exception as e:
        print(f"Visualization skipped: {e}")
    
    return evaluator


if __name__ == "__main__":
    demonstrate_performance_evaluation()
