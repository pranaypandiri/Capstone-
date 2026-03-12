# Quick Start Guide - Customer Communicator Agent

## 5-Minute Quick Start

### 1. Prerequisites Check
```bash
python --version  # Should be 3.8+
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API Key
**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

**Linux/macOS:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

### 4. Run Agent
```bash
python customer_communicator_agent.py
```

### 5. Check Output
Output will be generated in:
```
Outputs/resolution_message_output_01.json
```

---

## Testing the Agent (10 Minutes)

```bash
# Run comprehensive test suite
python test_agent.py
```

Expected output:
```
✓ Full Test: PASSED
✓ Personalization: PASSED
✓ Compliance: PASSED
✓ Channel Selection: PASSED
✓ ALL TESTS PASSED
```

---

## Key Features Demo

### Generate Personalized Message
```python
from customer_communicator_agent import CustomerCommunicatorAgent

agent = CustomerCommunicatorAgent()

# Your data
resolution_plan = {...}
credit_confirmation = {...}
customer_profile = {...}

# Generate message
message = agent.generate_message(
    resolution_plan,
    credit_confirmation,
    customer_profile
)

print(message['body'])
# Output: "Hello Anita Rao, we apologise for the delay..."
```

### Validate Compliance
```python
# Message automatically validated for:
# - GDPR compliance ✓
# - Brand tone ✓
# - Regulatory compliance ✓

print(message['compliance'])
# {'gdpr': True, 'brand': True}
```

### Multi-Channel Support
```python
# Agent automatically selects channel:
print(message['dispatch_channel'])
# 'email' | 'sms' | 'portal'
```

---

## Project Structure

```
Customer_Communicator_Agent/
│
├── customer_communicator_agent.py     # Main agent implementation
├── test_agent.py                      # Test suite
├── advanced_usage.py                  # Advanced patterns
├── config.py                          # Configuration
│
├── Data_Sources/
│   └── communication_templates.json   # Message templates
│
├── Inputs/
│   ├── customer_profile_sample_01.json
│   ├── resolution_plan_output_01.json
│   └── credit_confirmation_output_01.json
│
├── Outputs/
│   └── resolution_message_output_01.json
│
├── README.md                          # Full documentation
├── ARCHITECTURE.md                    # Architecture & design
├── DEPLOYMENT.md                      # Deployment guide
├── QUICKSTART.md                      # This file
├── requirements.txt                   # Dependencies
└── OAI_CONFIG_LIST.json              # LLM config
```

---

## Common Commands

```bash
# Run main agent
python customer_communicator_agent.py

# Run tests
python test_agent.py

# Run advanced examples
python advanced_usage.py

# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source venv/bin/activate
```

---

## API Usage

### Basic Usage
```python
from customer_communicator_agent import CustomerCommunicatorAgent
import json

# Initialize
agent = CustomerCommunicatorAgent()

# Load inputs
with open('Inputs/resolution_plan_output_01.json') as f:
    plan = json.load(f)

with open('Inputs/credit_confirmation_output_01.json') as f:
    credit = json.load(f)

with open('Inputs/customer_profile_sample_01.json') as f:
    profile = json.load(f)

# Process
result = agent.generate_message(plan, credit, profile)

# Output
print(json.dumps(result, indent=2))
```

### End-to-End Processing
```python
# All in one call
output = agent.process(
    resolution_plan_file='Inputs/resolution_plan_output_01.json',
    credit_confirmation_file='Inputs/credit_confirmation_output_01.json',
    customer_profile_file='Inputs/customer_profile_sample_01.json',
    output_file='Outputs/resolution_message_output_01.json'
)
```

---

## Output Format

```json
{
  "complaint_id": "CMP-2025-00089",
  "customer_id": "100034",
  "to": {
    "name": "Anita Rao",
    "email": "anita.rao@acmeretail.example",
    "phone": "+91-80-5555-1100"
  },
  "body": "Hello Anita Rao, we apologise for the delay. New ETA: 2025-11-28. A goodwill credit of 2299.50 INR has been approved.\n\nRegards,\nCustomer Care",
  "dispatch_channel": "email",
  "tone": "empathetic",
  "compliance": {
    "gdpr": true,
    "brand": true
  },
  "validation_status": "pass",
  "timestamp": "2025-11-28T17:06:56",
  "agent_id": "COM-01"
}
```

---

## Troubleshooting

### Error: "API Key not found"
```bash
# Set the API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Verify it's set
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY%  # Windows
```

### Error: "Template file not found"
```bash
# Verify file exists
ls Data_Sources/communication_templates.json

# If missing, check working directory
pwd
```

### Error: "Module not found: autogen"
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import autogen; print(autogen.__version__)"
```

### Slow Performance
```bash
# Check API availability
curl https://api.openai.com/v1/models

# Reduce token limit in config.py
"max_tokens": 500  # Instead of 1000
```

---

## Next Steps

1. ✅ Run the quick start
2. ✅ Run the test suite
3. 📖 Read [README.md](README.md) for comprehensive documentation
4. 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
5. 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
6. 💡 Explore [advanced_usage.py](advanced_usage.py) for advanced patterns

---

## Support & Documentation

| Resource | Purpose |
|----------|---------|
| [README.md](README.md) | Full feature documentation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and patterns |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide |
| [test_agent.py](test_agent.py) | Working code examples |
| [advanced_usage.py](advanced_usage.py) | Advanced usage patterns |

---

## Key Points

✓ **AutoGen-powered** - Uses AutoGen framework for multi-agent orchestration  
✓ **AI-generated messages** - Powered by GPT-4 for natural language generation  
✓ **Compliant** - Validates GDPR and brand compliance  
✓ **Multi-channel** - Supports email, SMS, and portal dispatch  
✓ **Production-ready** - Comprehensive testing and error handling  
✓ **Extensible** - Easy to customize templates and rules  

---

**Last Updated**: January 4, 2026  
**Version**: 1.0
