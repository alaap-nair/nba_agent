#langchain agent factory
import os
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from tools import StatsTool, ScheduleTool, StandingsTool
from judgeval.common.tracer import Tracer

def build_agent():
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    tracer = Tracer(project_name="nba_agent")   # trace everything
    return initialize_agent(
        tools=[StatsTool(), ScheduleTool(), StandingsTool()],
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,  # Enable verbose mode to see what's happening
        max_iterations=5,  # Increase iteration limit
        max_execution_time=30,  # Set execution time limit to 30 seconds
        early_stopping_method="generate",  # Better stopping method
        tracer=tracer,  # pipes traces to Judgment
        handle_parsing_errors=True  # Handle parsing errors gracefully
    )
