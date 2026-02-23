# System Commands & Running Guide

## 📖 Overview

This document lists all commands to run the NFRA system.

---

## 🎯 Quick Start (Fastest Way)

**One-liner to start everything:**
```bash
cd /Users/ath1614/YellowSense/IDP2/frontend && npm run dev
```

Then open: **http://localhost:3000/dashboard**

**That's it!** Everything else runs automatically.

---

## 🚀 Running the System

### Environment Setup (One Time)

```bash
# Navigate to project
cd /Users/ath1614/YellowSense/IDP2

# Activate Python environment
source .venv/bin/activate

# Install Python dependencies
pip install -r config/requirements.txt
pip install -r config/requirements-ocr.txt
pip install -r config/requirements-llm.txt
```

### Start Frontend + Backend

```bash
# Terminal 1: Start backend + frontend
cd /Users/ath1614/YellowSense/IDP2/frontend
npm run dev

# Automatically starts:
# - Backend API on port 3000
# - Frontend on http://localhost:3000
# - Next.js dev server
```

### Start External Services (If Needed)

```bash
# Terminal 2: OCR Service
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate
bash scripts/setup/setup_local_ocr_strict.sh

# Terminal 3: LLM Service  
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate
bash scripts/setup/setup_llm_vm.sh
```

### Usage

1. Open browser: http://localhost:3000/dashboard
2. Click "Choose File"
3. Select PDF (e.g., `sample_financial_report.pdf`)
4. Click "Upload & Process"
5. Wait for completion (60-90 seconds)
6. Click "View Report"

---

## 🏃 Common Commands

### Check If Services Are Running

```bash
# Check OCR service
curl http://34.47.203.146:8000/health
# Expected: 200 OK

# Check LLM service
curl http://34.180.45.142:8000/health
# Expected: 200 OK

# Check frontend
curl http://localhost:3000
# Expected: 200 OK (HTML page)
```

### Process Single PDF (Terminal)

```bash
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Basic usage
python nfra/nfra_pipeline.py sample_financial_report.pdf

# With custom output file
python nfra/nfra_pipeline.py sample_financial_report.pdf \
  --output data/output/results/my_report.json

# With document type
python nfra/nfra_pipeline.py sample_financial_report.pdf \
  --type "Annual Report" \
  --output data/output/results/my_report.json
```

### View Results

```bash
# List all results
ls -lh data/output/results/

# View specific result
cat data/output/results/phase4_*.json | python -m json.tool | head -100

# Count results
ls -1 data/output/results/*.json | wc -l
```

### Batch Processing

```bash
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Process files in a directory
python scripts/batch/run_disciplinary_batch.py \
  --input-dir data/input/disciplinary_cases \
  --output-dir data/output/disciplinary_output
```

### Clear Cache/Old Runs

```bash
# Remove old job tracking
rm -rf data/output/jobs/*

# Remove old uploads
rm -rf data/input/samples/*

# Remove old results
rm -rf data/output/results/phase4_*.json

# Clear temp files
rm -rf data/cache/*
```

---

## 🧪 Testing Commands

### Test All Services

```bash
cd /Users/ath1614/YellowSense/IDP2
bash tests/test_nfra_services.sh
```

Output shows:
- ✓ OCR service health
- ✓ LLM service health  
- ✓ Configuration loaded
- ✓ Services ready

### Test Individual Modules

```bash
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Test OCR
python scripts/utilities/run_ocr.py sample_financial_report.pdf

# Test compliance checking
python -c "from nfra.compliance_engine import ComplianceEngine; print('✓ Compliance engine works')"

# Test analytics
python -c "from nfra.analytics_engine import FinancialAnalyzer; print('✓ Analytics engine works')"
```

### Performance Benchmark

```bash
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Benchmark pipeline (measures time for each step)
python tests/sample_outputs/benchmark.py
```

---

## 📊 Viewing Results

### Via Web Interface

```
1. http://localhost:3000/dashboard
   ↓
2. Click "View Report" button
   ↓
3. Two views available:
   - "Formatted Report" (beautiful UI)
   - "Raw JSON" (dev view)
```

### Via Terminal

```bash
# View entire JSON (formatted)
cat data/output/results/phase4_*.json | python -m json.tool

# View specific section
cat data/output/results/phase4_*.json | python -c "
import sys, json
data = json.load(sys.stdin)
print(json.dumps(data['analytics'], indent=2))
"

# Quick health score
cat data/output/results/phase4_*.json | python -c "
import sys, json
data = json.load(sys.stdin)
score = data.get('analytics', {}).get('summary', {}).get('financial_health_score')
print(f'Health Score: {score}')
"
```

### Via Python Script

```python
import json

# Load results
with open('data/output/results/phase4_<jobId>.json') as f:
    results = json.load(f)

# Print analytics
analytics = results['analytics']['summary']
print(f"Health Score: {analytics['financial_health_score']}")

# Print compliance
compliance = results['compliance']['compliance_score']
print(f"Compliance: {compliance}")

# Print extraction
extraction = results['extraction']['financial_metrics']
revenue = extraction['revenue']['value']
print(f"Revenue: ₹{revenue} Cr")
```

---

## 🔧 Configuration & Customization

### Environment Variables

```bash
# Copy example
cp config/.env.example .env

# Edit to customize
nano .env

# Key variables:
# NFRA_OCR_VM_IP=34.47.203.146      # OCR service IP
# NFRA_LLM_VM_IP=34.180.45.142      # LLM service IP
# NFRA_OCR_PORT=8000                # OCR port
# NFRA_LLM_PORT=8000                # LLM port
```

### Compliance Rules

```bash
# Edit rules that are checked
nano nfra/rules/indas_rules.json
nano nfra/rules/sebi_rules.json
nano nfra/rules/rbi_rules.json
nano nfra/rules/brsr_rules.json

# Format: JSON with rule definitions
# { "rule_id": "...", "description": "...", "check": [...] }
```

### Pipeline Configuration

```bash
# Edit pipeline settings
nano nfra/config.yaml

# Settings:
# timeout: Request timeout
# batch_size: OCR batch processing
# chunk_size: Text segmentation
# model: LLM model to use
```

---

## 🐛 Debugging

### See Pipeline Logs

```bash
# Watch real-time logs while processing
cd /Users/ath1614/YellowSense/IDP2
tail -f data/output/jobs/*.status.json

# Or from web interface:
# Dashboard shows live logs in scroll box
```

### Enable Debug Mode

```bash
# Python verbose output
python -v nfra/nfra_pipeline.py sample_financial_report.pdf

# Or set debug environment variable
DEBUG=1 python nfra/nfra_pipeline.py sample_financial_report.pdf
```

### Check What Went Wrong

```bash
cd /Users/ath1614/YellowSense/IDP2

# See error logs  
cat data/output/jobs/<jobId>.status.json | python -m json.tool

# Extract only error messages
cat data/output/jobs/<jobId>.status.json | \
  python -c "import sys,json; d=json.load(sys.stdin); [print(l) for l in d['logs'] if 'ERR' in l]"

# Check if services are responding
for service in OCR LLM; do
  curl -s http://service:8000/health && echo "$service OK" || echo "$service DOWN"
done
```

---

## 📦 Deployment

### Deploy to Production Server

```bash
# 1. Copy project to server
scp -r /Users/ath1614/YellowSense/IDP2 user@server:/var/www/

# 2. Install on server
ssh user@server
cd /var/www/IDP2
bash scripts/setup/setup_local.sh

# 3. Start services
cd /var/www/IDP2/frontend
npm run build
npm run start
```

### Docker Deployment (Future)

```bash
# Build Docker image
docker build -t nfra-system .

# Run container
docker run -p 3000:3000 -v /data:/app/data nfra-system

# Access at: http://server:3000
```

---

## 🚨 Troubleshooting Commands

### Port Already in Use

```bash
# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 8000 (services)
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Wait and restart
sleep 2
cd frontend && npm run dev
```

### Out of Memory

```bash
# Check memory usage
free -h

# Clear cache
rm -rf data/cache/*

# Clear node modules cache
cd frontend && rm -rf node_modules/.cache

# Restart with memory limit
node --max-old-space-size=4096 /path/to/server.js
```

### Database/File Lock Issues

```bash
# Remove lock files
rm -f data/output/jobs/*.lock
rm -f data/output/results/*.lock

# Force restart
pkill -f python
pkill -f node
sleep 2
cd frontend && npm run dev
```

### Service Connection Issues

```bash
# Test OCR connection
python -c "import requests; print(requests.get('http://34.47.203.146:8000/health').status_code)"

# Test LLM connection
python -c "import requests; print(requests.get('http://34.180.45.142:8000/health').status_code)"

# Check network
ping 34.47.203.146
ping 34.180.45.142

# Check firewall
sudo ufw status
```

---

## 📊 Monitoring

### System Resources

```bash
# Check CPU/Memory
top -l 1 | grep -E "^CPU|^Mem"

# Check disk space
df -h | grep "/Volumes\|/Users"

# Monitor in real-time
watch -n 2 'free -h && echo --- && df -h'
```

### Log Monitoring

```bash
# Follow job logs
watch -n 1 'ls -lt data/output/jobs/*.status.json | head -3'

# Count results generated
watch -n 5 'echo "Results: $(ls -1 data/output/results/phase4_*.json 2>/dev/null | wc -l)"'

# Monitor file sizes
du -sh data/output/results data/input/samples
```

---

## 📝 Common Workflows

### Process & Download Results

```bash
# 1. Upload via web interface
# 2. Check status
curl http://localhost:3000/api/process/status?jobId=<JOB_ID>

# 3. When complete, download
curl http://localhost:3000/api/process/result?jobId=<JOB_ID> > results.json

# 4. View locally
cat results.json | python -m json.tool | less
```

### Batch & Archive

```bash
# 1. Process batch
python scripts/batch/run_disciplinary_batch.py \
  --input-dir data/input/disciplinary_cases \
  --output-dir data/output/disciplinary_output

# 2. Archive results
tar -czf data/output/results.tar.gz data/output/results/

# 3. Backup
cp -r data/output/results /backup/nfra_results_$(date +%Y%m%d)
```

### Compare Results

```bash
# Generate report comparing two runs
python -c "
import json
from pathlib import Path

results = list(Path('data/output/results').glob('phase4_*.json'))
results.sort()

for r in results[-2:]:
    with open(r) as f:
        d = json.load(f)
        score = d['analytics']['summary']['financial_health_score']
        print(f'{r.name}: {score}')
"
```

---

## 🎓 Learning Commands

### Understand the Pipeline

```bash
# Read main pipeline code
cat nfra/nfra_pipeline.py | head -100

# See all modules
ls -la nfra/*.py

# Check rules by framework
jq . nfra/rules/indas_rules.json | head -20
```

### Trace Execution

```bash
# Run with strace (shows all system calls)
strace -o trace.log python nfra/nfra_pipeline.py sample_financial_report.pdf

# See what files were created
cat trace.log | grep "open\|write" | tail -20
```

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:3000/dashboard |
| API Root | http://localhost:3000/api |
| OCR Service | http://34.47.203.146:8000 |
| LLM Service | http://34.180.45.142:8000 |
| Flow Guide | [docs/PROJECT_FLOW.md](docs/PROJECT_FLOW.md) |
| API Reference | [docs/API_REFERENCE.md](docs/API_REFERENCE.md) |
| Quick Start | [docs/QUICKSTART.md](docs/QUICKSTART.md) |

---

## ✅ Startup Checklist

Before running system:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Node.js 14+ installed: `node --version`
- [ ] Project folder exists: `ls /Users/ath1614/YellowSense/IDP2`
- [ ] .venv activated: `source .venv/bin/activate`
- [ ] Dependencies installed: `pip list | grep torch`
- [ ] Port 3000 is free: `lsof -i :3000 || echo "Free"`
- [ ] Services online: Run `tests/test_nfra_services.sh`
- [ ] Sample PDF exists: `ls sample_financial_report.pdf`

Ready? Run: `cd frontend && npm run dev`

