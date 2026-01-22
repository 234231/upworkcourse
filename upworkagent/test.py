# upworkagent/test_full_flow.py
from agents.router import IntentRouter
from agents.researcher import ResearcherNode
from agents.analyst import AnalystNode

def run_full_system():
    # 1. State Setup
# In your test script, change the input to be very specific:
    state = {"input": "RESEARCH: Analyze my open Upwork tabs", "urls": [], "competitors": []}
    
    # 2. Router
    router = IntentRouter()
    next_step = router.classify(state["input"])
    print(f"Router decided: {next_step}")
    
    # 3. Researcher
    if next_step == "researcher":
        researcher = ResearcherNode()
        res_output = researcher.work(state)
        state.update(res_output)
    
    # 4. Analyst
    analyst = AnalystNode()
    final_output = analyst.work(state)
    
    print("\n--- FINAL SEO STRATEGY ---")
    print(final_output["seo_strategy"])

if __name__ == "__main__":
    run_full_system()