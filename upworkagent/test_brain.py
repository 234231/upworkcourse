# upworkagent/test_brain.py
import os
import sys

# Tell Python to look in the current directory for agents and tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.router import IntentRouter
from dotenv import load_dotenv

load_dotenv()

def run_test():
    try:
        router = IntentRouter()
        
        print("--- Testing Router Intelligence ---")
        
        test_1 = "Scrape these 5 profiles: http://upwork.com/freelancers/~01"
        result_1 = router.classify(test_1)
        print(f"Input: {test_1}\nResult: {result_1}\n")
        
        test_2 = "Here is my bio: I am a senior python developer with 10 years experience"
        result_2 = router.classify(test_2)
        print(f"Input: {test_2}\nResult: {result_2}\n")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_test()