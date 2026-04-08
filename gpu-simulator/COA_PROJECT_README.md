# GPU Parallel Floating-Point Simulator
## Complete Computer Organization and Architecture (COA) Demonstration

### Project Overview
This project demonstrates all 5 Course Outcomes (CO1-CO5) of Computer Organization and Architecture through a practical GPU-style parallel floating-point computation simulator.

---

## 📚 Course Outcomes Coverage

### ✅ CO1: Instruction Cycle Simulation
**Module:** `coa_modules/co1_instruction_cycle.py`

**Demonstrates:**
- **Fetch Stage**: Retrieve instruction from memory using Program Counter (PC)
- **Decode Stage**: Interpret opcode and operands using Control Unit
- **Execute Stage**: Perform operation in ALU (Arithmetic Logic Unit)
- **Program Counter**: Tracks current instruction
- **Instruction Register**: Holds current instruction

**Key Concepts:**
```
PC → Fetch → IR → Decode → ALU → Execute → Result
```

**Operations Supported:**
- ADD (Addition)
- MUL (Multiplication)
- SUB (Subtraction)
- DIV (Division)

---

### ✅ CO2: Performance Evaluation
**Module:** `coa_modules/co2_performance_evaluation.py`

**Demonstrates:**
- **Execution Time Measurement**: High-resolution timing
- **CPU vs GPU Comparison**: Sequential vs Parallel
- **Speedup Calculation**: `Speedup = T_cpu / T_gpu`
- **Efficiency Metrics**: `Efficiency = (Speedup / Cores) × 100%`
- **Throughput**: Operations per second
- **Latency**: Time per operation
- **Performance Visualization**: Graphs and charts

**Metrics Calculated:**
- Execution time (seconds)
- Speedup ratio (x times faster)
- Parallel efficiency (%)
- Throughput (ops/sec)
- Latency (μs/op)

---

### ✅ CO3: Interrupt Handling Simulation
**Module:** `coa_modules/co3_interrupt_handling.py`

**Demonstrates:**
- **Interrupt Request (IRQ)**: Trigger interrupts
- **Interrupt Service Routine (ISR)**: Handler functions
- **Context Switching**: Save/restore CPU state
- **Interrupt Vector Table (IVT)**: Maps interrupts to handlers
- **Interrupt Enable/Disable**: Control interrupt processing
- **Nested Interrupt Prevention**: Disable during ISR

**Interrupt Types:**
- TIMER: Time-critical tasks
- IO_READY: I/O device ready
- ERROR: Error handling
- CHECKPOINT: Computation checkpoints
- MEMORY: Memory management

**Process:**
```
Normal Execution → Interrupt Occurs → Save Context → 
Execute ISR → Restore Context → Resume Execution
```

---

### ✅ CO4: I/O Interfacing Simulation
**Module:** `coa_modules/co4_io_interfacing.py`

**Demonstrates:**
- **Input Devices**: Keyboard simulation
- **Output Devices**: Display simulation
- **Secondary Storage**: Disk I/O operations
- **I/O Controllers**: Device management
- **Device Status Registers**: Track device state
- **DMA (Direct Memory Access)**: Efficient data transfer
- **I/O Buffering**: Temporary data storage

**I/O Operations:**
- Read from keyboard (input)
- Write to display (output)
- Read from disk (file input)
- Write to disk (file output)
- DMA transfers (memory-to-memory)

**Device States:**
- READY: Available for I/O
- BUSY: Processing request
- ERROR: Device error

---

### ✅ CO5: GPU Architecture Simulation
**Module:** `coa_modules/co5_gpu_architecture.py`

**Demonstrates:**
- **Thread Blocks**: Groups of parallel threads
- **Grid Structure**: Collection of thread blocks
- **Thread-to-Data Mapping**: How threads process data
- **Parallel Execution Model**: SIMD (Single Instruction Multiple Data)
- **Memory Hierarchy**: Registers → Shared → Global → Host
- **Kernel Execution**: Parallel computation
- **Multiprocessing**: Simulates GPU cores

**Architecture:**
```
Grid
├── Block 0 (256 threads)
├── Block 1 (256 threads)
├── Block 2 (256 threads)
└── ...
```

**Memory Hierarchy:**
```
Registers (Fastest, Per-thread)
    ↓
Shared Memory (Fast, Per-block)
    ↓
Global Memory (Slower, All threads)
    ↓
Host Memory (Slowest, CPU RAM)
```

---

## 🚀 Installation and Setup

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
```

### Install Dependencies
```bash
cd gpu-simulator
pip install -r requirements.txt
```

**Required Packages:**
- numpy: Numerical computations
- matplotlib: Performance visualization
- psutil: System information
- multiprocessing: Parallel processing (built-in)

---

## 💻 How to Run

### Option 1: Full Integrated Demo (Recommended for Viva)
```bash
python coa_integrated_demo.py
```
Then select option **1** for full demonstration with user input.

**What it does:**
1. Asks for dataset size and operation
2. Demonstrates all 5 COs in sequence
3. Shows complete workflow
4. Displays comprehensive results

### Option 2: Quick Demo (No User Input)
```bash
python coa_integrated_demo.py
```
Then select option **2** for quick demonstration.

**What it does:**
- Runs all CO demonstrations automatically
- Uses default values
- Faster execution
- Good for testing

### Option 3: Individual CO Demonstrations

**CO1: Instruction Cycle**
```bash
python -m coa_modules.co1_instruction_cycle
```

**CO2: Performance Evaluation**
```bash
python -m coa_modules.co2_performance_evaluation
```

**CO3: Interrupt Handling**
```bash
python -m coa_modules.co3_interrupt_handling
```

**CO4: I/O Interfacing**
```bash
python -m coa_modules.co4_io_interfacing
```

**CO5: GPU Architecture**
```bash
python -m coa_modules.co5_gpu_architecture
```

---

## 📊 Sample Output

### Execution Flow
```
1. CO4: Get user input (dataset size, operation)
2. CO1: Simulate instruction cycle
3. CO5: Setup GPU architecture
4. CO2: Measure CPU performance
5. CO3: Handle interrupts during execution
6. CO2: Measure GPU performance
7. CO2: Compare and analyze results
8. CO4: Display and save results
```

### Sample Performance Results
```
╔══════════════════════════════════════════════════════════════╗
║                    SIMULATION RESULTS                        ║
╠══════════════════════════════════════════════════════════════╣
║  Operation:        ADD                                       ║
║  Dataset Size:     10,000 elements                           ║
║                                                              ║
║  CPU Time:         0.052300 seconds                          ║
║  GPU Time:         0.008900 seconds                          ║
║  Speedup:          5.88x                                     ║
║  Efficiency:       73.50%                                    ║
║                                                              ║
║  Throughput:       1,123,596 ops/sec                         ║
║  Latency:          0.890 μs/op                               ║
║                                                              ║
║  Performance Gain: 82.98%                                    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎯 Viva Preparation Guide

### Key Points to Explain

#### 1. **Instruction Cycle (CO1)**
- "The instruction cycle has three stages: Fetch, Decode, and Execute"
- "Program Counter (PC) tracks which instruction to execute next"
- "Control Unit decodes the instruction and prepares the ALU"
- "ALU performs the actual computation"

#### 2. **Performance Evaluation (CO2)**
- "We measure execution time using high-resolution timers"
- "Speedup shows how much faster parallel execution is"
- "Efficiency indicates how well we utilize available cores"
- "Throughput measures operations per second"

#### 3. **Interrupt Handling (CO3)**
- "Interrupts allow the CPU to respond to events immediately"
- "We save the current state (context) before handling interrupt"
- "ISR (Interrupt Service Routine) executes the handler code"
- "After ISR, we restore context and resume normal execution"

#### 4. **I/O Interfacing (CO4)**
- "I/O controllers manage communication with devices"
- "Device status registers track if device is ready or busy"
- "DMA allows direct memory access without CPU intervention"
- "Buffering improves I/O performance"

#### 5. **GPU Architecture (CO5)**
- "GPU uses SIMD model: Same instruction on multiple data"
- "Thread blocks group threads that execute together"
- "Grid contains multiple thread blocks"
- "Memory hierarchy: Registers (fast) → Shared → Global (slow)"

### Common Viva Questions

**Q: Why is GPU faster than CPU?**
A: GPU executes many operations in parallel using multiple cores, while CPU executes sequentially. For data-parallel tasks like vector operations, GPU can process thousands of elements simultaneously.

**Q: What is speedup?**
A: Speedup = T_sequential / T_parallel. It measures how many times faster the parallel version is compared to sequential.

**Q: What happens during an interrupt?**
A: 1) Save current CPU state, 2) Execute ISR, 3) Restore state, 4) Resume execution.

**Q: What is DMA?**
A: Direct Memory Access allows I/O devices to transfer data directly to/from memory without CPU intervention, freeing CPU for other tasks.

**Q: What is the instruction cycle?**
A: Fetch (get instruction) → Decode (interpret instruction) → Execute (perform operation). This repeats for every instruction.

---

## 📁 Project Structure

```
gpu-simulator/
├── coa_modules/
│   ├── __init__.py                      # Package initialization
│   ├── co1_instruction_cycle.py         # CO1: Instruction cycle
│   ├── co2_performance_evaluation.py    # CO2: Performance metrics
│   ├── co3_interrupt_handling.py        # CO3: Interrupt handling
│   ├── co4_io_interfacing.py            # CO4: I/O operations
│   └── co5_gpu_architecture.py          # CO5: GPU architecture
├── coa_integrated_demo.py               # Main demonstration
├── COA_PROJECT_README.md                # This file
└── requirements.txt                     # Dependencies
```

---

## 🔧 Customization

### Change Dataset Size
Edit in `coa_integrated_demo.py` or provide as input:
```python
dataset_size = 50000  # Change to desired size
```

### Change Operation
Supported operations: ADD, MUL, SUB, DIV
```python
operation = "MUL"  # Change to desired operation
```

### Change Thread Block Size
Edit in `co5_gpu_architecture.py`:
```python
threads_per_block = 512  # Default is 256
```

---

## 📈 Performance Expectations

### Typical Speedup Values
- Small datasets (< 10K): 2-4x speedup
- Medium datasets (10K-100K): 4-8x speedup
- Large datasets (> 100K): 8-15x speedup

### Factors Affecting Performance
- Dataset size (larger = better speedup)
- Number of CPU cores available
- Operation complexity
- Memory bandwidth
- Python overhead

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure you're in the `gpu-simulator` directory
```bash
cd gpu-simulator
python coa_integrated_demo.py
```

### Issue: "No module named 'numpy'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Slow performance
**Solution:** Reduce dataset size or use fewer cores
```python
dataset_size = 1000  # Smaller size
num_cores = 2        # Fewer cores
```

---

## 📝 Code Comments

All code is heavily commented with:
- **COA Concept Mapping**: Links code to COA concepts
- **Inline Explanations**: What each section does
- **Function Docstrings**: Purpose and parameters
- **Section Headers**: Clear organization

---

## ✅ Verification Checklist

Before viva, verify:
- [ ] All 5 CO modules run without errors
- [ ] Integrated demo completes successfully
- [ ] Performance graphs are generated
- [ ] Results are displayed correctly
- [ ] You understand each CO concept
- [ ] You can explain the code flow
- [ ] You can answer common questions

---

## 🎓 Learning Outcomes

After completing this project, you will understand:
1. How CPU executes instructions (Fetch-Decode-Execute)
2. How to measure and compare performance
3. How interrupts work in computer systems
4. How I/O devices interface with CPU
5. How GPU parallel architecture works
6. Difference between sequential and parallel processing
7. Performance metrics (speedup, efficiency, throughput)
8. Memory hierarchy in computing systems

---

## 📚 References

### COA Concepts
- Computer Organization and Architecture by William Stallings
- Computer Architecture: A Quantitative Approach by Hennessy & Patterson

### GPU Programming
- CUDA Programming Guide (NVIDIA)
- Introduction to Parallel Computing

### Python Multiprocessing
- Python multiprocessing documentation
- Parallel Programming with Python

---

## 👨‍💻 Author
COA Project - GPU Parallel Floating-Point Simulator
Created for Computer Organization and Architecture course demonstration

---

## 📄 License
Educational use only - For COA course demonstration

---

## 🎯 Quick Start for Viva

1. **Navigate to project directory:**
   ```bash
   cd gpu-simulator
   ```

2. **Run integrated demo:**
   ```bash
   python coa_integrated_demo.py
   ```

3. **Select option 1** (Full demo)

4. **Enter values when prompted:**
   - Dataset size: 10000
   - Operation: ADD

5. **Watch the demonstration** - All COs will be shown

6. **Review the results** - Note speedup and efficiency

7. **Be ready to explain** each CO concept

---

## 💡 Tips for Viva Success

1. **Run the demo before viva** to ensure everything works
2. **Understand the flow** from CO4 → CO1 → CO5 → CO2 → CO3
3. **Know the formulas**: Speedup, Efficiency, Throughput
4. **Explain with diagrams**: Draw instruction cycle, interrupt flow
5. **Be confident**: You have working code demonstrating all concepts!

---

**Good luck with your viva! 🎉**
