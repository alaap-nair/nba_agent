#!/usr/bin/env python3
"""
NBA Agent Launcher
Easy way to run the different interfaces
"""

import subprocess
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("🏀 NBA Agent Launcher")
        print("Usage: python launcher.py [app_name]")
        print("\nAvailable apps:")
        print("  web       - Original Streamlit web interface")
        print("  web-ux    - Enhanced UX Streamlit interface")
        print("  chat      - Terminal chat interface")
        print("  enhanced  - Enhanced chat with flexible query parsing")
        print("  plan      - Agentic planning chat")
        print("  tests     - Run test suite")
        print("\nExample: python launcher.py web-ux")
        return
    
    app_name = sys.argv[1].lower()
    
    if app_name == "web":
        print("🏀 Starting original web interface...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "apps/app.py"])
    elif app_name == "web-ux":
        print("🏀 Starting enhanced UX web interface...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "apps/app_ux_improved.py"])
    elif app_name == "chat":
        print("🏀 Starting terminal chat interface...")
        subprocess.run([sys.executable, "apps/chat.py"])
    elif app_name == "enhanced":
        print("🏀 Starting enhanced chat with flexible query parsing...")
        subprocess.run([sys.executable, "apps/enhanced_chat.py"])
    elif app_name == "plan":
        print("🏀 Starting planning chat interface...")
        subprocess.run([sys.executable, "apps/chat_planner.py"])
    elif app_name == "tests":
        print("🏀 Running test suite...")
        if len(sys.argv) > 2:
            subprocess.run([sys.executable, "run_judgment_tests.py"] + sys.argv[2:])
        else:
            subprocess.run([sys.executable, "run_judgment_tests.py", "--help"])
    else:
        print(f"❌ Unknown app: {app_name}")
        print("Available: web, web-ux, chat, enhanced, plan, tests")

if __name__ == "__main__":
    main() 