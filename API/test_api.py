"""
Quick test script to verify API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_policies_listing():
    print("Testing /api/policies endpoint...")
    response = requests.get(f"{BASE_URL}/api/policies")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} client groups")
    for client_group in data:
        print(f"\nClient: {client_group['clientName']}")
        print(f"  Account: {client_group['clientAccountNumber']}")
        print(f"  Policies: {len(client_group['policies'])}")
        print(f"  Total Alerts: {client_group['totalAlerts']} (H:{client_group['highSeverityCount']}, M:{client_group['mediumSeverityCount']}, L:{client_group['lowSeverityCount']})")
        for policy in client_group['policies']:
            print(f"    - {policy['policyLabel']}: {len(policy['alerts'])} alerts")

def test_policy_detail():
    print("\n\nTesting /api/policies/POL-90002 endpoint...")
    response = requests.get(f"{BASE_URL}/api/policies/POL-90002")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Policy: {data['policyLabel']}")
    print(f"Alerts: {len(data['alerts'])}")
    for alert in data['alerts']:
        print(f"  - [{alert['severity']}] {alert['title']}")

def test_client():
    print("\n\nTesting /api/clients/101-123456-001 endpoint...")
    response = requests.get(f"{BASE_URL}/api/clients/101-123456-001")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Client: {data['client']['clientName']}")
    print(f"Age: {data['clientSuitabilityProfile']['age']}")
    print(f"Risk Tolerance: {data['clientSuitabilityProfile']['riskTolerance']}")
    print(f"Primary Objective: {data['clientSuitabilityProfile']['primaryObjective']}")

def test_products():
    print("\n\nTesting /api/products endpoint...")
    response = requests.get(f"{BASE_URL}/api/products")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Products: {len(data)}")
    
    # Count by carrier
    symetra = sum(1 for p in data if p['carrier'] == 'Symetra')
    brighthouse = sum(1 for p in data if p['carrier'] == 'Brighthouse Financial')
    print(f"  Symetra: {symetra}")
    print(f"  Brighthouse Financial: {brighthouse}")
    print(f"  Others: {len(data) - symetra - brighthouse}")

def test_policy_alternatives():
    print("\n\nTesting /api/policies/POL-90002/alternatives endpoint...")
    response = requests.get(f"{BASE_URL}/api/policies/POL-90002/alternatives")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Current Policy: {data['currentPolicy']['policyLabel']}")
    print(f"Alternatives Found: {len(data['alternatives'])}")
    for alt in data['alternatives']:
        print(f"\n  {alt['carrier']} - {alt['productName']}")
        if alt.get('indexOptions'):
            caps = [opt['currentValue'] for opt in alt['indexOptions'] if 'Cap' in opt['strategy']]
            if caps:
                print(f"    Cap Rate: {max(caps)}%")
        if alt.get('currentFixedRate'):
            print(f"    Fixed Rate: {alt['currentFixedRate']}%")
        print(f"    Key Benefits: {', '.join(alt['keyBenefits'][:2])}")
    
    print(f"\nComparison Notes:")
    for note in data['comparisonNotes']:
        print(f"  - {note}")

def test_ai_provider_info():
    print("\n\nTesting /api/ai/provider-info endpoint...")
    response = requests.get(f"{BASE_URL}/api/ai/provider-info")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Provider: {data['provider']}")
    print(f"Mode: {data['mode']}")
    print(f"Model: {data.get('model', 'N/A')}")

def test_ai_quick_actions():
    print("\n\nTesting /api/ai/quick-actions/REPLACEMENT endpoint...")
    response = requests.get(f"{BASE_URL}/api/ai/quick-actions/REPLACEMENT")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Alert Type: {data['alert_type']}")
    print(f"Quick Actions:")
    for action in data['actions']:
        print(f"  - {action}")

def test_ai_chat():
    print("\n\nTesting /api/ai/chat endpoint...")
    
    # Test with REPLACEMENT alert context
    request_data = {
        "message": "Why was this replacement alert triggered?",
        "context": {
            "client_id": "101-123456-001",
            "policy_id": "POL-90002",
            "alert_type": "REPLACEMENT",
            "current_cap": "3.4%",
            "alert_severity": "HIGH",
            "client_name": "Jennifer Martinez",
            "policy_label": "Symetra Protector 5 IUL"
        },
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/chat", json=request_data)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"\nAI Response:")
    print(f"  {data['message']}")
    if data.get('based_on'):
        print(f"\nBased on: {data['based_on']}")
    print(f"\nToken Usage: {data.get('token_usage', 'N/A')}")

if __name__ == "__main__":
    try:
        test_health()
        test_policies_listing()
        test_policy_detail()
        test_client()
        test_products()
        test_policy_alternatives()
        test_ai_provider_info()
        test_ai_quick_actions()
        test_ai_chat()
        print("\n✅ All tests passed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API at http://localhost:8000")
        print("Make sure the server is running with: uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
