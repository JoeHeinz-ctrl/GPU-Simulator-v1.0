# Quick Demo Card - Automatic CO Integration
## 30-Second Reference for Viva

---

## 🎯 One-Click Demo Flow

### 1. Initialize Dataset
**Click**: "Initialize Dataset" button

**Watch For**:
- Console: `[CO4: I/O] Reading configuration...`
- Console: `[CO4: I/O] Writing dataset to memory...`

**Say**: "CO4 handles input/output operations"

---

### 2. Run CPU Simulation
**Click**: "CPU Baseline" button

**Watch For**:
- Console: `[CO1: Instruction Cycle] Loading CPU instructions...`
- CO1 Panel: Stages light up (Fetch → Decode → Execute)
- CO1 Panel: PC and ACC values update

**Say**: "CO1 demonstrates instruction cycle - Fetch, Decode, Execute"

---

### 3. Run GPU Simulation
**Click**: "GPU Accelerated" button

**Watch For**:
- Console: `[CO5: GPU] Creating thread block grid...`
- CO5 Panel: Thread blocks appear and animate
- Console: `[CO3: Interrupt] Timer interrupt triggered!` (50% chance)
- CO3 Panel: Interrupt flow animates (if triggered)
- Console: `[CO2: Performance] Calculating speedup...`
- Hero Stats: Speedup and Efficiency update

**Say**: "CO5 shows parallel architecture, CO3 handles interrupts, CO2 evaluates performance"

---

## 📊 What Each CO Shows

| CO | Where to Look | What You'll See |
|----|---------------|-----------------|
| **CO1** | CO1 Panel + Console | Fetch→Decode→Execute stages, PC/ACC values |
| **CO2** | Hero Stats + Console | Speedup ratio, Efficiency %, Performance charts |
| **CO3** | CO3 Panel + Console | Interrupt flow (if triggered), Context switching |
| **CO4** | Console Messages | I/O operations during data init and results |
| **CO5** | CO5 Panel + Console | Thread block grid, Parallel execution |

---

## 🎬 30-Second Viva Script

**Setup**: Select "50K Elements" and "Vector Addition"

**Demo**:
1. Click "Initialize Dataset" → Point to console: "CO4 I/O"
2. Click "CPU Baseline" → Point to CO1 panel: "Instruction cycle"
3. Click "GPU Accelerated" → Point to CO5 panel: "Thread blocks"
4. Point to hero stats: "CO2 performance - 5x speedup"
5. If interrupt triggered, point to CO3 panel: "Interrupt handling"

**Finish**: "All 5 COs demonstrated automatically in one workflow"

---

## 💡 Key Points to Mention

- **Automatic**: "COs activate based on simulation pipeline"
- **Integrated**: "All COs work together, not separately"
- **Realistic**: "Simulates real computer system behavior"
- **Configuration-based**: "Adapts to dataset size and operation"
- **Console labels**: "Each CO clearly labeled in output"

---

## 🔍 If Asked to Show Specific CO

**CO1**: Scroll to CO1 panel, click "Run Instruction Cycle" for detailed view
**CO2**: Point to charts and hero stats
**CO3**: Click "Trigger Interrupt" for manual demonstration
**CO4**: Point to dropdown controls and console
**CO5**: Click "Visualize Thread Blocks" for detailed view

---

## ✅ Quick Checklist

Before demo:
- [ ] Server running (http://localhost:8000)
- [ ] Page loaded and responsive
- [ ] Select 50K Elements
- [ ] Select Vector Addition
- [ ] Console visible
- [ ] All panels visible (scroll to see CO1, CO3, CO5)

---

## 🎯 Remember

**Main workflow** = All COs automatic
**Individual buttons** = Detailed CO-specific demos
**Console messages** = Show which CO is active
**Panels update** = Real-time visualization

**You're ready!** 🚀
