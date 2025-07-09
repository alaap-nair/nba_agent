#!/usr/bin/env python3
"""
Quick launcher for NBA Agent Enhanced Visualizations
Run this to see the enhanced interface with modern visualizations
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    print("🏀 NBA Agent - Enhanced Visualization Demo")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Check if visualization files exist
    viz_files = ['visualizations.py', 'smart_interface.py', 'app_enhanced.py', 'demo_visualization.py']
    missing_files = [f for f in viz_files if not Path(f).exists()]
    
    if missing_files:
        print(f"⚠️ Missing files: {', '.join(missing_files)}")
        print("Please ensure all visualization files are in the current directory.")
        sys.exit(1)
    
    print("✅ All dependencies and files found!")
    print("\n🚀 Choose what to run:")
    print("1. 📊 Enhanced NBA Agent App (Full Experience)")
    print("2. 🎯 Visualization Demo (Feature Showcase)")
    print("3. 🏀 Original App (For Comparison)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🏀 Starting Enhanced NBA Agent...")
        print("💡 Features: Interactive charts, smart interface, mobile-optimized")
        print("🔗 Opening in browser...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_enhanced.py"])
    
    elif choice == "2":
        print("\n🎯 Starting Visualization Demo...")
        print("💡 Features: All visualization components showcase")
        print("🔗 Opening in browser...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "demo_visualization.py"])
    
    elif choice == "3":
        print("\n🏀 Starting Original NBA Agent...")
        print("💡 Basic interface for comparison")
        print("🔗 Opening in browser...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    
    else:
        print("❌ Invalid choice. Please run again and choose 1, 2, or 3.")
        sys.exit(1)

if __name__ == "__main__":
    main() 