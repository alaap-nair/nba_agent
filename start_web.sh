#!/bin/bash

echo "🏀 Starting NBA Agent Web Interface..."
echo "=================================="

# Load environment variables
source activate_env.sh

# Activate virtual environment
source .venv/bin/activate

# Start Streamlit app
streamlit run app.py --server.port 8501 --server.address localhost

echo "🏀 NBA Agent is now running at http://localhost:8501" 