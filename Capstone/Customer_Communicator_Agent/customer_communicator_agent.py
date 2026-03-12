"""
Customer Communicator Agent - Generates personalized communication for complaint resolution
Using AutoGen Framework for multi-agent orchestration
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import autogen
from autogen import ConversableAgent, config_list_from_json

# Load environment variables from .env file
load_dotenv()


class CustomerCommunicatorAgent:
    """
    Generates personalized resolution messages for customers in complaint resolution workflow.
    
    Inputs:
    - Resolution plan (from Remedy Planner Agent)
    - Credit confirmation (from Credit Trigger Agent)
    - Customer profile (from CRM)
    
    Outputs:
    - Personalized resolution message ready for dispatch
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the Customer Communicator Agent
        
        Args:
            config_file: Path to OAI_CONFIG_LIST.json for LLM configuration
        """
        self.agent_id = "COM-01"
        self.timestamp = datetime.now().isoformat()
        
        # Load configuration
        if config_file and os.path.exists(config_file):
            self.config_list = config_list_from_json(config_file)
        else:
            # Fallback: use environment variable or default configuration
            self.config_list = self._setup_default_config()
        
        # Load templates
        self.templates = self._load_templates()
        
        # Initialize AutoGen agents
        self._setup_agents()
    
    def _setup_default_config(self) -> list:
        """Setup default LLM configuration"""
        # Try to use environment variable for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return [
                {
                    "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
                    "api_key": api_key,
                    "base_url": os.getenv("OPENAI_BASE_URL", "https://schoolofagenticaitraining.openai.azure.com/"),
                    "api_type": os.getenv("OPENAI_API_TYPE", "azure"),
                    "api_version": os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
                }
            ]
        else:
            # Return empty list - will use default behavior
            return []
    
    def _load_templates(self) -> Dict[str, str]:
        """Load communication templates from JSON file"""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "Data_Sources",
            "communication_templates.json"
        )
        
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Templates file not found at {template_path}")
            return {
                "delay_resolution": "Hello {{name}}, we apologise for the delay. New ETA: {{eta}}. A goodwill credit of {{amount}} {{currency}} has been approved.",
                "signature": "Regards,\nCustomer Care"
            }
    
    def _setup_agents(self):
        """Initialize AutoGen agents for message generation and validation"""
        # User Proxy Agent (acts as orchestrator)
        self.user_proxy = ConversableAgent(
            name="UserProxy",
            system_message="You are a helpful assistant coordinating message generation and validation.",
            llm_config=False,  # No LLM for user proxy
            human_input_mode="NEVER"
        )
        
        # Message Generator Agent
        self.message_generator = ConversableAgent(
            name="MessageGenerator",
            system_message="""You are an expert customer communication specialist. 
Your role is to generate personalized, empathetic, and compliant resolution messages.

Key responsibilities:
- Use provided customer profile to personalize messages
- Incorporate resolution details (ETA, credit amount, etc.)
- Maintain empathetic and professional tone
- Ensure compliance with brand guidelines
- Keep messages concise yet informative

Format the output as a clean, ready-to-send message.""",
            llm_config={"config_list": self.config_list} if self.config_list else False,
            human_input_mode="NEVER"
        )
        
        # Compliance Validator Agent
        self.compliance_validator = ConversableAgent(
            name="ComplianceValidator",
            system_message="""You are a compliance and quality assurance specialist for customer communications.

Your role is to validate messages for:
- GDPR compliance (no unnecessary personal data retention)
- Brand tone alignment (empathetic, professional, helpful)
- Regulatory compliance (accurate information, proper disclaimers)
- Clarity and comprehensiveness

Provide validation feedback in JSON format with:
- "gdpr": boolean
- "brand": boolean
- "compliance_status": "pass" or "fail"
- "issues": list of any issues found
- "suggestions": list of improvement suggestions""",
            llm_config={"config_list": self.config_list} if self.config_list else False,
            human_input_mode="NEVER"
        )
    
    def generate_message(
        self,
        resolution_plan: Dict[str, Any],
        credit_confirmation: Dict[str, Any],
        customer_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized resolution message using AutoGen multi-agent orchestration
        
        Args:
            resolution_plan: Output from Remedy Planner Agent
            credit_confirmation: Output from Credit Trigger Agent
            customer_profile: Customer profile from CRM
        
        Returns:
            Personalized message with compliance validation
        """
        
        # Extract key information
        recipient_info = self._extract_recipient_info(customer_profile)
        message_context = self._build_message_context(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        # Step 1: Use Message Generator Agent to generate the message
        print("  [Agent] Invoking Message Generator Agent...")
        base_message = self._generate_message_with_agent(message_context, customer_profile)
        
        # Step 2: Use Compliance Validator Agent to validate
        print("  [Agent] Invoking Compliance Validator Agent...")
        compliance_check = self._validate_with_agent(base_message, message_context)
        
        # Build output
        output = {
            "complaint_id": resolution_plan.get("complaint_id"),
            "customer_id": resolution_plan.get("customer_id"),
            "to": {
                "name": recipient_info.get("name"),
                "email": recipient_info.get("email"),
                "phone": recipient_info.get("phone")
            },
            "body": base_message,
            "dispatch_channel": self._determine_dispatch_channel(customer_profile),
            "tone": "empathetic",
            "compliance": {
                "gdpr": compliance_check.get("gdpr", True),
                "brand": compliance_check.get("brand", True)
            },
            "validation_status": compliance_check.get("compliance_status", "pass"),
            "timestamp": self.timestamp,
            "agent_id": self.agent_id
        }
        
        return output
    
    def _generate_message_with_agent(self, context: Dict[str, Any], customer_profile: Dict[str, Any]) -> str:
        """
        Use Message Generator Agent to generate personalized message
        
        Orchestrates multi-agent conversation between Message Generator and user proxy
        """
        # Prepare the prompt for the Message Generator Agent
        prompt = f"""Generate a personalized customer resolution message with these details:

Customer Name: {context.get('name', 'Valued Customer')}
Organization: {context.get('organization', '')}
Complaint ID: {context.get('complaint_id')}
Complaint Category: {context.get('category')}
Issue: {context.get('category', 'Order Issue')}
New ETA: {context.get('eta')}
Goodwill Credit Amount: {context.get('amount')} {context.get('currency')}
Carrier: {context.get('carrier')}

Requirements:
1. Personalize with customer's first name
2. Express empathy and apologize for the inconvenience
3. Explain the resolution (new ETA and credit)
4. Be professional yet warm
5. Keep it concise (under 250 words)
6. End with appreciation

Generate ONLY the message body, no additional text."""

        try:
            # Check if LLM config is available
            if not self.config_list:
                print("    → No LLM configured, using template-based generation")
                return self._render_message(context)
            
            # Use agent to generate message via LLM
            print("    → Sending request to Message Generator Agent...")
            response = self.message_generator.generate_reply(
                messages=[{"content": prompt, "role": "user"}]
            )
            
            # Extract message from agent response
            if response and isinstance(response, str) and response.strip():
                print("    ✓ Message generated by Agent")
                return response.strip()
            else:
                print("    → Agent returned empty response, using fallback")
                return self._render_message(context)
                
        except Exception as e:
            print(f"    ⚠ Agent generation error: {str(e)}")
            print(f"    → Using template-based fallback generation")
            return self._render_message(context)
    
    def _validate_with_agent(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Compliance Validator Agent to validate message
        
        Orchestrates multi-agent conversation for compliance checking
        """
        validation_prompt = f"""Validate this customer message for compliance:

MESSAGE:
{message}

Validate for:
1. GDPR Compliance: No unnecessary personal data retention, secure handling
2. Brand Tone: Professional, empathetic, helpful (no demanding language)
3. Regulatory: Accurate information, no false promises
4. Clarity: Clear, addresses key points

Return a JSON response with:
{{
    "gdpr": true/false,
    "brand": true/false,
    "compliance_status": "pass" or "fail",
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1"]
}}"""

        try:
            # Check if LLM config is available
            if not self.config_list:
                print("    → No LLM configured, using basic validation")
                return self._validate_compliance(message, context)
            
            print("    → Sending request to Compliance Validator Agent...")
            # Use agent to validate
            response = self.compliance_validator.generate_reply(
                messages=[{"content": validation_prompt, "role": "user"}]
            )
            
            # Parse agent response
            if response and isinstance(response, str):
                # Try to extract JSON from response
                import re
                import json
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                        print("    ✓ Compliance validated by Agent")
                        return result
                    except json.JSONDecodeError:
                        pass
            
            # Fallback to basic validation
            print("    → Agent response parsing failed, using basic validation")
            return self._validate_compliance(message, context)
            
        except Exception as e:
            print(f"    ⚠ Agent validation error: {str(e)}")
            print(f"    → Using basic validation fallback")
            return self._validate_compliance(message, context)
    
    def _extract_recipient_info(self, customer_profile: Dict[str, Any]) -> Dict[str, str]:
        """Extract recipient information from customer profile"""
        kna1 = customer_profile.get("KNA1", {})
        knvv = customer_profile.get("KNVV", {})
        
        # Extract contact name and email
        name = kna1.get("NAME1", "Valued Customer")
        # Try to extract first name from email or NAME1
        contact_name = name.split()[0] if name else "Valued Customer"
        
        return {
            "name": contact_name,
            "full_name": name,
            "email": kna1.get("SMTP_ADDR", ""),
            "phone": kna1.get("TELF1", ""),
            "organization": name
        }
    
    def _build_message_context(
        self,
        resolution_plan: Dict[str, Any],
        credit_confirmation: Dict[str, Any],
        customer_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build context for message rendering"""
        recipient = self._extract_recipient_info(customer_profile)
        
        # Extract resolution details
        actions = resolution_plan.get("actions", [])
        expedite_action = next((a for a in actions if a.get("type") == "Expedite"), None)
        credit_action = next((a for a in actions if a.get("type") == "GoodwillCredit"), None)
        
        # Extract credit details
        credit_info = credit_confirmation.get("approval", {})
        
        context = {
            "name": recipient.get("name", "Customer"),
            "organization": recipient.get("organization", ""),
            "complaint_id": resolution_plan.get("complaint_id"),
            "category": resolution_plan.get("category", ""),
            "eta": expedite_action.get("details", {}).get("new_eta", "") if expedite_action else "",
            "amount": credit_info.get("amount", 0),
            "currency": customer_profile.get("KNVV", {}).get("WAERS", "INR"),
            "credit_doc": credit_info.get("credit_doc", ""),
            "conditions": credit_info.get("conditions", []),
            "carrier": expedite_action.get("details", {}).get("carrier", "") if expedite_action else ""
        }
        
        return context
    
    def _render_message(self, context: Dict[str, Any]) -> str:
        """
        Render message using templates and context
        
        Args:
            context: Message context with placeholders filled
        
        Returns:
            Rendered message string
        """
        # Select appropriate template based on complaint category
        template_key = self._select_template(context.get("category", ""))
        template = self.templates.get(template_key, self.templates.get("delay_resolution"))
        
        # Fill template with context
        message = self._fill_template(template, context)
        
        # Add signature
        signature = self.templates.get("signature", "Regards,\nCustomer Care")
        
        return f"{message}\n\n{signature}"
    
    def _select_template(self, category: str) -> str:
        """Select appropriate template based on complaint category"""
        category_map = {
            "Delivery Delay": "delay_resolution",
            "Quality Issue": "quality_resolution",
            "Billing Error": "billing_resolution",
            "Service Issue": "service_resolution"
        }
        return category_map.get(category, "delay_resolution")
    
    def _fill_template(self, template: str, context: Dict[str, Any]) -> str:
        """Fill template with context values"""
        result = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result
    
    def _determine_dispatch_channel(self, customer_profile: Dict[str, Any]) -> str:
        """Determine preferred dispatch channel"""
        kna1 = customer_profile.get("KNA1", {})
        
        if kna1.get("SMTP_ADDR"):
            return "email"
        elif kna1.get("TELF1"):
            return "sms"
        else:
            return "portal"
    
    def _validate_compliance(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate message for GDPR and brand compliance
        
        Args:
            message: Generated message
            context: Message context
        
        Returns:
            Compliance validation results
        """
        # Basic validation checks
        gdpr_pass = self._check_gdpr_compliance(message, context)
        brand_pass = self._check_brand_compliance(message)
        
        compliance_status = "pass" if (gdpr_pass and brand_pass) else "fail"
        
        return {
            "gdpr": gdpr_pass,
            "brand": brand_pass,
            "compliance_status": compliance_status,
            "issues": [],
            "suggestions": []
        }
    
    def _check_gdpr_compliance(self, message: str, context: Dict[str, Any]) -> bool:
        """Check GDPR compliance"""
        # Check if message contains sensitive data that shouldn't be logged
        sensitive_patterns = ["password", "card", "ssn", "date of birth"]
        
        message_lower = message.lower()
        for pattern in sensitive_patterns:
            if pattern in message_lower:
                return False
        
        return True
    
    def _check_brand_compliance(self, message: str) -> bool:
        """Check brand tone compliance"""
        # Check for professional and empathetic tone
        positive_indicators = ["apologise", "sorry", "understand", "help", "assist"]
        negative_indicators = ["demand", "must", "will be", "required"]
        
        message_lower = message.lower()
        
        has_empathy = any(word in message_lower for word in positive_indicators)
        has_demands = any(word in message_lower for word in negative_indicators)
        
        return has_empathy and not has_demands
    
    def process(
        self,
        resolution_plan_file: str,
        credit_confirmation_file: str,
        customer_profile_file: str,
        output_file: str = None
    ) -> Dict[str, Any]:
        """
        End-to-end processing of message generation
        
        Args:
            resolution_plan_file: Path to resolution plan JSON
            credit_confirmation_file: Path to credit confirmation JSON
            customer_profile_file: Path to customer profile JSON
            output_file: Optional output file path
        
        Returns:
            Generated message output
        """
        
        # Load inputs
        with open(resolution_plan_file, 'r') as f:
            resolution_plan = json.load(f)
        
        with open(credit_confirmation_file, 'r') as f:
            credit_confirmation = json.load(f)
        
        with open(customer_profile_file, 'r') as f:
            customer_profile = json.load(f)
        
        # Generate message
        output = self.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        # Save output if file path provided
        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Message saved to {output_file}")
        
        return output


def main():
    """Main execution function"""
    
    # Initialize agent
    print("Initializing Customer Communicator Agent...")
    agent = CustomerCommunicatorAgent()
    
    # Define file paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    resolution_plan_file = os.path.join(base_path, "Inputs", "resolution_plan_output_01.json")
    credit_confirmation_file = os.path.join(base_path, "Inputs", "credit_confirmation_output_01.json")
    customer_profile_file = os.path.join(base_path, "Inputs", "customer_profile_sample_01.json")
    output_file = os.path.join(base_path, "Outputs", "resolution_message_output_01.json")
    
    # Process
    print("Generating personalized resolution message...")
    result = agent.process(
        resolution_plan_file,
        credit_confirmation_file,
        customer_profile_file,
        output_file
    )
    
    # Display result
    print("\n" + "="*60)
    print("RESOLUTION MESSAGE GENERATED")
    print("="*60)
    print(json.dumps(result, indent=2))
    print("="*60)


if __name__ == "__main__":
    main()
