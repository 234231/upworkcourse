import logging
from typing import Annotated, List, Union, Dict
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("UpworkAgent")

# --- THE AGENT STATE ---
class UpworkAgentState(TypedDict):
    # This stores the conversation history
    messages: Annotated[list, add_messages]
    
    # Store your original profile details
    current_profile: Dict[str, str]
    
    # Store SEO keywords and competitor analysis
    seo_benchmarks: List[str]
    
    # The 'Planning' field - tells the agent what to do next
    next_action: str
    
    # A list of improvements suggested by the thinking node
    suggested_edits: List[str]

logger.info("Project State Initialized Successfully.")

if __name__ == "__main__":
    # Test to see if logging works
    test_state = {
        "messages": [],
        "current_profile": {"headline": "Python Dev"},
        "seo_benchmarks": [],
        "next_action": "start",
        "suggested_edits": []
    }
    print("State Manager is ready!")
    logger.info(f"Initial State Test: {test_state['current_profile']}")