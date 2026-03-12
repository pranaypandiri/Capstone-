# Customer Communicator Agent - Flask API Documentation

## Overview
REST API wrapper for the Customer Communicator Agent that enables multi-agent orchestration for generating personalized customer resolution messages through HTTP endpoints.

## Quick Start

### 1. Start the Flask Server
```bash
python flask_api.py
```

Output:
```
======================================================================
CUSTOMER COMMUNICATOR AGENT - FLASK API
======================================================================
Starting Flask API server...
Local: http://127.0.0.1:5000
Environment: development

Available Endpoints:
  - GET  /health                    (Health check)
  - GET  /api/v1/status             (Agent status)
  - POST /api/v1/generate-message   (Generate single message)
  - POST /api/v1/batch-generate     (Generate multiple messages)
  - POST /api/v1/validate           (Validate message compliance)
======================================================================
```

### 2. Test with Postman
- Import `Postman_Collection.json` into Postman
- Or use the curl commands below

### 3. View Terminal Output
All requests/responses are logged to the terminal in real-time

---

## API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API and agent are running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Customer Communicator API",
  "timestamp": "2026-01-13T10:30:45.123456",
  "agent_ready": true
}
```

**CURL:**
```bash
curl -X GET http://127.0.0.1:5000/health
```

---

### 2. Agent Status
**GET** `/api/v1/status`

Get agent configuration and available endpoints.

**Response:**
```json
{
  "agent_id": "COM-01",
  "status": "ready",
  "timestamp": "2026-01-13T10:30:45.123456",
  "endpoints": {
    "health": "/health",
    "generate_message": "/api/v1/generate-message",
    "batch_generate": "/api/v1/batch-generate",
    "validate": "/api/v1/validate",
    "status": "/api/v1/status"
  }
}
```

**CURL:**
```bash
curl -X GET http://127.0.0.1:5000/api/v1/status
```

---

### 3. Generate Single Message
**POST** `/api/v1/generate-message`

Generate a personalized resolution message for a single customer using multi-agent orchestration.

**Request Body:**
```json
{
  "customer_profile": {
    "KNA1": {
      "customer_id": "100034",
      "name": "Acme",
      "email": "anita.rao@acmeretail.example",
      "phone": "+91-80-5555-1100"
    },
    "KNVV": {
      "currency": "INR"
    }
  },
  "resolution_plan": {
    "complaint_id": "CMP-2025-00089",
    "category": "Delivery Delay",
    "description": "Order delayed in transit",
    "actions": [
      {
        "action_type": "Expedite",
        "carrier": "BlueDart",
        "delivery_date": "2025-11-28"
      }
    ]
  },
  "credit_confirmation": {
    "approval_status": "approved",
    "goodwill_credit": {
      "amount": 2299.50,
      "currency": "INR"
    }
  }
}
```

**Response (Success 200):**
```json
{
  "status": "success",
  "data": {
    "complaint_id": "CMP-2025-00089",
    "customer_id": "100034",
    "to": {
      "name": "Acme",
      "email": "anita.rao@acmeretail.example",
      "phone": "+91-80-5555-1100"
    },
    "body": "Dear Acme,\n\nWe sincerely apologize for the delay in delivering your order...",
    "dispatch_channel": "email",
    "tone": "empathetic",
    "compliance": {
      "gdpr": true,
      "brand": true
    },
    "validation_status": "pass",
    "timestamp": "2026-01-13T10:30:45.123456",
    "agent_id": "COM-01"
  },
  "timestamp": "2026-01-13T10:30:45.123456"
}
```

**Terminal Output:**
```
======================================================================
INCOMING API REQUEST
======================================================================
Timestamp: 2026-01-13T10:30:45.123456
Customer ID: 100034
Complaint ID: CMP-2025-00089
======================================================================

[API] Processing request through agent...

[API] ✓ Message generation completed successfully
======================================================================
RESPONSE SENT TO CLIENT
======================================================================
{
  "complaint_id": "CMP-2025-00089",
  "customer_id": "100034",
  "to": {
    "name": "Acme",
    "email": "anita.rao@acmeretail.example",
    "phone": "+91-80-5555-1100"
  },
  "body": "Dear Acme,\n\nWe sincerely apologize for the delay...",
  ...
}
======================================================================
```

**CURL:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{
    "customer_profile": {...},
    "resolution_plan": {...},
    "credit_confirmation": {...}
  }'
```

**Error Response (400):**
```json
{
  "error": "Missing required fields: customer_profile, resolution_plan, credit_confirmation",
  "status": "failed"
}
```

---

### 4. Batch Generate Messages
**POST** `/api/v1/batch-generate`

Generate messages for multiple customers in a single request.

**Request Body:**
```json
{
  "messages": [
    {
      "customer_profile": {...},
      "resolution_plan": {...},
      "credit_confirmation": {...}
    },
    {
      "customer_profile": {...},
      "resolution_plan": {...},
      "credit_confirmation": {...}
    }
  ]
}
```

**Response (Success 200):**
```json
{
  "status": "completed",
  "total": 2,
  "succeeded": 2,
  "failed": 0,
  "results": [
    {
      "index": 1,
      "status": "success",
      "data": {
        "complaint_id": "CMP-2025-00089",
        ...
      }
    },
    {
      "index": 2,
      "status": "success",
      "data": {
        "complaint_id": "CMP-2025-00090",
        ...
      }
    }
  ],
  "timestamp": "2026-01-13T10:30:45.123456"
}
```

**Terminal Output:**
```
======================================================================
BATCH API REQUEST - Processing 2 messages
======================================================================

[Batch] Processing message 1/2...
[Batch] ✓ Message 1 completed

[Batch] Processing message 2/2...
[Batch] ✓ Message 2 completed

======================================================================
BATCH PROCESSING COMPLETE - 2/2 succeeded
======================================================================
```

**CURL:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/batch-generate \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [...]
  }'
```

---

### 5. Validate Message Compliance
**POST** `/api/v1/validate`

Validate a message for GDPR compliance and brand tone.

**Request Body:**
```json
{
  "message": "Dear Acme,\n\nWe sincerely apologize for the delay in delivering your order...",
  "context": {
    "customer_id": "100034",
    "complaint_id": "CMP-2025-00089",
    "category": "Delivery Delay"
  }
}
```

**Response (Success 200):**
```json
{
  "status": "success",
  "validation": {
    "gdpr": true,
    "brand": true,
    "compliance_status": "pass",
    "issues": [],
    "suggestions": []
  },
  "timestamp": "2026-01-13T10:30:45.123456"
}
```

**Terminal Output:**
```
[Validation] Processing compliance check...
[Validation] ✓ Compliance check completed
```

**CURL:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "...",
    "context": {...}
  }'
```

---

## HTTP Status Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing/invalid fields |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Internal Server Error | Server/agent error |
| 503 | Service Unavailable | Agent not initialized |

---

## Error Handling

### Agent Not Initialized
**Response (503):**
```json
{
  "error": "Agent not initialized",
  "status": "failed"
}
```

### Missing Required Fields
**Response (400):**
```json
{
  "error": "Missing required fields: customer_profile, resolution_plan, credit_confirmation",
  "status": "failed"
}
```

### Processing Error
**Response (500):**
```json
{
  "error": "Error generating message: [error details]",
  "status": "failed",
  "timestamp": "2026-01-13T10:30:45.123456"
}
```

---

## Using Postman

### Import Collection
1. Open Postman
2. Click **Import** button
3. Select `Postman_Collection.json`
4. All endpoints will be pre-configured

### Environment Setup (Optional)
Create a Postman environment with:
```json
{
  "base_url": "http://127.0.0.1:5000"
}
```

Then use `{{base_url}}` in request URLs.

### View Response
- Click **Send** button
- Response appears in lower panel
- Terminal shows detailed logs

---

## Terminal Output Example

When you make a request from Postman, you'll see detailed logging in the terminal:

```
======================================================================
INCOMING API REQUEST
======================================================================
Timestamp: 2026-01-13T10:32:15.456789
Customer ID: 100034
Complaint ID: CMP-2025-00089
======================================================================

[API] Processing request through agent...

  [Agent] Invoking Message Generator Agent...
    → Sending request to Message Generator Agent...
    ✓ Message generated by Agent

  [Agent] Invoking Compliance Validator Agent...
    → Sending request to Compliance Validator Agent...
    ✓ Compliance validated by Agent

[API] ✓ Message generation completed successfully
======================================================================
RESPONSE SENT TO CLIENT
======================================================================
{
  "complaint_id": "CMP-2025-00089",
  "customer_id": "100034",
  "to": {
    "name": "Acme",
    "email": "anita.rao@acmeretail.example",
    "phone": "+91-80-5555-1100"
  },
  "body": "Dear Acme,\n\nThank you for bringing this to our attention...",
  "dispatch_channel": "email",
  "tone": "empathetic",
  "compliance": {
    "gdpr": true,
    "brand": true
  },
  "validation_status": "pass",
  "timestamp": "2026-01-13T10:32:15.456789",
  "agent_id": "COM-01"
}
======================================================================
```

---

## Request/Response Flow

```
┌─────────────┐
│   Postman   │
└──────┬──────┘
       │
       │ HTTP POST
       ▼
┌──────────────────────────────┐
│     Flask API Server         │
│    (flask_api.py:5000)       │
└──────┬───────────────────────┘
       │
       │ Process request
       ▼
┌──────────────────────────────────────────┐
│  CustomerCommunicatorAgent               │
│  ├─ Agent 1: Message Generator           │
│  │  └─ LLM: Azure GPT-4o                │
│  └─ Agent 2: Compliance Validator        │
│     └─ LLM: Azure GPT-4o                │
└──────┬───────────────────────────────────┘
       │
       │ Return response
       ▼
┌──────────────────────────────┐
│     JSON Response Body       │
│   + Terminal Logging         │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────┐
│   Postman   │
│  (Display)  │
└─────────────┘
```

---

## Troubleshooting

### Agent shows "not initialized"
- Ensure `.env` file has valid Azure OpenAI credentials
- Check if `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL` are set
- Run: `python customer_communicator_agent.py` first to verify

### Port 5000 already in use
- Kill the process: `lsof -ti:5000 | xargs kill -9`
- Or change port in `flask_api.py`: `app.run(port=5001)`

### Request times out
- Check internet connection to Azure OpenAI
- Verify Azure credentials are valid
- Increase timeout in Postman (Settings → General → Request timeout)

### No terminal output
- Ensure terminal is in focus
- Flask debug mode should show logs automatically
- Check if Flask server started without errors

---

## Integration Examples

### Python Client
```python
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Generate message
response = requests.post(
    f"{BASE_URL}/api/v1/generate-message",
    json={
        "customer_profile": {...},
        "resolution_plan": {...},
        "credit_confirmation": {...}
    }
)

print(response.json())
```

### JavaScript/Node.js
```javascript
const baseUrl = "http://127.0.0.1:5000";

fetch(`${baseUrl}/api/v1/generate-message`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    customer_profile: {...},
    resolution_plan: {...},
    credit_confirmation: {...}
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Performance Notes

- **Single Message Generation**: ~3-5 seconds (LLM processing time)
- **Batch Processing**: Linear with number of messages
- **Validation**: ~1-2 seconds per message
- All times depend on Azure OpenAI response times

---

## Support
For issues or questions, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- AutoGen Documentation: https://microsoft.github.io/autogen/
- Postman Learning Center: https://learning.postman.com/
