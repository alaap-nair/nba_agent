#langchain agent factory
import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage
from tools import StatsTool, ScheduleTool, StandingsTool, RosterTool, ArenaTool

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Conversation memory allows the agent to maintain context across turns
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Initialize agent without tracer if Judgment credentials are missing
    agent_kwargs = {
        "tools": [StatsTool(), ScheduleTool(), StandingsTool(), RosterTool(), ArenaTool()],
        "llm": llm,
        "agent": AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        "verbose": True,  # Enable verbose mode to see what's happening
        "max_iterations": 5,  # Increase iteration limit
        "max_execution_time": 30,  # Set execution time limit to 30 seconds
        "early_stopping_method": "generate",  # Better stopping method
        "handle_parsing_errors": True,  # Handle parsing errors gracefully
        "memory": memory,
    }
    
    # Add tracer only if Judgment API key is available
    try:
        from judgeval.common.tracer import Tracer
        if os.getenv("JUDGMENT_API_KEY"):
            tracer = Tracer(project_name="nba_agent", deep_tracing=False)
            agent_kwargs["tracer"] = tracer
            print("✅ Judgment tracing enabled")
        else:
            print("⚠️  Running without Judgment tracing (no API key found)")
    except Exception as e:
        print(f"⚠️  Running without Judgment tracing: {e}")
    
    return initialize_agent(**agent_kwargs)


class PlanningAgent:
    """Wrapper agent that generates a plan before answering."""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.base_agent = build_agent()

    def _generate_plan(self, question: str) -> str:
        prompt = (
            "You are an NBA assistant planning a strategy to answer the user's question. "
            "Break the question into short numbered steps."
        )
        resp = self.llm.invoke(f"{prompt}\nQuestion: {question}\nPlan:")
        # resp can be a message or string depending on llm implementation
        if isinstance(resp, BaseMessage):
            return resp.content
        return str(resp)

    def invoke(self, inputs: dict):
        question = inputs.get("input", "")
        plan = self._generate_plan(question)
        answer = self.base_agent.invoke({"input": question}).get("output", "")
        return {"plan": plan, "answer": answer}

    def run(self, question: str) -> str:
        return self.invoke({"input": question})["answer"]


def build_planning_agent() -> PlanningAgent:
    """Create a PlanningAgent for step-by-step reasoning."""
    return PlanningAgent()
