import json
import requests
import pprint

# Load the test request data
with open('test_request.json', 'r') as f:
    test_data = json.load(f)

# Send the request to the API
response = requests.post('http://localhost:8000/process', json=test_data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    result = response.json()
    
    # Print user ID and timestamp
    print(f"User ID: {result['user_id']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Confidence: {result['confidence']}")
    print("\n--- TOP RECOMMENDATIONS ---")
    
    # Print the top 3 recommendations
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"\n{i}. {rec.get('type', 'UNKNOWN').upper()}: {rec.get('action', 'Unknown').replace('_', ' ').title()}")
        print(f"   Priority: {rec.get('priority', 'unknown')}")
        print(f"   Source: {rec.get('source_agent', 'unknown')}")
        if 'description' in rec:
            print(f"   Description: {rec['description']}")
    
    # Print insights
    print("\n--- KEY INSIGHTS ---")
    for i, insight in enumerate(result['insights'][:3], 1):
        print(f"\n{i}. {insight.get('type', 'UNKNOWN').upper()}")
        # Handle different insight structures
        for key in ['title', 'category', 'name']:
            if key in insight:
                print(f"   {key.title()}: {insight[key]}")
                break
        if 'description' in insight:
            print(f"   Description: {insight['description']}")
    
    # Print agent contributions
    print("\n--- AGENT CONTRIBUTIONS ---")
    for agent, contribution in result['agent_contributions'].items():
        print(f"\n{agent.upper()}")
        if 'confidence' in contribution:
            print(f"   Confidence: {contribution['confidence']}")
        if 'key_findings' in contribution and contribution['key_findings']:
            findings = contribution['key_findings']
            if isinstance(findings, list) and len(findings) > 0:
                print(f"   Key Findings: {', '.join(findings[:2])}...")
            else:
                print(f"   Key Findings: {findings}")
    
    # Save the full response to a file for further examination
    with open('full_response.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("\nFull response saved to 'full_response.json'")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)
