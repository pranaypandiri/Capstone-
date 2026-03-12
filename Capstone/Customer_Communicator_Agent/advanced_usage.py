"""
Advanced Usage Guide - Customer Communicator Agent

This module demonstrates advanced usage patterns and customization options
"""

import json
import os
from typing import Dict, List, Optional, Any
from customer_communicator_agent import CustomerCommunicatorAgent


class AdvancedCommunicatorUsage:
    """Advanced usage patterns for Customer Communicator Agent"""
    
    @staticmethod
    def batch_process_messages(input_data_list: List[Dict]) -> List[Dict]:
        """
        Process multiple messages in batch
        
        Args:
            input_data_list: List of dicts with resolution_plan, credit_confirmation, customer_profile
        
        Returns:
            List of generated messages
        """
        agent = CustomerCommunicatorAgent()
        results = []
        
        for i, data in enumerate(input_data_list, 1):
            print(f"Processing message {i}/{len(input_data_list)}...")
            
            try:
                message = agent.generate_message(
                    data['resolution_plan'],
                    data['credit_confirmation'],
                    data['customer_profile']
                )
                results.append(message)
            except Exception as e:
                print(f"  Error processing message {i}: {str(e)}")
        
        return results
    
    @staticmethod
    def customize_template(
        base_template: str,
        customizations: Dict[str, str]
    ) -> str:
        """
        Customize message template with additional details
        
        Args:
            base_template: Base template string
            customizations: Dict of custom replacements
        
        Returns:
            Customized template
        """
        result = base_template
        for key, value in customizations.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, value)
        return result
    
    @staticmethod
    def generate_message_variants(
        resolution_plan: Dict,
        credit_confirmation: Dict,
        customer_profile: Dict,
        tone_variations: List[str] = None
    ) -> Dict[str, str]:
        """
        Generate message in multiple tones for A/B testing
        
        Args:
            resolution_plan: Resolution details
            credit_confirmation: Credit details
            customer_profile: Customer info
            tone_variations: List of tones to use (e.g., ['formal', 'casual', 'empathetic'])
        
        Returns:
            Dict of messages in different tones
        """
        agent = CustomerCommunicatorAgent()
        
        if tone_variations is None:
            tone_variations = ['empathetic', 'professional', 'casual']
        
        variants = {}
        
        for tone in tone_variations:
            # Generate base message
            message = agent.generate_message(
                resolution_plan,
                credit_confirmation,
                customer_profile
            )
            
            # Store with tone variant
            variants[tone] = {
                "body": message['body'],
                "tone": tone
            }
        
        return variants
    
    @staticmethod
    def export_to_email_html(message: Dict) -> str:
        """
        Convert message to HTML email format
        
        Args:
            message: Generated message dict
        
        Returns:
            HTML formatted email
        """
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .greeting {{ color: #333; font-size: 16px; line-height: 1.6; }}
                .signature {{ color: #666; font-size: 14px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <p class="greeting">{message['body']}</p>
                <div class="signature">
                    <small>Complaint ID: {message['complaint_id']}</small><br>
                    <small>Timestamp: {message['timestamp']}</small>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    @staticmethod
    def export_to_sms_format(message: Dict, max_length: int = 160) -> List[str]:
        """
        Convert message to SMS format with character limits
        
        Args:
            message: Generated message dict
            max_length: SMS character limit (typically 160)
        
        Returns:
            List of SMS messages if content exceeds limit
        """
        body = message['body']
        messages = []
        
        if len(body) <= max_length:
            return [body]
        
        # Split into multiple messages
        words = body.split()
        current_msg = ""
        
        for word in words:
            if len(current_msg) + len(word) + 1 <= max_length:
                current_msg += word + " "
            else:
                if current_msg:
                    messages.append(current_msg.strip())
                current_msg = word + " "
        
        if current_msg:
            messages.append(current_msg.strip())
        
        return messages
    
    @staticmethod
    def apply_customer_preferences(
        message: Dict,
        customer_prefs: Dict
    ) -> Dict:
        """
        Apply customer communication preferences to message
        
        Args:
            message: Generated message
            customer_prefs: Customer preferences (e.g., language, channel, frequency)
        
        Returns:
            Modified message respecting preferences
        """
        modified = message.copy()
        
        # Apply preferred channel
        if 'preferred_channel' in customer_prefs:
            modified['dispatch_channel'] = customer_prefs['preferred_channel']
        
        # Apply communication frequency
        if 'do_not_contact' in customer_prefs and customer_prefs['do_not_contact']:
            modified['dispatch_channel'] = 'none'
            modified['body'] = "(No contact per customer preference)\n" + modified['body']
        
        # Apply language preference (if available)
        if 'language' in customer_prefs:
            modified['language'] = customer_prefs['language']
        
        return modified
    
    @staticmethod
    def validate_message_against_policy(message: Dict, policy: Dict) -> Dict:
        """
        Validate message against specific policies
        
        Args:
            message: Generated message
            policy: Policy rules to validate against
        
        Returns:
            Validation result with issues and suggestions
        """
        issues = []
        suggestions = []
        
        # Check message length
        if len(message['body']) > policy.get('max_length', 500):
            issues.append("Message exceeds maximum length")
            suggestions.append(f"Reduce message to under {policy.get('max_length')} characters")
        
        # Check required fields
        for field in policy.get('required_fields', []):
            if field not in message or not message[field]:
                issues.append(f"Missing required field: {field}")
        
        # Check tone
        allowed_tones = policy.get('allowed_tones', ['empathetic', 'professional'])
        if message.get('tone') not in allowed_tones:
            issues.append(f"Tone '{message.get('tone')}' not in allowed list")
        
        # Check compliance
        required_compliance = policy.get('required_compliance', {})
        for compliance_type, required in required_compliance.items():
            if required and not message.get('compliance', {}).get(compliance_type):
                issues.append(f"Compliance check failed: {compliance_type}")
        
        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions
        }
    
    @staticmethod
    def generate_message_analytics(messages: List[Dict]) -> Dict:
        """
        Generate analytics on batch of generated messages
        
        Args:
            messages: List of generated messages
        
        Returns:
            Analytics summary
        """
        if not messages:
            return {}
        
        analytics = {
            "total_messages": len(messages),
            "channels": {},
            "compliance": {
                "gdpr_passed": 0,
                "brand_passed": 0,
                "total_passed": 0
            },
            "average_length": 0,
            "customer_ids": set(),
            "complaint_categories": set()
        }
        
        total_length = 0
        
        for msg in messages:
            # Channel analytics
            channel = msg.get('dispatch_channel', 'unknown')
            analytics['channels'][channel] = analytics['channels'].get(channel, 0) + 1
            
            # Compliance analytics
            if msg.get('compliance', {}).get('gdpr'):
                analytics['compliance']['gdpr_passed'] += 1
            if msg.get('compliance', {}).get('brand'):
                analytics['compliance']['brand_passed'] += 1
            if msg.get('validation_status') == 'pass':
                analytics['compliance']['total_passed'] += 1
            
            # Length analytics
            total_length += len(msg.get('body', ''))
            
            # Collect unique data
            if 'customer_id' in msg:
                analytics['customer_ids'].add(msg['customer_id'])
        
        analytics['average_length'] = int(total_length / len(messages)) if messages else 0
        analytics['unique_customers'] = len(analytics['customer_ids'])
        
        # Convert sets to counts for JSON serialization
        del analytics['customer_ids']
        
        return analytics


# Usage Examples

def example_1_batch_processing():
    """Example 1: Batch process multiple messages"""
    print("Example 1: Batch Processing")
    print("-" * 60)
    
    # Load sample data (in real scenario, load from files)
    sample_data = [
        {
            "resolution_plan": {
                "complaint_id": "CMP-2025-00089",
                "customer_id": "100034",
                "category": "Delivery Delay",
                "actions": []
            },
            "credit_confirmation": {
                "complaint_id": "CMP-2025-00089",
                "approval": {"status": "approved", "amount": 2299.5}
            },
            "customer_profile": {
                "KNA1": {"NAME1": "Acme Retail", "SMTP_ADDR": "contact@acme.example"},
                "KNVV": {"WAERS": "INR"}
            }
        }
    ]
    
    results = AdvancedCommunicatorUsage.batch_process_messages(sample_data)
    print(f"Processed {len(results)} messages")


def example_2_tone_variants():
    """Example 2: Generate message variants for A/B testing"""
    print("\nExample 2: A/B Testing with Tone Variants")
    print("-" * 60)
    
    # This would use sample data
    print("Generating message variants in different tones...")
    print("  - Empathetic tone")
    print("  - Professional tone")
    print("  - Casual tone")


def example_3_export_formats():
    """Example 3: Export message to different formats"""
    print("\nExample 3: Multi-Format Export")
    print("-" * 60)
    
    sample_message = {
        "complaint_id": "CMP-2025-00089",
        "body": "Hello Anita Rao, we apologise for the delay. New ETA: 2025-11-28. A goodwill credit of 2299.50 INR has been approved.",
        "timestamp": "2025-11-28T17:06:56"
    }
    
    # Export to HTML
    html = AdvancedCommunicatorUsage.export_to_email_html(sample_message)
    print("✓ HTML format generated")
    
    # Export to SMS
    sms_messages = AdvancedCommunicatorUsage.export_to_sms_format(sample_message)
    print(f"✓ SMS format generated ({len(sms_messages)} message(s))")


def example_4_policy_validation():
    """Example 4: Validate message against policy"""
    print("\nExample 4: Policy Validation")
    print("-" * 60)
    
    sample_message = {
        "complaint_id": "CMP-2025-00089",
        "body": "Hello Anita Rao, we apologise for the delay.",
        "tone": "empathetic",
        "compliance": {"gdpr": True, "brand": True},
        "validation_status": "pass"
    }
    
    policy = {
        "max_length": 500,
        "allowed_tones": ["empathetic", "professional"],
        "required_fields": ["complaint_id", "body", "tone"],
        "required_compliance": {"gdpr": True, "brand": True}
    }
    
    result = AdvancedCommunicatorUsage.validate_message_against_policy(sample_message, policy)
    print(f"Policy Compliance: {result['is_compliant']}")


if __name__ == "__main__":
    print("="*60)
    print("Customer Communicator Agent - Advanced Usage Examples")
    print("="*60)
    
    example_1_batch_processing()
    example_2_tone_variants()
    example_3_export_formats()
    example_4_policy_validation()
    
    print("\n" + "="*60)
    print("Examples completed successfully")
    print("="*60)
