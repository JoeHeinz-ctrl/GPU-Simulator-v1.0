"""
COA Modules Package
Computer Organization and Architecture demonstration modules

This package contains modules demonstrating all 5 Course Outcomes (COs):
- CO1: Instruction Cycle Simulation
- CO2: Performance Evaluation
- CO3: Interrupt Handling
- CO4: I/O Interfacing
- CO5: GPU Architecture
"""

from .co1_instruction_cycle import InstructionCycleSimulator, Instruction, demonstrate_instruction_cycle
from .co2_performance_evaluation import PerformanceEvaluator, PerformanceMetrics, demonstrate_performance_evaluation
from .co3_interrupt_handling import InterruptHandler, simulate_computation_with_interrupts
from .co4_io_interfacing import IOInterfaceSimulator, demonstrate_io_interfacing
from .co5_gpu_architecture import GPUArchitectureSimulator, demonstrate_gpu_architecture

__all__ = [
    'InstructionCycleSimulator',
    'Instruction',
    'demonstrate_instruction_cycle',
    'PerformanceEvaluator',
    'PerformanceMetrics',
    'demonstrate_performance_evaluation',
    'InterruptHandler',
    'simulate_computation_with_interrupts',
    'IOInterfaceSimulator',
    'demonstrate_io_interfacing',
    'GPUArchitectureSimulator',
    'demonstrate_gpu_architecture',
]
