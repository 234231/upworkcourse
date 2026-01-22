import sys
import asyncio
import os

# 1. FIX: Resolve Windows ProactorEventLoop (Must be at the very top)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from dotenv import load_dotenv
from agents.router import IntentRouter
from agents.researcher import ResearcherNode
from agents.analyst import AnalystNode

# Load API keys from .env
load_dotenv()

class UpworkAgent:
    def __init__(self, profile_port=9222):
        """
        Initializes the agent and connects tools to the correct Chrome profile.
        """
        self.router = IntentRouter()
        self.researcher = ResearcherNode()
        
        # 2. FIX: Sync ports across all tools to prevent 'No URLs Found'
        port_url = f"http://127.0.0.1:{profile_port}"
        self.researcher.tab_hunter.cdp_url = port_url
        self.researcher.scraper.cdp_url = port_url
        
        self.analyst = AnalystNode()

    def run(self, user_prompt):
        print(f"\n--- 🧠 Agent Input: {user_prompt} ---")
        
        # 3. ROUTING: Determine if we need to scrape or just analyze
        decision = self.router.classify(user_prompt)
        print(f"DEBUG: Router Decision -> {decision}")
        
        state = {
            "input": user_prompt, 
            "competitors": [], 
            "urls": [],
            "seo_strategy": ""
        }
        
        # 4. RESEARCHER: Scrape the browser if intent is Research
        if "researcher" in decision.lower():
            print("Action: Hunting for Upwork tabs...")
            res_data = self.researcher.work(state)
            state.update(res_data)
            
            if not state["competitors"]:
                print("⚠️ Warning: No profiles were scraped.")

        # 5. ANALYST: Process data with NVIDIA Llama-3.1-405B
        print(f"Action: Analyzing {len(state['competitors'])} profile(s)...")
        analysis_result = self.analyst.work(state)
        
        # Return final result for Streamlit/Terminal
        return analysis_result.get("seo_strategy", "I couldn't generate a strategy. Check Chrome connection.")

if __name__ == "__main__":
    # Terminal Test Code
    # Ensure Chrome is running with --remote-debugging-port=9222
    agent = UpworkAgent(profile_port=9222)
    
    # Using your specific requirement for freelancer profiles
    print("Testing connection to open Chrome tabs...")
    result = agent.run("Analyze the freelancer profiles I have open")
    
    print("\n" + "="*30)
    print("FINAL STRATEGY OUTPUT")
    print("="*30)
    print(result)