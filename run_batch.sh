#!/bin/bash

# IDP Pipeline - Batch Processing Script
# Usage: ./run_batch.sh [disciplinary|apar|both] [--clean]

set -e

PROJECT_ROOT="/Users/ath1614/YellowSense/IDP2"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse arguments
MODE=${1:-both}
CLEAN_FLAG=""
if [[ "$2" == "--clean" ]] || [[ "$1" == "--clean" ]]; then
    CLEAN_FLAG="--clean"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}IDP Pipeline - Batch Processing${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to run disciplinary batch
run_disciplinary() {
    echo -e "${GREEN}📂 Processing Disciplinary Cases...${NC}"
    echo "Source: data/Disciplinary cases/"
    echo "Output: outputs/disciplinary/"
    echo ""
    python3 scripts/batch/run_disciplinary_batch.py $CLEAN_FLAG
    echo ""
}

# Function to run APAR batch
run_apar() {
    echo -e "${GREEN}📂 Processing APAR Documents...${NC}"
    echo "Source: data/"
    echo "Output: outputs/apar/"
    echo ""
    python3 scripts/batch/run_apar_batch.py --source data/ $CLEAN_FLAG
    echo ""
}

# Execute based on mode
case $MODE in
    disciplinary)
        run_disciplinary
        ;;
    apar)
        run_apar
        ;;
    both)
        run_disciplinary
        echo -e "${BLUE}----------------------------------------${NC}"
        run_apar
        ;;
    *)
        echo -e "${RED}Error: Invalid mode '$MODE'${NC}"
        echo "Usage: ./run_batch.sh [disciplinary|apar|both] [--clean]"
        exit 1
        ;;
esac

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Batch Processing Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Output locations:"
echo "  - Disciplinary: outputs/disciplinary/"
echo "  - APAR: outputs/apar/"
echo "  - JSON: json_dumps/"
echo ""
