"""
Customer Communicator Agent - Configuration Module
"""

# Agent Configuration
AGENT_CONFIG = {
    "agent_id": "COM-01",
    "agent_name": "Customer Communicator",
    "description": "Generates personalized communication for complaint resolution",
    
    # LLM Configuration
    "llm_config": {
        "config_list": "OAI_CONFIG_LIST.json",
        "cache_seed": 42,
        "temperature": 0.7,
        "max_tokens": 1000
    },
    
    # Message Generation Settings
    "message_settings": {
        "tone": "empathetic",
        "max_message_length": 500,
        "include_signature": True,
        "include_complaint_id": True
    },
    
    # Compliance Settings
    "compliance_settings": {
        "check_gdpr": True,
        "check_brand_tone": True,
        "check_regulatory": True,
        "sensitive_data_patterns": [
            "password", "card", "ssn", "date of birth",
            "bank account", "routing number"
        ]
    },
    
    # Template Settings
    "template_settings": {
        "template_file": "Data_Sources/communication_templates.json",
        "default_template": "delay_resolution",
        "category_mapping": {
            "Delivery Delay": "delay_resolution",
            "Quality Issue": "quality_resolution",
            "Billing Error": "billing_resolution",
            "Service Issue": "service_resolution"
        }
    },
    
    # Dispatch Settings
    "dispatch_settings": {
        "preferred_channels": ["email", "sms", "portal"],
        "default_channel": "email",
        "channel_config": {
            "email": {"enabled": True, "template": "email"},
            "sms": {"enabled": True, "template": "sms", "max_length": 160},
            "portal": {"enabled": True, "template": "portal"}
        }
    }
}

# Input/Output Configuration
IO_CONFIG = {
    "input_dir": "Inputs",
    "output_dir": "Outputs",
    "data_sources_dir": "Data_Sources",
    
    "input_files": {
        "resolution_plan": "resolution_plan_output_01.json",
        "credit_confirmation": "credit_confirmation_output_01.json",
        "customer_profile": "customer_profile_sample_01.json"
    },
    
    "output_files": {
        "resolution_message": "resolution_message_output_01.json",
        "audit_log": "audit_log_01.json"
    }
}

# Validation Rules
VALIDATION_RULES = {
    "required_fields": {
        "resolution_plan": ["complaint_id", "customer_id", "category", "actions"],
        "credit_confirmation": ["complaint_id", "approval", "validation_status"],
        "customer_profile": ["KNA1", "KNVV"],
        "output": ["complaint_id", "to", "body", "compliance", "validation_status"]
    },
    
    "tone_keywords": {
        "empathetic": ["apologise", "understand", "help", "assist", "appreciate"],
        "professional": ["resolution", "credit", "customer", "support"],
        "avoid": ["demand", "must", "required", "forced"]
    }
}

# AutoGen Agent System Messages
SYSTEM_MESSAGES = {
    "message_generator": """You are an expert customer communication specialist.
    
Your role is to generate personalized, empathetic, and compliant resolution messages for customers.

Key responsibilities:
- Use provided customer profile to personalize messages
- Incorporate resolution details (ETA, credit amount, carrier, etc.)
- Maintain empathetic and professional tone throughout
- Ensure compliance with brand guidelines
- Keep messages concise yet informative
- Address customer by preferred name when available
- Include relevant details about the resolution

Guidelines:
1. Start with acknowledgment of the issue and apology
2. Explain what went wrong (if appropriate)
3. Describe the solution/resolution
4. Mention any goodwill gestures (credits, etc.)
5. Provide next steps or expected timeline
6. End with appreciation and support contact info

Format the output as a clean, ready-to-send message that can be sent via email, SMS, or portal.""",
    
    "compliance_validator": """You are a compliance and quality assurance specialist for customer communications.

Your role is to validate customer messages for compliance, tone, and accuracy.

Validation areas:
1. GDPR Compliance: No unnecessary personal data retention, proper handling of sensitive info
2. Brand Tone: Empathetic, professional, helpful, non-threatening language
3. Regulatory Compliance: Accurate information, proper disclaimers, no false promises
4. Clarity & Completeness: Message is clear, addresses all key points, no ambiguity

Output Format (JSON):
{
    "gdpr": boolean,
    "brand": boolean,
    "compliance_status": "pass" or "flag",
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "tone_assessment": "empathetic|neutral|aggressive"
}"""
}
