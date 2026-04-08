# Quick Start Guide

## 🎓 Two Ways to Use This Project

### Option A: COA Demonstration (For Viva/Learning)
Run the complete COA modules demonstration covering all 5 Course Outcomes.

### Option B: Web Application (Interactive Simulator)
Use the web-based GPU simulator with visual interface.

---

## 🎓 Option A: COA Demonstration

### Step 1: Install Dependencies
```bash
cd gpu-simulator
pip install -r requirements.txt
```

### Step 2: Run Tests (Verify Everything Works)
```bash
python test_coa_modules.py
```
You should see: "🎉 All tests passed! Project is ready for viva."

### Step 3: Run Integrated Demo
```bash
python coa_integrated_demo.py
```

Choose option 1 for full interactive demo or option 2 for quick demo.

### What You'll See:
- **CO1**: Instruction Cycle (Fetch-Decode-Execute)
- **CO2**: Performance Evaluation (CPU vs GPU comparison with charts)
- **CO3**: Interrupt Handling (ISR and context switching)
- **CO4**: I/O Interfacing (Input/Output device simulation)
- **CO5**: GPU Architecture (Parallel processing visualization)

---

## 🚀 Option B: Web Application

### Step 1: Install Dependencies
```bash
cd gpu-simulator
python install.py
```

If that fails, try:
```bash
pip install fastapi uvicorn numpy pydantic
```

### Step 2: Start the Server
```bash
python run_server.py
```

### Step 3: Open Browser
Go to: http://localhost:8000

## 🎮 First Simulation

1. **Select Dataset Size**: Start with "50,000 elements"
2. **Choose Operation**: Select "Vector Addition"
3. **Generate Data**: Click "Generate Data" button
4. **Run CPU Simulation**: Click "Run CPU Simulation"
5. **Run GPU Simulation**: Click "Run GPU Simulation"
6. **Compare Results**: See the speedup ratio and charts!

## ❌ If Something Goes Wrong

### Can't Install Dependencies?
Try this minimal installation:
```bash
pip install fastapi uvicorn numpy
```

### Server Won't Start?
Make sure you're in the right directory:
```bash
cd gpu-simulator
python run_server.py
```

### Still Having Issues?
1. Check you have Python 3.8+: `python --version`
2. Try creating a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Mac/Linux
   ```
3. Install again: `pip install fastapi uvicorn numpy pydantic`

## 🎯 What You'll Learn

- **Parallel Processing**: How GPUs speed up computations
- **Thread Blocks**: How work is divided across processors
- **Performance Analysis**: Understanding speedup and efficiency
- **Floating-Point Operations**: Different types of mathematical operations

## 📊 Expected Results

With 50K elements:
- **Vector Addition**: ~2-4x speedup
- **Matrix Multiplication**: ~3-6x speedup
- **Larger datasets**: Even better speedup!

## 🔧 Advanced Usage

- Try different dataset sizes (10K, 100K, 500K)
- Compare different operations
- Analyze the performance charts
- Observe thread block visualization

Happy learning! 🎓