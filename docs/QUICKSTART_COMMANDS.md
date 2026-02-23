# 🚀 IDP Pipeline - Quick Start

## One-Line Commands (Copy & Paste)

### Process Disciplinary Cases (Preserves Folder Structure)
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh disciplinary --clean
```

### Process APAR Documents
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh apar --clean
```

### Process Everything (Both)
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh both --clean
```

---

## 📁 What Happens?

### Disciplinary Cases
```
INPUT:                                  OUTPUT:
data/Disciplinary cases/                outputs/disciplinary/
├── CO Brief/                           ├── CO Brief/
│   └── Charge Memorandum.pdf           │   └── Charge Memorandum/
├── IO Report/                          │       ├── Charge Memorandum_Summary.docx ✅
│   └── report.pdf                      │       └── Charge Memorandum_extracted_data.json
└── Brief Background/                   ├── IO Report/
    └── file.pdf                        │   └── report/
                                        │       ├── report_Summary.docx ✅
                                        │       └── report_extracted_data.json
                                        └── Brief Background/
                                            └── file/
                                                ├── file_Summary.docx ✅
                                                └── file_extracted_data.json
```

### APAR Documents
```
INPUT:                                  OUTPUT:
data/                                   outputs/apar/
├── APAR 1.pdf                          ├── APAR 1/
└── APAR -Ravinesh 1.pdf                │   ├── APAR 1.docx ✅
                                        │   └── APAR 1_extracted_data.json
                                        └── APAR -Ravinesh 1/
                                            ├── APAR -Ravinesh 1.docx ✅
                                            └── APAR -Ravinesh 1_extracted_data.json
```

---

## 📊 Output Files

| Document Type | Output Format | Contains |
|---------------|---------------|----------|
| **Disciplinary** | `*_Summary.docx` | Executive summary with allegations, evidence, chronology |
| **Disciplinary** | `*_extracted_data.json` | Structured JSON data |
| **APAR** | `*.docx` | Formatted table with gradings and pen-pictures |
| **APAR** | `*_extracted_data.json` | Structured JSON data |

---

## ⏱️ Processing Time

- **Per Document**: ~60-80 seconds
- **10 Documents**: ~10-15 minutes
- **50 Documents**: ~50-70 minutes

---

## 🔍 Check Results

```bash
# View output structure
tree outputs/

# Count processed files
find outputs -name "*.docx" | wc -l

# Open a result
open "outputs/disciplinary/CO Brief/Charge Memorandum/Charge Memorandum_Summary.docx"
```

---

## 📖 Full Documentation

- **[TERMINAL_COMMANDS.md](TERMINAL_COMMANDS.md)** - Complete command reference
- **[QUICK_COMMANDS.md](QUICK_COMMANDS.md)** - Quick reference guide
- **[COMPLETE_TEST_REPORT.md](COMPLETE_TEST_REPORT.md)** - Test results and validation

---

## ✅ Features

- ✅ **Preserves folder structure** from input to output
- ✅ **Automatic document classification** (APAR vs Disciplinary)
- ✅ **Batch processing** with progress tracking
- ✅ **Error handling** with retry logic
- ✅ **JSON export** for structured data
- ✅ **DOCX generation** for both document types

---

## 🎯 That's It!

Just run the command and wait for completion. The pipeline will:
1. Find all PDFs in the input folder
2. Process each one (OCR → LLM → Generate DOCX)
3. Save outputs preserving the folder structure
4. Show progress and summary

**No manual intervention needed!**
