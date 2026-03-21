# GPU Parallel Floating-Point Simulator

An educational web application that demonstrates parallel programming concepts by simulating GPU-style parallel computing using Python multiprocessing. This project helps students understand thread blocks, parallel execution, floating-point arithmetic, and performance speedup through interactive simulations.

## 🎯 Project Overview

This simulator provides a hands-on learning experience for understanding how GPUs accelerate floating-point computations through parallel processing. By comparing sequential CPU execution with simulated parallel GPU execution, students can observe and analyze the performance benefits of parallel computing.

### Educational Goals

- **Thread Blocks**: Understand how GPUs organize work into thread blocks
- **Parallel Execution**: See how operations are distributed across multiple processing units
- **Floating-Point Arithmetic**: Learn how mathematical operations scale with parallelization
- **Performance Speedup**: Analyze speedup ratios and efficiency metrics

## 🏗️ Architecture

The application consists of three main layers:

```
┌─────────────────────────────────────────┐
│           Frontend Layer                │
│  ┌─────────────────┐ ┌─────────────────┐│
│  │  Web Dashboard  │ │ Chart.js Viz    ││
│  └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          Web Service Layer              │
│  ┌─────────────────┐ ┌─────────────────┐│
│  │  FastAPI Server │ │   API Routes    ││
│  └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│         Computation Layer               │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐ │
│ │ CPU  │ │ GPU  │ │Perf  │ │Workload  │ │
│ │Engine│ │Sim   │ │Analyzer│ │Generator │ │
│ └──────┘ └──────┘ └──────┘ └──────────┘ │
└─────────────────────────────────────────┘
```

## 🧠 How GPU Parallelism Works

### Traditional CPU Processing (Sequential)
```python
# Sequential processing - one element at a time
for i in range(n):
    result[i] = a[i] + b[i]
```

### GPU-Style Parallel Processing (Simulated)
```python
# Parallel processing - multiple elements simultaneously
# Each worker process handles a chunk of data
chunks = divide_data_into_chunks(data, num_processes)
with multiprocessing.Pool() as pool:
    results = pool.map(process_chunk, chunks)
combined_result = combine_results(results)
```

### Thread Block Simulation

Our simulator mimics CUDA thread blocks using Python multiprocessing:

1. **Data Division**: Large datasets are divided into chunks (thread blocks)
2. **Worker Processes**: Each chunk is assigned to a worker process (simulating GPU cores)
3. **Parallel Execution**: All workers execute simultaneously
4. **Result Combination**: Results from all workers are combined into the final output

```
Dataset: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                        ↓
            Divide into Thread Blocks
                        ↓
Block 1: [1, 2, 3]    Block 2: [4, 5, 6]    Block 3: [7, 8, 9]    Block 4: [10, 11, 12]
    ↓                     ↓                     ↓                        ↓
Process 1             Process 2             Process 3                Process 4
    ↓                     ↓                     ↓                        ↓
Result 1              Result 2              Result 3                 Result 4
                        ↓
                Combine Results
                        ↓
            Final Result: [...]
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**:
   ```bash
   cd gpu-simulator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies** (choose one method):

   **Method 1 - Automatic installation:**
   ```bash
   python install.py
   ```

   **Method 2 - Standard pip install:**
   ```bash
   pip install -r requirements.txt
   ```

   **Method 3 - If above fails, try simplified requirements:**
   ```bash
   pip install -r requirements-simple.txt
   ```

   **Method 4 - Manual installation:**
   ```bash
   pip install fastapi uvicorn numpy pydantic
   ```

### Running the Application

1. **Start the server**:
   ```bash
   python run_server.py
   ```
   
   Or alternatively:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

3. **Begin simulation**:
   - Select a dataset size (10K, 50K, 100K, or 500K elements)
   - Choose an operation (Vector Addition, Multiplication, Dot Product, or Matrix Multiplication)
   - Click "Generate Data" to create the dataset
   - Run CPU and GPU simulations to compare performance

## 🎮 Using the Simulator

### Step-by-Step Tutorial

1. **Generate Data**:
   - Choose dataset size: Start with 50K elements for good performance demonstration
   - Select operation: Vector Addition is good for beginners
   - Click "Generate Data" - should complete in under 1 second

2. **Run CPU Simulation**:
   - Click "Run CPU Simulation"
   - Observe the execution time (baseline performance)
   - Note the sequential processing approach

3. **Run GPU Simulation**:
   - Click "Run GPU Simulation"
   - Compare execution time with CPU
   - Observe the thread block visualization

4. **Analyze Results**:
   - Check the speedup ratio (GPU time / CPU time)
   - View performance charts
   - Understand the parallel processing benefits

### Supported Operations

| Operation | Description | Complexity | Best For Learning |
|-----------|-------------|------------|-------------------|
| **Vector Addition** | Element-wise addition: `c[i] = a[i] + b[i]` | O(n) | Understanding basic parallelism |
| **Vector Multiplication** | Element-wise multiplication: `c[i] = a[i] * b[i]` | O(n) | Floating-point operations |
| **Dot Product** | Sum of products: `result = Σ(a[i] * b[i])` | O(n) | Reduction operations |
| **Matrix Multiplication** | Standard matrix product | O(n³) | Complex parallel algorithms |

### Dataset Sizes

- **10K elements**: Quick demonstrations, minimal speedup
- **50K elements**: Good balance of performance and speed
- **100K elements**: Clear speedup demonstration
- **500K elements**: Maximum performance benefits

## 📊 Understanding the Results

### Example Output
```
CPU Execution Time: 1.28 seconds
GPU Execution Time: 0.36 seconds
Speedup: 3.55x

Performance Analysis:
- Efficiency: 89% (3.55x speedup with 4 processes)
- Throughput Improvement: 72%
- Elements per second (CPU): 390,625
- Elements per second (GPU): 1,388,889
```

### Performance Metrics Explained

- **Speedup Ratio**: CPU_time / GPU_time
  - > 1.0: Parallel processing is faster
  - < 1.0: Sequential processing is faster (due to overhead)
  - = 1.0: Equal performance

- **Efficiency**: Speedup / Number_of_Processes
  - 1.0: Perfect linear scaling
  - < 1.0: Overhead or non-parallelizable work

- **Throughput**: Elements processed per second

### When Parallel Processing Helps Most

✅ **Good for parallelization**:
- Large datasets (100K+ elements)
- Computationally intensive operations
- Independent operations (embarrassingly parallel)

❌ **Limited benefit**:
- Small datasets (< 10K elements)
- Operations with dependencies
- High communication overhead

## 🔧 Technical Implementation

### Core Components

1. **WorkloadGenerator**: Creates floating-point datasets
   ```python
   generator = WorkloadGenerator()
   dataset = generator.generate_dataset(50000, "vector_add")
   ```

2. **CPUEngine**: Sequential processing baseline
   ```python
   cpu = CPUEngine()
   result, time = cpu.vector_add(vector_a, vector_b)
   ```

3. **GPUSimulator**: Parallel processing simulation
   ```python
   gpu = GPUSimulator(num_processes=4)
   result, time = gpu.vector_add_parallel(vector_a, vector_b)
   ```

4. **PerformanceAnalyzer**: Metrics and comparison
   ```python
   analyzer = PerformanceAnalyzer()
   analysis = analyzer.analyze_results(cpu_result, gpu_result, ...)
   ```

### API Endpoints

- `POST /api/generate-data`: Create datasets
- `POST /api/run-cpu-simulation`: Execute CPU processing
- `POST /api/run-gpu-simulation`: Execute parallel processing
- `GET /api/performance-history`: Retrieve performance data
- `GET /api/thread-block-info`: Get parallelization details

## 🎓 Educational Concepts

### Parallel Programming Principles

1. **Decomposition**: Breaking problems into independent parts
2. **Load Balancing**: Distributing work evenly across processors
3. **Synchronization**: Coordinating parallel execution
4. **Scalability**: Performance improvement with more processors

### GPU Computing Concepts

1. **SIMD (Single Instruction, Multiple Data)**: Same operation on different data
2. **Thread Hierarchy**: Threads → Blocks → Grid
3. **Memory Hierarchy**: Global, shared, and local memory
4. **Occupancy**: Efficient use of processing units

### Performance Analysis

1. **Amdahl's Law**: Theoretical speedup limits
2. **Overhead**: Cost of parallelization
3. **Scalability**: Performance vs. problem size
4. **Efficiency**: Resource utilization

## 🛠️ Development and Extension

### Project Structure
```
gpu-simulator/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── routes.py            # API endpoints
│   ├── models.py            # Data models
│   ├── workload_generator.py # Dataset creation
│   ├── cpu_engine.py        # Sequential processing
│   ├── parallel_engine.py   # Parallel simulation
│   └── performance.py       # Performance analysis
├── frontend/
│   ├── index.html           # Web dashboard
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Adding New Operations

1. **Implement in CPUEngine**:
   ```python
   def new_operation(self, data):
       start_time = time.perf_counter()
       # Sequential implementation
       result = process_sequentially(data)
       end_time = time.perf_counter()
       return result, end_time - start_time
   ```

2. **Implement in GPUSimulator**:
   ```python
   def new_operation_parallel(self, data):
       # Divide data into chunks
       # Process in parallel
       # Combine results
   ```

3. **Add to API routes and frontend**

### Customization Options

- **Process Count**: Adjust `num_processes` in GPUSimulator
- **Dataset Sizes**: Modify `SUPPORTED_SIZES` in WorkloadGenerator
- **Visualization**: Customize Chart.js configurations
- **Operations**: Add new mathematical operations

## 🔍 Troubleshooting

### Common Issues

1. **Slow Performance**:
   - Reduce dataset size
   - Check available CPU cores
   - Close other applications

2. **Import Errors**:
   - Verify virtual environment activation
   - Try: `python install.py` for automatic installation
   - Try: `pip install -r requirements-simple.txt` for minimal dependencies
   - Manually install: `pip install fastapi uvicorn numpy pydantic`

3. **NumPy Installation Issues**:
   - Update pip: `python -m pip install --upgrade pip`
   - Install setuptools: `pip install setuptools wheel`
   - Try pre-compiled wheels: `pip install --only-binary=numpy numpy`

4. **Port Already in Use**:
   - Change port: `python run_server.py` (edit the file to change port)
   - Kill existing process: Check Task Manager (Windows) or `ps aux | grep python`

5. **Browser Issues**:
   - Clear browser cache
   - Try different browser
   - Check JavaScript console for errors

6. **Module Import Errors**:
   - Make sure you're in the `gpu-simulator` directory
   - Use `python run_server.py` instead of `uvicorn app.main:app`
   - Check that all files are in the correct directories

### Performance Tips

- Start with smaller datasets (10K-50K elements)
- Use vector operations before matrix operations
- Monitor system resources during large simulations
- Close unnecessary applications for better performance

## 📚 Further Learning

### Recommended Reading

1. **Parallel Programming**:
   - "An Introduction to Parallel Programming" by Peter Pacheco
   - "Parallel Programming in C with MPI and OpenMP" by Michael Quinn

2. **GPU Computing**:
   - "CUDA by Example" by Jason Sanders
   - "Programming Massively Parallel Processors" by David Kirk

3. **Performance Analysis**:
   - "Computer Architecture: A Quantitative Approach" by Hennessy & Patterson

### Online Resources

- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)
- [OpenMP Tutorials](https://computing.llnl.gov/tutorials/openMP/)
- [Parallel Computing Coursera Courses](https://www.coursera.org/courses?query=parallel%20computing)

## 🤝 Contributing

This is an educational project. Contributions that enhance learning are welcome:

- Additional mathematical operations
- Improved visualizations
- Better educational explanations
- Performance optimizations
- Bug fixes

## 📄 License

This project is created for educational purposes. Feel free to use and modify for learning and teaching parallel programming concepts.

## 🙏 Acknowledgments

- Inspired by CUDA parallel programming model
- Built with FastAPI, NumPy, and Chart.js
- Educational concepts from parallel computing literature

---

**Happy Learning! 🚀**

*Understanding parallel programming is key to modern high-performance computing. This simulator provides a foundation for exploring these concepts in an interactive, visual way.*