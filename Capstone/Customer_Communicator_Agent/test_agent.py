"""
Test and Execution Script for Customer Communicator Agent
Demonstrates the agent's capabilities and validates outputs
"""

import json
import os
import sys
from pathlib import Path
from customer_communicator_agent import CustomerCommunicatorAgent


class AgentTester:
    """Test harness for Customer Communicator Agent"""
    
    def __init__(self, base_path: str = None):
        """Initialize tester"""
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))
        self.agent = CustomerCommunicatorAgent()
    
    def run_full_test(self):
        """Run comprehensive agent test"""
        print("\n" + "="*80)
        print("CUSTOMER COMMUNICATOR AGENT - COMPREHENSIVE TEST")
        print("="*80)
        
        # Load test data
        print("\n[1/5] Loading test data...")
        resolution_plan = self._load_json("Inputs/resolution_plan_output_01.json")
        credit_confirmation = self._load_json("Inputs/credit_confirmation_output_01.json")
        customer_profile = self._load_json("Inputs/customer_profile_sample_01.json")
        
        if not all([resolution_plan, credit_confirmation, customer_profile]):
            print("ERROR: Failed to load test data")
            return False
        
        print(f"  ✓ Resolution Plan: {resolution_plan.get('complaint_id')}")
        print(f"  ✓ Credit Confirmation: {credit_confirmation.get('complaint_id')}")
        print(f"  ✓ Customer Profile: {customer_profile.get('KNA1', {}).get('NAME1')}")
        
        # Generate message
        print("\n[2/5] Generating message...")
        output = self.agent.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        if output:
            print(f"  ✓ Message generated for: {output['to']['name']}")
            print(f"  ✓ Dispatch channel: {output['dispatch_channel']}")
            print(f"  ✓ Compliance status: {output['compliance']['gdpr']} (GDPR), {output['compliance']['brand']} (Brand)")
        
        # Validate output structure
        print("\n[3/5] Validating output structure...")
        if self._validate_output_structure(output):
            print("  ✓ All required fields present")
        else:
            print("  ✗ Missing required fields")
            return False
        
        # Display message preview
        print("\n[4/5] Message preview:")
        print("-" * 80)
        print(output['body'])
        print("-" * 80)
        
        # Save output
        print("\n[5/5] Saving output...")
        output_path = os.path.join(self.base_path, "Outputs", "resolution_message_output_01.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"  ✓ Output saved to: {output_path}")
        
        # Summary
        print("\n" + "="*80)
        print("TEST RESULTS SUMMARY")
        print("="*80)
        print(f"Status: ✓ PASSED")
        print(f"Complaint ID: {output['complaint_id']}")
        print(f"Customer: {output['to']['name']} ({output['to']['email']})")
        print(f"Channel: {output['dispatch_channel']}")
        print(f"Compliance: GDPR={output['compliance']['gdpr']}, Brand={output['compliance']['brand']}")
        print("="*80)
        
        return True
    
    def test_message_personalization(self):
        """Test message personalization capabilities"""
        print("\n" + "="*80)
        print("TEST: Message Personalization")
        print("="*80)
        
        resolution_plan = self._load_json("Inputs/resolution_plan_output_01.json")
        credit_confirmation = self._load_json("Inputs/credit_confirmation_output_01.json")
        customer_profile = self._load_json("Inputs/customer_profile_sample_01.json")
        
        output = self.agent.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        # Check for personalization
        message = output['body'].lower()
        customer_name = customer_profile['KNA1']['NAME1'].split()[0].lower()
        
        checks = [
            ("Customer name included", customer_name in message),
            ("Apology/empathy expressed", any(w in message for w in ["apologise", "sorry", "apologize"])),
            ("Credit amount mentioned", str(credit_confirmation['approval']['amount']) in output['body']),
            ("Currency included", "INR" in output['body']),
            ("ETA provided", "2025-11-28" in output['body']),
        ]
        
        print("\nPersonalization Checks:")
        all_passed = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
            all_passed = all_passed and result
        
        return all_passed
    
    def test_compliance_validation(self):
        """Test compliance validation"""
        print("\n" + "="*80)
        print("TEST: Compliance Validation")
        print("="*80)
        
        resolution_plan = self._load_json("Inputs/resolution_plan_output_01.json")
        credit_confirmation = self._load_json("Inputs/credit_confirmation_output_01.json")
        customer_profile = self._load_json("Inputs/customer_profile_sample_01.json")
        
        output = self.agent.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        print("\nCompliance Checks:")
        checks = [
            ("GDPR Compliance", output['compliance']['gdpr']),
            ("Brand Tone Compliance", output['compliance']['brand']),
            ("Overall Validation Status", output['validation_status'] == 'pass'),
        ]
        
        all_passed = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
            all_passed = all_passed and result
        
        return all_passed
    
    def test_dispatch_channel_selection(self):
        """Test dispatch channel selection"""
        print("\n" + "="*80)
        print("TEST: Dispatch Channel Selection")
        print("="*80)
        
        resolution_plan = self._load_json("Inputs/resolution_plan_output_01.json")
        credit_confirmation = self._load_json("Inputs/credit_confirmation_output_01.json")
        customer_profile = self._load_json("Inputs/customer_profile_sample_01.json")
        
        output = self.agent.generate_message(
            resolution_plan,
            credit_confirmation,
            customer_profile
        )
        
        print(f"\nSelected Channel: {output['dispatch_channel']}")
        print(f"Recipient Email: {output['to']['email']}")
        print(f"Recipient Phone: {output['to']['phone']}")
        
        valid_channels = ['email', 'sms', 'portal']
        is_valid = output['dispatch_channel'] in valid_channels
        
        print(f"\nChannel Validation: {'✓ PASS' if is_valid else '✗ FAIL'}")
        
        return is_valid
    
    def _load_json(self, relative_path: str) -> dict:
        """Load JSON file"""
        full_path = os.path.join(self.base_path, relative_path)
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  Error loading {relative_path}: {str(e)}")
            return None
    
    def _validate_output_structure(self, output: dict) -> bool:
        """Validate output structure"""
        required_fields = [
            'complaint_id', 'customer_id', 'to', 'body',
            'dispatch_channel', 'tone', 'compliance',
            'validation_status', 'timestamp', 'agent_id'
        ]
        
        required_to_fields = ['name', 'email']
        required_compliance_fields = ['gdpr', 'brand']
        
        # Check top-level fields
        for field in required_fields:
            if field not in output:
                print(f"  Missing field: {field}")
                return False
        
        # Check to fields
        for field in required_to_fields:
            if field not in output['to']:
                print(f"  Missing field in 'to': {field}")
                return False
        
        # Check compliance fields
        for field in required_compliance_fields:
            if field not in output['compliance']:
                print(f"  Missing field in 'compliance': {field}")
                return False
        
        return True


def main():
    """Run all tests"""
    tester = AgentTester()
    
    results = {
        "Full Test": tester.run_full_test(),
        "Personalization": tester.test_message_personalization(),
        "Compliance": tester.test_compliance_validation(),
        "Channel Selection": tester.test_dispatch_channel_selection(),
    }
    
    print("\n" + "="*80)
    print("OVERALL TEST RESULTS")
    print("="*80)
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("="*80))
    print(f"Overall Status: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    print("="*80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
