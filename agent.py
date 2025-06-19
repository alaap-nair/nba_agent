#langchain agent factory
import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import StatsTool, ScheduleTool, StandingsTool

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Initialize agent without tracer if Judgment credentials are missing
    agent_kwargs = {
        "tools": [StatsTool(), ScheduleTool(), StandingsTool()],
        "llm": llm,
        "agent": AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        "verbose": True,  # Enable verbose mode to see what's happening
        "max_iterations": 5,  # Increase iteration limit
        "max_execution_time": 30,  # Set execution time limit to 30 seconds
        "early_stopping_method": "generate",  # Better stopping method
        "handle_parsing_errors": True  # Handle parsing errors gracefully
    }
    
    # Add tracer only if Judgment API key is available
    try:
        from judgeval.common.tracer import Tracer
        if os.getenv("JUDGMENT_API_KEY"):
            tracer = Tracer(project_name="nba_agent")
            agent_kwargs["tracer"] = tracer
            print("✅ Judgment tracing enabled")
        else:
            print("⚠️  Running without Judgment tracing (no API key found)")
    except Exception as e:
        print(f"⚠️  Running without Judgment tracing: {e}")
    
    return initialize_agent(**agent_kwargs)
