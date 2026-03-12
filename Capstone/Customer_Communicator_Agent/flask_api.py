"""
Flask API for Customer Communicator Agent
Provides REST endpoints for generating personalized customer resolution messages
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from customer_communicator_agent import CustomerCommunicatorAgent

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the agent
try:
    agent = CustomerCommunicatorAgent()
    print("✓ Agent initialized successfully")
except Exception as e:
    print(f"✗ Error initializing agent: {e}")
    agent = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Customer Communicator API",
        "timestamp": datetime.now().isoformat(),
        "agent_ready": agent is not None
    }), 200


@app.route('/api/v1/generate-message', methods=['POST'])
def generate_message():
    """
    Generate personalized resolution message
    
    Expected JSON body:
    {
        "customer_profile": {...},
        "resolution_plan": {...},
        "credit_confirmation": {...}
    }
    """
    try:
        if agent is None:
            return jsonify({
                "error": "Agent not initialized",
                "status": "failed"
            }), 503
        
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['customer_profile', 'resolution_plan', 'credit_confirmation']):
            return jsonify({
                "error": "Missing required fields: customer_profile, resolution_plan, credit_confirmation",
                "status": "failed"
            }), 400
        
        customer_profile = data['customer_profile']
        resolution_plan = data['resolution_plan']
        credit_confirmation = data['credit_confirmation']
        
        print("\n" + "="*70)
        print("INCOMING API REQUEST")
        print("="*70)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Customer ID: {customer_profile.get('KNA1', {}).get('customer_id', 'N/A')}")
        print(f"Complaint ID: {resolution_plan.get('complaint_id', 'N/A')}")
        print("="*70)
        
        # Call agent to generate message
        print("\n[API] Processing request through agent...")
        result = agent.generate_message(
            resolution_plan=resolution_plan,
            credit_confirmation=credit_confirmation,
            customer_profile=customer_profile
        )
        
        print("\n[API] ✓ Message generation completed successfully")
        print("="*70)
        print("RESPONSE SENT TO CLIENT")
        print("="*70)
        print(json.dumps(result, indent=2))
        print("="*70)
        
        return jsonify({
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        error_msg = f"Error generating message: {str(e)}"
        print(f"\n✗ {error_msg}")
        return jsonify({
            "error": error_msg,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/v1/batch-generate', methods=['POST'])
def batch_generate():
    """
    Generate messages for multiple customers
    
    Expected JSON body:
    {
        "messages": [
            {
                "customer_profile": {...},
                "resolution_plan": {...},
                "credit_confirmation": {...}
            },
            ...
        ]
    }
    """
    try:
        if agent is None:
            return jsonify({
                "error": "Agent not initialized",
                "status": "failed"
            }), 503
        
        data = request.get_json()
        
        if 'messages' not in data or not isinstance(data['messages'], list):
            return jsonify({
                "error": "Invalid format: expected 'messages' as array",
                "status": "failed"
            }), 400
        
        messages = data['messages']
        results = []
        
        print("\n" + "="*70)
        print(f"BATCH API REQUEST - Processing {len(messages)} messages")
        print("="*70)
        
        for idx, msg_data in enumerate(messages, 1):
            try:
                print(f"\n[Batch] Processing message {idx}/{len(messages)}...")
                
                if not all(key in msg_data for key in ['customer_profile', 'resolution_plan', 'credit_confirmation']):
                    results.append({
                        "index": idx,
                        "status": "failed",
                        "error": "Missing required fields"
                    })
                    continue
                
                result = agent.generate_message(
                    resolution_plan=msg_data['resolution_plan'],
                    credit_confirmation=msg_data['credit_confirmation'],
                    customer_profile=msg_data['customer_profile']
                )
                
                results.append({
                    "index": idx,
                    "status": "success",
                    "data": result
                })
                
                print(f"[Batch] ✓ Message {idx} completed")
            
            except Exception as e:
                results.append({
                    "index": idx,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"[Batch] ✗ Message {idx} failed: {str(e)}")
        
        print("\n" + "="*70)
        print(f"BATCH PROCESSING COMPLETE - {len([r for r in results if r['status'] == 'success'])}/{len(results)} succeeded")
        print("="*70)
        
        return jsonify({
            "status": "completed",
            "total": len(messages),
            "succeeded": len([r for r in results if r['status'] == 'success']),
            "failed": len([r for r in results if r['status'] == 'failed']),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        error_msg = f"Batch processing error: {str(e)}"
        print(f"\n✗ {error_msg}")
        return jsonify({
            "error": error_msg,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/v1/validate', methods=['POST'])
def validate():
    """
    Validate message content for compliance
    
    Expected JSON body:
    {
        "message": "...",
        "context": {...}
    }
    """
    try:
        if agent is None:
            return jsonify({
                "error": "Agent not initialized",
                "status": "failed"
            }), 503
        
        data = request.get_json()
        
        if 'message' not in data or 'context' not in data:
            return jsonify({
                "error": "Missing required fields: message, context",
                "status": "failed"
            }), 400
        
        message = data['message']
        context = data['context']
        
        print("\n[Validation] Processing compliance check...")
        
        # Validate using agent's validation method
        validation_result = agent._validate_with_agent(message, context)
        
        print("[Validation] ✓ Compliance check completed")
        
        return jsonify({
            "status": "success",
            "validation": validation_result,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        error_msg = f"Validation error: {str(e)}"
        print(f"[Validation] ✗ {error_msg}")
        return jsonify({
            "error": error_msg,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/v1/status', methods=['GET'])
def status():
    """Get agent status and configuration"""
    return jsonify({
        "agent_id": agent.agent_id if agent else "N/A",
        "status": "ready" if agent else "not_initialized",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "generate_message": "/api/v1/generate-message",
            "batch_generate": "/api/v1/batch-generate",
            "validate": "/api/v1/validate",
            "status": "/api/v1/status"
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "status": "failed",
        "available_endpoints": {
            "health": "/health",
            "generate_message": "/api/v1/generate-message",
            "batch_generate": "/api/v1/batch-generate",
            "validate": "/api/v1/validate",
            "status": "/api/v1/status"
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    print(f"\n✗ Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "status": "failed",
        "timestamp": datetime.now().isoformat()
    }), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("CUSTOMER COMMUNICATOR AGENT - FLASK API")
    print("="*70)
    print(f"Starting Flask API server...")
    print(f"Local: http://127.0.0.1:5000")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print("\nAvailable Endpoints:")
    print("  - GET  /health                    (Health check)")
    print("  - GET  /api/v1/status             (Agent status)")
    print("  - POST /api/v1/generate-message   (Generate single message)")
    print("  - POST /api/v1/batch-generate     (Generate multiple messages)")
    print("  - POST /api/v1/validate           (Validate message compliance)")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
