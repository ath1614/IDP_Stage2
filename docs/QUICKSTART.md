# Quick Start Guide - NFRA Compliance System

## 🚀 Start in 3 Steps

### Step 1: Start Frontend (1 command)
```bash
cd /Users/ath1614/YellowSense/IDP2/frontend
npm run dev
```
✓ Opens automatically at **http://localhost:3000/dashboard**

### Step 2: Upload PDF
- Click "Choose File" 
- Select `sample_financial_report.pdf` (already in root)
- Click "Upload & Process"

### Step 3: View Results
- Watch progress in real-time
- Click "View Report" when done
- See formatted results or download JSON

---

## 📊 What You'll See

```
Dashboard shows:
├── Upload Form (drag & drop enabled)
├── Live Progress Bar (0-100%)
├── Processing Logs (real-time updates)
├── Results Link (click to view)
└── Download Options (JSON + formatted report)

Results Page shows:
├── Financial Metrics (Revenue, Profit, etc.)
├── Health Score (0-100%)
├── Compliance Status (4 frameworks)
├── Detailed Analytics (all ratios)
└── RAG Q&A Capability
```

---

## 🔍 Key Metrics to Look For

| Metric | Good Range | What It Means |
|--------|------------|---------------|
| Health Score | 80%+ | Company is financially healthy |
| Current Ratio | 1.5-2.0 | Can pay short-term debts |
| Net Margin | 10%+ | Profitable operations |
| Debt-to-Equity | <1.5 | Not over-leveraged |
| ROE | 15%+ | Good shareholder returns |
| Compliance | 60%+ | Following regulations |

---

## 💾 Where Results Are Saved

```
After processing, check:
├── Web UI at: http://localhost:3000/result/<jobId>
├── JSON file at: data/output/results/phase4_<jobId>.json
├── Status logs at: data/output/jobs/<jobId>.status.json
└── Original PDF at: data/input/samples/<jobId>_<filename>.pdf
```

---

## ⚡ Command Reference

### Run Pipeline from Terminal
```bash
# Activate environment
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Process a PDF
python nfra/nfra_pipeline.py sample_financial_report.pdf \
  --output data/output/results/report.json

# View results
cat data/output/results/report.json | python -m json.tool | head -50
```

### Batch Process Multiple Files
```bash
python scripts/batch/run_disciplinary_batch.py \
  --input-dir data/input/disciplinary_cases \
  --output-dir data/output/disciplinary_output
```

### Check Service Status
```bash
bash tests/test_nfra_services.sh
```

---

## 🐛 If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Port 3000 already in use | `lsof -i :3000 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| npm modules not found | `cd frontend && npm install` |
| Python not found | `cd /Users/ath1614/YellowSense/IDP2 && source .venv/bin/activate` |
| OCR service down | Check: `curl http://34.47.203.146:8000/health` |
| LLM service down | Check: `curl http://34.180.45.142:8000/health` |
| Results not showing | Wait 30+ seconds, refresh page, or check `data/output/results/` |

---

## 📖 Learn More

- **Full Guide:** [docs/PROJECT_FLOW.md](../docs/PROJECT_FLOW.md)
  - Complete pipeline explanation
  - What each step does
  - How to interpret results
  - Compliance rules breakdown

- **Implementation Status:** [docs/IMPLEMENTATION_STATUS.md](../docs/IMPLEMENTATION_STATUS.md)
  - What's been built
  - What's working
  - Known issues

- **Testing Guide:** [docs/TESTING_GUIDE.md](../docs/TESTING_GUIDE.md)
  - How to test components
  - Example test cases
  - Debugging tips

---

## 🎯 Sample Outputs Explained

### Health Score Breakdown
```
Financial Health = 83.33%
├── Profitability (30%): 28% score → 8.4 points
├── Liquidity (25%): 25% score → 6.25 points  
├── Solvency (25%): 23% score → 5.75 points
└── Efficiency (20%): 19% score → 3.8 points
   = 8.4 + 6.25 + 5.75 + 3.8 = 24.2 out of 29 = 83%
```

### Compliance Summary
```
Overall: 40% Compliant
├── IndAS: ✓ PASS (4 rules checked, all passed)
├── SEBI: ✓ PASS (5 rules checked, all passed)
├── RBI: ✓ PASS (3 rules checked, all passed)
└── BRSR: ? Unable to Verify (only 3 of 9 rules could verify)
```

### Sample JSON Structure
```json
{
  "document": {"filename": "...", "type": "...", "status": "processed"},
  "ocr": {"status": "success", "text": "...", "pages": 25},
  "segmentation": {"total_sections_found": 10, "sections": [...]},
  "extraction": {"revenue": 450.5, "assets": 1245.8, ...},
  "analytics": {"health_score": "83.33%", "metrics": {...}},
  "compliance": {"compliance_score": "40%", "frameworks": [...]},
  "rag": {"status": "success", "documents_indexed": 45}
}
```

---

## 🌐 API Endpoints (for advanced users)

```bash
# Upload and start processing
POST /api/process
Body: {filename: "...", filedata: "base64..."}

# Check job status
GET /api/process/status?jobId=<jobId>

# Get completed results
GET /api/process/result?jobId=<jobId>

# Get latest test summary
GET /api/summary
```

---

## 📧 File Locations

```
Code:
├── Frontend: frontend/
├── Pipeline: nfra/
├── Scripts: scripts/
└── Tests: tests/

Data:
├── Inputs: data/input/
├── Outputs: data/output/results/
├── Jobs: data/output/jobs/
└── Config: config/

Docs:
├── This guide: docs/QUICKSTART.md
├── Full flow: docs/PROJECT_FLOW.md
├── Implementation: docs/IMPLEMENTATION_STATUS.md
└── Testing: docs/TESTING_GUIDE.md
```

---

## ✅ Checklist to Get Started

- [ ] Navigate to `/Users/ath1614/YellowSense/IDP2`
- [ ] Run: `cd frontend && npm run dev`
- [ ] Open: http://localhost:3000/dashboard
- [ ] Upload: `sample_financial_report.pdf` (in root)
- [ ] Wait: For processing to complete (60-90 seconds)
- [ ] View: Results in formatted or JSON view
- [ ] Download: JSON or formatted report
- [ ] Check: `data/output/results/` folder for files

---

**Ready?** Start with Step 1 above! 🚀
