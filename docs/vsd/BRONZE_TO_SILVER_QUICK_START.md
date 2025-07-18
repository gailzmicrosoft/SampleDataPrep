# Bronze to Silver Notebook - Quick Start

> **Purpose**: Essential steps to run Bronze_to_Silver_Schema_Analysis.ipynb  
> **Time**: 5 minutes setup + notebook execution

## 🚀 Quick Setup Steps

### 1. Activate Environment
```powershell
cd C:\Repos\Code\SampleDataPrep
src\.venv\Scripts\Activate.ps1
```
✅ Look for `(.venv)` in terminal

### 2. Test Environment
```powershell
src\.venv\Scripts\python.exe -c "import pandas; print('✅ Ready')"
```

### 3. Configure VS Code
- Press `Ctrl+Shift+P`
- Type: `Python: Select Interpreter`
- Choose: `src\.venv\Scripts\python.exe`

### 4. Open Notebook
- Navigate to: `src/notebooks/Bronze_to_Silver_Schema_Analysis.ipynb`
- Press `Ctrl+Shift+P` → `Jupyter: Restart Kernel` (if needed)

## ▶️ Execute Notebook

Run each cell in order:

1. **Cell 1-2**: Markdown headers (no execution)
2. **Cell 3**: Configuration imports ✅
3. **Cell 4**: Connectivity test (PySpark errors = normal!)
4. **Cell 5**: Markdown header (no execution)
5. **Cell 6-12**: Continue running (PySpark errors = expected)

## 🎯 Expected Results

- ✅ Pandas imports successfully
- ❌ PySpark errors (normal in local environment)
- ✅ Analysis framework displayed
- ✅ Implementation plan generated

## 🚨 Quick Fixes

**"No module named 'pandas'"**: Re-run steps 1-3

**Kernel hanging**: `Ctrl+Shift+P` → `Jupyter: Restart Kernel`

**Wrong interpreter**: Check bottom-left VS Code status bar

## ✅ Success = Ready for Phase 1

When complete, you'll have the transformation roadmap to create:
- `Customer_Bronze_to_Silver_Transform.ipynb`
- Implementation plan for 4 phases
- Clear next steps for data transformation

---
*PySpark errors are expected - focus on the analysis patterns!*
