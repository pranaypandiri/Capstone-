# Customer Communicator Agent - Architecture & Design Document

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    O2C Complaint Resolution Workflow             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Complaint    │  │   Evidence   │  │    Remedy    │           │
│  │ Classifier   │→ │  Collector   │→ │   Planner    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                              ↓                    │
│                                       ┌──────────────┐           │
│                                       │    Credit    │           │
│                                       │   Trigger    │           │
│                                       └──────────────┘           │
│                                              ↓                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │     CUSTOMER COMMUNICATOR AGENT (This Module)           │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐ │    │
│  │  │   Message    │   │ Compliance   │   │   Dispatch   │ │    │
│  │  │  Generator   │→  │  Validator   │→  │  Selector    │ │    │
│  │  └──────────────┘   └──────────────┘   └──────────────┘ │    │
│  │                                                           │    │
│  │  Output: Personalized Resolution Message                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                    │
│                    ┌──────────────────┐                          │
│                    │  Audit Logger    │                          │
│                    │  & Dispatcher    │                          │
│                    └──────────────────┘                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Diagram

```
CustomerCommunicatorAgent (Main Orchestrator)
│
├── Message Generator Agent (AutoGen)
│   └── Uses: Customer Profile, Resolution Details, Templates
│       Produces: Personalized message content
│
├── Compliance Validator Agent (AutoGen)
│   └── Uses: Generated message content
│       Produces: Compliance validation results
│
├── Template Manager
│   └── Uses: communication_templates.json
│       Produces: Rendered message with substitutions
│
└── Output Formatter
    └── Uses: All above results
        Produces: Final JSON message object
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        INPUTS                                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Resolution Plan      Credit Confirmation    Customer Profile     │
│  ├─ complaint_id      ├─ status              ├─ KNA1             │
│  ├─ category          ├─ amount              │  ├─ NAME1          │
│  ├─ actions           ├─ currency            │  ├─ SMTP_ADDR      │
│  └─ cost_estimate     └─ credit_doc          │  └─ TELF1          │
│                                               └─ KNVV             │
│                                                  └─ WAERS         │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
            ╔════════════════════════════╗
            ║   Data Extraction & Build   ║
            ║   Message Context          ║
            ╚════════════════════════════╝
                         │
                ┌────────┼────────┐
                ↓        ↓        ↓
            ┌──────┐  ┌──────┐  ┌──────┐
            │Name  │  │ ETA  │  │Amnt  │
            └──────┘  └──────┘  └──────┘
                │        │        │
                └────────┼────────┘
                         ↓
            ╔════════════════════════════╗
            ║   Template Selection &      ║
            ║   Rendering                 ║
            ╚════════════════════════════╝
                         │
                         ↓
            ╔════════════════════════════╗
            ║   Message Generation       ║
            ║   (LLM-powered)            ║
            ╚════════════════════════════╝
                         │
                         ↓
            ╔════════════════════════════╗
            ║   Compliance Validation    ║
            ║   - GDPR                   ║
            ║   - Brand Tone             ║
            ║   - Regulatory             ║
            ╚════════════════════════════╝
                         │
                         ↓
            ╔════════════════════════════╗
            ║   Dispatch Channel         ║
            ║   Selection                ║
            ╚════════════════════════════╝
                         │
┌────────────────────────┴────────────────────────────────┐
│                     OUTPUT                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Personalized Resolution Message                 │  │
│  ├──────────────────────────────────────────────────┤  │
│  │ ├─ complaint_id                                  │  │
│  │ ├─ to: {name, email, phone}                      │  │
│  │ ├─ body: <empathetic resolution message>         │  │
│  │ ├─ dispatch_channel: email|sms|portal            │  │
│  │ ├─ compliance: {gdpr: bool, brand: bool}         │  │
│  │ ├─ validation_status: pass|flag                  │  │
│  │ ├─ timestamp: ISO8601                            │  │
│  │ └─ agent_id: COM-01                              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Agent Responsibilities

### Message Generator Agent

**Purpose**: Generate contextually appropriate, personalized messages

**Inputs**:
- Customer name and organization
- Complaint category and details
- Resolution actions and timeline
- Credit/refund amount and conditions

**Actions**:
- Analyze complaint context
- Select appropriate tone and style
- Generate personalized content
- Incorporate all relevant details
- Maintain professional brand voice

**Outputs**:
- Draft message content
- Metadata (tone, style, length)

### Compliance Validator Agent

**Purpose**: Ensure message meets all regulatory and brand standards

**Inputs**:
- Generated message content
- Policy rules and constraints
- Brand guidelines

**Validation Checks**:
1. **GDPR Compliance**
   - Minimal personal data retention
   - Proper data handling
   - Privacy notifications if needed

2. **Brand Compliance**
   - Empathetic tone
   - Professional language
   - Brand voice consistency
   - No contradictory messaging

3. **Regulatory Compliance**
   - Accurate information
   - No false promises
   - Proper disclaimers
   - Clear terms and conditions

**Outputs**:
- Compliance report
- Issues identified
- Improvement suggestions
- Final validation status

## Design Patterns

### 1. Template Strategy Pattern

Messages are generated using predefined templates that are:
- Category-specific
- Customizable with variables
- Validated before deployment
- Easily extensible

### 2. Chain of Responsibility

Processing flows through sequential agents:
```
Message Generation → Compliance Check → Format Selection → Output
```

Each step can modify or reject the message.

### 3. Decorator Pattern

Compliance checks wrap the message generation:
- Base message + GDPR decorator
- Base message + Brand decorator
- Base message + Channel decorator

### 4. Factory Pattern

Dispatch channels are created based on customer profile:
```python
if customer_profile['SMTP_ADDR']:
    channel = EmailChannel()
elif customer_profile['TELF1']:
    channel = SMSChannel()
else:
    channel = PortalChannel()
```

## Class Diagram

```
┌─────────────────────────────────┐
│ CustomerCommunicatorAgent       │
├─────────────────────────────────┤
│ - agent_id: str                 │
│ - config_list: dict             │
│ - templates: dict               │
│ - message_generator: Agent      │
│ - compliance_validator: Agent   │
├─────────────────────────────────┤
│ + generate_message()            │
│ + process()                     │
│ - _extract_recipient_info()     │
│ - _build_message_context()      │
│ - _render_message()             │
│ - _validate_compliance()        │
│ - _determine_dispatch_channel() │
└─────────────────────────────────┘
        △              △
        │              │
        │              │
    Uses         Uses
        │              │
    ┌───┴──────────┬──┴──────────┐
    │              │             │
┌───────────┐ ┌──────────┐ ┌──────────┐
│  AutoGen  │ │Templates │ │ Profile  │
│  Agents   │ │  Manager │ │  Manager │
└───────────┘ └──────────┘ └──────────┘
```

## Sequence Diagram

```
User/System          Agent              Generator         Validator
    │                  │                    │                  │
    ├─ process()───────>│                    │                  │
    │                   │                    │                  │
    │                   ├─ load inputs────>  │                  │
    │                   ├─ extract context─> │                  │
    │                   ├─ render template─> │                  │
    │                   │                    │                  │
    │                   ├─ generate message─>│                  │
    │                   │<─────message───────┤                  │
    │                   │                    │                  │
    │                   ├─ validate──────────────────────────>│
    │                   │                    │  check GDPR    │
    │                   │                    │  check brand   │
    │                   │<───validation result───────────────┤
    │                   │                    │                  │
    │                   ├─ format output────>│                  │
    │<─ return JSON─────┤                    │                  │
    │                   │                    │                  │
```

## State Diagram

```
        ┌─────────────────┐
        │   INITIALIZED   │
        └────────┬────────┘
                 │ process()
                 ▼
        ┌─────────────────┐
        │  INPUTS_LOADED  │
        └────────┬────────┘
                 │ extract_context()
                 ▼
        ┌─────────────────┐
        │ CONTEXT_READY   │
        └────────┬────────┘
                 │ generate_message()
                 ▼
        ┌─────────────────┐
        │ MESSAGE_DRAFT   │
        └────────┬────────┘
                 │ validate_compliance()
                 ▼
        ┌─────────────────┐     Failed
        │  VALIDATING     ├────────────┐
        └────────┬────────┘            │
                 │ Passed              │
                 ▼                     ▼
        ┌─────────────────┐    ┌──────────────┐
        │  COMPLIANCE_OK  │    │  NEEDS_REVIEW│
        └────────┬────────┘    └──────────────┘
                 │ format_output()
                 ▼
        ┌─────────────────┐
        │  OUTPUT_READY   │
        └────────┬────────┘
                 │ save()
                 ▼
        ┌─────────────────┐
        │    COMPLETED    │
        └─────────────────┘
```

## Error Handling Flow

```
Input Validation
    ├─ Missing fields?
    │   └─→ Use defaults / Report
    │
    ├─ Invalid format?
    │   └─→ Parse / Report
    │
    └─ Proceed

Message Generation
    ├─ LLM API Error?
    │   └─→ Fallback to templates
    │
    ├─ Template not found?
    │   └─→ Use default template
    │
    └─ Proceed

Compliance Check
    ├─ GDPR Issue?
    │   └─→ Flag for review
    │
    ├─ Brand Issue?
    │   └─→ Suggest modifications
    │
    └─ Proceed

Output Generation
    ├─ Serialization Error?
    │   └─→ Log and retry
    │
    └─ Complete
```

## Performance Optimization

### Caching Strategy
```python
# Cache templates on initialization
self.templates = self._load_templates()  # Cached

# Cache LLM configs
self.config_list = config_list_from_json(config_file)  # Cached
```

### Batch Processing Optimization
```python
# Process multiple messages efficiently
results = []
for message_data in batch:
    result = agent.generate_message(...)  # Reuses agents
    results.append(result)
```

### Lazy Loading
- Templates loaded only when needed
- LLM agents initialized on first use
- Validation rules applied selectively

## Security Considerations

1. **API Key Management**
   - Stored in environment variables
   - Never logged or exposed
   - Rotated regularly

2. **Data Privacy**
   - PII masked in logs
   - Compliance checks for data exposure
   - Audit trails for all operations

3. **Input Validation**
   - JSON schema validation
   - Type checking
   - Size limits enforcement

4. **Output Sanitization**
   - HTML escaping for email format
   - Character limits for SMS
   - Compliance verification

## Extension Points

### Adding New Agents

```python
def _setup_agents(self):
    # Add new validation agent
    self.sentiment_analyzer = ConversableAgent(
        name="SentimentAnalyzer",
        system_message="Analyze sentiment...",
        llm_config={"config_list": self.config_list}
    )
```

### Adding New Validation Rules

```python
def _validate_compliance(self, message, context):
    # Add custom validation
    custom_check = self._custom_validation(message)
    return {
        "gdpr": gdpr_pass,
        "brand": brand_pass,
        "custom": custom_pass
    }
```

### Adding New Dispatch Channels

```python
def _determine_dispatch_channel(self, customer_profile):
    if customer_profile.get('WHATSAPP_ID'):
        return 'whatsapp'
    # ... existing logic
```

---

**Document Version**: 1.0  
**Last Updated**: January 4, 2026
