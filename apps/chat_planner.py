#!/usr/bin/env python3
"""Interactive chat using the PlanningAgent."""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import build_planning_agent


def main():
    print("🏀 NBA Planner Agent Chat")
    print("=" * 50)
    print("Ask me complex NBA questions and I'll plan the steps!")
    print("Type 'quit' to exit.\n")

    agent = build_planning_agent()

    while True:
        try:
            question = input("🤔 Ask: ").strip()
            if question.lower() in {"quit", "exit", "bye"}:
                print("👋 Goodbye!")
                break
            if not question:
                continue

            print("🤖 Planning...")
            result = agent.invoke({"input": question})
            plan = result.get("plan", "")
            answer = result.get("answer", "")
            if plan:
                print("📝 Plan:\n" + plan)
            print(f"📊 {answer}\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
