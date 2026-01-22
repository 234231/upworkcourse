import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state_manager import UpworkAgentState, logger

# Load environment variables from .env
load_dotenv()

# --- CONFIGURATION ---
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# This reads DEEPSEEK_API_KEY from your .env as requested
API_KEY = os.getenv("DEEPSEEK_API_KEY") 
MODEL_ID = "mistralai/devstral-2512:free"

class Supervisor:
    def __init__(self):
        # Initialize the NVIDIA model via OpenRouter
        self.llm = ChatOpenAI(
            model=MODEL_ID,
            openai_api_key=API_KEY,
            openai_api_base=OPENROUTER_BASE_URL,
            temperature=0,  
        )

    def plan_next_step(self, state: UpworkAgentState):
        logger.info(f"Supervisor ({MODEL_ID}) is analyzing state...")
        
        system_prompt = (
            "You are the Lead Planner for an Upwork Agent. "
            "Analyze the current state and pick exactly ONE next action from this list:\n"
            "SCRAPE_PROFILE - If current_profile is empty.\n"
            "SEO_ANALYSIS   - If we have profile data but no keywords/benchmarks.\n"
            "GENERATE_EDITS - If we have all data but haven't written suggestions.\n"
            "FINISH         - If the profile is fully optimized.\n"
            "\nRespond with ONLY the word of the action."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Current State: {state}")
        ]

        # Call the model
        response = self.llm.invoke(messages)
        
        # Clean the output (removes any <think> tags or extra prose)
        next_action = response.content.split("</think>")[-1].strip().upper()
        
        logger.info(f"Decision Made: {next_action}")
        return {"next_action": next_action}

# --- TEST THE BRAIN ---
if __name__ == "__main__":
    manager = Supervisor()
    # Test with an empty profile to see if it picks SCRAPE_PROFILE
    test_state = {
        "messages": [],
        "current_profile": {}, 
        "seo_benchmarks": [],
        "next_action": "",
        "suggested_edits": []
    }
    result = manager.plan_next_step(test_state)
    print(f"\n>>> The Agent decided to: {result['next_action']}")