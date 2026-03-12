# Flask API for Customer Communicator Agent

## 🎯 Overview

Transform your Customer Communicator Agent from a command-line tool into a production-ready REST API using Flask. Test endpoints with Postman and see real-time logs in your terminal.

**Key Features:**
- ✅ RESTful API with 5 endpoints
- ✅ Multi-agent orchestration (Message Generator + Compliance Validator)
- ✅ Azure OpenAI integration (GPT-4o)
- ✅ Real-time terminal logging for all requests
- ✅ Single & batch message generation
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive error handling

---

## 📁 New Files Created

| File | Purpose |
|------|---------|
| `flask_api.py` | Main Flask API server (5 endpoints) |
| `Postman_Collection.json` | Pre-configured Postman requests |
| `API_DOCUMENTATION.md` | Full API documentation |
| `POSTMAN_GUIDE.md` | Step-by-step Postman testing guide |
| `test_api.bat` | Windows batch script for quick curl tests |

---

## 🚀 Quick Start

### 1. Verify Flask Installation
```bash
python -m pip list | grep -i flask
```

Should show:
```
Flask 3.1.2
Flask-CORS 6.0.2
```

### 2. Start the API Server
```bash
python flask_api.py
```

**Output:**
```
✓ Agent initialized successfully

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

 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 3. Test with Postman
- Open Postman
- Click **Import** button
- Select `Postman_Collection.json`
- All endpoints pre-configured!

### 4. View Real-Time Logs
All terminal output shows:
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
{...json response...}
======================================================================
```

---

## 📊 API Endpoints

### Health Check
```
GET /health
```
Quick check if API is running.

### Agent Status
```
GET /api/v1/status
```
Get agent configuration and available endpoints.

### Generate Single Message
```
POST /api/v1/generate-message
```
Generate personalized message for one customer.

**Input:**
```json
{
  "customer_profile": {...},
  "resolution_plan": {...},
  "credit_confirmation": {...}
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "complaint_id": "CMP-2025-00089",
    "body": "Dear Acme, We sincerely apologize...",
    "compliance": {...},
    "validation_status": "pass"
  }
}
```

### Batch Generate
```
POST /api/v1/batch-generate
```
Generate messages for multiple customers.

**Input:**
```json
{
  "messages": [
    {...message1...},
    {...message2...}
  ]
}
```

**Output:**
```json
{
  "status": "completed",
  "total": 2,
  "succeeded": 2,
  "failed": 0,
  "results": [...]
}
```

### Validate Message
```
POST /api/v1/validate
```
Validate message for GDPR & brand compliance.

---

## 🧪 Testing Methods

### Method 1: Postman (Recommended)
1. Import `Postman_Collection.json`
2. Click any endpoint
3. Click **Send**
4. View response + terminal logs

### Method 2: cURL (Command Line)
```bash
# Health check
curl http://127.0.0.1:5000/health

# Generate message
curl -X POST http://127.0.0.1:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{...json body...}'
```

### Method 3: Windows Batch Script
```bash
test_api.bat
```
Interactive menu for quick testing.

### Method 4: Python Client
```python
import requests

response = requests.post(
    "http://127.0.0.1:5000/api/v1/generate-message",
    json={...}
)
print(response.json())
```

---

## 💻 Terminal Output Example

When you send a request from Postman, the terminal shows:

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
{
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
}
======================================================================
127.0.0.1 - - [13/Jan/2026 10:35:45] "POST /api/v1/generate-message HTTP/1.1" 200 -
```

---

## 🔍 Understanding the Flow

```
┌──────────────┐
│   Postman    │
└──────┬───────┘
       │ HTTP POST/GET
       ▼
┌────────────────────────────────┐
│   Flask API Server             │
│   (http://127.0.0.1:5000)      │
└──────┬────────────────────────┘
       │ Validate & Process
       ▼
┌────────────────────────────────────────────────┐
│  CustomerCommunicatorAgent                     │
│  ├─ Message Generator Agent                    │
│  │  └─ LLM: Azure GPT-4o (personalization)    │
│  └─ Compliance Validator Agent                 │
│     └─ LLM: Azure GPT-4o (validation)         │
└──────┬────────────────────────────────────────┘
       │ Response with agents' outputs
       ▼
┌────────────────────────────────┐
│   JSON Response                │
│   + Terminal Logging           │
└──────┬────────────────────────┘
       │
       ▼
┌──────────────┐
│   Postman    │  ← Shows response
└──────────────┘
       ↑
       │
   Terminal ← Shows detailed logs
```

---

## 📝 Example Requests

### Request 1: Health Check
```
GET http://127.0.0.1:5000/health
```

### Request 2: Generate Message
```
POST http://127.0.0.1:5000/api/v1/generate-message
Content-Type: application/json

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
}
```

### Response:
```json
{
  "status": "success",
  "data": {
    "complaint_id": "CMP-2025-00089",
    "customer_id": "100034",
    "to": {...},
    "body": "Dear Acme,\n\nWe sincerely apologize...",
    "dispatch_channel": "email",
    "tone": "empathetic",
    "compliance": {"gdpr": true, "brand": true},
    "validation_status": "pass",
    "timestamp": "2026-01-13T10:35:45.123456",
    "agent_id": "COM-01"
  },
  "timestamp": "2026-01-13T10:35:45.123456"
}
```

---

## 🛠️ Configuration

### Port Configuration
To change port from 5000 to another (e.g., 8080):

Edit `flask_api.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)  # Change here
```

### CORS Configuration
CORS is enabled for all origins. To restrict:

Edit `flask_api.py`:
```python
from flask_cors import CORS

# Change from:
CORS(app)  # All origins

# To:
CORS(app, origins=['http://localhost:3000', 'https://myapp.com'])
```

### Debug Mode
- `debug=True`: Auto-reload on code changes, detailed errors
- `debug=False`: Production mode (don't change while testing)

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -ti:5000

# Kill it
kill -9 <PID>

# Or use different port in flask_api.py
```

### Flask Not Found
```bash
# Install Flask
python -m pip install flask flask-cors

# Verify
python -m pip list | grep Flask
```

### Agent Not Initializing
- Check `.env` file has valid Azure credentials
- Verify `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL` are set
- Test: `python customer_communicator_agent.py`

### Request Timeout
- Increase Postman timeout: Settings → General → Request timeout
- Check Azure OpenAI service status
- Verify internet connection

### CORS Errors
- Flask-CORS is enabled by default
- If errors persist, check browser console
- Ensure correct URL in Postman

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| `API_DOCUMENTATION.md` | Complete API reference |
| `POSTMAN_GUIDE.md` | Step-by-step Postman guide |
| `flask_api.py` | Source code with docstrings |

---

## 🎓 Learning Path

1. **Start Here:** Run `python flask_api.py`
2. **Quick Test:** Use Postman collection
3. **View Logs:** Watch terminal output
4. **Read Docs:** Check `POSTMAN_GUIDE.md`
5. **Deep Dive:** Review `API_DOCUMENTATION.md`
6. **Modify:** Edit `flask_api.py` for custom endpoints

---

## 🚀 Next Steps

### For Development:
- Modify Flask endpoints in `flask_api.py`
- Add new routes
- Customize error handling
- Add logging

### For Integration:
- Import Postman collection
- Test with your frontend
- Use Python/JavaScript clients
- Deploy to production

### For Production:
- Use WSGI server (Gunicorn)
- Enable SSL/HTTPS
- Add authentication
- Setup load balancer
- Monitor performance

---

## 📞 Support

**Questions?** Check:
1. `API_DOCUMENTATION.md` - Full API reference
2. `POSTMAN_GUIDE.md` - Postman usage
3. `README.md` - Project overview
4. Code comments in `flask_api.py`

---

## ✅ Verification Checklist

Before using in production:
- [ ] Flask server running without errors
- [ ] Postman can connect to `http://127.0.0.1:5000`
- [ ] Health check endpoint returns 200
- [ ] Generate message endpoint works
- [ ] Terminal shows detailed logs
- [ ] Azure credentials are correct
- [ ] All 5 endpoints tested
- [ ] Error handling works correctly

---

**Status:** ✅ API Ready to Use
**Server:** http://127.0.0.1:5000
**Version:** 1.0
**Last Updated:** 2026-01-13
