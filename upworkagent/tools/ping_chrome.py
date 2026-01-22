# tools/ping_chrome.py
import requests

def check_chrome():
    try:
    # Try IPv4 specifically
        r = requests.get("http://127.0.0.1:9222/json/version", timeout=2)
        print(f"✅ Door Open! Connected to: {r.json()['Browser']}")
    except:
        print("❌ Door Closed. Python cannot see Chrome.")
if __name__ == "__main__":
    check_chrome()
    