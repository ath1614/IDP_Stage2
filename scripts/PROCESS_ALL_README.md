# Single-Command IDP Pipeline

Process all PDFs in a folder structure with one command.

## Usage

```bash
python scripts/process_all.py <input_folder>
```

## What It Does

1. **Recursively scans** the entire folder structure for PDF files
2. **Automatically classifies** each PDF as APAR or Disciplinary
3. **Processes** each document through OCR and extraction
4. **Generates output**:
   - APAR → Structured DOCX table
   - Disciplinary → Executive summary DOCX
5. **Preserves folder structure** in output

## Examples

### Process entire folder
```bash
python scripts/process_all.py data/input/
```

### Specify custom output location
```bash
python scripts/process_all.py data/input/ --output data/results/
```

## Output Structure

Input:
```
data/input/
├── folder1/
│   ├── apar1.pdf
│   └── subfolder/
│       └── disciplinary1.pdf
└── folder2/
    └── apar2.pdf
```

Output:
```
data/input/processed_output/
├── folder1/
│   ├── apar1.docx          (table format)
│   └── subfolder/
│       └── disciplinary1.docx  (summary format)
└── folder2/
    └── apar2.docx          (table format)
```

## Features

- ✅ Single command execution
- ✅ Recursive folder traversal
- ✅ Automatic classification (APAR vs Disciplinary)
- ✅ Preserves folder hierarchy
- ✅ Ignores non-PDF files
- ✅ Progress tracking
- ✅ Error handling per file
- ✅ Summary report

## Requirements

- OCR VM running at `OCR_VM_IP`
- LLM VM running at `LLM_VM_IP`
- Environment configured in `.env`
