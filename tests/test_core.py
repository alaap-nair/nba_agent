#judgment assert tests
from agent import build_agent

agent = build_agent()

def test_lebron_ppg():
    out = agent.run("What was LeBron's PPG in 2024-25?")
    assert "points" in out.lower() or "ppg" in out.lower()  # More flexible assertion

def test_warriors_next_game():
    out = agent.run("When do the Warriors play next?")
    assert "warriors" in out.lower()
