# IDP2 Project Structure (Clean - IDP Only)

## 🎯 Project Scope
**Intelligent Document Processing for Government Documents**
- APAR (Annual Performance Appraisal Reports)
- Disciplinary Cases

## 📁 Directory Structure

```
IDP2/
├── config/                    # Configuration files
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-ocr.txt   # OCR dependencies
│   ├── requirements-llm.txt   # LLM dependencies
│   ├── config.yaml           # Pipeline config
│   └── .env.example          # Environment template
│
├── data/                      # Data files
│   ├── APAR -Ravinesh 1.pdf  # APAR sample
│   ├── APAR 1.pdf            # APAR sample
│   ├── Charge Memorandum.pdf # Disciplinary sample
│   ├── Disciplinary cases/   # Disciplinary documents
│   ├── input/                # Input directory
│   ├── output/               # Generated outputs
│   ├── cache/                # Cached data
│   ├── prompts/              # LLM prompts
│   └── ground_truth/         # Benchmark data
│
├── src/                       # Source code
│   ├── process_pipeline.py   # Main IDP pipeline
│   ├── ocr_service.py        # OCR service client
│   ├── llm_service.py        # LLM service client
│   ├── run_ocr.py            # OCR runner
│   ├── services/             # Service modules
│   └── utils/                # Utility functions
│
├── scripts/                   # Scripts
│   ├── batch/
│   │   ├── run_apar_batch.py        # APAR batch processing
│   │   └── run_disciplinary_batch.py # Disciplinary batch
│   ├── utilities/
│   │   ├── flatten_apar.py          # APAR utilities
│   │   ├── flatten_docx.py          # DOCX utilities
│   │   └── convert_pdf_to_docx.py   # Conversion
│   ├── vm/                   # VM management
│   ├── setup/                # Setup scripts
│   └── deployment/           # Deployment scripts
│
├── tests/                     # Test files
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── sample_outputs/       # Test outputs
│
├── docs/                      # Documentation
│   ├── API_REFERENCE.md      # API docs
│   ├── COMMANDS.md           # Command reference
│   ├── PROJECT_FLOW.md       # Workflow
│   ├── QUICKSTART.md         # Quick start
│   └── problem_statement.txt # Problem statement
│
├── .env                       # Environment variables
├── .gitignore                # Git ignore
└── README.md                 # Main documentation
```

## 🔑 Key Files

### Core Pipeline
- **`src/process_pipeline.py`** - Main IDP pipeline orchestrator
  - OCR processing
  - Document classification (APAR/Disciplinary)
  - LLM extraction
  - Output generation (DOCX/PDF/JSON)

### Batch Processing
- **`scripts/batch/run_apar_batch.py`** - Process multiple APAR documents
- **`scripts/batch/run_disciplinary_batch.py`** - Process multiple disciplinary cases

### Services
- **`src/ocr_service.py`** - Surya OCR integration
- **`src/llm_service.py`** - LLM service integration
- **`src/run_ocr.py`** - OCR execution wrapper

## 📊 Data Flow

```
Input PDF
    ↓
OCR Service (Surya)
    ↓
Text Extraction
    ↓
Document Classification
    ↓
LLM Processing (Qwen/Llama)
    ↓
Structured Extraction
    ↓
Output Generation
    ↓
DOCX/PDF/JSON
```

## 🎯 Processing Modes

### 1. APAR Mode (`--mode apar`)
- Extracts officer details
- Grading information
- Pen-picture analysis
- Outputs: DOCX table + JSON

### 2. Disciplinary Mode (`--mode summary`)
- Executive summary generation
- Allegations extraction
- Evidence compilation
- Chronology building
- Outputs: PDF report + JSON

### 3. Auto Mode (`--mode auto`)
- Automatic classification
- Selects appropriate processing

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
OCR_VM_IP=34.47.176.38
LLM_VM_IP=34.93.108.135
```

### Pipeline Config (`config/config.yaml`)
- Timeout settings
- Batch sizes
- Model parameters

## 📈 Output Structure

### APAR Output
```
output/
└── <document_name>/
    ├── <document_name>.docx    # Formatted table
    └── <document_name>.json    # Structured data
```

### Disciplinary Output
```
output/
└── <document_name>/
    ├── <document_name>_Summary.pdf  # Executive summary
    └── <document_name>.json         # Structured data
```

## 🧹 Cleanup Summary

**Removed NFRA Components:**
- ❌ `nfra/` - NFRA compliance engine
- ❌ `frontend/` - Next.js dashboard
- ❌ `docs/reports/` - NFRA reports
- ❌ `docs/analysis/` - NFRA analysis
- ❌ `docs/pitch/` - Pitch decks
- ❌ NFRA-specific documentation

**Kept IDP Components:**
- ✅ Core pipeline (`src/process_pipeline.py`)
- ✅ Batch scripts (APAR/Disciplinary)
- ✅ Sample data (APAR/Disciplinary PDFs)
- ✅ Shared services (OCR/LLM)
- ✅ IDP documentation

## 📝 Notes

- NFRA project moved to `/Users/ath1614/YellowSense/NFRA_CLEAN/`
- Shared infrastructure (OCR/LLM services) retained
- VM scripts retained for deployment
- All IDP functionality preserved
