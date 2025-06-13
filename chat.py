#!/usr/bin/env python3
"""
Interactive NBA Agent Chat
Run this to chat with your NBA agent!
"""

from agent import build_agent

def main():
    print("🏀 NBA Agent Chat")
    print("=" * 50)
    print("Ask me about NBA stats and schedules!")
    print("Examples:")
    print("  - What was LeBron's PPG in 2024-25?")
    print("  - When do the Warriors play next?")
    print("  - What are Curry's stats this season?")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    # Build the agent
    agent = build_agent()
    
    while True:
        try:
            # Get user input
            question = input("🤔 Ask me anything: ").strip()
            
            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'bye', 'stop']:
                print("👋 Thanks for chatting! See you later!")
                break
            
            if not question:
                continue
                
            # Get response from agent using the new invoke method
            print("🤖 Thinking...")
            response = agent.invoke({"input": question})
            # Extract the output from the response dict
            output = response.get("output", str(response))
            print(f"📊 {output}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Sorry, I encountered an error: {e}")
            print("Please try asking something else.\n")

if __name__ == "__main__":
    main() 