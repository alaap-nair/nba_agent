#!/usr/bin/env python3
"""
Enhanced UX Demo Launcher for NBA Agent Pro

This script launches the enhanced user experience version of the NBA Agent
with improved onboarding, personalization, and interactive features.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        "streamlit",
        "langchain",
        "langchain-openai", 
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_env_vars():
    """Check if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your environment or .env file")
        return False
    
    return True

def main():
    """Launch the enhanced UX NBA Agent demo"""
    print("🏀 NBA Agent Pro - Enhanced UX Demo Launcher")
    print("=" * 50)
    
    # Check requirements
    print("📋 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    print("🔐 Checking environment variables...")
    if not check_env_vars():
        sys.exit(1)
    
    print("✅ All requirements met!")
    print()
    
    # Check if enhanced UX app exists
    app_file = Path("app_ux_improved.py")
    if not app_file.exists():
        print("❌ Enhanced UX app file not found: app_ux_improved.py")
        sys.exit(1)
    
    print("🚀 Launching NBA Agent Pro with Enhanced UX...")
    print()
    print("Features included in this demo:")
    print("• 🎯 Interactive onboarding for new users")
    print("• ⭐ Personalized favorites system")
    print("• 🔄 Smart suggestions based on time of day")
    print("• 📊 Enhanced stat visualizations")
    print("• 🎨 Improved animations and micro-interactions")
    print("• 📱 Mobile-responsive design")
    print("• 🌟 Contextual tips and hints")
    print("• ⚡ Better loading states and feedback")
    print()
    print("🌐 Opening in your default browser...")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app_ux_improved.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
    
    except KeyboardInterrupt:
        print("\n👋 Thanks for trying NBA Agent Pro Enhanced UX!")
        print("🌟 We hope you enjoyed the improved experience!")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 