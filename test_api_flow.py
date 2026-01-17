import requests
import os
import shutil

BASE_URL = "http://localhost:8000"

def test_api():
    print("--- Testing API Flow ---")
    
    # 1. Use an existing PDF
    real_pdf = "Data/raw/clean_contract.pdf"
    if not os.path.exists(real_pdf):
        print(f"File {real_pdf} not found. listing Data/raw:")
        print(os.listdir("Data/raw"))
        return

    test_file = "test_contract.pdf"
    shutil.copy(real_pdf, test_file)
    
    # Check if server is up
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"Root check: {resp.status_code}")
    except Exception as e:
        print(f"Server not reachable: {e}")
        return

    # 2. Upload
    print("Uploading document...")
    with open(test_file, "rb") as f:
        files = {'file': (test_file, f, 'application/pdf')}
        resp = requests.post(f"{BASE_URL}/documents/upload", files=files)
    
    if resp.status_code != 200:
        print(f"Upload failed: {resp.status_code} - {resp.text}")
        return
    
    data = resp.json()
    doc_id = data['id']
    print(f"Upload success. Doc ID: {doc_id}")

    # 3. Analyze
    print(f"Triggering analysis for {doc_id}...")
    resp = requests.post(f"{BASE_URL}/documents/{doc_id}/analyze")
    
    if resp.status_code != 200:
        print(f"Analysis failed: {resp.status_code} - {resp.text}")
    else:
        result = resp.json()
        print("Analysis success!")
        # Print first few chars of keys to verify
        print(f"Keys: {list(result.keys())}")
        print(f"Risk Score: {result.get('risk_score')}")

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_api()
