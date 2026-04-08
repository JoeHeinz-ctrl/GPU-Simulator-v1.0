"""
CO5: GPU Architecture Simulation (Enhanced)
Demonstrates: Parallel processing architecture similar to GPU

This module simulates GPU-style parallel architecture:
1. Thread blocks and grids
2. Shared memory
3. Thread synchronization
4. Parallel execution model
5. Memory hierarchy
"""

import multiprocessing as mp
import numpy as np
import time
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class ThreadBlock:
    """Represents a GPU thread block"""
    block_id: int
    thread_count: int
    data_start: int
    data_end: int
    shared_memory: Dict[str, Any] = None


@dataclass
class GPUGrid:
    """Represents GPU grid structure"""
    grid_size: int  # Number of blocks
    block_size: int  # Threads per block
    total_threads: int
    blocks: List[ThreadBlock] = None


class GPUArchitectureSimulator:
    """
    Simulates GPU parallel architecture
    
    COA Concept Mapping:
    - Thread Blocks: Groups of threads that execute together
    - Grid: Collection of thread blocks
    - Shared Memory: Fast memory shared within a block
    - Global Memory: Main GPU memory accessible by all threads
    - Thread Synchronization: Coordination between threads
    - SIMD: Single Instruction Multiple Data execution
    """
    
    def __init__(self, num_cores: int = None, verbose: bool = True):
        self.num_cores = num_cores or mp.cpu_count()
        self.verbose = verbose
        self.grid = None
        self.execution_log = []
    
    def create_grid(self, data_size: int, threads_per_block: int = 256) -> GPUGrid:
        """
        Create GPU grid structure
        
        COA Concept: Grid and Block organization
        Similar to CUDA grid/block hierarchy
        """
        # Calculate grid dimensions
        num_blocks = (data_size + threads_per_block - 1) // threads_per_block
        total_threads = num_blocks * threads_per_block
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"GPU GRID CONFIGURATION")
            print(f"{'='*60}")
            print(f"  Data Size: {data_size:,} elements")
            print(f"  Threads per Block: {threads_per_block}")
            print(f"  Number of Blocks: {num_blocks}")
            print(f"  Total Threads: {total_threads:,}")
            print(f"  Available CPU Cores: {self.num_cores}")
            print(f"{'='*60}")
        
        # Create thread blocks
        blocks = []
        for block_id in range(num_blocks):
            data_start = block_id * threads_per_block
            data_end = min(data_start + threads_per_block, data_size)
            
            block = ThreadBlock(
                block_id=block_id,
                thread_count=data_end - data_start,
                data_start=data_start,
                data_end=data_end,
                shared_memory={}
            )
            blocks.append(block)
        
        self.grid = GPUGrid(
            grid_size=num_blocks,
            block_size=threads_per_block,
            total_threads=total_threads,
            blocks=blocks
        )
        
        return self.grid
    
    def visualize_thread_blocks(self):
        """
        Visualize thread block structure
        
        COA Concept: Thread hierarchy visualization
        """
        if not self.grid:
            print("No grid created yet")
            return
        
        print(f"\n{'='*60}")
        print(f"THREAD BLOCK VISUALIZATION")
        print(f"{'='*60}")
        
        # Show grid structure
        print(f"\nGrid Structure:")
        print(f"  ┌{'─'*50}┐")
        print(f"  │ Grid (Size: {self.grid.grid_size} blocks)".ljust(51) + "│")
        print(f"  ├{'─'*50}┤")
        
        for i, block in enumerate(self.grid.blocks[:10]):  # Show first 10 blocks
            print(f"  │ Block {block.block_id}: Threads[{block.data_start}:{block.data_end}] ({block.thread_count} threads)".ljust(51) + "│")
        
        if len(self.grid.blocks) > 10:
            print(f"  │ ... ({len(self.grid.blocks) - 10} more blocks)".ljust(51) + "│")
        
        print(f"  └{'─'*50}┘")
        
        # Show thread-to-data mapping
        print(f"\nThread-to-Data Mapping:")
        print(f"  Each thread processes one data element")
        print(f"  Threads execute in parallel within blocks")
        print(f"  Blocks execute independently")
        
        # Visual representation
        print(f"\n  Visual Representation (first 5 blocks):")
        for i, block in enumerate(self.grid.blocks[:5]):
            threads_visual = "█" * min(block.thread_count // 10, 40)
            print(f"  Block {i}: [{threads_visual}] {block.thread_count} threads")
        
        print(f"{'='*60}")
    
    def execute_kernel_parallel(self, data_a: np.ndarray, data_b: np.ndarray, 
                                operation: str) -> Tuple[np.ndarray, float]:
        """
        Execute parallel kernel (GPU-style)
        
        COA Concept: Parallel kernel execution
        SIMD: Single Instruction Multiple Data
        """
        if not self.grid:
            self.create_grid(len(data_a))
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"LAUNCHING GPU KERNEL")
            print(f"{'='*60}")
            print(f"  Operation: {operation}")
            print(f"  Grid Size: {self.grid.grid_size} blocks")
            print(f"  Block Size: {self.grid.block_size} threads")
            print(f"  Execution Model: SIMD (Single Instruction Multiple Data)")
            print(f"{'='*60}")
        
        start_time = time.perf_counter()
        
        # Create process pool (simulates GPU cores)
        with mp.Pool(processes=self.num_cores) as pool:
            # Prepare work for each block
            tasks = []
            for block in self.grid.blocks:
                task = (
                    data_a[block.data_start:block.data_end],
                    data_b[block.data_start:block.data_end],
                    operation,
                    block.block_id
                )
                tasks.append(task)
            
            if self.verbose:
                print(f"\n[KERNEL EXECUTION]")
                print(f"  Distributing {len(tasks)} blocks across {self.num_cores} cores")
            
            # Execute in parallel (simulates GPU parallel execution)
            results = pool.starmap(self._execute_block, tasks)
        
        # Combine results
        result = np.concatenate([r[0] for r in results])
        
        execution_time = time.perf_counter() - start_time
        
        if self.verbose:
            print(f"  ✓ Kernel execution completed")
            print(f"  Execution Time: {execution_time:.6f} seconds")
            print(f"{'='*60}")
        
        # Log execution
        self.execution_log.append({
            'operation': operation,
            'data_size': len(data_a),
            'num_blocks': self.grid.grid_size,
            'execution_time': execution_time
        })
        
        return result, execution_time
    
    @staticmethod
    def _execute_block(block_data_a: np.ndarray, block_data_b: np.ndarray, 
                      operation: str, block_id: int) -> Tuple[np.ndarray, int]:
        """
        Execute computation for a single thread block
        
        COA Concept: Thread block execution
        Each block processes its assigned data chunk
        """
        # Simulate thread block execution
        if operation == "ADD":
            result = block_data_a + block_data_b
        elif operation == "MUL":
            result = block_data_a * block_data_b
        elif operation == "SUB":
            result = block_data_a - block_data_b
        elif operation == "DIV":
            result = np.divide(block_data_a, block_data_b, 
                             where=block_data_b!=0, out=np.zeros_like(block_data_a))
        else:
            result = block_data_a + block_data_b
        
        return result, block_id
    
    def show_memory_hierarchy(self):
        """
        Display GPU memory hierarchy
        
        COA Concept: Memory hierarchy in GPU
        """
        print(f"\n{'='*60}")
        print(f"GPU MEMORY HIERARCHY")
        print(f"{'='*60}")
        print(f"""
  ┌─────────────────────────────────────────────┐
  │         REGISTERS (Fastest)                 │
  │         - Per-thread private memory         │
  │         - Lowest latency                    │
  └─────────────────────────────────────────────┘
                    ↓
  ┌─────────────────────────────────────────────┐
  │         SHARED MEMORY                       │
  │         - Per-block shared memory           │
  │         - Fast, low latency                 │
  │         - Thread synchronization            │
  └─────────────────────────────────────────────┘
                    ↓
  ┌─────────────────────────────────────────────┐
  │         GLOBAL MEMORY                       │
  │         - Accessible by all threads         │
  │         - Larger capacity                   │
  │         - Higher latency                    │
  └─────────────────────────────────────────────┘
                    ↓
  ┌─────────────────────────────────────────────┐
  │         HOST MEMORY (CPU RAM)               │
  │         - Highest capacity                  │
  │         - Highest latency                   │
  └─────────────────────────────────────────────┘
        """)
        print(f"{'='*60}")
    
    def get_performance_metrics(self) -> Dict:
        """Get GPU performance metrics"""
        if not self.execution_log:
            return {}
        
        total_time = sum(log['execution_time'] for log in self.execution_log)
        avg_time = total_time / len(self.execution_log)
        
        return {
            'total_kernels_executed': len(self.execution_log),
            'total_execution_time': total_time,
            'average_execution_time': avg_time,
            'grid_size': self.grid.grid_size if self.grid else 0,
            'block_size': self.grid.block_size if self.grid else 0
        }


def demonstrate_gpu_architecture():
    """
    Demonstration function for CO5
    Shows GPU architecture and parallel execution
    """
    print("\n" + "="*70)
    print("CO5 DEMONSTRATION: GPU ARCHITECTURE SIMULATION")
    print("="*70)
    print("\nCOA Concepts Demonstrated:")
    print("• Thread Blocks and Grid Organization")
    print("• Parallel Execution Model (SIMD)")
    print("• Thread-to-Data Mapping")
    print("• Memory Hierarchy")
    print("• Shared Memory")
    print("• Parallel Kernel Execution")
    print("="*70)
    
    # Create GPU simulator
    gpu = GPUArchitectureSimulator(verbose=True)
    
    # Create sample data
    data_size = 10000
    data_a = np.random.rand(data_size).astype(np.float32)
    data_b = np.random.rand(data_size).astype(np.float32)
    
    # 1. Create and visualize grid
    print("\n" + "="*70)
    print("STEP 1: GRID CREATION")
    print("="*70)
    gpu.create_grid(data_size, threads_per_block=256)
    gpu.visualize_thread_blocks()
    
    # 2. Show memory hierarchy
    print("\n" + "="*70)
    print("STEP 2: MEMORY HIERARCHY")
    print("="*70)
    gpu.show_memory_hierarchy()
    
    # 3. Execute parallel kernel
    print("\n" + "="*70)
    print("STEP 3: PARALLEL KERNEL EXECUTION")
    print("="*70)
    result, exec_time = gpu.execute_kernel_parallel(data_a, data_b, "ADD")
    
    print(f"\n[RESULTS]")
    print(f"  Input Size: {data_size:,} elements")
    print(f"  Output Size: {len(result):,} elements")
    print(f"  Sample Results: {result[:5]}")
    print(f"  Execution Time: {exec_time:.6f} seconds")
    
    # 4. Performance metrics
    print("\n" + "="*70)
    print("STEP 4: PERFORMANCE METRICS")
    print("="*70)
    metrics = gpu.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    print("="*70)
    
    return gpu, result, exec_time


if __name__ == "__main__":
    demonstrate_gpu_architecture()
