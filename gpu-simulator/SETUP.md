# GPU Simulator - Quick Setup Guide

## 🚀 EASIEST WAY: One-Click Setup (Recommended)

### For Windows:
**Just double-click:** `setup_and_run.bat`

### For Mac/Linux:
**Just run:** `bash setup_and_run.sh`

That's it! The script will:
- ✓ Check Python installation
- ✓ Install all dependencies automatically
- ✓ Start the server
- ✓ Open at http://localhost:8000

---

## 📋 Manual Setup (Alternative Method)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Python Dependencies
Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install all required packages:
- fastapi (web framework)
- uvicorn (web server)
- numpy (numerical computing)
- reportlab (PDF generation)
- python-multipart (file handling)

### Step 2: Run the Application
```bash
python run_server.py
```

### Step 3: Open in Browser
Open your web browser and go to:
```
http://localhost:8000
```

## That's It!
The application should now be running. You can:
- Initialize datasets
- Run CPU/GPU simulations
- View all 5 Course Outcomes (CO1-CO5) in action
- Export results as PDF

## Troubleshooting

**If port 8000 is already in use:**
- Stop other applications using port 8000
- Or modify `run_server.py` to use a different port

**If packages fail to install:**
- Make sure Python and pip are up to date
- Try: `python -m pip install --upgrade pip`
- Then retry: `pip install -r requirements.txt`

**If the browser shows "Connection Refused":**
- Make sure the server is running (check terminal output)
- Wait a few seconds for the server to fully start
- Try refreshing the browser

## Quick Demo
1. Click "Initialize Dataset" → Select size (e.g., 50000) → Click "Generate"
2. Click "Run CPU Simulation" → Watch CO1 (Instruction Cycle) activate
3. Click "Run GPU Simulation" → Watch CO5, CO3, CO2 activate automatically
4. Check the console for labeled messages: [CO1], [CO2], [CO3], [CO4], [CO5]
5. View performance charts and speedup metrics

## Project Structure
```
gpu-simulator/
├── app/                    # Backend Python code
│   ├── main.py            # FastAPI application
│   ├── routes.py          # API endpoints
│   ├── models.py          # Data models
│   ├── cpu_engine.py      # CPU simulation
│   ├── parallel_engine.py # GPU simulation
│   ├── instruction_cycle.py   # CO1: Instruction Cycle
│   ├── interrupt_handler.py   # CO3: Interrupt Handling
│   ├── performance.py     # CO2: Performance Evaluation
│   └── ...
├── frontend/              # Frontend HTML/CSS/JS
│   ├── index.html        # Main UI
│   ├── style.css         # Styling
│   └── script.js         # Interactive logic
├── requirements.txt       # Python dependencies
├── run_server.py         # Server startup script
├── README.md             # Complete documentation
└── SETUP.md              # This file

```

## For Questions or Issues
Refer to README.md for complete project documentation including:
- Detailed architecture explanation
- All 5 Course Outcomes coverage
- API documentation
- Technical implementation details
