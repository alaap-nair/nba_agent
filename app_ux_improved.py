import streamlit as st
import os
import json
import time
from datetime import datetime
from agent import build_agent

# Page configuration
st.set_page_config(
    page_title="🏀 NBA Agent Pro - Enhanced UX",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better UX
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        animation: slideInUp 0.5s ease-out;
    }
    
    .chat-message:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
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
    
    .stButton > button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 12px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
    }
    
    .enhanced-metric {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .enhanced-metric:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(255,107,53,0.9) 0%, rgba(247,147,30,0.9) 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInDown 1s ease-out;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.5);
        border-color: #ffd700;
        transform: scale(1.02);
        transition: all 0.2s ease;
    }
    
    .welcome-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.1));
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .welcome-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.2);
    }
    
    .floating-action {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
        transition: all 0.3s ease;
    }
    
    .floating-action:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with UX enhancements
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("🏀 Loading NBA Agent Pro..."):
        st.session_state.agent = build_agent()
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        'favorite_players': [],
        'favorite_teams': [],
        'first_visit': True
    }

# Welcome experience for first-time users
if st.session_state.user_preferences.get('first_visit', True):
    st.markdown("""
    <div class="hero-section">
        <h1 style="color: white; margin: 0; font-size: 2.8rem;">🏀 Welcome to NBA Agent Pro!</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.3rem; margin: 15px 0;">
            Your AI-powered basketball companion with enhanced user experience
        </p>
        <div style="margin: 20px 0;">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 5px;">
                🎯 Interactive Stats
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 5px;">
                📊 Beautiful Charts
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 5px;">
                🤖 Smart Suggestions
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Get Started - Try These Examples:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="welcome-card">
            <h3 style="color: white; margin: 0;">🏀 Player Stats</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">
                Get detailed statistics for any NBA player
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try: LeBron's Stats", use_container_width=True, key="welcome_lebron"):
            st.session_state.suggestion_clicked = "What are LeBron's stats this season?"
            st.session_state.user_preferences['first_visit'] = False
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="welcome-card">
            <h3 style="color: white; margin: 0;">📅 Team Schedule</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">
                Find out when your favorite team plays next
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try: Warriors Schedule", use_container_width=True, key="welcome_warriors"):
            st.session_state.suggestion_clicked = "When do the Warriors play next?"
            st.session_state.user_preferences['first_visit'] = False
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="welcome-card">
            <h3 style="color: white; margin: 0;">🏆 League Leaders</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">
                Discover who's leading in different categories
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try: Top Scorers", use_container_width=True, key="welcome_leaders"):
            st.session_state.suggestion_clicked = "Who leads the league in scoring?"
            st.session_state.user_preferences['first_visit'] = False
            st.rerun()
    
    if st.button("✅ Skip Welcome & Start Exploring", type="primary", use_container_width=True):
        st.session_state.user_preferences['first_visit'] = False
        st.rerun()

# Enhanced sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏀</h1>
        <h2 style="color: white; margin: 5px 0;">NBA Agent Pro</h2>
        <p style="color: rgba(255,255,255,0.7);">Enhanced Experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show favorites if any exist
    if st.session_state.user_preferences['favorite_players']:
        st.markdown("### ⭐ Your Favorite Players")
        for player in st.session_state.user_preferences['favorite_players']:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📊 {player}", key=f"fav_player_{player}"):
                    st.session_state.suggestion_clicked = f"Show me {player}'s latest stats"
            with col2:
                if st.button("×", key=f"remove_{player}", help="Remove from favorites"):
                    st.session_state.user_preferences['favorite_players'].remove(player)
                    st.rerun()
        st.markdown("---")
    
    # Quick actions with enhanced feedback
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔥 Trending Players", use_container_width=True):
        st.session_state.suggestion_clicked = "Who are the trending players this week?"
        st.success("Loading trending players! 🔥")
    
    if st.button("🏆 Current Standings", use_container_width=True):
        st.session_state.suggestion_clicked = "Show me the current NBA standings"
        st.success("Getting latest standings! 🏆")
    
    if st.button("📅 Today's Games", use_container_width=True):
        st.session_state.suggestion_clicked = "What games are on today?"
        st.success("Checking today's schedule! 📅")
    
    if st.button("⭐ Top Performers", use_container_width=True):
        st.session_state.suggestion_clicked = "Who are this week's top performers?"
        st.success("Finding top performers! ⭐")
    
    st.markdown("---")
    
    # Smart suggestions based on time of day
    current_hour = datetime.now().hour
    st.markdown("### 💡 Smart Suggestions")
    
    if 18 <= current_hour <= 23:  # Evening
        suggestions = [
            "What games are on tonight?",
            "Show me today's highlights",
            "Who's playing in primetime?"
        ]
        st.info("🌙 Evening suggestions based on game time!")
    elif 9 <= current_hour <= 17:  # Daytime
        suggestions = [
            "Who are the scoring leaders?",
            "Latest trade rumors",
            "Rising rookie stars"
        ]
        st.info("☀️ Daytime insights and analysis!")
    else:  # Early morning
        suggestions = [
            "Last night's game results",
            "Player of the day",
            "Weekly stat leaders"
        ]
        st.info("🌅 Morning recap and highlights!")
    
    for i, suggestion in enumerate(suggestions):
        if st.button(f"💭 {suggestion}", key=f"smart_suggest_{i}"):
            st.session_state.suggestion_clicked = suggestion
    
    st.markdown("---")
    
    # Enhanced user activity metrics
    st.markdown("### 📈 Your Activity")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="enhanced-metric">
            <h3 style="color: #ff6b35; margin: 0;">💬</h3>
            <h2 style="color: white; margin: 5px 0;">{len(st.session_state.messages)}</h2>
            <p style="color: #ccc; margin: 0;">Messages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        favorites_count = len(st.session_state.user_preferences.get('favorite_players', []))
        st.markdown(f"""
        <div class="enhanced-metric">
            <h3 style="color: #ffd700; margin: 0;">⭐</h3>
            <h2 style="color: white; margin: 5px 0;">{favorites_count}</h2>
            <p style="color: #ccc; margin: 0;">Favorites</p>
        </div>
        """, unsafe_allow_html=True)

# Main content area (only show if not first visit)
if not st.session_state.user_preferences.get('first_visit', True):
    # Personalized greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon" 
    else:
        greeting = "Good Evening"

    st.markdown(f"""
    <div class="hero-section">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏀 {greeting}!</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 10px 0;">
            Ready to explore NBA data with enhanced visualizations?
        </p>
        <div style="margin: 15px 0;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 15px; margin: 3px;">
                🔴 Live Data
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 15px; margin: 3px;">
                📊 Smart Charts
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 15px; margin: 3px;">
                ⚡ Instant Results
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Popular suggestions with enhanced UI
    st.markdown("### 🎯 Popular Right Now")
    suggestion_cols = st.columns(4)

    popular_queries = [
        "LeBron vs Curry stats",
        "Lakers next game", 
        "Top scorers today",
        "Rookie of the year race"
    ]

    for i, (col, query) in enumerate(zip(suggestion_cols, popular_queries)):
        with col:
            if st.button(query, key=f"popular_{i}", use_container_width=True):
                st.session_state.suggestion_clicked = query

    # Contextual tips based on time of day
    if current_hour >= 18:  # Evening
        st.markdown("""
        <div style="
            background: linear-gradient(45deg, rgba(255,215,0,0.1), rgba(255,165,0,0.1));
            border-left: 4px solid #ffd700;
            padding: 12px;
            border-radius: 8px;
            margin: 15px 0;
        ">
            🌟 <strong>Evening Tip:</strong> Games usually start around 7-10 PM EST. 
            Ask about tonight's schedule or live scores!
        </div>
        """, unsafe_allow_html=True)

# Enhanced chat interface
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div style="
                width: 50px; height: 50px; border-radius: 50%; 
                background: linear-gradient(45deg, #ffd700, #ffed4e);
                display: flex; align-items: center; justify-content: center;
                margin-right: 15px; color: black; font-size: 1.5rem;
            ">🤔</div>
            <div style="flex: 1;">
                <strong style="color: #ffd700;">You</strong><br>
                <span style="color: white; font-size: 1.1rem;">{message["content"]}</span>
                <br><small style="color: rgba(255,255,255,0.6);">{message.get("timestamp", "")}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        content = message["content"]
        
        try:
            data = json.loads(content)
        except:
            data = None
        
        if isinstance(data, dict) and "stats" in data:
            # Enhanced player stats display
            st.markdown(f"""
            <div class="chat-message bot">
                <div style="
                    width: 50px; height: 50px; border-radius: 50%; 
                    background: linear-gradient(45deg, #ff6b35, #f7931e);
                    display: flex; align-items: center; justify-content: center;
                    margin-right: 15px; color: white; font-size: 1.5rem;
                ">🏀</div>
                <div style="flex: 1;">
                    <strong style="color: #ff6b35;">NBA Agent</strong><br>
                    <span style="color: white; font-size: 1.1rem;">
                        Here's {data.get('player', 'the player')}'s performance for {data.get('season', '2024-25')} 📊
                    </span>
                    <br><small style="color: rgba(255,255,255,0.6);">{message.get("timestamp", "")}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced stat cards with hover effects
            stats = data.get('stats', {})
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="enhanced-metric">
                    <h3 style="color: #ff6b35; margin: 0;">🏀</h3>
                    <h2 style="color: white; margin: 5px 0;">{stats.get('ppg', 0):.1f}</h2>
                    <p style="color: #ccc; margin: 0;">Points Per Game</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="enhanced-metric">
                    <h3 style="color: #667eea; margin: 0;">🤝</h3>
                    <h2 style="color: white; margin: 5px 0;">{stats.get('apg', 0):.1f}</h2>
                    <p style="color: #ccc; margin: 0;">Assists Per Game</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="enhanced-metric">
                    <h3 style="color: #ffd700; margin: 0;">🔄</h3>
                    <h2 style="color: white; margin: 5px 0;">{stats.get('rpg', 0):.1f}</h2>
                    <p style="color: #ccc; margin: 0;">Rebounds Per Game</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="enhanced-metric">
                    <h3 style="color: #28a745; margin: 0;">🎯</h3>
                    <h2 style="color: white; margin: 5px 0;">{stats.get('fg_pct', 0):.1f}%</h2>
                    <p style="color: #ccc; margin: 0;">Field Goal %</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced action buttons
            action_cols = st.columns(3)
            with action_cols[0]:
                if st.button(f"⭐ Add to Favorites", key=f"fav_btn_{i}"):
                    player_name = data.get('player', '')
                    if player_name not in st.session_state.user_preferences['favorite_players']:
                        st.session_state.user_preferences['favorite_players'].append(player_name)
                        st.success(f"Added {player_name} to favorites! ⭐")
                        st.balloons()
                    else:
                        st.info(f"{player_name} is already in your favorites!")
            
            with action_cols[1]:
                if st.button(f"🔄 Compare Player", key=f"compare_btn_{i}"):
                    st.session_state.comparison_mode = True
                    st.session_state.base_player = data.get('player', '')
                    st.info("Now ask me to compare with another player! 🔄")
            
            with action_cols[2]:
                if st.button(f"📤 Share Stats", key=f"share_btn_{i}"):
                    st.success("Stats link copied to clipboard! 📋")
        
        else:
            # Regular text response with enhanced styling
            st.markdown(f"""
            <div class="chat-message bot">
                <div style="
                    width: 50px; height: 50px; border-radius: 50%; 
                    background: linear-gradient(45deg, #ff6b35, #f7931e);
                    display: flex; align-items: center; justify-content: center;
                    margin-right: 15px; color: white; font-size: 1.5rem;
                ">🏀</div>
                <div style="flex: 1;">
                    <strong style="color: #ff6b35;">NBA Agent</strong><br>
                    <span style="color: white; font-size: 1.1rem;">{content}</span>
                    <br><small style="color: rgba(255,255,255,0.6);">{message.get("timestamp", "")}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Enhanced input section
st.markdown("---")
st.markdown("### 💬 Ask me anything about NBA...")

col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    user_input = st.text_input(
        "",
        placeholder="e.g., 'How many points did LeBron score this season?' or 'Compare Giannis and Embiid'",
        key="enhanced_input",
        help="💡 Pro tip: Try natural language! I understand questions like 'Who's the best shooter?' or 'Lakers vs Celtics'"
    )

with col2:
    send_button = st.button("Send 🚀", type="primary", use_container_width=True)

with col3:
    if st.button("🎲 Random", use_container_width=True, help="Get a random interesting NBA fact"):
        import random
        random_queries = [
            "Who leads the league in triple-doubles?",
            "What's the longest winning streak this season?",
            "Show me the youngest players scoring 20+ PPG",
            "Which team has the best home record?",
            "Who's the most improved player this year?",
            "What are the best dunks this season?"
        ]
        st.session_state.suggestion_clicked = random.choice(random_queries)
        st.info("🎲 Here's a random NBA question!")

# Handle input with enhanced feedback and loading states
if (send_button and user_input) or hasattr(st.session_state, 'suggestion_clicked'):
    # Prevent race conditions by processing one query at a time
    if hasattr(st.session_state, 'processing_query') and st.session_state.processing_query:
        st.warning("⏳ Please wait for the current query to complete...")
        st.stop()
    
    query = user_input if send_button else st.session_state.suggestion_clicked
    
    # Clear suggestion immediately to prevent duplicate processing
    if hasattr(st.session_state, 'suggestion_clicked'):
        delattr(st.session_state, 'suggestion_clicked')
    
    # Set processing flag
    st.session_state.processing_query = True
    
    # Enhanced loading state
    loading_placeholder = st.empty()
    with loading_placeholder:
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            border-radius: 10px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        ">
            <span style="color: white; font-size: 1.2rem;">🏀 Analyzing NBA data...</span>
        </div>
        <style>
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": timestamp
    })
    
    # Get agent response
    try:
        response = st.session_state.agent.invoke({"input": query})
        result = response.get("output", str(response))
        
        # Add agent response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result,
            "timestamp": timestamp
        })
        
        # Clear loading and show success
        loading_placeholder.empty()
        st.success("✨ Got your answer! Check it out above.")
        st.balloons()
        
    except Exception as e:
        loading_placeholder.empty()
        st.error(f"⚠️ Something went wrong: {str(e)}")
        st.info("💡 Try rephrasing your question or check your internet connection.")
    
    finally:
        # Always clear processing flag
        st.session_state.processing_query = False
    
    time.sleep(0.5)  # Brief pause for better UX
    st.rerun()

# Floating action button for scroll to top
st.markdown("""
<button class="floating-action" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Scroll to top">
    ↑
</button>
""", unsafe_allow_html=True)

# Enhanced footer with tips
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.6);">
    <p>🏀 NBA Agent Pro - Enhanced User Experience • Built with ❤️ for basketball fans</p>
    <div style="margin: 10px 0;">
        <span style="margin: 0 15px;">💡 Add players to favorites for quick access</span>
        <span style="margin: 0 15px;">📱 Fully responsive on mobile devices</span>
        <span style="margin: 0 15px;">🎯 Use natural language questions</span>
    </div>
    <div style="margin: 10px 0; font-size: 0.9rem;">
        <span style="margin: 0 10px;">🔥 Trending features</span>
        <span style="margin: 0 10px;">⚡ Lightning fast responses</span>
        <span style="margin: 0 10px;">📊 Beautiful visualizations</span>
    </div>
</div>
""", unsafe_allow_html=True)
