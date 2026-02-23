#!/bin/bash
# Start OCR Service on VM

echo "Starting OCR Service on 34.14.176.182..."

ssh tech@34.14.176.182 << 'EOF'
cd ~
pkill -f ocr_service.py
source venv_ocr/bin/activate
nohup python ocr_service.py > ocr_service.log 2>&1 &
echo $! > ocr_service.pid
sleep 5
curl http://localhost:8000/api/health
echo ""
echo "OCR Service started. PID: $(cat ocr_service.pid)"
EOF

echo "Testing from local..."
sleep 2
curl http://34.14.176.182:8000/api/health
