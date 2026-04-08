"""
INTEGRATED COA DEMONSTRATION
GPU Parallel Floating-Point Simulator with Complete COA Coverage

This is the main demonstration file that integrates all 5 Course Outcomes:
CO1: Instruction Cycle Simulation
CO2: Performance Evaluation
CO3: Interrupt Handling
CO4: I/O Interfacing
CO5: GPU Architecture

Author: COA Project
Purpose: Viva Demonstration - Complete COA Concepts
"""

import numpy as np
import time
from coa_modules import (
    InstructionCycleSimulator, Instruction,
    PerformanceEvaluator,
    InterruptHandler,
    IOInterfaceSimulator,
    GPUArchitectureSimulator
)


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"{title:^80}")
    print("="*80)


def print_section(title: str):
    """Print formatted subsection"""
    print("\n" + "-"*80)
    print(f"{title}")
    print("-"*80)


def integrated_demonstration():
    """
    Main integrated demonstration showing all COs working together
    """
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "GPU PARALLEL FLOATING-POINT SIMULATOR".center(78) + "█")
    print("█" + "Complete COA Demonstration (CO1-CO5)".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    print("\n" + "="*80)
    print("COURSE OUTCOMES COVERAGE")
    print("="*80)
    print("✓ CO1: Instruction Cycle Simulation (Fetch-Decode-Execute)")
    print("✓ CO2: Performance Evaluation (CPU vs GPU Comparison)")
    print("✓ CO3: Interrupt Handling (ISR and Context Switching)")
    print("✓ CO4: I/O Interfacing (Input/Output Device Simulation)")
    print("✓ CO5: GPU Architecture (Parallel Processing)")
    print("="*80)
    
    # ========================================================================
    # CO4: I/O INTERFACING - Get user input
    # ========================================================================
    print_header("CO4: I/O INTERFACING - USER INPUT")
    
    io_sim = IOInterfaceSimulator(verbose=True)
    
    print("\nPlease provide simulation parameters:")
    dataset_size_input = io_sim.get_user_input("Enter dataset size (e.g., 10000)")
    operation_input = io_sim.get_user_input("Enter operation (ADD/MUL/SUB/DIV)")
    
    try:
        dataset_size = int(dataset_size_input)
    except:
        dataset_size = 10000
        print(f"Using default dataset size: {dataset_size}")
    
    operation = operation_input.upper() if operation_input.upper() in ["ADD", "MUL", "SUB", "DIV"] else "ADD"
    
    # Display configuration
    config_output = f"""
╔══════════════════════════════════════════════════════════════╗
║              SIMULATION CONFIGURATION                        ║
╠══════════════════════════════════════════════════════════════╣
║  Dataset Size: {dataset_size:>10,} elements                      ║
║  Operation:    {operation:<10}                                  ║
║  Mode:         CPU vs GPU Parallel Comparison                ║
╚══════════════════════════════════════════════════════════════╝
"""
    io_sim.display_output(config_output)
    
    # ========================================================================
    # CO1: INSTRUCTION CYCLE SIMULATION
    # ========================================================================
    print_header("CO1: INSTRUCTION CYCLE SIMULATION")
    
    print("\nSimulating instruction cycle for floating-point operations...")
    print("Demonstrating: Fetch → Decode → Execute cycle")
    
    # Create instruction simulator
    instruction_sim = InstructionCycleSimulator(verbose=True)
    
    # Create sample program with floating-point instructions
    sample_program = [
        Instruction(operation, 10.5, 20.3),
        Instruction(operation, 5.0, 3.0),
        Instruction(operation, 100.0, 25.5),
    ]
    
    instruction_sim.load_program(sample_program)
    instruction_results = instruction_sim.run_program()
    
    print(f"\n✓ Instruction cycle demonstration completed")
    print(f"  Total instructions executed: {len(instruction_results)}")
    
    # ========================================================================
    # CO5: GPU ARCHITECTURE - Setup parallel processing
    # ========================================================================
    print_header("CO5: GPU ARCHITECTURE - PARALLEL PROCESSING SETUP")
    
    print("\nInitializing GPU-style parallel architecture...")
    
    # Create GPU simulator
    gpu_sim = GPUArchitectureSimulator(verbose=True)
    
    # Create grid structure
    gpu_sim.create_grid(dataset_size, threads_per_block=256)
    gpu_sim.visualize_thread_blocks()
    gpu_sim.show_memory_hierarchy()
    
    # ========================================================================
    # CO2: PERFORMANCE EVALUATION - Prepare measurement
    # ========================================================================
    print_header("CO2: PERFORMANCE EVALUATION - SETUP")
    
    print("\nInitializing performance measurement system...")
    perf_eval = PerformanceEvaluator(verbose=True)
    
    # Generate test data
    print(f"\nGenerating test data: {dataset_size:,} floating-point numbers...")
    np.random.seed(42)
    data_a = np.random.rand(dataset_size).astype(np.float32)
    data_b = np.random.rand(dataset_size).astype(np.float32)
    print(f"✓ Test data generated")
    
    # ========================================================================
    # CO3: INTERRUPT HANDLING - Setup interrupt system
    # ========================================================================
    print_header("CO3: INTERRUPT HANDLING - SETUP")
    
    print("\nInitializing interrupt handling system...")
    interrupt_handler = InterruptHandler(verbose=True)
    
    # Register interrupt handlers
    def computation_interrupt_handler(data):
        print(f"\n  [ISR] Computation checkpoint interrupt")
        print(f"  [ISR] Saving intermediate results...")
        time.sleep(0.1)
        print(f"  [ISR] Checkpoint saved")
        return "Checkpoint completed"
    
    def memory_interrupt_handler(data):
        print(f"\n  [ISR] Memory management interrupt")
        print(f"  [ISR] Optimizing memory allocation...")
        time.sleep(0.1)
        print(f"  [ISR] Memory optimized")
        return "Memory managed"
    
    interrupt_handler.register_interrupt_handler("CHECKPOINT", computation_interrupt_handler)
    interrupt_handler.register_interrupt_handler("MEMORY", memory_interrupt_handler)
    
    # ========================================================================
    # EXECUTION PHASE - CPU Computation
    # ========================================================================
    print_header("EXECUTION PHASE: CPU SEQUENTIAL PROCESSING")
    
    print("\nExecuting CPU sequential computation...")
    print(f"Operation: {operation}")
    print(f"Data size: {dataset_size:,} elements")
    
    cpu_state = {'pc': 0, 'accumulator': 0.0, 'registers': {}}
    
    def cpu_compute(a, b, op):
        """CPU sequential computation"""
        if op == "ADD":
            return a + b
        elif op == "MUL":
            return a * b
        elif op == "SUB":
            return a - b
        elif op == "DIV":
            return np.divide(a, b, where=b!=0, out=np.zeros_like(a))
        return a + b
    
    # Measure CPU time
    cpu_result, cpu_time = perf_eval.measure_execution_time(cpu_compute, data_a, data_b, operation)
    
    print(f"\n✓ CPU computation completed")
    print(f"  Execution time: {cpu_time:.6f} seconds")
    print(f"  Sample results: {cpu_result[:5]}")
    
    # Trigger interrupt during computation
    print("\n⚡ Simulating interrupt during computation...")
    interrupt_handler.trigger_interrupt("CHECKPOINT", "cpu_computation")
    interrupt_handler.process_interrupts(cpu_state)
    
    # ========================================================================
    # EXECUTION PHASE - GPU Parallel Computation
    # ========================================================================
    print_header("EXECUTION PHASE: GPU PARALLEL PROCESSING")
    
    print("\nExecuting GPU parallel computation...")
    print(f"Operation: {operation}")
    print(f"Data size: {dataset_size:,} elements")
    print(f"Parallel cores: {gpu_sim.num_cores}")
    
    # Measure GPU time
    gpu_result, gpu_time = gpu_sim.execute_kernel_parallel(data_a, data_b, operation)
    
    print(f"\n✓ GPU computation completed")
    print(f"  Execution time: {gpu_time:.6f} seconds")
    print(f"  Sample results: {gpu_result[:5]}")
    
    # Trigger interrupt after GPU computation
    print("\n⚡ Simulating memory management interrupt...")
    interrupt_handler.trigger_interrupt("MEMORY", "gpu_memory")
    interrupt_handler.process_interrupts(cpu_state)
    
    # ========================================================================
    # CO2: PERFORMANCE EVALUATION - Analysis
    # ========================================================================
    print_header("CO2: PERFORMANCE EVALUATION - ANALYSIS")
    
    print("\nAnalyzing performance metrics...")
    
    # Compare performance
    metrics = perf_eval.compare_cpu_gpu(
        cpu_time, gpu_time, operation, dataset_size, gpu_sim.num_cores
    )
    
    # Calculate additional metrics
    throughput = perf_eval.calculate_throughput(dataset_size, gpu_time)
    latency = perf_eval.calculate_latency(gpu_time, dataset_size)
    
    # Verify results
    print("\n[RESULT VERIFICATION]")
    results_match = np.allclose(cpu_result, gpu_result, rtol=1e-5)
    print(f"  CPU and GPU results match: {results_match}")
    if not results_match:
        max_diff = np.max(np.abs(cpu_result - gpu_result))
        print(f"  Maximum difference: {max_diff}")
    
    # ========================================================================
    # CO4: I/O INTERFACING - Output results
    # ========================================================================
    print_header("CO4: I/O INTERFACING - RESULTS OUTPUT")
    
    print("\nWriting results to output devices...")
    
    # Display results
    results_output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SIMULATION RESULTS                        ║
╠══════════════════════════════════════════════════════════════╣
║  Operation:        {operation:<10}                              ║
║  Dataset Size:     {dataset_size:>10,} elements                  ║
║                                                              ║
║  CPU Time:         {cpu_time:>10.6f} seconds                    ║
║  GPU Time:         {gpu_time:>10.6f} seconds                    ║
║  Speedup:          {metrics.speedup:>10.2f}x                        ║
║  Efficiency:       {metrics.efficiency:>10.2f}%                        ║
║                                                              ║
║  Throughput:       {throughput:>10,.0f} ops/sec                  ║
║  Latency:          {latency:>10.3f} μs/op                       ║
║                                                              ║
║  Performance Gain: {((cpu_time-gpu_time)/cpu_time*100):>10.2f}%                        ║
╚══════════════════════════════════════════════════════════════╝
"""
    io_sim.display_output(results_output)
    
    # Save to disk
    results_data = {
        'operation': operation,
        'dataset_size': dataset_size,
        'cpu_time': cpu_time,
        'gpu_time': gpu_time,
        'speedup': metrics.speedup,
        'efficiency': metrics.efficiency
    }
    io_sim.write_to_disk("simulation_results.dat", str(results_data))
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_header("DEMONSTRATION SUMMARY")
    
    print("\n✓ All Course Outcomes Successfully Demonstrated:")
    print("\n  CO1: Instruction Cycle")
    print(f"      • Executed {len(instruction_results)} instructions")
    print(f"      • Demonstrated Fetch-Decode-Execute cycle")
    
    print("\n  CO2: Performance Evaluation")
    print(f"      • CPU Time: {cpu_time:.6f}s")
    print(f"      • GPU Time: {gpu_time:.6f}s")
    print(f"      • Speedup: {metrics.speedup:.2f}x")
    print(f"      • Efficiency: {metrics.efficiency:.2f}%")
    
    print("\n  CO3: Interrupt Handling")
    stats = interrupt_handler.get_statistics()
    print(f"      • Interrupts handled: {stats['interrupts_handled']}")
    print(f"      • Context switches performed")
    print(f"      • ISR execution demonstrated")
    
    print("\n  CO4: I/O Interfacing")
    io_stats = io_sim.get_io_statistics()
    print(f"      • Input operations: {io_stats['keyboard']['requests_processed']}")
    print(f"      • Output operations: {io_stats['display']['requests_processed']}")
    print(f"      • Disk I/O operations: {io_stats['disk']['requests_processed']}")
    print(f"      • DMA transfers: {io_stats['dma_transfers']}")
    
    print("\n  CO5: GPU Architecture")
    gpu_metrics = gpu_sim.get_performance_metrics()
    print(f"      • Grid size: {gpu_metrics['grid_size']} blocks")
    print(f"      • Block size: {gpu_metrics['block_size']} threads")
    print(f"      • Parallel execution demonstrated")
    print(f"      • Memory hierarchy explained")
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nAll COA concepts have been demonstrated with working code.")
    print("This project is ready for viva presentation.")
    print("="*80 + "\n")


def quick_demo():
    """Quick demonstration without user input (for testing)"""
    print("\n" + "="*80)
    print("QUICK DEMONSTRATION MODE (No User Input Required)")
    print("="*80)
    
    # Use default values
    dataset_size = 10000
    operation = "ADD"
    
    print(f"\nUsing default configuration:")
    print(f"  Dataset Size: {dataset_size:,}")
    print(f"  Operation: {operation}")
    
    # Generate data
    np.random.seed(42)
    data_a = np.random.rand(dataset_size).astype(np.float32)
    data_b = np.random.rand(dataset_size).astype(np.float32)
    
    # CO1: Instruction Cycle
    print_header("CO1: INSTRUCTION CYCLE")
    from coa_modules.co1_instruction_cycle import demonstrate_instruction_cycle
    demonstrate_instruction_cycle()
    
    # CO2: Performance Evaluation
    print_header("CO2: PERFORMANCE EVALUATION")
    from coa_modules.co2_performance_evaluation import demonstrate_performance_evaluation
    demonstrate_performance_evaluation()
    
    # CO3: Interrupt Handling
    print_header("CO3: INTERRUPT HANDLING")
    from coa_modules.co3_interrupt_handling import simulate_computation_with_interrupts
    simulate_computation_with_interrupts()
    
    # CO4: I/O Interfacing (skip user input)
    print_header("CO4: I/O INTERFACING")
    print("\n(Skipping interactive input in quick demo mode)")
    
    # CO5: GPU Architecture
    print_header("CO5: GPU ARCHITECTURE")
    from coa_modules.co5_gpu_architecture import demonstrate_gpu_architecture
    demonstrate_gpu_architecture()
    
    print("\n" + "="*80)
    print("QUICK DEMONSTRATION COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*80)
    print("GPU PARALLEL FLOATING-POINT SIMULATOR")
    print("Complete COA Demonstration (CO1-CO5)")
    print("="*80)
    print("\nSelect demonstration mode:")
    print("1. Full Integrated Demo (with user input)")
    print("2. Quick Demo (no user input, all COs)")
    print("="*80)
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        quick_demo()
    else:
        integrated_demonstration()
