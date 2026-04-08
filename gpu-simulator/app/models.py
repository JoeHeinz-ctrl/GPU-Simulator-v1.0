"""
Data models for GPU Parallel Floating-Point Simulator
Defines core data structures and API models for the educational simulation system
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union, List, Dict, Any, Optional
from pydantic import BaseModel, Field
import numpy as np


# Core Data Models (using dataclasses for internal representation)

@dataclass
class Dataset:
    """Represents a floating-point dataset for computational operations"""
    size: int
    data: np.ndarray
    created_at: datetime
    operation_type: str


@dataclass
class SimulationResult:
    """Results from a single simulation run (CPU or GPU)"""
    operation: str
    dataset_size: int
    execution_time: float
    result_data: Union[np.ndarray, float]
    timestamp: datetime
    engine_type: str  # 'cpu' or 'gpu'


@dataclass
class PerformanceMetrics:
    """Performance comparison metrics between CPU and GPU execution"""
    cpu_time: float
    gpu_time: float
    speedup_ratio: float
    dataset_size: int
    operation: str
    num_processes: int
    timestamp: datetime


@dataclass
class ThreadBlockInfo:
    """Information about thread block distribution in GPU simulation"""
    num_blocks: int
    block_size: int
    total_elements: int
    process_distribution: List[int]


# API Request Models (using Pydantic for validation)

class GenerateDataRequest(BaseModel):
    """Request model for dataset generation endpoint"""
    size: int = Field(..., ge=1000, le=1000000, description="Dataset size (1K-1M elements)")
    operation_type: str = Field(..., pattern="^(vector_add|vector_multiply|dot_product|matrix_multiply)$")


class SimulationRequest(BaseModel):
    """Request model for simulation execution endpoints"""
    operation: str = Field(..., pattern="^(vector_add|vector_multiply|dot_product|matrix_multiply)$")
    dataset_size: int = Field(..., ge=1000, le=1000000)
    num_processes: Optional[int] = Field(None, ge=1, le=16, description="Number of worker processes for GPU simulation")


# API Response Models

class SimulationResponse(BaseModel):
    """Response model for simulation execution"""
    success: bool
    execution_time: float = Field(..., ge=0.0)
    result_summary: str
    performance_metrics: Optional[Dict[str, Any]] = None
    thread_block_info: Optional[Dict[str, Any]] = None


class PerformanceHistoryResponse(BaseModel):
    """Response model for performance history endpoint"""
    history: List[Dict[str, Any]]
    summary_stats: Dict[str, float]


class ThreadBlockInfoResponse(BaseModel):
    """Response model for thread block information"""
    num_blocks: int = Field(..., ge=1)
    block_size: int = Field(..., ge=1)
    total_elements: int = Field(..., ge=1)
    process_distribution: List[int]


class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    message: str
    error_code: Optional[str] = None


class PDFReportRequest(BaseModel):
    """Request model for PDF report generation"""
    simulation_data: Dict[str, Any] = Field(..., description="Simulation metrics and results")
    chart_images: Dict[str, str] = Field(..., description="Chart images as base64 encoded strings")
    thread_viz_image: str = Field(default="", description="Thread visualization as base64 encoded string")
    console_logs: List[str] = Field(default_factory=list, description="Console log messages")
    include_branding: bool = Field(default=True, description="Include branding in report")
    report_title: str = Field(default="GPU Quantum Compute Simulation Report", description="Report title")


class BenchmarkRequest(BaseModel):
    """Request model for benchmark suite execution"""
    operations: List[str] = Field(
        default=["vector_add", "vector_multiply", "dot_product", "matrix_multiply"],
        description="Operations to benchmark"
    )
    dataset_sizes: List[int] = Field(
        default=[10000, 50000, 100000, 500000],
        description="Dataset sizes to test"
    )
    num_processes: Optional[int] = Field(None, ge=1, le=16, description="Number of processes for GPU simulation")


class BenchmarkResult(BaseModel):
    """Single benchmark test result"""
    operation: str
    dataset_size: int
    cpu_time: float
    gpu_time: float
    speedup: float
    timestamp: str


class BenchmarkResults(BaseModel):
    """Complete benchmark suite results"""
    results: List[BenchmarkResult]
    total_tests: int
    average_speedup: float
    best_speedup: float
    worst_speedup: float
    total_duration: float
    completed: bool = True


class OptimizationSuggestions(BaseModel):
    """Auto-optimization recommendations"""
    recommended_processes: int = Field(..., description="Recommended number of processes")
    recommended_dataset_size: int = Field(..., description="Recommended dataset size")
    cpu_cores: int = Field(..., description="Available CPU cores")
    available_memory_gb: float = Field(..., description="Available system memory in GB")
    rationale: Dict[str, str] = Field(..., description="Explanation for each recommendation")


# Validation Functions

def validate_dataset_size(size: int) -> bool:
    """Validate that dataset size is within supported range"""
    supported_sizes = [10000, 50000, 100000, 500000]
    return size in supported_sizes


def validate_operation_type(operation: str) -> bool:
    """Validate that operation type is supported"""
    supported_operations = ["vector_add", "vector_multiply", "dot_product", "matrix_multiply"]
    return operation in supported_operations


def validate_floating_point_array(arr: np.ndarray) -> bool:
    """Validate that array contains valid floating-point numbers"""
    if not isinstance(arr, np.ndarray):
        return False
    if arr.dtype not in [np.float32, np.float64]:
        return False
    if not np.all(np.isfinite(arr)):
        return False
    return True


# Type Aliases for clarity
DatasetSize = int
ExecutionTime = float
SpeedupRatio = float
ProcessCount = int



# COA Demonstration Models

class InstructionCycleRequest(BaseModel):
    """Request model for instruction cycle simulation"""
    num_instructions: int = Field(default=5, ge=1, le=20, description="Number of instructions to execute")


class InstructionCycleResponse(BaseModel):
    """Response model for instruction cycle simulation"""
    success: bool
    co: str = "CO1"
    title: str
    description: str
    total_instructions: int
    final_pc: int
    final_accumulator: float
    execution_log: List[Dict[str, Any]]
    cpu_state: Dict[str, Any]


class InterruptTriggerRequest(BaseModel):
    """Request model for triggering interrupts"""
    interrupt_type: str = Field(default="USER_TRIGGERED", pattern="^(TIMER|IO_COMPLETE|USER_TRIGGERED|ERROR)$")
    data: Optional[Dict[str, Any]] = None


class InterruptHandleRequest(BaseModel):
    """Request model for handling interrupts"""
    current_state: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Current CPU state (PC, accumulator, registers)"
    )


class ThreadVisualizationResponse(BaseModel):
    """Response model for thread visualization"""
    success: bool
    co: str = "CO5"
    title: str
    num_blocks: int
    block_size: int
    total_elements: int
    num_processes: int
    blocks: List[Dict[str, Any]]
    architecture: Dict[str, Any]
