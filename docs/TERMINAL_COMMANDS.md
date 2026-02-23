# IDP Pipeline - Terminal Commands Guide

## 🎯 Simple Commands (Copy & Paste)

### Option 1: Using Shell Script (Easiest)

```bash
# Process ONLY Disciplinary Cases
cd /Users/ath1614/YellowSense/IDP2
./run_batch.sh disciplinary

# Process ONLY APAR Documents
cd /Users/ath1614/YellowSense/IDP2
./run_batch.sh apar

# Process BOTH (Disciplinary + APAR)
cd /Users/ath1614/YellowSense/IDP2
./run_batch.sh both

# With --clean flag (delete previous outputs)
cd /Users/ath1614/YellowSense/IDP2
./run_batch.sh both --clean
```

---

### Option 2: Direct Python Commands

#### Disciplinary Cases
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_disciplinary_batch.py
```

**With clean:**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_disciplinary_batch.py --clean
```

#### APAR Documents
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_apar_batch.py --source data/
```

**With clean:**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_apar_batch.py --source data/ --clean
```

---

## 📁 Folder Structure Preservation

### Input → Output Mapping

#### Disciplinary Cases
```
INPUT:                                  OUTPUT:
data/Disciplinary cases/                outputs/disciplinary/
├── Brief Background/                   ├── Brief Background/
│   ├── file1.pdf                       │   └── file1/
│   └── file2.pdf                       │       ├── file1_Summary.docx
├── CO Brief/                           │       └── file1_extracted_data.json
│   ├── Charge Memorandum.pdf           ├── CO Brief/
│   └── Defence Exhibit.pdf             │   ├── Charge Memorandum/
└── IO Report/                          │   │   ├── Charge Memorandum_Summary.docx
    └── report.pdf                      │   │   └── Charge Memorandum_extracted_data.json
                                        │   └── Defence Exhibit/
                                        │       ├── Defence Exhibit_Summary.docx
                                        │       └── Defence Exhibit_extracted_data.json
                                        └── IO Report/
                                            └── report/
                                                ├── report_Summary.docx
                                                └── report_extracted_data.json
```

#### APAR Documents
```
INPUT:                                  OUTPUT:
data/                                   outputs/apar/
├── APAR 1.pdf                          ├── APAR 1/
├── APAR -Ravinesh 1.pdf                │   ├── APAR 1.docx
└── (any APAR*.pdf)                     │   └── APAR 1_extracted_data.json
                                        └── APAR -Ravinesh 1/
                                            ├── APAR -Ravinesh 1.docx
                                            └── APAR -Ravinesh 1_extracted_data.json
```

---

## 📊 Output Files

### Disciplinary Cases
Each PDF generates:
- **DOCX Report**: `<filename>_Summary.docx` (Executive summary with sections)
- **JSON Data**: `<filename>_extracted_data.json` (Structured data)

### APAR Documents
Each PDF generates:
- **DOCX Table**: `<filename>.docx` (Formatted table with gradings)
- **JSON Data**: `<filename>_extracted_data.json` (Structured data)

---

## 🔍 Verify Results

### Check output structure
```bash
cd /Users/ath1614/YellowSense/IDP2

# View disciplinary outputs
tree outputs/disciplinary/

# View APAR outputs
tree outputs/apar/

# View JSON dumps
tree json_dumps/
```

### Count processed files
```bash
# Count disciplinary DOCX files
find outputs/disciplinary -name "*_Summary.docx" | wc -l

# Count APAR DOCX files
find outputs/apar -name "*.docx" | wc -l

# Count all JSON files
find json_dumps -name "*.json" | wc -l
```

### View specific output
```bash
# Open DOCX file
open "outputs/disciplinary/CO Brief/Charge Memorandum/Charge Memorandum_Summary.docx"

# View JSON data
cat "json_dumps/CO Brief/Charge Memorandum/Charge Memorandum_extracted_data.json" | python3 -m json.tool
```

---

## ⚡ Quick Reference

| Task | Command |
|------|---------|
| Process all disciplinary | `./run_batch.sh disciplinary` |
| Process all APAR | `./run_batch.sh apar` |
| Process everything | `./run_batch.sh both` |
| Clean & process | `./run_batch.sh both --clean` |
| Single disciplinary file | `python3 src/process_pipeline.py "path/to/file.pdf" --mode summary` |
| Single APAR file | `python3 src/process_pipeline.py "path/to/file.pdf" --mode apar` |

---

## 📝 Notes

- **Folder structure is automatically preserved** from input to output
- Each PDF gets its own subfolder in the output
- JSON files are saved in `json_dumps/` directory
- Use `--clean` to delete previous results before processing
- Processing time: ~60-80 seconds per document
- All commands must be run from project root: `/Users/ath1614/YellowSense/IDP2`

---

## 🎯 Most Common Use Cases

### 1. Process all disciplinary cases (preserving structure)
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh disciplinary --clean
```

### 2. Process all APAR documents
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh apar --clean
```

### 3. Process everything at once
```bash
cd /Users/ath1614/YellowSense/IDP2 && ./run_batch.sh both --clean
```

---

## ✅ Expected Results

After running the commands, you will have:

1. **Disciplinary outputs** in `outputs/disciplinary/` with exact folder structure from input
2. **APAR outputs** in `outputs/apar/` with one folder per PDF
3. **JSON data** in `json_dumps/` with structured extraction results
4. **Console output** showing progress and success/failure counts

Example console output:
```
🚀 Starting Disciplinary Batch Processing...
📂 Source: data/Disciplinary cases
📂 Output: outputs/disciplinary
📄 Found 15 PDF files.

[1/15] Processing: Charge Memorandum.pdf
  Category: CO Brief
  ✅ COMPLETED in 65.23s

...

🎉 Batch Processing Finished.
Total: 15
✅ Success: 15
❌ Failed: 0
```
