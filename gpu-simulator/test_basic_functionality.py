"""
Basic functionality test for GPU Parallel Floating-Point Simulator
Tests core components to ensure they work correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import numpy as np
from app.workload_generator import WorkloadGenerator
from app.cpu_engine import CPUEngine
from app.parallel_engine import GPUSimulator
from app.performance import PerformanceAnalyzer

def test_workload_generator():
    """Test dataset generation"""
    print("Testing WorkloadGenerator...")
    generator = WorkloadGenerator()
    
    # Test dataset generation
    dataset = generator.generate_dataset(10000, "vector_add")
    assert dataset.size == 10000
    assert len(dataset.data) == 10000
    assert dataset.data.dtype == np.float64
    
    # Test vector pair generation
    vec_a, vec_b = generator.generate_vector_pair(10000)
    assert len(vec_a) == 10000
    assert len(vec_b) == 10000
    
    print("✓ WorkloadGenerator tests passed")

def test_cpu_engine():
    """Test CPU sequential processing"""
    print("Testing CPUEngine...")
    cpu = CPUEngine()
    
    # Create test data
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([2.0, 3.0, 4.0, 5.0])
    
    # Test vector addition
    result, time = cpu.vector_add(a, b)
    expected = np.array([3.0, 5.0, 7.0, 9.0])
    assert np.allclose(result, expected)
    assert time > 0
    
    # Test dot product
    result, time = cpu.dot_product(a, b)
    expected = 1*2 + 2*3 + 3*4 + 4*5  # 40
    assert abs(result - expected) < 1e-10
    
    print("✓ CPUEngine tests passed")

def test_gpu_simulator():
    """Test GPU parallel simulation"""
    print("Testing GPUSimulator...")
    gpu = GPUSimulator(num_processes=2)
    
    # Create test data
    a = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    b = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    
    # Test parallel vector addition
    result, time = gpu.vector_add_parallel(a, b)
    expected = np.array([3.0, 5.0, 7.0, 9.0, 11.0, 13.0])
    assert np.allclose(result, expected)
    assert time > 0
    
    # Test thread block info
    info = gpu.get_thread_block_info(10000)
    assert info.total_elements == 10000
    assert info.num_blocks > 0
    assert info.block_size > 0
    
    print("✓ GPUSimulator tests passed")

def test_performance_analyzer():
    """Test performance analysis"""
    print("Testing PerformanceAnalyzer...")
    analyzer = PerformanceAnalyzer()
    
    # Test speedup calculation
    speedup = analyzer.calculate_speedup(2.0, 1.0)
    assert speedup == 2.0
    
    # Test edge case handling
    speedup = analyzer.calculate_speedup(1.0, 0.0)
    assert speedup > 0  # Should handle zero GPU time
    
    print("✓ PerformanceAnalyzer tests passed")

def test_integration():
    """Test integration between components"""
    print("Testing component integration...")
    
    # Initialize components
    generator = WorkloadGenerator()
    cpu = CPUEngine()
    gpu = GPUSimulator(num_processes=2)
    analyzer = PerformanceAnalyzer()
    
    # Generate data (use supported size)
    vec_a, vec_b = generator.generate_vector_pair(10000)
    
    # Run CPU simulation
    cpu_result, cpu_time = cpu.vector_add(vec_a, vec_b)
    
    # Run GPU simulation
    gpu_result, gpu_time = gpu.vector_add_parallel(vec_a, vec_b)
    
    # Verify results match
    assert np.allclose(cpu_result, gpu_result, rtol=1e-10)
    
    # Analyze performance
    analysis = analyzer.analyze_results(
        (cpu_result, cpu_time), 
        (gpu_result, gpu_time),
        "vector_add", 
        10000, 
        2
    )
    
    assert "speedup" in analysis
    assert analysis["results_consistent"] == True
    
    print("✓ Integration tests passed")

if __name__ == "__main__":
    print("Running basic functionality tests...\n")
    
    try:
        test_workload_generator()
        test_cpu_engine()
        test_gpu_simulator()
        test_performance_analyzer()
        test_integration()
        
        print("\n🎉 All tests passed! The GPU Parallel Floating-Point Simulator is working correctly.")
        print("\nTo run the application:")
        print("1. cd gpu-simulator")
        print("2. pip install -r requirements.txt")
        print("3. uvicorn app.main:app --reload")
        print("4. Open http://localhost:8000 in your browser")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)