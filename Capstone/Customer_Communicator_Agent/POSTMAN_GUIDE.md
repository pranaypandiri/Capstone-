# Customer Communicator Agent - Flask API - Quick Start Guide

## ✅ Server Status: RUNNING

The Flask API server is now running at: **http://127.0.0.1:5000**

---

## 📋 POSTMAN TESTING GUIDE

### Step 1: Open Postman
- Download Postman: https://www.postman.com/downloads/

### Step 2: Import Collection
1. Click **Import** button (top-left)
2. Select **Postman_Collection.json** from this folder
3. All endpoints are pre-configured

### Step 3: Send Requests
All requests will show:
- **Response** in Postman (JSON format)
- **Terminal Output** in your CLI (real-time logging)

---

## 🚀 Quick Test Requests

### Test 1: Health Check
**Method:** GET  
**URL:** `http://127.0.0.1:5000/health`

In Postman:
1. Click **New** → **Request**
2. Set method to **GET**
3. Paste URL: `http://127.0.0.1:5000/health`
4. Click **Send**

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Customer Communicator API",
  "timestamp": "2026-01-13T...",
  "agent_ready": true
}
```

**Terminal Output:**
```
[2026-01-13 10:35:45] GET /health - 200 OK
```

---

### Test 2: Get Agent Status
**Method:** GET  
**URL:** `http://127.0.0.1:5000/api/v1/status`

**Expected Response:**
```json
{
  "agent_id": "COM-01",
  "status": "ready",
  "timestamp": "2026-01-13T...",
  "endpoints": {...}
}
```

---

### Test 3: Generate Single Message
**Method:** POST  
**URL:** `http://127.0.0.1:5000/api/v1/generate-message`

**Steps:**
1. Create new request in Postman
2. Set method to **POST**
3. Paste URL above
4. Go to **Body** tab
5. Select **raw** and **JSON** format
6. Paste this:

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

7. Click **Send**

**Expected Response (Postman):**
```json
{
  "status": "success",
  "data": {
    "complaint_id": "CMP-2025-00089",
    "customer_id": "100034",
    "to": {...},
    "body": "Dear Acme,\n\nWe sincerely apologize for the delay...",
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

**Terminal Output (CLI):**
```
======================================================================
INCOMING API REQUEST
======================================================================
Timestamp: 2026-01-13T10:35:45.123456
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
  ...
  "body": "Dear Acme,\n\nWe sincerely apologize for the delay in delivering your order with Complaint ID CMP-2025-00089...",
  ...
}
======================================================================
127.0.0.1 - - [13/Jan/2026 10:35:45] "POST /api/v1/generate-message HTTP/1.1" 200 -
```

---

### Test 4: Batch Generate Messages
**Method:** POST  
**URL:** `http://127.0.0.1:5000/api/v1/batch-generate`

**Steps:**
1. New POST request in Postman
2. In **Body** tab, paste:

```json
{
  "messages": [
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
    },
    {
      "customer_profile": {
        "KNA1": {
          "customer_id": "100035",
          "name": "Beta Corp",
          "email": "contact@betacorp.example",
          "phone": "+91-80-5555-1101"
        },
        "KNVV": {
          "currency": "INR"
        }
      },
      "resolution_plan": {
        "complaint_id": "CMP-2025-00090",
        "category": "Quality Issue",
        "actions": [
          {
            "action_type": "Replace",
            "quantity": 5
          }
        ]
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
}
```

3. Click **Send**

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

---

## 📊 Real-Time Terminal Output

Every Postman request shows detailed logs in the terminal:

**Terminal Window Shows:**
- Incoming request details (customer ID, complaint ID)
- Agent processing status
- Message generation confirmation
- Compliance validation confirmation
- Complete response JSON
- HTTP status code

Example:
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
```

---

## 🔧 Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check API health |
| GET | `/api/v1/status` | Get agent status |
| POST | `/api/v1/generate-message` | Generate single message |
| POST | `/api/v1/batch-generate` | Generate multiple messages |
| POST | `/api/v1/validate` | Validate message compliance |

---

## 📝 Using the Postman Collection

**File:** `Postman_Collection.json`

### Import Steps:
1. Open Postman
2. Click **Import** button (top-left)
3. Choose **File** tab
4. Select `Postman_Collection.json`
5. Click **Import**

All 5 endpoints will be pre-configured:
- ✅ Health Check
- ✅ Agent Status
- ✅ Generate Single Message
- ✅ Batch Generate Messages
- ✅ Validate Message Compliance

### Using Pre-Configured Requests:
1. Expand collection in left sidebar
2. Click any request
3. Click **Send**
4. View response + terminal logs

---

## 🎯 What's Happening Behind the Scenes

1. **Postman sends JSON** → Flask API receives it
2. **Flask validates** → Checks for required fields
3. **Agent processes** → Calls Message Generator and Compliance Validator agents
4. **Agents invoke LLM** → Azure GPT-4o generates intelligent responses
5. **Response generated** → JSON returned to Postman
6. **Terminal logs** → All details displayed in your CLI

---

## 🛠️ Common Postman Settings

### Headers
Most requests need:
```
Content-Type: application/json
```

### Timeout (if requests time out)
Settings → General → Request timeout: 30000ms

### Pretty Print
Response automatically formatted as JSON

---

## 📋 Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | ✅ Success |
| 400 | ❌ Bad request (missing fields) |
| 500 | ❌ Server error |
| 503 | ❌ Service unavailable |

---

## 🚀 Try It Now!

1. **Keep terminal running** with Flask server
2. **Open Postman**
3. **Import Postman_Collection.json**
4. **Click any endpoint**
5. **Click Send**
6. **Watch terminal** for real-time logs

---

## 📚 Full Documentation

See **API_DOCUMENTATION.md** for:
- Detailed endpoint documentation
- Request/response examples
- Error handling
- Integration examples
- Performance notes

---

**Status:** ✅ API Server Running at http://127.0.0.1:5000
