# NFRA Financial Compliance System - Complete Flow Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [The Pipeline - Step by Step](#the-pipeline---step-by-step)
4. [Compliance Rules & Frameworks](#compliance-rules--frameworks)
5. [Running the System](#running-the-system)
6. [Understanding the Output](#understanding-the-output)

---

## 🎯 Project Overview

**What is this project?**
This system automatically analyzes financial documents (like annual reports) to:
- Extract financial data (Revenue, Profit, Assets, etc.)
- Check if the company follows financial rules (Compliance)
- Calculate financial health scores
- Answer questions about the document using AI

**Why is it useful?**
- Auditors and regulators can quickly validate financial compliance
- Saves time extracting data manually from documents
- Ensures companies follow required financial standards
- Provides AI-powered insights/answering on complex financial data

**Key Technologies:**
- **OCR (Optical Character Recognition)**: Reads text from PDF documents
- **LLM (Language Model)**: Understands and extracts financial data
- **Compliance Engines**: Checks if data follows regulatory rules
- **RAG (Retrieval Augmented Generation)**: Answers questions using the document

---

## 🏗️ System Architecture

### Three Main Components

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Web Interface)                      │
│              http://localhost:3000/dashboard              │
└────────────────────┬────────────────────────────────────────┘
                     │ Upload PDF
                     ↓
┌─────────────────────────────────────────────────────────────┐
│          FRONTEND (React/Next.js on Port 3000)            │
│   - Upload interface                                       │
│   - Progress tracking                                      │
│   - Results display (formatted + JSON)                     │
└────────────────────┬────────────────────────────────────────┘
                     │ API Calls
                     ↓
┌─────────────────────────────────────────────────────────────┐
│     BACKEND (Node.js API + Python Pipeline)              │
│   ├─ /api/process - Start pipeline job                    │
│   ├─ /api/process/status - Check progress                │
│   └─ /api/process/result - Get results                   │
│                                                            │
│   Spawns Python: nfra_pipeline.py                        │
└────────────────────┬────────────────────────────────────────┘
                     │ Processes PDF
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    EXTERNAL SERVICES (Running on separate VMs)            │
│  - OCR Service: 34.47.203.146:8000 (Reads PDF text)      │
│  - LLM Service: 34.180.45.142:8000 (Extracts data)       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
PDF File
   ↓
[1] OCR Service → Extract text from PDF
   ↓           → Returns: Raw text content
[2] Segmenter  → Find document sections
   ↓           → Returns: Executive Summary, Balance Sheet, etc.
[3] Table      → Extract financial tables
   Extractor   → Returns: Revenue, Profit tables
   ↓
[4] LLM        → Structure financial data
   Service     → Returns: {revenue: 450.5, profit: 78.45, ...}
   ↓
[5] Analytics  → Calculate health score
   Engine      → Returns: Financial ratios, trends, health %
   ↓
[6] Compliance → Check regulatory compliance
   Engine      → Returns: Pass/Fail for IndAS, SEBI, RBI, BRSR
   ↓
[7] Compilation → Combine all results
               → Returns: Final JSON output
   ↓
[8] RAG        → Index for Q&A capability
   Engine      → Returns: Indexed documents
   ↓
Final Output: phase4_<jobId>.json (saved to data/output/results/)
```

---

## 🔄 The Pipeline - Step by Step

### Step 1️⃣: OCR (Optical Character Recognition)

**What it does:**
- Converts PDF pages into images
- Sends images to OCR service (running on 34.47.203.146)
- OCR reads text from images (even if scanned)
- Returns all extracted text as a string

**Input:** PDF file path  
**Output:** Raw text string (entire document)

**Example:**
```
INPUT:  sample_financial_report.pdf
OUTPUT: "TECHCORP FINANCIAL SOLUTIONS LIMITED
         ANNUAL FINANCIAL REPORT 2025-26
         Revenue: ₹450.5 Crores
         ..."
```

**Check:** If OCR fails = ❌ Stop (can't process without text)

---

### Step 2️⃣: Document Segmentation

**What it does:**
- Reads the extracted text
- Finds major sections (Executive Summary, Balance Sheet, Income Statement, etc.)
- Identifies section boundaries and content
- Classifies what type of section each is

**Input:** Raw text from OCR  
**Output:** Structured sections with their content

**Example:**
```
{
  "total_sections_found": 10,
  "sections": [
    {"name": "Executive Summary", "content": "...", "type": "summary"},
    {"name": "Balance Sheet", "content": "...", "type": "financial_statement"},
    {"name": "Income Statement", "content": "...", "type": "financial_statement"}
  ]
}
```

**Why it matters:** 
- Helps focus on relevant sections for analysis
- Improves data extraction accuracy

---

### Step 3️⃣: Table Extraction

**What it does:**
- Finds financial tables in the document text
- Identifies rows and columns
- Extracts numerical data (Revenue, Profit, Assets, etc.)
- Detects table structure and relationships

**Input:** Raw text from OCR  
**Output:** Structured table data

**Example:**
```
{
  "total_tables_found": 5,
  "tables": [
    {
      "name": "Revenue by Segment",
      "data": [
        {"segment": "Advisory", "revenue": "202.7"},
        {"segment": "Technology", "revenue": "157.7"}
      ]
    }
  ]
}
```

**Why it matters:**
- Financial data heavily relies on tables
- Accurate extraction = accurate analysis

---

### Step 4️⃣: LLM Extraction (Language Model)

**What it does:**
- Uses AI (Language Model on 34.180.45.142)
- Understands financial context and terminology
- Extracts structured financial data from text
- Connects related information intelligently

**Input:** Raw text + segmented sections + tables  
**Output:** Structured financial data

**Example:**
```
{
  "company_name": "TechCorp Financial Solutions Limited",
  "fiscal_year": "2025-26",
  "financial_metrics": {
    "revenue": {
      "value": 450.5,
      "currency": "INR",
      "unit": "Crore",
      "ytd_growth": "15%"
    },
    "net_profit": {
      "value": 78.45,
      "currency": "INR",
      "unit": "Crore",
      "ytd_growth": "12%"
    },
    "total_assets": {
      "value": 1245.8,
      "currency": "INR",
      "unit": "Crore"
    }
  }
}
```

**Why it matters:**
- Converts unstructured text to structured data
- Makes data usable for analytics and checks
- Understands context (not just keyword matching)

---

### Step 5️⃣: Financial Analytics

**What it does:**
- Calculates financial ratios (Profitability, Liquidity, Solvency, etc.)
- Analyzes trends (Year-over-Year growth)
- Determines financial health score
- Identifies strengths and weaknesses

**Input:** Structured financial data  
**Output:** Analytics results with metrics and health score

**Key Metrics Calculated:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| Gross Margin | (Revenue - COGS) / Revenue | How much profit from each sale |
| Net Margin | Net Profit / Revenue | Final profit percentage |
| ROA (Return on Assets) | Net Profit / Total Assets | How efficiently assets generate profit |
| ROE (Return on Equity) | Net Profit / Shareholder Equity | Return to shareholders |
| Current Ratio | Current Assets / Current Liabilities | Can company pay short-term debts? |
| Debt-to-Equity | Total Debt / Equity | Balance of financing |

**Health Score Calculation:**
```
Financial Health Score (0-100) = 
  (Profitability Score × 30%) +
  (Liquidity Score × 25%) +
  (Solvency Score × 25%) +
  (Efficiency Score × 20%)
```

**Example Output:**
```
{
  "summary": {
    "financial_health_score": "83.33%",
    "rating": "Excellent"
  },
  "profitability": {
    "gross_margin": "48.3%",
    "net_margin": "17.41%",
    "operating_margin": "19.6%",
    "roe": "21%",
    "roa": "6.3%"
  },
  "liquidity": {
    "current_ratio": "2.0",
    "quick_ratio": "1.8"
  }
}
```

**Why it matters:**
- Shows if company is financially healthy
- Identifies risk areas
- Helps auditors assess viability

---

### Step 6️⃣: Compliance Validation

**What it does:**
- Checks if company follows required financial regulations
- Uses 4 major regulatory frameworks:
  1. **IndAS** (Indian Accounting Standards)
  2. **SEBI** (Securities and Exchange Board)
  3. **RBI** (Reserve Bank of India)
  4. **BRSR** (Business Responsibility and Sustainability Reporting)
- Each framework has specific rules and formats

**Input:** Structured financial data  
**Output:** Compliance status for each framework

**Example Compliance Check:**

```
FRAMEWORK: IndAS (Indian Accounting Standards)
─────────────────────────────────────────────

Rule 1: Assets must be classified into Current/Non-Current
Status: ✓ PASS (Found both classifications)

Rule 2: Revenue must show YoY comparison
Status: ✓ PASS (Found prior year: 391.8 Cr vs 450.5 Cr)

Rule 3: Debt-to-Equity ratio must be disclosed
Status: ✓ PASS (Disclosed as 1.0)

Result: 4/4 rules passed = COMPLIANT
```

**Output Format:**
```
{
  "compliance_score": "40%",
  "findings": [
    {
      "framework": "IndAS",
      "status": "COMPLIANT",
      "findings_count": 4
    },
    {
      "framework": "SEBI",
      "status": "COMPLIANT",
      "findings_count": 5
    }
  ],
  "summary": "Company complies with major frameworks"
}
```

**Why it matters:**
- Ensures legal compliance
- Identifies regulatory violations
- Reduces audit risk

---

### Step 7️⃣: Result Compilation

**What it does:**
- Combines all outputs from steps 1-6
- Creates a comprehensive JSON file with all findings
- Organizes data by category

**Output:** Complete phase4_<jobId>.json file

**File Structure:**
```
{
  "document": {
    "filename": "sample_financial_report.pdf",
    "type": "Annual Report",
    "status": "processed"
  },
  "ocr": { ... },          // Step 1 output
  "segmentation": { ... }, // Step 2 output
  "tables": { ... },       // Step 3 output
  "extraction": { ... },   // Step 4 output
  "analytics": { ... },    // Step 5 output
  "compliance": { ... },   // Step 6 output
  "rag": { ... }          // Step 8 output
}
```

---

### Step 8️⃣: RAG Indexing (Question Answering)

**What it does:**
- Creates a searchable index of the document
- Enables AI to answer questions about the document
- Uses semantic search (finds meaning, not just keywords)
- Stores chunks of content with metadata

**Input:** Complete document content  
**Output:** Indexed database for Q&A

**Example Usage:**
```
User Question: "What was the company's profitability trend?"
↓
RAG searches its index: Finds sections about "net income growth"
↓
Returns: "Net profit grew 12% YoY from ₹70.0 Cr to ₹78.45 Cr"
```

**Why it matters:**
- Enables conversational AI on documents
- Answers complex questions instantly
- No manual data lookup needed

---

## ✅ Compliance Rules & Frameworks

### IndAS (Indian Accounting Standards)

**Purpose:** Standardize how companies present financial statements in India

**Key Rules Checked:**
1. **Classification:** Assets/Liabilities correctly classified (Current/Non-Current)
2. **Valuation:** Assets valued at cost or fair market value
3. **Disclosure:** All material items disclosed with comparatives
4. **Revenue Recognition:** Revenue recognized when performance obligations met
5. **Depreciation:** Fixed assets depreciated over useful life

**Example:**
```
Rule: Balance Sheet must show Assets = Liabilities + Equity
Check: ₹1,245.8 Cr = (₹872.6 Cr + ₹373.2 Cr) ✓ PASS
```

---

### SEBI (Securities and Exchange Board of India)

**Purpose:** Protect investor interests and regulate securities market

**Key Rules Checked:**
1. **Disclosure:** Material information disclosed to public
2. **Fraud Prevention:** No evidence of financial manipulation
3. **Related Parties:** Related party transactions disclosed
4. **Insider Trading:** No suspicious transactions by insiders
5. **Corporate Governance:** Board independence and committees

**Example:**
```
Rule: Company must disclose all related-party transactions
Check: ₹28 Cr related party transactions found and disclosed ✓ PASS
```

---

### RBI (Reserve Bank of India)

**Purpose:** Maintain financial system stability and regulate banks

**Key Rules Checked:**
1. **Capital Adequacy:** Company maintains minimum capital ratios
2. **Liquidity:** Current Ratio ≥ 1.5 (can pay short-term debts)
3. **Asset Quality:** Bad loans ≤ 2% of portfolio
4. **Provisioning:** Adequate reserves for potential losses
5. **Interest Rate Risk:** Interest rate exposure disclosed

**Example:**
```
Rule: Current Ratio must be ≥ 1.5 for liquidity
Check: Current Ratio = 2.0 ✓ PASS (Company has ₹2 for every ₹1 debt)
```

---

### BRSR (Business Responsibility and Sustainability Reporting)

**Purpose:** Ensure companies report on social/environmental impact

**Key Rules Checked:**
1. **ESG Disclosure:** Environmental, Social, Governance data provided
2. **Carbon Footprint:** GHG emissions reported
3. **Employee Welfare:** Employee benefits and safety reported
4. **Community Impact:** Corporate social responsibility disclosed
5. **Board Diversity:** Gender/diversity in management disclosed

**Example:**
```
Rule: Must report women employees percentage
Check: 38% women workforce disclosed ✓ PASS
```

---

## 🚀 Running the System

### Prerequisites

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check Node.js version
node --version    # Should be 14+
npm --version     # Should be 6+
```

### Quick Start (3 Commands)

**Command 1: Start OCR Service**
```bash
# This reads text from PDFs
# Already running on: 34.47.203.146:8000
# (If down locally, follow deployment guide in config/)
```

**Command 2: Start LLM Service**
```bash
# This extracts financial data using AI
# Already running on: 34.180.45.142:8000
# (If down locally, follow deployment guide in config/)
```

**Command 3: Start Frontend & Backend**
```bash
cd /Users/ath1614/YellowSense/IDP2/frontend
npm run dev
```

Then open: **http://localhost:3000/dashboard**

---

### Full Setup (If services are down)

**Step 1: Activate Python Environment**
```bash
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate
```

**Step 2: Install Dependencies**
```bash
# For OCR service
pip install -r config/requirements-ocr.txt

# For LLM service
pip install -r config/requirements-llm.txt

# For main pipeline
pip install -r config/requirements.txt
```

**Step 3: Set Environment Variables**
```bash
# Copy example to actual .env
cp config/.env.example .env

# Edit .env to set service IPs/ports
nano .env
```

**Step 4: Start Services**
```bash
# Terminal 1 - OCR Service
bash scripts/setup/setup_local_ocr_strict.sh

# Terminal 2 - LLM Service
bash scripts/setup/setup_llm_vm.sh

# Terminal 3 - Test Services
bash tests/test_nfra_services.sh
```

**Step 5: Start Frontend**
```bash
# Terminal 4
cd frontend && npm run dev
```

---

### How to Process a Document

#### Method 1: Via Web Interface (Easiest)

```
1. Go to http://localhost:3000/dashboard
2. Click "Choose File" → Select PDF
3. Click "Upload & Process"
4. Watch logs in real-time
5. Click "View Report" when done
6. See formatted results or download JSON
```

#### Method 2: Via Command Line

```bash
# Activate environment
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

# Run pipeline directly
python nfra/nfra_pipeline.py sample_financial_report.pdf \
  --type "Annual Report" \
  --output data/output/results/my_report.json

# View results
cat data/output/results/my_report.json | python -m json.tool
```

#### Method 3: Batch Processing

```bash
# Process multiple documents
cd /Users/ath1614/YellowSense/IDP2
source .venv/bin/activate

python scripts/batch/run_disciplinary_batch.py \
  --input-dir data/input/disciplinary_cases \
  --output-dir data/output/disciplinary_output
```

---

## 📊 Understanding the Output

### Output File Location

After processing, results are saved to:
```
/Users/ath1614/YellowSense/IDP2/data/output/results/phase4_<jobId>.json
```

### Understanding Each Section

#### 1. Document Metadata
```json
{
  "document": {
    "filename": "sample_financial_report.pdf",
    "type": "Annual Report",
    "status": "processed"
  }
}
```
**What it means:** Document info you uploaded

---

#### 2. OCR Results
```json
{
  "ocr": {
    "status": "success",
    "text": "TECHCORP FINANCIAL... [full text]",
    "pages": 25,
    "char_count": 45000
  }
}
```
**What it means:** Text extracted from PDF

**Check:**
- ✓ If char_count > 1000: Good OCR quality
- ✗ If char_count < 100: Poor PDF quality or OCR failed

---

#### 3. Segmentation Results
```json
{
  "segmentation": {
    "total_sections_found": 10,
    "sections": [
      {
        "name": "Executive Summary",
        "start_line": 15,
        "end_line": 45,
        "type": "summary"
      }
    ]
  }
}
```
**What it means:** Document broken into logical sections

**Check:**
- ✓ If total_sections_found ≥ 5: Comprehensive document
- ⚠ If total_sections_found < 3: Incomplete document

---

#### 4. Extraction Results
```json
{
  "extraction": {
    "company": "TechCorp Financial Solutions Limited",
    "financial_metrics": {
      "revenue": {
        "value": 450.5,
        "unit": "Crore",
        "currency": "INR"
      },
      "net_profit": {
        "value": 78.45,
        "unit": "Crore"
      },
      "total_assets": {
        "value": 1245.8,
        "unit": "Crore"
      }
    },
    "auditor": "Deloitte Haskins & Sells LLP",
    "audit_opinion": "Unqualified Opinion"
  }
}
```
**What it means:** Extracted financial data from document

**Check Key Metrics:**
- Revenue: ₹450.5 Cr (Growth 15% YoY ✓)
- Profit: ₹78.45 Cr (Healthy margin ✓)
- Assets: ₹1,245.8 Cr (Strong balance sheet ✓)
- Auditor Opinion: "Unqualified" = No issues found ✓

---

#### 5. Analytics Results
```json
{
  "analytics": {
    "summary": {
      "financial_health_score": "83.33%",
      "rating": "Excellent"
    },
    "profitability": {
      "gross_margin": "48.3%",
      "net_margin": "17.41%",
      "roe": "21%"
    },
    "liquidity": {
      "current_ratio": "2.0",
      "quick_ratio": "1.8"
    },
    "solvency": {
      "debt_to_equity": "1.0",
      "interest_coverage": "11.1x"
    }
  }
}
```
**What it means:** Financial health analysis

**Interpreting Scores:**
| Score | Rating | Meaning |
|-------|--------|---------|
| 80-100% | Excellent | Very healthy company |
| 60-79% | Good | Solid financial position |
| 40-59% | Fair | Some concerns, needs monitoring |
| 20-39% | Poor | Significant risks |
| < 20% | Critical | Company in trouble |

**Key Benchmarks:**
- Current Ratio > 1.5 ✓ Can pay debts
- Debt-to-Equity < 1.5 ✓ Not over-leveraged
- ROE > 15% ✓ Good shareholder returns
- Net Margin > 10% ✓ Profitable operations

---

#### 6. Compliance Results
```json
{
  "compliance": {
    "compliance_score": "40%",
    "summary": {
      "compliant_frameworks": 6,
      "non_compliant": 0,
      "unable_to_verify": 9
    },
    "frameworks": [
      {
        "name": "IndAS",
        "status": "COMPLIANT",
        "findings": 4,
        "rules": [
          {
            "rule": "Assets classify into Current/Non-Current",
            "status": "PASS",
            "evidence": "Found: Current ₹500Cr, Non-Current ₹745.8Cr"
          }
        ]
      }
    ]
  }
}
```
**What it means:** Regulatory compliance check results

**Interpreting Compliance Score:**
| Score | Meaning |
|-------|---------|
| 80-100% | Fully compliant with all regulations |
| 60-79% | Compliant with minor gaps |
| 40-59% | Generally compliant with some issues |
| 20-39% | Notable non-compliance |
| < 20% | Serious regulatory violations |

**Status Meanings:**
- **PASS** (✓): Rule met, evidence found
- **FAIL** (✗): Rule violated, issue found
- **UNABLE_TO_VERIFY** (?): Not enough data to check

---

#### 7. RAG Results
```json
{
  "rag": {
    "status": "success",
    "documents_indexed": 45,
    "chunks_created": 120,
    "query_capability": "enabled"
  }
}
```
**What it means:** Document indexed for Q&A

**Capability:**
- ✓ You can now ask questions about the document
- ✓ AI will find relevant sections and answer
- ✓ Questions like "What was revenue trend?" will work

---

### Dashboard Display

The web interface shows a formatted version:

```
┌─ FINANCIAL METRICS ─────────────────────────────┐
│ Revenue: ₹450.5 Cr (Growth: +15%)              │
│ Net Profit: ₹78.45 Cr (Growth: +12%)           │
│ Health Score: 83.33% ✓ Excellent               │
└──────────────────────────────────────────────────┘

┌─ ANALYTICAL INSIGHTS ───────────────────────────┐
│ • Profitability: Strong (Net Margin 17.41%)    │
│ • Liquidity: Excellent (Current Ratio 2.0x)    │
│ • Solvency: Healthy (Debt-to-Equity 1.0)       │
│ • Efficiency: Good (ROE 21%)                   │
└──────────────────────────────────────────────────┘

┌─ COMPLIANCE ASSESSMENT ─────────────────────────┐
│ ✓ IndAS Compliant                              │
│ ✓ SEBI Compliant                               │
│ ✓ RBI Compliant                                │
│ ? BRSR Unable to Verify (3 items)             │
│ Overall: 40% (Generally Compliant)            │
└──────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
/Users/ath1614/YellowSense/IDP2/
│
├── frontend/                    # React app on port 3000
│   ├── pages/
│   │   ├── index.js           # Landing page
│   │   ├── dashboard.js       # Main upload interface
│   │   ├── result/[jobId].js  # Results display
│   │   └── api/               # API routes
│   │       ├── process.js     # Start job
│   │       ├── process/status.js   # Check status
│   │       └── process/result.js   # Get results
│   └── components/             # React components
│
├── nfra/                        # Python pipeline
│   ├── nfra_pipeline.py        # Main orchestrator (Step 1-8)
│   ├── compliance_engine.py    # Step 6 - Compliance checks
│   ├── document_segmenter.py   # Step 2 - Find sections
│   ├── table_extractor.py      # Step 3 - Extract tables
│   ├── analytics_engine.py     # Step 5 - Calculate metrics
│   ├── rag_engine.py           # Step 8 - Q&A indexing
│   └── rules/                  # Compliance rule files
│       ├── indas_rules.json
│       ├── sebi_rules.json
│       ├── rbi_rules.json
│       └── brsr_rules.json
│
├── data/                        # All data organized here
│   ├── input/                  # Source documents
│   │   ├── samples/            # PDFs to process
│   │   ├── apar_documents/
│   │   └── disciplinary_cases/
│   │
│   └── output/                 # Processing results
│       ├── results/            # JSON outputs
│       ├── jobs/               # Job status files
│       └── [other outputs]
│
├── scripts/                     # Utility scripts
│   ├── setup/                  # Setup scripts
│   ├── deployment/             # Deploy scripts
│   ├── utilities/              # Helper scripts
│   └── batch/                  # Batch processing
│
├── config/                      # Configuration
│   ├── requirements.txt
│   ├── requirements-ocr.txt
│   ├── requirements-llm.txt
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── PROJECT_FLOW.md         # This file
│   ├── IMPLEMENTATION_STATUS.md
│   └── TESTING_GUIDE.md
│
└── sample_financial_report.pdf  # Test document
```

---

## 🔧 Troubleshooting

### OCR Service Not Responding

```bash
# Check service status
curl http://34.47.203.146:8000/health

# If down, restart:
bash scripts/setup/setup_local_ocr_strict.sh
```

### LLM Service Error

```bash
# Check service status
curl http://34.180.45.142:8000/health

# If down, restart:
bash scripts/setup/setup_llm_vm.sh
```

### Pipeline Timeout

```bash
# Increase timeout in nfra/nfra_pipeline.py:
# Change: timeout=300 → timeout=600
```

### Out of Memory

```bash
# Check available memory
free -h

# If low, clear cache:
rm -rf data/cache/*
```

---

## 📞 Quick Reference

### Output Locations
```bash
# Processed PDFs
data/input/samples/

# Results  
data/output/results/

# Job tracking
data/output/jobs/

# Configuration
config/
```

### Key Commands
```bash
# Check services
bash tests/test_nfra_services.sh

# Process single document
python nfra/nfra_pipeline.py <pdf_path> --output results.json

# Batch processing
python scripts/batch/run_disciplinary_batch.py --input-dir <dir>

# Start web interface
cd frontend && npm run dev
```

### Key URLs
```
Dashboard:    http://localhost:3000/dashboard
API Root:     http://localhost:3000/api
OCR Service:  http://34.47.203.146:8000
LLM Service:  http://34.180.45.142:8000
```

---

## 🎓 Learning Path

1. **Understand the basics** (Read this flow guide)
2. **Run the demo** (Upload sample_financial_report.pdf)
3. **Review the output** (Check JSON and formatted report)
4. **Try compliance** (Check which rules pass/fail)
5. **Analyze metrics** (Understand health score breakdown)
6. **Build custom rules** (Edit rules/ JSON files)
7. **Deploy to production** (Set up proper infrastructure)

---

## 📚 Related Documentation

- [Implementation Status](IMPLEMENTATION_STATUS.md) - What's been built
- [Testing Guide](TESTING_GUIDE.md) - How to test each component
- [Compliance Framework](PROJECT_ANALYSIS.md) - Deep dive into rules
- [API Reference](API_REFERENCE.md) - API endpoint details

---

**Last Updated:** 17 February 2026  
**System Status:** ✓ Operational  
**Components:** All functional  
**Services:** Online and ready
