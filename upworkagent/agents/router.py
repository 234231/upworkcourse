# agents/router.py

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("DEEPSEEK_API_KEY") 
        


if not api_key:
    raise ValueError("❌ API Key missing! Check your .env file for DEEPSEEK_API_KEY")
class IntentRouter:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model="mistralai/devstral-2512:free"
        )

    def classify(self, user_input: str):
       # agents/router.py
# ... inside the prompt variable ...
        prompt = f"""
        Analyze the user input and choose exactly ONE category:
        1. RESEARCH: Use this if the user wants to scan tabs, scrape profiles, or analyze competitors.
        2. ANALYST: Use this if the user pasted a bio directly into the chat.
        3. INTERVIEWER: Use this only if the user is asking a general question or is being vague.
        
        Input: "{user_input}"
        Category:"""
        
        response = self.llm.invoke(prompt)
        content = response.content.upper()
        
        if "CLIPBOARD" in content: return "analyst"
        if "RESEARCH" in content: return "researcher"
        return "interviewer"