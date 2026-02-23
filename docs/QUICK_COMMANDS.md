# IDP Pipeline - Quick Commands

## 🚀 Batch Processing Commands

### Disciplinary Cases (Preserves Folder Structure)

**Process all disciplinary cases:**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_disciplinary_batch.py
```

**With clean output (delete previous results):**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_disciplinary_batch.py --clean
```

**Input Structure:**
```
data/Disciplinary cases/
├── Brief Background/
│   └── file1.pdf
├── CO Brief/
│   └── file2.pdf
└── IO Report/
    └── file3.pdf
```

**Output Structure (Mirrors Input):**
```
outputs/disciplinary/
├── Brief Background/
│   └── file1/
│       ├── file1_Summary.docx
│       └── file1_extracted_data.json
├── CO Brief/
│   └── file2/
│       ├── file2_Summary.docx
│       └── file2_extracted_data.json
└── IO Report/
    └── file3/
        ├── file3_Summary.docx
        └── file3_extracted_data.json
```

---

### APAR Documents (Preserves Folder Structure)

**Process all APAR files:**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_apar_batch.py --source data/
```

**With clean output:**
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 scripts/batch/run_apar_batch.py --source data/ --clean
```

**Input Structure:**
```
data/
├── APAR 1.pdf
├── APAR -Ravinesh 1.pdf
└── (any folder with APAR*.pdf files)
```

**Output Structure:**
```
outputs/apar/
├── APAR 1/
│   ├── APAR 1.docx
│   └── APAR 1_extracted_data.json
└── APAR -Ravinesh 1/
    ├── APAR -Ravinesh 1.docx
    └── APAR -Ravinesh 1_extracted_data.json
```

---

## 📝 Single File Processing

### Disciplinary Case
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 src/process_pipeline.py "data/Disciplinary cases/CO Brief/Charge Memorandum.pdf" \
  --output-dir outputs/single_test \
  --mode summary
```

### APAR Document
```bash
cd /Users/ath1614/YellowSense/IDP2
python3 src/process_pipeline.py "data/APAR 1.pdf" \
  --output-dir outputs/single_test \
  --mode apar
```

---

## 📊 Output Locations

### Disciplinary Cases
- **DOCX Reports**: `outputs/disciplinary/<Category>/<FileName>/`
- **JSON Data**: `json_dumps/<Category>/<FileName>/`

### APAR Documents
- **DOCX Tables**: `outputs/apar/<FileName>/`
- **JSON Data**: `json_dumps/Uncategorized/<FileName>/`

---

## 🔍 Check Results

### View output structure
```bash
tree outputs/disciplinary/
tree outputs/apar/
```

### Count processed files
```bash
find outputs/disciplinary -name "*.docx" | wc -l
find outputs/apar -name "*.docx" | wc -l
```

### View JSON data
```bash
cat json_dumps/CO\ Brief/Charge\ Memorandum/Charge\ Memorandum_extracted_data.json | python3 -m json.tool
```

---

## ⚡ Quick Start (Copy-Paste Ready)

### Process Everything

**Disciplinary:**
```bash
cd /Users/ath1614/YellowSense/IDP2 && python3 scripts/batch/run_disciplinary_batch.py --clean
```

**APAR:**
```bash
cd /Users/ath1614/YellowSense/IDP2 && python3 scripts/batch/run_apar_batch.py --source data/ --clean
```

---

## 📋 Notes

- Folder structure is automatically preserved
- Each PDF gets its own output folder
- JSON files are saved separately in `json_dumps/`
- Use `--clean` to delete previous results before processing
- Processing time: ~60-80 seconds per document
