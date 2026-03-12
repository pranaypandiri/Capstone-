# Customer Communicator Agent - AutoGen Implementation

## Overview

The **Customer Communicator Agent** is an intelligent agent that generates personalized, compliant, and empathetic resolution messages for customers in the complaint resolution workflow. It leverages the AutoGen framework for multi-agent orchestration and OpenAI's language models for natural language generation.

## Architecture

### Agent Components

The Customer Communicator Agent consists of several specialized components:

1. **Message Generator Agent**
   - Generates personalized resolution messages
   - Incorporates customer context and resolution details
   - Maintains empathetic and professional tone
   - Uses communication templates

2. **Compliance Validator Agent**
   - Validates GDPR compliance
   - Checks brand tone alignment
   - Ensures regulatory compliance
   - Provides improvement suggestions

3. **Main Orchestrator (CustomerCommunicatorAgent)**
   - Coordinates between agents
   - Manages data flow
   - Handles template rendering
   - Produces final output

### Data Flow

```
Resolution Plan + Credit Confirmation + Customer Profile
                    ↓
         CustomerCommunicatorAgent
                    ↓
    Message Generator → Context Building → Template Rendering
                    ↓
    Compliance Validator → GDPR & Brand Checks
                    ↓
         Personalized Resolution Message
```

## Input Specifications

### Resolution Plan (`resolution_plan_output_01.json`)
```json
{
  "complaint_id": "CMP-2025-00089",
  "customer_id": "100034",
  "category": "Delivery Delay",
  "actions": [
    {
      "type": "Expedite",
      "details": {
        "new_eta": "2025-11-28",
        "carrier": "BlueDart"
      }
    },
    {
      "type": "GoodwillCredit",
      "details": {
        "percent": 5,
        "apply_to": "item_total",
        "estimated_amount": 2299.5
      }
    }
  ],
  "cost_estimate": {...},
  "policy_compliance": true,
  "validation_status": "pass"
}
```

### Credit Confirmation (`credit_confirmation_output_01.json`)
```json
{
  "complaint_id": "CMP-2025-00089",
  "customer_id": "100034",
  "approval": {
    "status": "approved",
    "amount": 2299.5,
    "currency": "INR",
    "credit_doc": "CR-2025-00221",
    "conditions": ["single_use", "visible_in_next_statement"]
  },
  "audit": {
    "timestamp": "2025-11-28T17:06:56",
    "agent_id": "CTA-01"
  },
  "validation_status": "pass"
}
```

### Customer Profile (`customer_profile_sample_01.json`)
```json
{
  "KNA1": {
    "KUNNR": "100034",
    "NAME1": "Acme Retail Pvt Ltd",
    "STRAS": "12 MG Road",
    "ORT01": "Bengaluru",
    "SMTP_ADDR": "anita.rao@acmeretail.example",
    "TELF1": "+91-80-5555-1100"
  },
  "KNVV": {
    "VKORG": "1000",
    "VTWEG": "10",
    "WAERS": "INR"
  }
}
```

## Output Specification

### Resolution Message Output (`resolution_message_output_01.json`)
```json
{
  "complaint_id": "CMP-2025-00089",
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

## Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd Customer_Communicator_Agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key:**
   ```bash
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY = "your-api-key-here"
   
   # On Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```

5. **Configure LLM settings (optional):**
   - Edit `OAI_CONFIG_LIST.json` with your OpenAI configuration
   - Update `config.py` with custom settings if needed

## Usage

### Basic Usage

```python
from customer_communicator_agent import CustomerCommunicatorAgent

# Initialize agent
agent = CustomerCommunicatorAgent()

# Process files
output = agent.process(
    resolution_plan_file="Inputs/resolution_plan_output_01.json",
    credit_confirmation_file="Inputs/credit_confirmation_output_01.json",
    customer_profile_file="Inputs/customer_profile_sample_01.json",
    output_file="Outputs/resolution_message_output_01.json"
)

# Print result
print(output)
```

### Running Tests

```bash
python test_agent.py
```

This executes:
- Full end-to-end test
- Message personalization test
- Compliance validation test
- Dispatch channel selection test

### Command Line Execution

```bash
python customer_communicator_agent.py
```

## Key Features

### 1. **Personalization**
- Extracts customer name and organization
- Incorporates resolution details (ETA, credit amount, carrier)
- Addresses customer by preferred name
- Customizes message based on complaint category

### 2. **Compliance & Validation**
- **GDPR Compliance**: Checks for sensitive data exposure
- **Brand Tone**: Validates empathetic and professional language
- **Regulatory Compliance**: Ensures accuracy and proper disclaimers
- **Audit Trail**: Maintains complete action history

### 3. **Template-Based Generation**
- Multiple templates for different complaint categories
- Support for context variable substitution
- Professional signature inclusion
- Extensible template system

### 4. **Multi-Channel Support**
- Email (primary channel)
- SMS (character-limited)
- Portal (in-app notification)
- Automatic channel selection based on customer profile

### 5. **Quality Assurance**
- Structure validation
- Tone assessment
- Compliance checks
- Comprehensive error handling

## Configuration

### Agent Configuration (`config.py`)

Key settings:

```python
AGENT_CONFIG = {
    "agent_id": "COM-01",
    "llm_config": {
        "temperature": 0.7,  # Creativity level
        "max_tokens": 1000   # Max response length
    },
    "compliance_settings": {
        "check_gdpr": True,
        "check_brand_tone": True
    },
    "message_settings": {
        "tone": "empathetic",
        "max_message_length": 500
    }
}
```

### Communication Templates (`Data_Sources/communication_templates.json`)

```json
{
  "delay_resolution": "Hello {{name}}, we apologise for the delay. New ETA: {{eta}}. A goodwill credit of {{amount}} {{currency}} has been approved.",
  "signature": "Regards,\nCustomer Care"
}
```

## API Reference

### CustomerCommunicatorAgent Class

#### Methods

**`__init__(config_file: str = None)`**
- Initializes the agent with optional config file
- Loads templates from data sources
- Sets up AutoGen agents

**`generate_message(resolution_plan, credit_confirmation, customer_profile) → Dict`**
- Generates personalized message
- Returns dict with message and validation details

**`process(resolution_plan_file, credit_confirmation_file, customer_profile_file, output_file) → Dict`**
- End-to-end processing of input files
- Saves output to JSON file
- Returns generated message

#### Internal Methods

**`_extract_recipient_info(customer_profile) → Dict`**
- Extracts name, email, phone from customer profile

**`_build_message_context(resolution_plan, credit_confirmation, customer_profile) → Dict`**
- Builds context for template rendering

**`_render_message(context) → str`**
- Fills template with context values
- Returns complete message with signature

**`_validate_compliance(message, context) → Dict`**
- Validates GDPR and brand compliance
- Returns compliance report

## Workflow Integration

### Within Complaint Resolution Workflow

1. **Input Stage**: Receives outputs from:
   - Remedy Planner Agent (resolution plan)
   - Credit Trigger Agent (credit confirmation)
   - CRM System (customer profile)

2. **Processing Stage**:
   - Extracts relevant data
   - Builds message context
   - Generates personalized message
   - Validates compliance

3. **Output Stage**:
   - Produces resolution message JSON
   - Passes to dispatch system
   - Logs to audit trail

### Orchestration

The agent is triggered by the **Orchestration Agent** after:
- ✓ Complaint classification complete
- ✓ Evidence collected
- ✓ Remedy plan finalized
- ✓ Credit approved (if applicable)

## Validation & Compliance

### GDPR Compliance Checks
- ✓ No unnecessary personal data in messages
- ✓ Proper data handling for sensitive information
- ✓ Transparent communication practices
- ✓ Right to be informed

### Brand Compliance Checks
- ✓ Professional and empathetic tone
- ✓ Brand voice consistency
- ✓ No threatening or demanding language
- ✓ Solution-oriented messaging

### Output Validation
- ✓ All required fields present
- ✓ Valid email/phone format
- ✓ Message length within limits
- ✓ Valid dispatch channel

## Error Handling

The agent handles various error scenarios:

```python
# Missing template file
→ Falls back to default template

# Invalid customer profile
→ Uses generic "Customer" greeting

# No email available
→ Selects SMS or portal channel

# LLM API unavailable
→ Uses rule-based message generation
```

## Performance Considerations

- **Message Generation**: ~1-2 seconds (with LLM)
- **Compliance Validation**: ~0.5-1 second
- **Template Rendering**: <100ms
- **File I/O**: <50ms

Optimizations:
- Template caching
- Batch processing for multiple messages
- Async validation (optional)

## Limitations & Future Enhancements

### Current Limitations
1. Single-language support (English only)
2. Limited template variations
3. Basic tone validation

### Future Enhancements
1. Multi-language support
2. AI-powered tone adjustment
3. A/B testing framework
4. Customer preference learning
5. Dynamic template generation
6. Real-time sentiment analysis

## Troubleshooting

### Issue: "API Key not found"
**Solution**: Set `OPENAI_API_KEY` environment variable

### Issue: "Template file not found"
**Solution**: Ensure `Data_Sources/communication_templates.json` exists

### Issue: "Invalid input data"
**Solution**: Validate JSON structure matches specifications

### Issue: "Message generation timeout"
**Solution**: Check LLM API availability, adjust timeout settings

## Testing

Run comprehensive test suite:

```bash
python test_agent.py
```

Tests included:
- ✓ Full end-to-end workflow
- ✓ Message personalization
- ✓ Compliance validation
- ✓ Channel selection
- ✓ Output structure validation

## Contributing & Extension

### Adding New Templates

1. Edit `Data_Sources/communication_templates.json`
2. Add new template with descriptive key
3. Update `config.py` category mapping

### Custom Compliance Rules

Extend `_validate_compliance()` method in `customer_communicator_agent.py`

### Multi-Language Support

Implement language detection and template mapping in `_select_template()` method

## Audit & Compliance

All actions are logged for compliance reporting:

```json
{
  "timestamp": "2025-11-28T17:06:56",
  "agent_id": "COM-01",
  "complaint_id": "CMP-2025-00089",
  "action": "message_generated",
  "compliance_checks": {"gdpr": true, "brand": true}
}
```

## License & Support

For support or enhancement requests, contact the development team.

---

**Version**: 1.0  
**Last Updated**: January 4, 2026  
**Status**: Production Ready
