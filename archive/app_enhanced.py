import streamlit as st
import os
import json
import time
from datetime import datetime
from agent import build_agent
from visualizations import NBAVisualizations, LiveGameWidget, add_enhanced_css
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="🏀 NBA Agent Pro",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add enhanced styling
add_enhanced_css()

# Enhanced CSS with modern glassmorphism design
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(255,107,53,0.9) 0%, rgba(247,147,30,0.9) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInUp 1s ease-out;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        animation: slideInUp 0.5s ease-out;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        border-left: 4px solid #ffd700;
        margin-left: 2rem;
    }
    
    .chat-message.bot {
        background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.05));
        border-left: 4px solid #ff6b35;
        margin-right: 2rem;
    }
    
    .quick-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 20px 0;
        justify-content: center;
    }
    
    .action-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .action-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .suggestion-chip {
        background: linear-gradient(45deg, rgba(255,215,0,0.8), rgba(255,165,0,0.8));
        color: black;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .suggestion-chip:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }
    
    .voice-input {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        color: white;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    
    .voice-input:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.5);
    }
    
    .live-indicator {
        background: #ff4757;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        animation: pulse 2s infinite;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("🏀 Loading NBA Agent Pro..."):
        st.session_state.agent = build_agent()
if "visualization_mode" not in st.session_state:
    st.session_state.visualization_mode = "Interactive"
if "comparison_player" not in st.session_state:
    st.session_state.comparison_player = None

# Sidebar with enhanced features
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: white; margin: 0;">🏀</h1>
        <h2 style="color: white; margin: 5px 0;">NBA Agent Pro</h2>
        <p style="color: rgba(255,255,255,0.7);">Your AI-powered NBA companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualization mode selector
    st.markdown("### 📊 Visualization Mode")
    viz_mode = st.radio(
        "Choose display style:",
        ["Interactive", "Detailed Charts", "Comparison Mode"],
        index=0
    )
    st.session_state.visualization_mode = viz_mode
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔥 Trending Players", use_container_width=True):
        st.session_state.quick_action = "trending"
    
    if st.button("🏆 Standings", use_container_width=True):
        st.session_state.quick_action = "standings"
    
    if st.button("📅 Today's Games", use_container_width=True):
        st.session_state.quick_action = "today_games"
    
    if st.button("⭐ Top Performers", use_container_width=True):
        st.session_state.quick_action = "top_performers"
    
    st.markdown("---")
    
    # Smart suggestions
    st.markdown("### 💡 Smart Suggestions")
    suggestions = [
        "LeBron vs Giannis stats",
        "Warriors next 5 games",
        "Top scorers this week",
        "Rookie of the year race"
    ]
    
    for suggestion in suggestions:
        if st.button(f"💭 {suggestion}", key=f"suggest_{suggestion}"):
            st.session_state.suggestion_clicked = suggestion
    
    st.markdown("---")
    
    # Chat stats with enhanced design
    st.markdown("### 📈 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", len(st.session_state.messages))
    with col2:
        if st.session_state.messages:
            st.metric("⏱️ Active", "🟢 Live")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content area
# Hero section
st.markdown("""
<div class="hero-section">
    <h1 style="color: white; margin: 0; font-size: 3rem;">🏀 NBA Agent Pro</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 10px 0;">
        Experience NBA data like never before with AI-powered insights and stunning visualizations
    </p>
    <div class="live-indicator">🔴 LIVE DATA</div>
</div>
""", unsafe_allow_html=True)

# Quick action buttons
st.markdown("""
<div class="quick-actions">
    <button class="action-button">🔥 Player Stats</button>
    <button class="action-button">📊 Team Analysis</button>
    <button class="action-button">🏆 Standings</button>
    <button class="action-button">📅 Schedule</button>
    <button class="action-button">⚡ Live Games</button>
</div>
""", unsafe_allow_html=True)

# Smart query suggestions
st.markdown("### 💭 Try asking me...")
suggestion_cols = st.columns(4)

smart_suggestions = [
    "What are LeBron's stats?",
    "Warriors next game?", 
    "Top scorers today",
    "Lakers vs Celtics comparison"
]

for i, (col, suggestion) in enumerate(zip(suggestion_cols, smart_suggestions)):
    with col:
        if st.button(suggestion, key=f"smart_suggest_{i}", use_container_width=True):
            st.session_state.suggestion_clicked = suggestion

# Display chat messages with enhanced visualizations
chat_container = st.container()
with chat_container:
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="avatar" style="
                        width: 50px; height: 50px; border-radius: 50%; 
                        background: linear-gradient(45deg, #ffd700, #ffed4e);
                        display: flex; align-items: center; justify-content: center;
                        margin-right: 15px; color: black; font-size: 1.5rem;
                    ">🤔</div>
                    <div class="message" style="flex: 1;">
                        <strong style="color: #ffd700;">You</strong><br>
                        <span style="color: white; font-size: 1.1rem;">{message["content"]}</span>
                        <br><small style="color: rgba(255,255,255,0.6);">{message.get("timestamp", "")}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                content = message["content"]
                
                # Try to parse JSON for structured data
                try:
                    data = json.loads(content)
                except:
                    data = None
                
                # Display based on visualization mode and data type
                if isinstance(data, dict) and "stats" in data:
                    # Player stats response
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar" style="
                            width: 50px; height: 50px; border-radius: 50%; 
                            background: linear-gradient(45deg, #ff6b35, #f7931e);
                            display: flex; align-items: center; justify-content: center;
                            margin-right: 15px; color: white; font-size: 1.5rem;
                        ">🏀</div>
                        <div class="message" style="flex: 1;">
                            <strong style="color: #ff6b35;">NBA Agent</strong><br>
                            <span style="color: white; font-size: 1.1rem;">
                                Here are {data.get('player', 'the player')}'s stats for {data.get('season', '2024-25')}
                            </span>
                            <br><small style="color: rgba(255,255,255,0.6);">{message.get('timestamp', '')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced visualizations based on mode
                    if st.session_state.visualization_mode == "Interactive":
                        # Interactive stat cards
                        NBAVisualizations.create_interactive_stat_cards(data)
                        
                        # Add comparison option
                        if st.button(f"🔄 Compare with another player", key=f"compare_{i}"):
                            st.session_state.comparison_mode = True
                            st.session_state.base_player_data = data
                    
                    elif st.session_state.visualization_mode == "Detailed Charts":
                        # Detailed charts
                        tab1, tab2, tab3 = st.tabs(["🎯 Radar Chart", "🏀 Shooting Chart", "📈 Season Progress"])
                        
                        with tab1:
                            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                            radar_fig = NBAVisualizations.create_player_radar_chart(data)
                            st.plotly_chart(radar_fig, use_container_width=True, theme="streamlit")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with tab2:
                            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                            shooting_fig = NBAVisualizations.create_shooting_chart(data)
                            st.plotly_chart(shooting_fig, use_container_width=True, theme="streamlit")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with tab3:
                            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                            progression_fig = NBAVisualizations.create_season_progression(data)
                            st.plotly_chart(progression_fig, use_container_width=True, theme="streamlit")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    elif st.session_state.visualization_mode == "Comparison Mode":
                        # Show comparison interface
                        st.info("💡 Enter another player's name to compare stats!")
                        
                        comparison_input = st.text_input("Compare with:", placeholder="Enter player name...")
                        if comparison_input and st.button("Compare", key=f"compare_btn_{i}"):
                            # This would trigger a new agent call for comparison
                            st.session_state.comparison_query = f"Get stats for {comparison_input}"
                
                elif isinstance(data, dict) and ("wins" in data or "team" in data):
                    # Team/standings response
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar" style="
                            width: 50px; height: 50px; border-radius: 50%; 
                            background: linear-gradient(45deg, #667eea, #764ba2);
                            display: flex; align-items: center; justify-content: center;
                            margin-right: 15px; color: white; font-size: 1.5rem;
                        ">🏆</div>
                        <div class="message" style="flex: 1;">
                            <strong style="color: #667eea;">NBA Agent</strong><br>
                            <span style="color: white; font-size: 1.1rem;">
                                {data.get('team', 'Team')} standings information
                            </span>
                            <br><small style="color: rgba(255,255,255,0.6);">{message.get('timestamp', '')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Team visualization
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🏆 Wins", data.get('wins', 0))
                    with col2:
                        st.metric("❌ Losses", data.get('losses', 0))
                    with col3:
                        st.metric("📊 Rank", data.get('rank', 'N/A'))
                
                else:
                    # Regular text response
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar" style="
                            width: 50px; height: 50px; border-radius: 50%; 
                            background: linear-gradient(45deg, #ff6b35, #f7931e);
                            display: flex; align-items: center; justify-content: center;
                            margin-right: 15px; color: white; font-size: 1.5rem;
                        ">🏀</div>
                        <div class="message" style="flex: 1;">
                            <strong style="color: #ff6b35;">NBA Agent</strong><br>
                            <span style="color: white; font-size: 1.1rem;">{content}</span>
                            <br><small style="color: rgba(255,255,255,0.6);">{message.get("timestamp", "")}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Live games widget (if applicable)
if datetime.now().hour >= 18:  # Show during evening hours
    st.markdown("### 🔴 Live Games")
    LiveGameWidget.create_live_score_widget({})

# Enhanced chat input with voice option
st.markdown("---")
input_col1, input_col2, input_col3 = st.columns([8, 1, 1])

with input_col1:
    user_input = st.text_input(
        "Ask me anything about NBA...",
        placeholder="e.g., 'How many points did LeBron score this season?'",
        key="user_input"
    )

with input_col2:
    send_button = st.button("Send 📤", use_container_width=True)

with input_col3:
    st.markdown("""
    <button class="voice-input" title="Voice Input (Coming Soon!)">
        🎤
    </button>
    """, unsafe_allow_html=True)

# Handle input
if (send_button and user_input) or (hasattr(st.session_state, 'suggestion_clicked')):
    query = user_input if send_button else st.session_state.suggestion_clicked
    
    if hasattr(st.session_state, 'suggestion_clicked'):
        delattr(st.session_state, 'suggestion_clicked')
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": timestamp
    })
    
    # Get agent response
    with st.spinner("🏀 Analyzing NBA data..."):
        response = st.session_state.agent.invoke({"input": query})
        result = response.get("output", str(response))
    
    # Add agent response
    st.session_state.messages.append({
        "role": "assistant", 
        "content": result,
        "timestamp": timestamp
    })
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.6);">
    <p>🏀 NBA Agent Pro - Powered by AI • Built with ❤️ for basketball fans</p>
    <p>Real-time data • Interactive visualizations • Smart insights</p>
</div>
""", unsafe_allow_html=True) 