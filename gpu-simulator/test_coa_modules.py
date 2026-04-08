"""
Test script to verify all COA modules are working correctly
Run this before viva to ensure everything is functional
"""

import sys
import traceback


def test_module(module_name, test_func):
    """Test a single module"""
    print(f"\n{'='*70}")
    print(f"Testing: {module_name}")
    print(f"{'='*70}")
    try:
        test_func()
        print(f"✓ {module_name} - PASSED")
        return True
    except Exception as e:
        print(f"✗ {module_name} - FAILED")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return False


def test_co1():
    """Test CO1: Instruction Cycle"""
    from coa_modules.co1_instruction_cycle import InstructionCycleSimulator, Instruction
    
    sim = InstructionCycleSimulator(verbose=False)
    program = [
        Instruction("ADD", 10.0, 20.0),
        Instruction("MUL", 5.0, 3.0),
    ]
    sim.load_program(program)
    results = sim.run_program()
    
    assert len(results) == 2, "Should execute 2 instructions"
    assert results[0] == 30.0, "ADD result should be 30.0"
    assert results[1] == 15.0, "MUL result should be 15.0"
    print("  - Instruction cycle working correctly")
    print(f"  - Executed {len(results)} instructions")


def test_co2():
    """Test CO2: Performance Evaluation"""
    from coa_modules.co2_performance_evaluation import PerformanceEvaluator
    
    evaluator = PerformanceEvaluator(verbose=False)
    metrics = evaluator.compare_cpu_gpu(0.1, 0.02, "ADD", 10000, 8)
    
    assert metrics.speedup > 0, "Speedup should be positive"
    assert metrics.efficiency > 0, "Efficiency should be positive"
    print(f"  - Performance evaluation working correctly")
    print(f"  - Speedup: {metrics.speedup:.2f}x")
    print(f"  - Efficiency: {metrics.efficiency:.2f}%")


def test_co3():
    """Test CO3: Interrupt Handling"""
    from coa_modules.co3_interrupt_handling import InterruptHandler
    
    handler = InterruptHandler(verbose=False)
    
    def test_isr(data):
        return "handled"
    
    handler.register_interrupt_handler("TEST", test_isr)
    handler.trigger_interrupt("TEST", None)
    
    state = {'pc': 0, 'accumulator': 0.0, 'registers': {}}
    results = handler.process_interrupts(state)
    
    assert len(results) == 1, "Should handle 1 interrupt"
    assert results[0] == "handled", "ISR should return 'handled'"
    print("  - Interrupt handling working correctly")
    print(f"  - Interrupts handled: {handler.interrupts_handled}")


def test_co4():
    """Test CO4: I/O Interfacing"""
    from coa_modules.co4_io_interfacing import IOInterfaceSimulator
    
    io_sim = IOInterfaceSimulator(verbose=False)
    
    # Test disk I/O
    io_sim.write_to_disk("test.dat", "test data")
    data = io_sim.read_from_disk("test.dat", 100)
    
    assert data is not None, "Should read data from disk"
    
    # Test DMA
    io_sim.perform_dma_transfer("DISK", "MEMORY", "test data")
    
    stats = io_sim.get_io_statistics()
    assert stats['disk']['requests_processed'] >= 2, "Should process disk requests"
    assert stats['dma_transfers'] >= 1, "Should perform DMA transfer"
    
    print("  - I/O interfacing working correctly")
    print(f"  - Disk operations: {stats['disk']['requests_processed']}")
    print(f"  - DMA transfers: {stats['dma_transfers']}")


def test_co5():
    """Test CO5: GPU Architecture"""
    import numpy as np
    from coa_modules.co5_gpu_architecture import GPUArchitectureSimulator
    
    gpu = GPUArchitectureSimulator(verbose=False)
    
    # Create test data
    data_a = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float32)
    data_b = np.array([2.0, 2.0, 2.0, 2.0, 2.0], dtype=np.float32)
    
    # Create grid
    grid = gpu.create_grid(len(data_a), threads_per_block=2)
    assert grid.grid_size > 0, "Should create grid"
    
    # Execute kernel
    result, exec_time = gpu.execute_kernel_parallel(data_a, data_b, "ADD")
    
    expected = np.array([3.0, 4.0, 5.0, 6.0, 7.0], dtype=np.float32)
    assert np.allclose(result, expected), "Results should match expected"
    assert exec_time > 0, "Execution time should be positive"
    
    print("  - GPU architecture working correctly")
    print(f"  - Grid size: {grid.grid_size} blocks")
    print(f"  - Execution time: {exec_time:.6f}s")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("COA MODULES TEST SUITE")
    print("="*70)
    print("\nTesting all 5 Course Outcome modules...")
    
    tests = [
        ("CO1: Instruction Cycle", test_co1),
        ("CO2: Performance Evaluation", test_co2),
        ("CO3: Interrupt Handling", test_co3),
        ("CO4: I/O Interfacing", test_co4),
        ("CO5: GPU Architecture", test_co5),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_module(name, test_func)
        results.append((name, result))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:<40} {status}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Project is ready for viva.")
        print("="*70)
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix errors before viva.")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
