# Quick Start Guide

## 🚀 Get Running in 3 Steps

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