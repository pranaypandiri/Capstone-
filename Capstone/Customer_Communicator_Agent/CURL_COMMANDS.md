# Flask API - cURL Command Examples

## Server Status
Server running at: `http://127.0.0.1:5000`

---

## 1. Health Check

### Command:
```bash
curl http://127.0.0.1:5000/health
```

### Response:
```json
{
  "status": "healthy",
  "service": "Customer Communicator API",
  "timestamp": "2026-01-13T10:35:45.123456",
  "agent_ready": true
}
```

---

## 2. Agent Status

### Command:
```bash
curl http://127.0.0.1:5000/api/v1/status
```

### Response:
```json
{
  "agent_id": "COM-01",
  "status": "ready",
  "timestamp": "2026-01-13T10:35:45.123456",
  "endpoints": {
    "health": "/health",
    "generate_message": "/api/v1/generate-message",
    "batch_generate": "/api/v1/batch-generate",
    "validate": "/api/v1/validate",
    "status": "/api/v1/status"
  }
}
```

---

## 3. Generate Single Message

### Command:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{
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
}'
```

### Response:
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
    "body": "Dear Acme,\n\nWe sincerely apologize for the delay in delivering your order with Complaint ID CMP-2025-00089. We understand how important timely delivery is for your organization, and we regret the inconvenience this may have caused.\n\nWe have been in touch with our carrier partner, BlueDart, and your shipment is now scheduled to reach you by 2025-11-28. To express our commitment to your satisfaction, we have issued a goodwill credit of 2,299.50 INR to your account.\n\nThank you for your patience and understanding.\n\nWarm regards,\n[Your Name]\n[Your Position]\n[Your Contact Information]",
    "dispatch_channel": "email",
    "tone": "empathetic",
    "compliance": {
      "gdpr": true,
      "brand": true
    },
    "validation_status": "pass",
    "timestamp": "2026-01-13T10:35:45.123456",
    "agent_id": "COM-01"
  },
  "timestamp": "2026-01-13T10:35:45.123456"
}
```

---

## 4. Batch Generate Messages

### Command:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/batch-generate \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
      "customer_profile": {
        "KNA1": {
          "customer_id": "100034",
          "name": "Acme",
          "email": "anita.rao@acmeretail.example",
          "phone": "+91-80-5555-1100"
        },
        "KNVV": {"currency": "INR"}
      },
      "resolution_plan": {
        "complaint_id": "CMP-2025-00089",
        "category": "Delivery Delay",
        "actions": [{
          "action_type": "Expedite",
          "carrier": "BlueDart",
          "delivery_date": "2025-11-28"
        }]
      },
      "credit_confirmation": {
        "approval_status": "approved",
        "goodwill_credit": {
          "amount": 2299.50,
          "currency": "INR"
        }
      }
    },
    {
      "customer_profile": {
        "KNA1": {
          "customer_id": "100035",
          "name": "Beta Corp",
          "email": "contact@betacorp.example",
          "phone": "+91-80-5555-1101"
        },
        "KNVV": {"currency": "INR"}
      },
      "resolution_plan": {
        "complaint_id": "CMP-2025-00090",
        "category": "Quality Issue",
        "actions": [{
          "action_type": "Replace",
          "quantity": 5
        }]
      },
      "credit_confirmation": {
        "approval_status": "approved",
        "goodwill_credit": {
          "amount": 1500.00,
          "currency": "INR"
        }
      }
    }
  ]
}'
```

### Response:
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
        "customer_id": "100034",
        "body": "Dear Acme,\n\nWe sincerely apologize for the delay...",
        "compliance": {"gdpr": true, "brand": true},
        "validation_status": "pass"
      }
    },
    {
      "index": 2,
      "status": "success",
      "data": {
        "complaint_id": "CMP-2025-00090",
        "customer_id": "100035",
        "body": "Dear Beta Corp,\n\nThank you for bringing this matter to our attention...",
        "compliance": {"gdpr": true, "brand": true},
        "validation_status": "pass"
      }
    }
  ],
  "timestamp": "2026-01-13T10:35:45.123456"
}
```

---

## 5. Validate Message

### Command:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
  "message": "Dear Acme,\n\nWe sincerely apologize for the delay in delivering your order with Complaint ID CMP-2025-00089. We understand how important timely delivery is for your organization, and we regret the inconvenience this may have caused.\n\nWe have been in touch with our carrier partner, BlueDart, and your shipment is now scheduled to reach you by 2025-11-28. To express our commitment to your satisfaction, we have issued a goodwill credit of 2,299.50 INR to your account.\n\nThank you for your patience and understanding.",
  "context": {
    "customer_id": "100034",
    "complaint_id": "CMP-2025-00089",
    "category": "Delivery Delay"
  }
}'
```

### Response:
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
  "timestamp": "2026-01-13T10:35:45.123456"
}
```

---

## Terminal Output Example

When you run any command, the terminal shows:

```
======================================================================
INCOMING API REQUEST
======================================================================
Timestamp: 2026-01-13T10:35:45.123456
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
{...json response...}
======================================================================
127.0.0.1 - - [13/Jan/2026 10:35:45] "POST /api/v1/generate-message HTTP/1.1" 200 -
```

---

## Save Commands to File

### On Windows:
Create `test_commands.txt` with all commands above, then run:
```bash
type test_commands.txt | Invoke-Expression
```

### On Linux/Mac:
Create `test_commands.sh`:
```bash
#!/bin/bash

# Test 1: Health
curl http://127.0.0.1:5000/health

# Test 2: Status
curl http://127.0.0.1:5000/api/v1/status

# Add other commands...
```

Then run:
```bash
chmod +x test_commands.sh
./test_commands.sh
```

---

## Quick Tips

### Copy JSON Output to File:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{...}' > response.json
```

### Pretty Print JSON:
```bash
curl http://127.0.0.1:5000/health | python -m json.tool
```

### Show Headers:
```bash
curl -i http://127.0.0.1:5000/health
```

### Show Timing:
```bash
curl -w "\nTotal time: %{time_total}s\n" http://127.0.0.1:5000/health
```

### Timeout After 10 Seconds:
```bash
curl --max-time 10 http://127.0.0.1:5000/health
```

---

## Error Testing

### Invalid Request (Missing Fields):
```bash
curl -X POST http://127.0.0.1:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{"customer_profile": {}}'
```

**Response:**
```json
{
  "error": "Missing required fields: customer_profile, resolution_plan, credit_confirmation",
  "status": "failed"
}
```

### Invalid Endpoint:
```bash
curl http://127.0.0.1:5000/invalid
```

**Response:**
```json
{
  "error": "Endpoint not found",
  "status": "failed",
  "available_endpoints": {...}
}
```

---

## Useful Command Shortcuts

### Windows PowerShell
```powershell
# Define base URL
$BaseURL = "http://127.0.0.1:5000"

# Test health
Invoke-RestMethod -Uri "$BaseURL/health"

# Test generate message
Invoke-RestMethod -Uri "$BaseURL/api/v1/generate-message" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{...json...}'
```

### Bash/Linux
```bash
# Define base URL
BASE_URL="http://127.0.0.1:5000"

# Test health
curl $BASE_URL/health

# Test generate message
curl -X POST $BASE_URL/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{...json...}'
```

---

## Performance Notes

- Health check: <100ms
- Single message generation: 3-5 seconds (LLM processing)
- Batch processing: Linear with message count
- Validation: 1-2 seconds per message
- All times depend on Azure OpenAI response

---

**Recommended:** Use Postman for easier testing!
Import `Postman_Collection.json` for pre-configured requests.
