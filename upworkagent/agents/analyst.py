# agents/analyst.py
from langchain_openai import ChatOpenAI
import os

class AnalystNode:
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        # Explicitly passing the key removes the warning
        self.llm = ChatOpenAI(model="mistralai/devstral-2512:free", openai_api_key=api_key)

    def work(self, state: dict):
        print("Analyst Node is processing competitor data...")
        
        competitors = state.get("competitors", [])
        if not competitors:
            return {"seo_strategy": "No data found to analyze.", "next_node": "END"}

        # Format the scraped data for the AI
        formatted_data = ""
        for comp in competitors:
            formatted_data += f"\nCOMPETITOR: {comp['headline']}\nBIO: {comp['bio']}\n"

        prompt = f"""
        You are an Upwork Profile SEO Expert. Analyze these competitors:
        {formatted_data}
        
        Provide a strategy for the user:
        1. **Keyword Analysis**: Which high-value keywords are they ranking for?
        2. **Hook Analysis**: How do they start their bio to catch clients?
        3. **The 'Better' Strategy**: Write a 3-sentence hook for the user that beats these competitors.
        """

        response = self.llm.invoke(prompt)
        
        print("✅ Analysis Complete.")
        return {
            "seo_strategy": response.content,
            "next_node": "END"
        }