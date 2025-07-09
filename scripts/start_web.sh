#!/bin/bash

echo "🏀 Starting NBA Agent Web Interface..."
echo "=================================="

# Navigate to project root
cd "$(dirname "$0")/.."

# Load environment variables
source scripts/activate_env.sh

# Activate virtual environment
source .venv/bin/activate

# Start enhanced Streamlit app by default, fallback to original
if [ -f "apps/app_ux_improved.py" ]; then
    echo "🚀 Starting Enhanced UX Interface..."
    streamlit run apps/app_ux_improved.py --server.port 8501 --server.address localhost
else
    echo "📱 Starting Original Interface..."
    streamlit run apps/app.py --server.port 8501 --server.address localhost
fi

echo "🏀 NBA Agent is now running at http://localhost:8501" 