# IDP Pipeline - Simple Commands

## 🚀 One-Line Commands

### Disciplinary Cases
```bash
cd /Users/ath1614/YellowSense/IDP2 && python3 scripts/batch/run_disciplinary_batch.py --clean
```

### APAR Documents
```bash
cd /Users/ath1614/YellowSense/IDP2 && python3 scripts/batch/run_apar_batch.py --source data/ --clean
```

---

## 📁 Output Structure

### Disciplinary Cases
```
INPUT:                                  OUTPUT:
data/Disciplinary cases/                outputs/disciplinary/
├── CO Brief/                           ├── CO Brief/
│   ├── Charge Memorandum.pdf           │   ├── Charge Memorandum_Summary.docx ✅
│   └── Defence Exhibit.pdf             │   └── Defence Exhibit_Summary.docx ✅
├── IO Report/                          ├── IO Report/
│   └── report.pdf                      │   └── report_Summary.docx ✅
└── Brief Background/                   └── Brief Background/
    └── file.pdf                            └── file_Summary.docx ✅
```

### APAR Documents
```
INPUT:                                  OUTPUT:
data/                                   outputs/apar/
├── APAR 1.pdf                          ├── APAR 1.docx ✅
└── APAR -Ravinesh 1.pdf                └── APAR -Ravinesh 1.docx ✅
```

---

## ✅ What You Get

- **Disciplinary**: `<filename>_Summary.docx` in category folder
- **APAR**: `<filename>.docx` in apar folder
- **No JSON files** - Only DOCX outputs
- **Folder structure preserved** from input

---

## 🔍 Check Results

```bash
# View disciplinary outputs
tree outputs/disciplinary/

# View APAR outputs  
ls -lh outputs/apar/

# Count files
find outputs -name "*.docx" | wc -l
```

---

## 📝 That's It!

Just run the command and get DOCX files in the same folder structure as your input.
