# API Reference - NFRA System

## Base URL
```
http://localhost:3000/api
```

All endpoints are relative to this base URL.

---

## 1. POST /process - Start Pipeline Job

**Purpose:** Upload a PDF and start the NFRA processing pipeline

**Request:**
```javascript
POST /api/process
Content-Type: application/json

{
  "filename": "sample_financial_report.pdf",
  "filedata": "data:application/pdf;base64,JVBERi0x..." // base64 encoded PDF
}
```

**Response (Success - 200):**
```json
{
  "jobId": "mlpo7mba-406a39c4"
}
```

**Response (Error - 400):**
```json
{
  "error": "Only PDF uploads supported"
}
```

**What Happens:**
1. Validates PDF file
2. Saves to: `data/input/samples/<jobId>_<filename>`
3. Creates job tracking: `data/output/jobs/<jobId>.status.json`
4. Spawns Python pipeline in background
5. Returns jobId to track progress

**Example (cURL):**
```bash
# Read file and convert to base64
base64_content=$(base64 -i sample_financial_report.pdf | tr -d '\n')

# Send request
curl -X POST http://localhost:3000/api/process \
  -H "Content-Type: application/json" \
  -d "{
    \"filename\": \"sample_financial_report.pdf\",
    \"filedata\": \"$base64_content\"
  }"
```

**Example (JavaScript):**
```javascript
const file = document.querySelector('input[type="file"]').files[0];
const reader = new FileReader();

reader.onload = async (e) => {
  const response = await fetch('/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      filename: file.name,
      filedata: e.target.result  // base64 data URL
    })
  });
  const { jobId } = await response.json();
  console.log('Job ID:', jobId);
};

reader.readAsDataURL(file);
```

---

## 2. GET /process/status - Check Job Status

**Purpose:** Poll the status of a running job

**Request:**
```
GET /api/process/status?jobId=mlpo7mba-406a39c4
```

**Response (Queued - 200):**
```json
{
  "jobId": "mlpo7mba-406a39c4",
  "status": "queued",
  "progress": 0,
  "logs": [],
  "output": null
}
```

**Response (Running - 200):**
```json
{
  "jobId": "mlpo7mba-406a39c4",
  "status": "running",
  "progress": 45,
  "logs": [
    "[1/8] Calling OCR service...",
    "✓ Extracted 45000 characters",
    "[2/8] Segmenting document...",
    "✓ Found 10 sections"
  ],
  "output": null
}
```

**Response (Completed - 200):**
```json
{
  "jobId": "mlpo7mba-406a39c4",
  "status": "completed",
  "progress": 100,
  "logs": [
    "[1/8] Calling OCR service...",
    "...",
    "[8/8] Indexing for RAG...",
    "✓ Processing complete"
  ],
  "output": "phase4_mlpo7mba-406a39c4.json",
  "exitCode": 0
}
```

**Response (Failed - 200):**
```json
{
  "jobId": "mlpo7mba-406a39c4",
  "status": "failed",
  "progress": 0,
  "logs": [
    "ERROR: OCR service not responding"
  ],
  "output": null,
  "exitCode": 1
}
```

**Status Codes:**
| Status | Meaning | Action |
|--------|---------|--------|
| queued | Waiting to start | Keep polling |
| running | Processing | Keep polling |
| completed | Done successfully | Fetch results |
| failed | Error occurred | Check logs |

**Progress Estimation:**
- 0-10%: OCR starting
- 10-30%: OCR + Segmentation
- 30-50%: Table extraction + LLM
- 50-70%: Analytics + Compliance
- 70-90%: Compilation
- 90-100%: RAG indexing

**Example (JavaScript):**
```javascript
async function pollStatus(jobId) {
  const checkInterval = setInterval(async () => {
    const response = await fetch(`/api/process/status?jobId=${jobId}`);
    const status = await response.json();
    
    console.log(`Status: ${status.status} (${status.progress}%)`);
    console.log('Recent logs:', status.logs.slice(-3));
    
    if (status.status === 'completed') {
      clearInterval(checkInterval);
      fetchResults(jobId);
    } else if (status.status === 'failed') {
      clearInterval(checkInterval);
      console.error('Job failed:', status.logs);
    }
  }, 2000); // Poll every 2 seconds
}
```

---

## 3. GET /process/result - Get Completed Results

**Purpose:** Retrieve the final JSON results from a completed job

**Request:**
```
GET /api/process/result?jobId=mlpo7mba-406a39c4
```

**Response (Success - 200):**
```json
{
  "document": {
    "filename": "sample_financial_report.pdf",
    "type": "Uploaded",
    "status": "processed"
  },
  "ocr": {
    "status": "success",
    "text": "TECHCORP FINANCIAL...",
    "pages": 25,
    "char_count": 45000
  },
  "segmentation": {
    "total_sections_found": 10,
    "sections": [
      {
        "name": "Executive Summary",
        "content": "...",
        "type": "summary"
      }
    ]
  },
  "extraction": {
    "company_name": "TechCorp Financial Solutions Limited",
    "fiscal_year": "2025-26",
    "financial_metrics": {
      "revenue": {
        "value": 450.5,
        "currency": "INR",
        "unit": "Crore",
        "ytd_growth": "15%"
      },
      "net_profit": {
        "value": 78.45,
        "currency": "INR",
        "unit": "Crore",
        "ytd_growth": "12%"
      }
    }
  },
  "analytics": {
    "summary": {
      "financial_health_score": "83.33%",
      "rating": "Excellent"
    },
    "profitability": {
      "gross_margin": "48.3%",
      "net_margin": "17.41%",
      "roe": "21%"
    },
    "liquidity": {
      "current_ratio": "2.0",
      "quick_ratio": "1.8"
    }
  },
  "compliance": {
    "compliance_score": "40%",
    "frameworks": [
      {
        "name": "IndAS",
        "status": "COMPLIANT",
        "findings": 4
      }
    ]
  },
  "rag": {
    "status": "success",
    "documents_indexed": 45,
    "chunks_created": 120
  }
}
```

**Response (Not Ready - 404):**
```json
{
  "error": "result not available yet",
  "status": "running"
}
```

**Response (Job Failed - 404):**
```json
{
  "error": "Result file missing",
  "status": "failed"
}
```

**Data Structure:**
- `document`: Input metadata
- `ocr`: Raw text extraction
- `segmentation`: Document sections found
- `extraction`: Structured financial data
- `analytics`: Health scores and ratios
- `compliance`: Regulatory compliance checks
- `rag`: Q&A indexing info

**Example (JavaScript):**
```javascript
async function fetchResults(jobId) {
  const response = await fetch(`/api/process/result?jobId=${jobId}`);
  
  if (!response.ok) {
    console.error('Results not ready yet');
    return;
  }
  
  const results = await response.json();
  
  // Display health score
  const healthScore = results.analytics.summary.financial_health_score;
  document.getElementById('healthScore').textContent = healthScore;
  
  // Display revenue
  const revenue = results.extraction.financial_metrics.revenue.value;
  document.getElementById('revenue').textContent = `₹${revenue} Cr`;
  
  // Display compliance status
  const compliance = results.compliance.compliance_score;
  document.getElementById('compliance').textContent = compliance;
}
```

---

## 4. GET /api/summary - Get Latest Test Summary

**Purpose:** Get a quick summary of the latest processed document

**Request:**
```
GET /api/summary
```

**Response (Success - 200):**
```json
{
  "ocr_chars": 45000,
  "segments": 10,
  "tables": 5,
  "health_score": 83.33,
  "compliance_score": 40,
  "rag_indexed": 45
}
```

**Response (No Data - 404):**
```json
{
  "error": "phase4_test.json not found. Run pipeline first."
}
```

**Use Case:**
- Quick dashboard update
- Create KPI cards
- Show overall system health

**Example (JavaScript):**
```javascript
async function updateDashboard() {
  const response = await fetch('/api/summary');
  const data = await response.json();
  
  // Update UI
  document.querySelector('.ocr-count').textContent = `${data.ocr_chars} chars`;
  document.querySelector('.health').textContent = `${data.health_score}%`;
  document.querySelector('.compliance').textContent = `${data.compliance_score}%`;
}
```

---

## Error Handling

**Common Error Responses:**

```json
// File format error
{
  "error": "Only PDF uploads supported"
}

// Missing parameters
{
  "error": "jobId required"
}

// Job not found
{
  "error": "job not found"
}

// Server error
{
  "error": "failed to read status"
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid input) |
| 404 | Not found (jobId, results) |
| 405 | Method not allowed |
| 500 | Server error |

---

## File Paths (Internal)

After processing, files are saved to:

```
Input PDF:
  /Users/ath1614/YellowSense/IDP2/data/input/samples/<jobId>_<filename>.pdf

Job Status:
  /Users/ath1614/YellowSense/IDP2/data/output/jobs/<jobId>.status.json

Results JSON:
  /Users/ath1614/YellowSense/IDP2/data/output/results/phase4_<jobId>.json
```

---

## Workflow Example

```
1. User uploads PDF
   ↓
POST /api/process
   ↓
Returns: { jobId: "xyz123" }
   ↓
2. Poll status every 2 seconds
   ↓
GET /api/process/status?jobId=xyz123
   ↓
Returns: { status: "running", progress: 45 }
   ↓
3. When status = "completed"
   ↓
GET /api/process/result?jobId=xyz123
   ↓
Returns: { analytics: {...}, compliance: {...}, ... }
   ↓
4. Display results on dashboard
```

---

## Rate Limiting

Currently **no rate limiting** is enabled. For production:
- Limit uploads to 1 per minute per user
- Limit status polls to 1 per second
- Implement API key authentication

---

## Authentication

Currently **no authentication** is required. For production:
- Add JWT tokens
- Implement per-user job isolation
- Log all API access

---

## Performance Notes

- **Response Times:**
  - Queued → 1-2 seconds
  - Running → 1-3 minutes (60-90 seconds typical)
  - Retrieved → <100ms

- **File Size Limits:**
  - Max PDF: 200 MB
  - Max request body: 200 MB

- **Concurrent Jobs:**
  - Can process multiple jobs simultaneously
  - Each gets unique jobId
  - Results are isolated

---

## Testing

### Using curl

```bash
# Check services
curl http://34.47.203.146:8000/health
curl http://34.180.45.142:8000/health

# Get summary
curl http://localhost:3000/api/summary

# Check status
curl http://localhost:3000/api/process/status?jobId=xyz123
```

### Using Postman

1. Import collection: [docs/api_collection.json](../docs/api_collection.json)
2. Set environment variables:
   - `base_url`: http://localhost:3000/api
   - `jobId`: xyz123
3. Run requests

### Using JavaScript

```javascript
// Fetch with error handling
async function apiCall(path, options = {}) {
  try {
    const response = await fetch(`/api${path}`, {
      method: options.method || 'GET',
      headers: { 'Content-Type': 'application/json', ...options.headers },
      body: options.body ? JSON.stringify(options.body) : undefined
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Usage
const result = await apiCall('/summary');
```

---

## Webhooks (Future)

Soon: Webhook support for completion notifications

```javascript
// Register webhook
POST /api/webhooks
{
  "event": "job.completed",
  "url": "https://yoursite.com/callback",
  "jobId": "optional_jobid"
}

// Server will POST when job completes:
POST https://yoursite.com/callback
{
  "jobId": "xyz123",
  "status": "completed",
  "results_url": "http://localhost:3000/api/process/result?jobId=xyz123"
}
```

---

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /process | POST | Start job |
| /process/status | GET | Check status |
| /process/result | GET | Get results |
| /summary | GET | Quick summary |
