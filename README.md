# Intelligent Document Processing (IDP) Pipeline

Automated pipeline for processing, extracting, and summarizing complex government documents: **Disciplinary Cases** and **Annual Performance Appraisal Reports (APAR)**.

## 🌟 Features

- **Automated Classification**: Detects document type (Disciplinary/APAR)
- **Robust OCR**: Surya OCR service on VM for scanned PDFs
- **LLM-Powered Extraction**:
  - **Disciplinary Cases**: Executive summaries (PDF) with allegations, evidence, chronology
  - **APAR**: Structured grading and pen-picture extraction
- **Batch Processing**: Process entire directories efficiently
- **Resilience**: Handles large documents via chunking and Map-Reduce

## 📂 Structure

```
IDP2/
├── src/
│   └── process_pipeline.py    # Main pipeline
├── scripts/
│   └── batch/
│       ├── run_apar_batch.py
│       └── run_disciplinary_batch.py
├── data/
│   ├── APAR*.pdf              # APAR samples
│   └── Disciplinary cases/    # Disciplinary samples
└── docs/                      # Documentation
```

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r config/requirements.txt
```

### Process Single Document
```bash
python src/process_pipeline.py data/APAR\ 1.pdf --mode apar
python src/process_pipeline.py data/Charge\ Memorandum.pdf --mode summary
```

### Batch Processing

**APAR Documents:**
```bash
python scripts/batch/run_apar_batch.py --source data/
```

**Disciplinary Cases:**
```bash
python scripts/batch/run_disciplinary_batch.py
```

## 🔧 Configuration

Configure VM endpoints in `.env`:
```bash
OCR_VM_IP=34.47.176.38
LLM_VM_IP=34.93.108.135
```

## 📊 Output

### APAR
- Structured DOCX table with grading and pen-pictures
- JSON data extraction

### Disciplinary Cases
- Executive summary PDF
- Comprehensive case analysis
- JSON structured data

## 📖 Documentation

- [Commands Guide](docs/COMMANDS.md) - Detailed command reference
- [API Reference](docs/API_REFERENCE.md) - API documentation
- [Project Flow](docs/PROJECT_FLOW.md) - Pipeline workflow

## 🏗️ Architecture

```
PDF Input → OCR (Surya) → LLM (Qwen/Llama) → Extraction → Output (DOCX/PDF/JSON)
```

## 📝 License

Proprietary - YellowSense Technologies Private Limited
