"""
API Routes for GPU Parallel Floating-Point Simulator
Handles all HTTP endpoints for the educational simulation system
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
import asyncio
import time
from io import BytesIO

from .models import (
    GenerateDataRequest, SimulationRequest, SimulationResponse,
    PerformanceHistoryResponse, ThreadBlockInfoResponse, ErrorResponse,
    PDFReportRequest, BenchmarkRequest, BenchmarkResults, OptimizationSuggestions
)
from .workload_generator import WorkloadGenerator
from .cpu_engine import CPUEngine
from .parallel_engine import GPUSimulator
from .performance import PerformanceAnalyzer
from .pdf_service import PDFExportService
from .benchmark_engine import BenchmarkEngine
from .optimization_service import OptimizationService

# Create API router
router = APIRouter()

# Global instances (in production, use dependency injection)
workload_generator = WorkloadGenerator()
cpu_engine = CPUEngine()
gpu_simulator = GPUSimulator()
performance_analyzer = PerformanceAnalyzer()
pdf_service = PDFExportService()
benchmark_engine = BenchmarkEngine()
optimization_service = OptimizationService()

# Global state for current dataset (in production, use proper state management)
current_datasets = {}
simulation_lock = asyncio.Lock()


@router.post("/generate-data", response_model=Dict[str, Any])
async def generate_data(request: GenerateDataRequest):
    """
    Generate floating-point dataset for computational operations.
    
    Creates random datasets of specified size for use in CPU and GPU simulations.
    Educational endpoint that demonstrates data preparation for parallel processing.
    
    Args:
        request: Dataset generation parameters
        
    Returns:
        Success status and dataset information
    """
    try:
        # Validate dataset size
        if request.size not in workload_generator.get_supported_sizes():
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported dataset size. Use one of: {workload_generator.get_supported_sizes()}"
            )
        
        # Generate dataset
        start_time = time.perf_counter()
        dataset = workload_generator.generate_dataset(request.size, request.operation_type)
        generation_time = time.perf_counter() - start_time
        
        # Validate generation time (educational requirement: < 5 seconds)
        if generation_time > 5.0:
            raise HTTPException(
                status_code=500,
                detail=f"Dataset generation took too long: {generation_time:.2f}s"
            )
        
        # Store dataset for subsequent operations
        dataset_key = f"{request.operation_type}_{request.size}"
        
        if request.operation_type == "matrix_multiply":
            # Generate matrix pair for matrix operations
            matrix_a, matrix_b = workload_generator.generate_matrix_pair(request.size)
            current_datasets[dataset_key] = {
                "type": "matrix_pair",
                "matrix_a": matrix_a,
                "matrix_b": matrix_b,
                "size": request.size,
                "operation": request.operation_type,
                "created_at": dataset.created_at
            }
        else:
            # Generate vector pair for vector operations
            vector_a, vector_b = workload_generator.generate_vector_pair(request.size)
            current_datasets[dataset_key] = {
                "type": "vector_pair", 
                "vector_a": vector_a,
                "vector_b": vector_b,
                "size": request.size,
                "operation": request.operation_type,
                "created_at": dataset.created_at
            }
        
        return {
            "success": True,
            "message": f"Dataset generated successfully",
            "dataset_size": request.size,
            "operation_type": request.operation_type,
            "generation_time": round(generation_time, 3),
            "memory_usage_mb": round(workload_generator.estimate_memory_usage(request.size), 2)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dataset generation failed: {str(e)}")


@router.post("/run-cpu-simulation", response_model=SimulationResponse)
async def run_cpu_simulation(request: SimulationRequest):
    """
    Execute floating-point operation using sequential CPU processing.
    
    Demonstrates traditional sequential processing for baseline performance
    measurement in educational parallel programming comparison.
    
    Args:
        request: Simulation parameters
        
    Returns:
        Simulation results with execution time and performance metrics
    """
    async with simulation_lock:  # Prevent concurrent simulations
        try:
            # Find dataset
            dataset_key = f"{request.operation}_{request.dataset_size}"
            if dataset_key not in current_datasets:
                raise HTTPException(
                    status_code=400,
                    detail="Dataset not found. Generate data first."
                )
            
            dataset = current_datasets[dataset_key]
            
            # Execute operation based on type
            if request.operation == "vector_add":
                result, exec_time = cpu_engine.vector_add(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Vector addition completed: {len(result)} elements"
                
            elif request.operation == "vector_multiply":
                result, exec_time = cpu_engine.vector_multiply(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Vector multiplication completed: {len(result)} elements"
                
            elif request.operation == "dot_product":
                result, exec_time = cpu_engine.dot_product(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Dot product result: {result:.6f}"
                
            elif request.operation == "matrix_multiply":
                result, exec_time = cpu_engine.matrix_multiply(dataset["matrix_a"], dataset["matrix_b"])
                result_summary = f"Matrix multiplication completed: {result.shape[0]}x{result.shape[1]} result"
                
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported operation: {request.operation}")
            
            # Store result for comparison
            current_datasets[dataset_key]["cpu_result"] = (result, exec_time)
            
            return SimulationResponse(
                success=True,
                execution_time=exec_time,
                result_summary=result_summary,
                performance_metrics={
                    "elements_per_second": round(request.dataset_size / exec_time, 0),
                    "operation": request.operation,
                    "engine": "cpu"
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"CPU simulation failed: {str(e)}")


@router.post("/run-gpu-simulation", response_model=SimulationResponse)
async def run_gpu_simulation(request: SimulationRequest):
    """
    Execute floating-point operation using parallel GPU simulation.
    
    Demonstrates parallel processing using multiprocessing to simulate
    GPU thread blocks for educational comparison with sequential CPU execution.
    
    Args:
        request: Simulation parameters
        
    Returns:
        Simulation results with execution time, performance metrics, and thread block info
    """
    async with simulation_lock:  # Prevent concurrent simulations
        try:
            # Find dataset
            dataset_key = f"{request.operation}_{request.dataset_size}"
            if dataset_key not in current_datasets:
                raise HTTPException(
                    status_code=400,
                    detail="Dataset not found. Generate data first."
                )
            
            dataset = current_datasets[dataset_key]
            
            # Configure GPU simulator
            if request.num_processes:
                gpu_sim = GPUSimulator(request.num_processes)
            else:
                gpu_sim = gpu_simulator
            
            # Execute operation based on type
            if request.operation == "vector_add":
                result, exec_time = gpu_sim.vector_add_parallel(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Parallel vector addition completed: {len(result)} elements"
                
            elif request.operation == "vector_multiply":
                result, exec_time = gpu_sim.vector_multiply_parallel(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Parallel vector multiplication completed: {len(result)} elements"
                
            elif request.operation == "dot_product":
                result, exec_time = gpu_sim.dot_product_parallel(dataset["vector_a"], dataset["vector_b"])
                result_summary = f"Parallel dot product result: {result:.6f}"
                
            elif request.operation == "matrix_multiply":
                result, exec_time = gpu_sim.matrix_multiply_parallel(dataset["matrix_a"], dataset["matrix_b"])
                result_summary = f"Parallel matrix multiplication completed: {result.shape[0]}x{result.shape[1]} result"
                
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported operation: {request.operation}")
            
            # Get thread block information for visualization
            thread_block_info = gpu_sim.get_thread_block_info(request.dataset_size)
            
            # Store result for comparison
            current_datasets[dataset_key]["gpu_result"] = (result, exec_time)
            
            # Perform comparison if CPU result exists
            performance_metrics = None
            if "cpu_result" in dataset:
                cpu_result = dataset["cpu_result"]
                gpu_result = (result, exec_time)
                
                analysis = performance_analyzer.analyze_results(
                    cpu_result, gpu_result, request.operation, 
                    request.dataset_size, gpu_sim.num_processes
                )
                performance_metrics = analysis
            
            return SimulationResponse(
                success=True,
                execution_time=exec_time,
                result_summary=result_summary,
                performance_metrics=performance_metrics,
                thread_block_info={
                    "num_blocks": thread_block_info.num_blocks,
                    "block_size": thread_block_info.block_size,
                    "total_elements": thread_block_info.total_elements,
                    "process_distribution": thread_block_info.process_distribution
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"GPU simulation failed: {str(e)}")


@router.get("/performance-history", response_model=PerformanceHistoryResponse)
async def get_performance_history():
    """
    Get historical performance data for visualization and analysis.
    
    Educational endpoint that provides performance metrics for charts
    and statistical analysis of parallel processing benefits.
    
    Returns:
        Performance history and summary statistics
    """
    try:
        history = performance_analyzer.get_performance_history()
        summary_stats = performance_analyzer.get_summary_statistics()
        
        return PerformanceHistoryResponse(
            history=history,
            summary_stats=summary_stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve performance history: {str(e)}")


@router.get("/thread-block-info")
async def get_thread_block_info(dataset_size: int = 10000):
    """
    Get thread block distribution information for visualization.
    
    Educational endpoint that shows how data is divided across
    simulated GPU thread blocks for parallel processing.
    
    Args:
        dataset_size: Size of dataset to analyze
        
    Returns:
        Thread block distribution information
    """
    try:
        if dataset_size not in workload_generator.get_supported_sizes():
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported dataset size. Use one of: {workload_generator.get_supported_sizes()}"
            )
        
        thread_info = gpu_simulator.get_thread_block_info(dataset_size)
        
        return {
            "success": True,
            "num_blocks": thread_info.num_blocks,
            "block_size": thread_info.block_size,
            "total_elements": thread_info.total_elements,
            "process_distribution": thread_info.process_distribution,
            "num_processes": gpu_simulator.num_processes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get thread block info: {str(e)}")


@router.get("/system-info")
async def get_system_info():
    """
    Get system information for educational context.
    
    Returns:
        Information about the simulation environment
    """
    import multiprocessing
    import platform
    
    return {
        "cpu_count": multiprocessing.cpu_count(),
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "simulator_processes": gpu_simulator.num_processes,
        "supported_dataset_sizes": workload_generator.get_supported_sizes(),
        "supported_operations": ["vector_add", "vector_multiply", "dot_product", "matrix_multiply"]
    }


@router.delete("/clear-data")
async def clear_all_data():
    """
    Clear all stored datasets and performance history.
    
    Educational utility for resetting the simulation environment.
    
    Returns:
        Confirmation of data clearing
    """
    try:
        current_datasets.clear()
        performance_analyzer.clear_history()
        cpu_engine.clear_execution_history()
        gpu_simulator.clear_execution_history()
        
        return {
            "success": True,
            "message": "All data cleared successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear data: {str(e)}")


@router.get("/export-results")
async def export_results(format_type: str = "dict"):
    """
    Export performance results for further analysis.
    
    Educational utility for exporting simulation data.
    
    Args:
        format_type: Export format ("dict" or "csv_data")
        
    Returns:
        Exported performance data
    """
    try:
        exported_data = performance_analyzer.export_results(format_type)
        
        return {
            "success": True,
            "format": format_type,
            "data": exported_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export results: {str(e)}")



@router.post("/export-pdf")
async def export_pdf(request: PDFReportRequest):
    """
    Generate and download PDF report of simulation results.
    
    Educational endpoint that creates a professional technical report
    containing performance metrics, charts, and visualizations.
    
    Args:
        request: PDF report generation parameters
        
    Returns:
        PDF file as streaming response
    """
    try:
        # Validate request data
        if not request.simulation_data:
            raise HTTPException(
                status_code=400,
                detail="Simulation data is required for PDF generation"
            )
        
        # Sanitize report title
        report_title = request.report_title[:100]  # Limit title length
        
        # Generate PDF
        start_time = time.perf_counter()
        pdf_bytes = pdf_service.generate_report(
            simulation_data=request.simulation_data,
            chart_images=request.chart_images,
            thread_viz_image=request.thread_viz_image,
            console_logs=request.console_logs,
            report_title=report_title
        )
        generation_time = time.perf_counter() - start_time
        
        # Validate generation time (should be < 10 seconds)
        if generation_time > 10.0:
            raise HTTPException(
                status_code=500,
                detail=f"PDF generation timeout: {generation_time:.2f}s"
            )
        
        # Validate PDF size (should be < 10MB)
        pdf_size_mb = len(pdf_bytes) / (1024 * 1024)
        if pdf_size_mb > 10:
            raise HTTPException(
                status_code=500,
                detail=f"PDF file too large: {pdf_size_mb:.2f}MB"
            )
        
        # Create filename with timestamp
        timestamp = time.strftime("%Y-%m-%d-%H%M%S")
        filename = f"quantum-compute-report-{timestamp}.pdf"
        
        # Return PDF as streaming response
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(pdf_bytes))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )



@router.post("/run-benchmark")
async def run_benchmark(request: BenchmarkRequest):
    """
    Execute automated benchmark suite across multiple configurations.
    
    Educational endpoint that systematically tests performance across
    different dataset sizes and operations.
    
    Args:
        request: Benchmark configuration parameters
        
    Returns:
        Benchmark results with statistical analysis
    """
    try:
        # Validate operations
        valid_operations = ["vector_add", "vector_multiply", "dot_product", "matrix_multiply"]
        for op in request.operations:
            if op not in valid_operations:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid operation: {op}"
                )
        
        # Validate dataset sizes
        valid_sizes = [10000, 50000, 100000, 500000]
        for size in request.dataset_sizes:
            if size not in valid_sizes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid dataset size: {size}"
                )
        
        # Run benchmark suite
        results = await benchmark_engine.run_benchmark_suite(
            operations=request.operations,
            dataset_sizes=request.dataset_sizes,
            num_processes=request.num_processes
        )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Benchmark execution failed: {str(e)}"
        )


@router.get("/benchmark-status")
async def get_benchmark_status():
    """
    Get current benchmark progress status.
    
    Educational endpoint for polling benchmark execution progress.
    
    Returns:
        Current benchmark progress information
    """
    try:
        progress = benchmark_engine.get_progress()
        
        if not progress:
            return {
                "status": "idle",
                "message": "No benchmark currently running"
            }
        
        return {
            "status": progress.status,
            "current_test": progress.current_test,
            "total_tests": progress.total_tests,
            "current_operation": progress.current_operation,
            "current_size": progress.current_size,
            "completed_tests": len(progress.completed_tests),
            "progress_percentage": round((progress.current_test / progress.total_tests) * 100, 1) if progress.total_tests > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get benchmark status: {str(e)}"
        )


@router.delete("/benchmark-cancel")
async def cancel_benchmark():
    """
    Cancel running benchmark suite.
    
    Educational endpoint for stopping long-running benchmarks.
    
    Returns:
        Cancellation confirmation
    """
    try:
        benchmark_engine.cancel_benchmark()
        
        return {
            "success": True,
            "message": "Benchmark cancellation requested"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cancel benchmark: {str(e)}"
        )



@router.get("/auto-optimize")
async def auto_optimize():
    """
    Get auto-optimization recommendations based on system capabilities.
    
    Educational endpoint that analyzes CPU cores and memory to suggest
    optimal configuration for best performance.
    
    Returns:
        Optimization suggestions with rationale
    """
    try:
        suggestions = optimization_service.get_optimization_suggestions()
        
        return {
            "success": True,
            **suggestions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate optimization suggestions: {str(e)}"
        )



# ============================================
# COA DEMONSTRATION ENDPOINTS
# ============================================

from .instruction_cycle import InstructionCycleSimulator, Instruction, create_sample_program
from .interrupt_handler import InterruptHandler, InterruptType, timer_isr, io_complete_isr, user_triggered_isr, error_isr

# Global instances for COA modules
instruction_simulator = InstructionCycleSimulator()
interrupt_handler = InterruptHandler()

# Register ISRs
interrupt_handler.register_isr(InterruptType.TIMER, timer_isr)
interrupt_handler.register_isr(InterruptType.IO_COMPLETE, io_complete_isr)
interrupt_handler.register_isr(InterruptType.USER_TRIGGERED, user_triggered_isr)
interrupt_handler.register_isr(InterruptType.ERROR, error_isr)


@router.post("/instruction-cycle")
async def run_instruction_cycle(num_instructions: int = 5) -> Dict[str, Any]:
    """
    CO1: Execute instruction cycle simulation
    
    Demonstrates Fetch-Decode-Execute cycle with step-by-step visualization.
    Educational endpoint for understanding CPU instruction processing.
    
    Args:
        num_instructions: Number of instructions to execute (default: 5)
        
    Returns:
        Complete execution trace with all stages
    """
    try:
        # Create sample program
        program = create_sample_program()[:num_instructions]
        
        # Load and execute
        instruction_simulator.load_program(program)
        result = instruction_simulator.run_program()
        
        return {
            "success": True,
            "co": "CO1",
            "title": "Instruction Cycle Simulation",
            "description": "Fetch → Decode → Execute cycle demonstration",
            **result,
            "cpu_state": instruction_simulator.get_state()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Instruction cycle simulation failed: {str(e)}"
        )


@router.post("/instruction-cycle/step")
async def step_instruction_cycle() -> Dict[str, Any]:
    """
    CO1: Execute single instruction step-by-step
    
    Returns one complete instruction cycle for animated UI display.
    
    Returns:
        Single instruction execution with all three stages
    """
    try:
        if instruction_simulator.pc >= len(instruction_simulator.memory):
            return {
                "success": False,
                "message": "Program execution complete or no program loaded"
            }
        
        steps = instruction_simulator.execute_single_instruction()
        
        return {
            "success": True,
            "steps": steps,
            "cpu_state": instruction_simulator.get_state()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Step execution failed: {str(e)}"
        )


@router.post("/trigger-interrupt")
async def trigger_interrupt(
    interrupt_type: str = "USER_TRIGGERED",
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    CO3: Trigger an interrupt
    
    Simulates interrupt occurrence for demonstration purposes.
    
    Args:
        interrupt_type: Type of interrupt (TIMER, IO_COMPLETE, USER_TRIGGERED, ERROR)
        data: Optional data associated with interrupt
        
    Returns:
        Interrupt trigger confirmation
    """
    try:
        # Convert string to enum
        try:
            int_type = InterruptType[interrupt_type.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid interrupt type: {interrupt_type}"
            )
        
        result = interrupt_handler.trigger_interrupt(int_type, data)
        
        return {
            "success": True,
            "co": "CO3",
            "title": "Interrupt Triggered",
            **result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger interrupt: {str(e)}"
        )


@router.post("/handle-interrupt")
async def handle_interrupt(current_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    CO3: Handle pending interrupt with context switching
    
    Demonstrates complete interrupt handling cycle including:
    - Context save
    - ISR execution
    - Context restore
    
    Args:
        current_state: Current CPU state (PC, accumulator, registers)
        
    Returns:
        Complete interrupt handling trace
    """
    try:
        if current_state is None:
            current_state = {
                "pc": 0,
                "accumulator": 0.0,
                "registers": {}
            }
        
        result = await interrupt_handler.handle_interrupt(current_state)
        
        return {
            "success": True,
            "co": "CO3",
            "title": "Interrupt Handling",
            "description": "Context switching and ISR execution",
            **result,
            "handler_status": interrupt_handler.get_status()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Interrupt handling failed: {str(e)}"
        )


@router.get("/interrupt-status")
async def get_interrupt_status() -> Dict[str, Any]:
    """
    CO3: Get interrupt handler status
    
    Returns current state of interrupt system.
    
    Returns:
        Interrupt handler status information
    """
    try:
        status = interrupt_handler.get_status()
        
        return {
            "success": True,
            "co": "CO3",
            **status
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get interrupt status: {str(e)}"
        )


@router.get("/thread-visualization")
async def get_thread_visualization(dataset_size: int = 50000) -> Dict[str, Any]:
    """
    CO5: Get enhanced thread block visualization data
    
    Returns detailed thread block mapping for UI visualization.
    
    Args:
        dataset_size: Size of dataset to visualize
        
    Returns:
        Thread block structure and mapping information
    """
    try:
        if dataset_size not in workload_generator.get_supported_sizes():
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported dataset size. Use one of: {workload_generator.get_supported_sizes()}"
            )
        
        thread_info = gpu_simulator.get_thread_block_info(dataset_size)
        
        # Enhanced visualization data
        blocks = []
        for i in range(thread_info.num_blocks):
            block_data = {
                "block_id": i,
                "thread_count": thread_info.process_distribution[i] if i < len(thread_info.process_distribution) else thread_info.block_size,
                "start_index": i * thread_info.block_size,
                "end_index": min((i + 1) * thread_info.block_size, dataset_size),
                "status": "ready"
            }
            blocks.append(block_data)
        
        return {
            "success": True,
            "co": "CO5",
            "title": "GPU Thread Block Visualization",
            "num_blocks": thread_info.num_blocks,
            "block_size": thread_info.block_size,
            "total_elements": thread_info.total_elements,
            "num_processes": gpu_simulator.num_processes,
            "blocks": blocks,
            "architecture": {
                "grid_dim": thread_info.num_blocks,
                "block_dim": thread_info.block_size,
                "total_threads": thread_info.num_blocks * thread_info.block_size,
                "warp_size": 32,  # Typical GPU warp size
                "warps_per_block": thread_info.block_size // 32
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get thread visualization: {str(e)}"
        )
