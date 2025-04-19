import requests
import json

def test_endpoint(url, method="GET", data=None):
    headers = {
        "Origin": "http://localhost:8000",
        "Content-Type": "application/json"
    }
    
    print(f"\nTesting {method} request to {url}")
    print("-" * 50)
    
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print("\nResponse Headers:")
        for key, value in response.headers.items():
            if key.lower().startswith('access-control'):
                print(f"  {key}: {value}")
        
        print("\nResponse Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

def main():
    base_url = "https://iplbackend-xenz.onrender.com"
    
    # Test root endpoint
    test_endpoint(f"{base_url}/")
    
    # Test stats endpoint
    test_endpoint(f"{base_url}/stats")
    
    # Test vote endpoint
    test_endpoint(
        f"{base_url}/vote",
        method="POST",
        data={"team_name": "Mumbai Indians"}
    )

if __name__ == "__main__":
    main() 