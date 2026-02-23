# Project Analysis: IDP vs NFRA Files

## 🎯 Project Scope Identification

This repository contains **TWO SEPARATE PROJECTS**:

### 1. **IDP (Intelligent Document Processing)** - APAR & Disciplinary Cases
- **Purpose**: Process government documents (APAR reports and Disciplinary cases)
- **Original Project**: As per README.md pinned context

### 2. **NFRA (Financial Compliance Engine)** - IndiaAI Challenge
- **Purpose**: Financial reporting compliance for IndiaAI Challenge
- **Added Later**: Separate project built on same infrastructure

---

## 📁 File Classification

### ✅ IDP FILES (APAR/Disciplinary - KEEP)

#### Core Pipeline
- `src/process_pipeline.py` - **IDP MAIN PIPELINE** (APAR/Disciplinary processing)
- `src/ocr_service.py` - OCR service (shared)
- `src/llm_service.py` - LLM service (shared)
- `src/run_ocr.py` - OCR runner (shared)

#### Scripts
- `scripts/batch/run_apar_batch.py` - **IDP: APAR batch processing**
- `scripts/batch/run_disciplinary_batch.py` - **IDP: Disciplinary batch processing**
- `scripts/utilities/flatten_apar.py` - APAR utility
- `scripts/utilities/flatten_docx.py` - Document utility
- `scripts/utilities/convert_pdf_to_docx.py` - Conversion utility

#### Data
- `data/APAR -Ravinesh 1.pdf` - **IDP: APAR sample**
- `data/APAR 1.pdf` - **IDP: APAR sample**
- `data/Charge Memorandum.pdf` - **IDP: Disciplinary sample**
- `data/Disciplinary cases/` - **IDP: Disciplinary documents folder**
- `data/pdf1.pdf` - Test file
- `data/test.pdf` - Test file

#### Documentation
- `README.md` - **IDP: Main documentation**
- `docs/QUICKSTART.md` - Mixed (mostly NFRA but references IDP)
- `docs/COMMANDS.md` - Mixed (mostly NFRA)
- `docs/API_REFERENCE.md` - Shared

---

### ❌ NFRA FILES (Financial Compliance - SEPARATE PROJECT)

#### Core Engine
- `nfra/` - **ENTIRE NFRA DIRECTORY**
  - `nfra/nfra_pipeline.py` - NFRA main pipeline
  - `nfra/compliance_engine.py` - Compliance checking
  - `nfra/analytics_engine.py` - Financial analytics
  - `nfra/rag_engine.py` - RAG system
  - `nfra/report_generator.py` - Report generation
  - `nfra/document_segmenter.py` - Document segmentation
  - `nfra/hyperlink_extractor.py` - Hyperlink extraction
  - `nfra/table_extractor.py` - Table extraction
  - `nfra/excel_csv_parser.py` - Excel/CSV parsing
  - `nfra/insight_bot.py` - Insight bot
  - `nfra/rule_mapper.py` - Rule mapping
  - `nfra/config.yaml` - NFRA config
  - `nfra/rules/` - Compliance rules
  - `nfra/regulations/` - Regulatory documents
  - `nfra/prompts/` - LLM prompts
  - `nfra/data/` - NFRA data

#### Frontend
- `frontend/` - **NFRA Dashboard** (Next.js)
- `NFRA-Frontend/` - Duplicate/old frontend

#### Scripts
- `scripts/utilities/generate_compliance_report.py` - NFRA report generation
- `scripts/utilities/generate_india_ai_report.py` - IndiaAI report
- `scripts/utilities/generate_sample_report.py` - Sample report

#### Data
- `data/samples/sample_financial_report.pdf` - **NFRA: Financial report**
- `data/samples/sample_financial_data.csv` - NFRA data
- `data/samples/sample_financial_data.xlsx` - NFRA data
- `data/samples/create_sample_excel.py` - NFRA data generator
- `uploads/` - **NFRA: Uploaded financial reports**

#### Documentation - NFRA Specific
- `docs/EXECUTIVE_SUMMARY_NFRA.md` - **NFRA**
- `docs/README_NFRA.md` - **NFRA**
- `docs/EXCEL_CSV_DISPLAY_FIX.md` - **NFRA**
- `docs/EXCEL_CSV_WORKING.md` - **NFRA**
- `docs/TEST_SYNTHETIC_DATA.md` - **NFRA**
- `docs/analysis/COMPLIANCE_ANALYSIS.md` - **NFRA**
- `docs/analysis/FRONTEND_BACKEND_ANALYSIS.md` - **NFRA**
- `docs/analysis/GAP_ANALYSIS_REPORT.md` - **NFRA**
- `docs/analysis/IMPLEMENTATION_UPDATE.md` - **NFRA**
- `docs/analysis/PHASE1_IMPLEMENTATION.md` - **NFRA**
- `docs/analysis/SOLUTION_DELIVERED.md` - **NFRA**
- `docs/pitch/` - **ALL NFRA pitch deck files**
- `docs/reports/APPLICATION_FORM_DETAILS.md` - **NFRA**
- `docs/reports/COMPREHENSIVE_AUDIT_REPORT.md` - **NFRA**
- `docs/reports/IndiaAI_Challenge_Report.pdf` - **NFRA**
- `docs/reports/Master_Technical_Report.pdf` - **NFRA**
- `docs/reports/PROBLEM_STATEMENT_COMPLIANCE_REPORT.pdf` - **NFRA**
- `docs/logo11.png` - **NFRA logo**

#### Source Code
- `src/nfra/` - NFRA source modules
- `src/benchmark_pipeline.py` - NFRA benchmarking
- `src/metrics_utils.py` - NFRA metrics

#### Tests
- `tests/test_nfra_services.sh` - **NFRA tests**
- Most test files are NFRA-related

---

### 🔄 SHARED FILES (Used by Both)

#### Infrastructure
- `src/ocr_service.py` - OCR service
- `src/llm_service.py` - LLM service
- `src/run_ocr.py` - OCR runner
- `scripts/vm/` - VM management scripts
- `scripts/setup/` - Setup scripts
- `scripts/deployment/` - Deployment scripts
- `.env` - Environment variables
- `config/` - Configuration files

---

## 📊 Summary Statistics

### IDP Project (APAR/Disciplinary)
- **Core Files**: 3 (process_pipeline.py + 2 batch scripts)
- **Data Files**: 4 PDFs + 1 folder
- **Documentation**: 1 main README
- **Purpose**: Government document processing

### NFRA Project (Financial Compliance)
- **Core Files**: 15+ Python modules in nfra/
- **Frontend**: Full Next.js application
- **Data Files**: 5+ financial reports
- **Documentation**: 20+ documents
- **Purpose**: IndiaAI Challenge submission

### Shared Infrastructure
- **OCR/LLM Services**: 3 files
- **VM Scripts**: 5+ files
- **Config**: Multiple files

---

## 🎯 Recommendations

### Option 1: Keep Both Projects Together
**Pros**: Shared infrastructure, single deployment
**Cons**: Confusing structure, mixed documentation

### Option 2: Separate Projects (RECOMMENDED)
**Pros**: Clear separation, easier maintenance
**Cons**: Duplicate infrastructure code

### Suggested Structure:
```
YellowSense/
├── IDP2/                    # APAR/Disciplinary (Original)
│   ├── src/
│   │   └── process_pipeline.py
│   ├── scripts/
│   │   └── batch/
│   │       ├── run_apar_batch.py
│   │       └── run_disciplinary_batch.py
│   ├── data/
│   │   ├── APAR*.pdf
│   │   └── Disciplinary cases/
│   └── README.md
│
├── NFRA/                    # Financial Compliance (New)
│   ├── nfra/
│   ├── frontend/
│   ├── docs/
│   └── README.md
│
└── shared/                  # Shared Infrastructure
    ├── ocr_service.py
    ├── llm_service.py
    └── vm_scripts/
```

---

## 🚀 Next Steps

1. **Decide**: Keep together or separate?
2. **If Separate**: 
   - Move NFRA files to `/Users/ath1614/YellowSense/NFRA_CLEAN` (already exists!)
   - Keep IDP files in `/Users/ath1614/YellowSense/IDP2`
   - Create shared library for common code
3. **If Together**: 
   - Rename to `YellowSense-Platform`
   - Clear documentation separating the two projects
   - Update README to explain both projects

---

## 📝 File Count

- **Total Files in Root (before cleanup)**: 41
- **IDP-specific files**: ~15
- **NFRA-specific files**: ~60+
- **Shared infrastructure**: ~10
- **After cleanup**: 3 in root + organized subdirectories
