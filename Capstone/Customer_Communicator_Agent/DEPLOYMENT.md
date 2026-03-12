# Customer Communicator Agent - Deployment & Integration Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Testing](#testing)
4. [Deployment](#deployment)
5. [Integration](#integration)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### System Requirements
- **Python**: 3.8+
- **OS**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum
- **Disk Space**: 500MB for dependencies

### Required Credentials
- **OpenAI API Key**: For GPT-4 language model access
- **Database Access**: For CRM and ERP connections (future enhancement)
- **Email/SMS Service**: For message dispatch

### Dependencies
All dependencies are listed in `requirements.txt`:
```
autogen>=0.2.0
openai>=1.0.0
python-dotenv>=0.19.0
```

---

## Development Setup

### Step 1: Environment Configuration

#### Windows PowerShell
```powershell
# Set API key
$env:OPENAI_API_KEY = "sk-your-api-key-here"

# Verify
echo $env:OPENAI_API_KEY
```

#### Linux/macOS Bash
```bash
# Set API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Verify
echo $OPENAI_API_KEY
```

#### Using .env file (Recommended)
Create `.env` file in project root:
```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
LOG_LEVEL=INFO
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

### Step 2: Virtual Environment Setup

```bash
# Navigate to project directory
cd Customer_Communicator_Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configuration

1. **LLM Configuration** (`OAI_CONFIG_LIST.json`):
```json
[
    {
        "model": "gpt-4-turbo",
        "api_key": "${OPENAI_API_KEY}",
        "base_url": "https://api.openai.com/v1",
        "api_type": "openai",
        "temperature": 0.7,
        "max_tokens": 1000
    }
]
```

2. **Agent Configuration** (`config.py`):
```python
AGENT_CONFIG = {
    "agent_id": "COM-01",
    "llm_config": {
        "config_list": "OAI_CONFIG_LIST.json",
        "cache_seed": 42,
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "compliance_settings": {
        "check_gdpr": True,
        "check_brand_tone": True
    }
}
```

---

## Testing

### Unit Tests

Run individual test components:

```bash
# Test message personalization
python -c "
from test_agent import AgentTester
tester = AgentTester()
tester.test_message_personalization()
"

# Test compliance validation
python -c "
from test_agent import AgentTester
tester = AgentTester()
tester.test_compliance_validation()
"

# Test channel selection
python -c "
from test_agent import AgentTester
tester = AgentTester()
tester.test_dispatch_channel_selection()
"
```

### Integration Tests

```bash
# Run full integration test
python test_agent.py
```

### Test Coverage

Test suite includes:
- ✓ End-to-end message generation
- ✓ Personalization accuracy
- ✓ Compliance validation (GDPR, Brand)
- ✓ Channel selection logic
- ✓ Output structure validation
- ✓ Error handling

### Test Data

Sample test data in `Inputs/`:
- `customer_profile_sample_01.json` - Customer data
- `resolution_plan_output_01.json` - Remedy plan
- `credit_confirmation_output_01.json` - Credit details

Expected output in `Outputs/`:
- `resolution_message_output_01.json` - Generated message

---

## Deployment

### Production Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] API key configured and validated
- [ ] Logging configured
- [ ] Error monitoring setup
- [ ] Documentation reviewed
- [ ] Performance tested with production-like data
- [ ] Security audit completed
- [ ] Backup and disaster recovery plan

### Deployment Options

#### Option 1: Direct Python Execution

```bash
# Simple execution
python customer_communicator_agent.py

# With logging
python -u customer_communicator_agent.py 2>&1 | tee execution.log
```

#### Option 2: Docker Containerization

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "customer_communicator_agent.py"]
```

**Build and Run:**
```bash
# Build image
docker build -t customer-communicator:1.0 .

# Run container
docker run \
  --env OPENAI_API_KEY="sk-your-key" \
  -v $(pwd)/Inputs:/app/Inputs \
  -v $(pwd)/Outputs:/app/Outputs \
  customer-communicator:1.0
```

#### Option 3: Kubernetes Deployment

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: customer-communicator-agent
  labels:
    app: customer-communicator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: customer-communicator
  template:
    metadata:
      labels:
        app: customer-communicator
    spec:
      containers:
      - name: agent
        image: customer-communicator:1.0
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-credentials
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: agent-data-pvc
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
kubectl get pods -l app=customer-communicator
```

#### Option 4: Serverless (AWS Lambda)

**Lambda Handler:**
```python
import json
import os
from customer_communicator_agent import CustomerCommunicatorAgent

def lambda_handler(event, context):
    try:
        agent = CustomerCommunicatorAgent()
        
        # Parse inputs from event
        resolution_plan = event['resolution_plan']
        credit_confirmation = event['credit_confirmation']
        customer_profile = event['customer_profile']
        
        # Generate message
        output = agent.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

**Deployment:**
```bash
# Package
zip -r lambda-deployment.zip . -x "venv/*" ".git/*"

# Upload to AWS Lambda
aws lambda create-function \
  --function-name customer-communicator-agent \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler customer_communicator_agent.lambda_handler \
  --zip-file fileb://lambda-deployment.zip
```

---

## Integration

### Integration with O2C Workflow

#### 1. Orchestration Agent Interface

```python
# Orchestration Agent calls Customer Communicator
orchestration_payload = {
    "agent_type": "customer_communicator",
    "inputs": {
        "resolution_plan": resolution_plan_output,
        "credit_confirmation": credit_confirmation_output,
        "customer_profile": customer_profile
    }
}

# Call Customer Communicator
response = communicator_agent.process(
    resolution_plan_file,
    credit_confirmation_file,
    customer_profile_file,
    output_file
)
```

#### 2. Message Routing

**Email Dispatch:**
```python
import smtplib
from email.mime.text import MIMEText

def send_email(message_output):
    sender = "noreply@company.com"
    recipient = message_output['to']['email']
    subject = f"Resolution for Complaint {message_output['complaint_id']}"
    
    msg = MIMEText(message_output['body'])
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    # Send via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
```

**SMS Dispatch:**
```python
from twilio.rest import Client

def send_sms(message_output):
    account_sid = "TWILIO_ACCOUNT_SID"
    auth_token = "TWILIO_AUTH_TOKEN"
    client = Client(account_sid, auth_token)
    
    # Split long messages for SMS
    from advanced_usage import AdvancedCommunicatorUsage
    sms_messages = AdvancedCommunicatorUsage.export_to_sms_format(message_output)
    
    for sms_text in sms_messages:
        message = client.messages.create(
            body=sms_text,
            from_="+1234567890",
            to=message_output['to']['phone']
        )
```

#### 3. Audit Logging

```python
import logging
from datetime import datetime

def log_message_generation(output):
    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "complaint_id": output['complaint_id'],
        "customer_id": output.get('customer_id'),
        "agent_id": output['agent_id'],
        "action": "message_generated",
        "channel": output['dispatch_channel'],
        "compliance": output['compliance'],
        "validation_status": output['validation_status']
    }
    
    # Log to file or database
    logging.info(json.dumps(audit_log))
    
    # Store in audit database
    audit_db.insert(audit_log)
```

### API Integration

#### REST API Wrapper

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
agent = CustomerCommunicatorAgent()

@app.route('/api/v1/generate-message', methods=['POST'])
def generate_message_api():
    """
    POST /api/v1/generate-message
    
    Request body:
    {
        "resolution_plan": {...},
        "credit_confirmation": {...},
        "customer_profile": {...}
    }
    """
    try:
        data = request.json
        
        output = agent.generate_message(
            data['resolution_plan'],
            data['credit_confirmation'],
            data['customer_profile']
        )
        
        return jsonify(output), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "agent_id": "COM-01"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Run API Server:**
```bash
python flask_app.py
```

**Call API:**
```bash
curl -X POST http://localhost:5000/api/v1/generate-message \
  -H "Content-Type: application/json" \
  -d '{
    "resolution_plan": {...},
    "credit_confirmation": {...},
    "customer_profile": {...}
  }'
```

#### GraphQL API (Alternative)

```python
import graphene
from graphene import ObjectType, String, Field

class MessageOutput(ObjectType):
    complaint_id = String()
    body = String()
    dispatch_channel = String()
    validation_status = String()

class Query(ObjectType):
    generate_message = Field(
        MessageOutput,
        resolution_plan=String(required=True),
        credit_confirmation=String(required=True),
        customer_profile=String(required=True)
    )
    
    def resolve_generate_message(self, info, **kwargs):
        # Implementation
        pass

schema = graphene.Schema(query=Query)
```

---

## Monitoring & Maintenance

### Logging Configuration

**logging_config.py:**
```python
import logging
import logging.handlers

# Configure file handler
file_handler = logging.handlers.RotatingFileHandler(
    'logs/agent.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

# Configure console handler
console_handler = logging.StreamHandler()

# Set format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger = logging.getLogger('CustomerCommunicator')
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
```

### Metrics & Monitoring

**Key Metrics:**
- Message generation latency
- Compliance check success rate
- API response time
- Error rate
- Message delivery rate

**Monitoring Tools:**
- Prometheus (metrics collection)
- Grafana (visualization)
- ELK Stack (logging)
- DataDog (APM)

### Maintenance Tasks

**Daily:**
- Monitor error logs
- Check API availability
- Verify message generation success rate

**Weekly:**
- Review performance metrics
- Check for unusual patterns
- Test failover procedures

**Monthly:**
- Update dependencies
- Review and optimize queries
- Conduct security audit
- Backup logs and data

### Rollback Procedure

```bash
# If new version causes issues

# 1. Stop current version
docker stop customer-communicator

# 2. Switch to previous image
docker run --name customer-communicator \
  --image customer-communicator:0.9 \
  ...

# 3. Verify health
curl http://localhost:5000/api/v1/health

# 4. Investigate issue
tail -f logs/agent.log
```

### Performance Optimization

**Tips:**
1. Use template caching
2. Batch process messages
3. Optimize LLM calls (fewer tokens)
4. Use connection pooling for databases
5. Implement rate limiting for API

**Benchmarking:**
```python
import time

def benchmark_message_generation(iterations=100):
    start = time.time()
    
    for _ in range(iterations):
        output = agent.generate_message(...)
    
    elapsed = time.time() - start
    avg_time = elapsed / iterations
    
    print(f"Average time: {avg_time:.2f}s")
    print(f"Messages/second: {1/avg_time:.2f}")
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| API Key Error | Invalid/missing key | Set OPENAI_API_KEY environment variable |
| Template Not Found | Wrong path | Verify Data_Sources/ directory structure |
| Generation Timeout | LLM slow | Increase timeout, reduce token limit |
| Memory Issues | Large batch | Process in smaller batches |
| Channel Selection Failed | Missing contact info | Ensure customer profile has email or phone |

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python customer_communicator_agent.py

# With verbose output
python -v customer_communicator_agent.py
```

---

**Document Version**: 1.0  
**Last Updated**: January 4, 2026  
**Maintainer**: AI Development Team
