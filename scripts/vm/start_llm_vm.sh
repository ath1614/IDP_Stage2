#!/bin/bash
# Start LLM Service on VM

echo "Starting LLM Service on 34.47.203.146..."

ssh tech@34.47.203.146 << 'EOF'
cd ~
pkill -f llm_service.py
source venv_llm/bin/activate
nohup python llm_service.py > llm_service.log 2>&1 &
echo $! > llm_service.pid
sleep 5
curl http://localhost:8000/api/health
echo ""
echo "LLM Service started. PID: $(cat llm_service.pid)"
EOF

echo "Testing from local..."
sleep 2
curl http://34.47.203.146:8000/api/health
