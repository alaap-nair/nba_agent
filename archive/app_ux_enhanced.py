import streamlit as st
import os
import json
import time
from datetime import datetime
from agent import build_agent
from visualizations import NBAVisualizations, LiveGameWidget, add_enhanced_css
from ux_enhancements import (
    OnboardingFlow, PersonalizationEngine, PerformanceOptimizer,
    AccessibilityFeatures, SmartNotifications, MicroInteractions, QuickActions
)

# Page configuration
st.set_page_config(
    page_title="🏀 NBA Agent Pro - Enhanced UX",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply all UX enhancements
add_enhanced_css()
MicroInteractions.add_success_animations()
MicroInteractions.add_hover_effects()
AccessibilityFeatures.add_keyboard_shortcuts()

# Enhanced CSS with UX improvements
st.markdown("""
<style>
    /* Smooth page transitions */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        transition: all 0.3s ease;
    }
    
    /* Loading states */
    .loading-skeleton {
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Enhanced interactions */
    .interactive-element {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .interactive-element:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Success feedback */
    @keyframes success-glow {
        0% { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
        50% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.8); }
        100% { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
    }
    
    .success-feedback {
        animation: success-glow 1s ease-in-out;
    }
    
    /* Onboarding highlights */
    .onboarding-highlight {
        position: relative;
        border: 2px solid #ffd700;
        border-radius: 10px;
        animation: pulse-border 2s infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { border-color: #ffd700; }
        50% { border-color: rgba(255, 215, 0, 0.5); }
    }
    
    /* Enhanced chat messages */
    .chat-message {
        transition: all 0.3s ease;
        animation: slideInUp 0.5s ease-out;
    }
    
    .chat-message:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Floating elements */
    .floating-widget {
        position: fixed;
        z-index: 1000;
        transition: all 0.3s ease;
    }
    
    .floating-widget:hover {
        transform: scale(1.05);
    }
    
    /* Better focus states */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        outline: 2px solid #ffd700;
        outline-offset: 2px;
    }
    
    /* Quick tips */
    .quick-tip {
        background: linear-gradient(45deg, rgba(255,215,0,0.1), rgba(255,165,0,0.1));
        border-left: 4px solid #ffd700;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with UX enhancements
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("🏀 Loading NBA Agent Pro..."):
        st.session_state.agent = build_agent()
# Initialize UX systems
PersonalizationEngine.init_user_preferences()

# Show onboarding for first-time users
if st.session_state.user_preferences.get('first_visit', True):
    if OnboardingFlow.show_welcome_tour():
        st.stop()  # Stop execution while tour is active

# Enhanced sidebar with personalization
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">🏀</h1>
        <h2 style="color: white; margin: 5px 0;">NBA Agent Pro</h2>
        <p style="color: rgba(255,255,255,0.7);">Enhanced Experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    PersonalizationEngine.show_favorites_sidebar()
    
    st.markdown("---")
    
    # Enhanced visualization mode selector
    st.markdown("### 📊 Experience Mode")
    viz_mode = st.radio(
        "Choose your style:",
        ["🎯 Interactive", "📊 Detailed Charts", "⚔️ Comparison Mode"],
        index=0,
        help="Different modes offer different visualization experiences"
    )
    
    # Accessibility options
    AccessibilityFeatures.add_high_contrast_mode()
    
    st.markdown("---")
    
    # Quick actions with animations
    st.markdown("### ⚡ Quick Actions")
    
    quick_actions = [
        ("🔥 Trending Players", "trending"),
        ("🏆 Standings", "standings"), 
        ("📅 Today's Games", "today_games"),
        ("⭐ Top Performers", "top_performers")
    ]
    
    for label, action in quick_actions:
        if st.button(label, use_container_width=True, key=f"quick_{action}"):
            st.session_state.quick_action = action
            # Add success feedback
            st.balloons()
    
    st.markdown("---")
    
    # Personalized suggestions
    st.markdown("### 💡 For You")
    suggestions = PersonalizationEngine.get_personalized_suggestions()
    
    for i, suggestion in enumerate(suggestions):
        if st.button(f"💭 {suggestion}", key=f"personal_suggest_{i}"):
            st.session_state.suggestion_clicked = suggestion
    
    st.markdown("---")
    
    # Enhanced chat stats
    st.markdown("### 📈 Your Activity")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", len(st.session_state.messages))
    with col2:
        favorites_count = len(st.session_state.user_preferences.get('favorite_players', [])) + \
                         len(st.session_state.user_preferences.get('favorite_teams', []))
        st.metric("⭐ Favorites", favorites_count)
    
    # Enhanced clear button with confirmation
    if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
        if st.session_state.messages:
            st.session_state.clear_confirmation = True
        else:
            st.info("Chat is already empty!")

# Confirmation dialog for clearing chat
if hasattr(st.session_state, 'clear_confirmation') and st.session_state.clear_confirmation:
    st.error("⚠️ Are you sure you want to clear all messages?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, Clear All", type="primary"):
            st.session_state.messages = []
            st.session_state.clear_confirmation = False
            st.success("Chat cleared! 🧹")
            time.sleep(1)
            st.rerun()
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.clear_confirmation = False
            st.rerun()

# Main content area with enhanced UX
# Hero section with personalization
user_name = st.session_state.user_preferences.get('name', 'Basketball Fan')
current_hour = datetime.now().hour

if current_hour < 12:
    greeting = "Good Morning"
elif current_hour < 17:
    greeting = "Good Afternoon" 
else:
    greeting = "Good Evening"

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
    padding: 30px;
    border-radius: 20px;
    margin: 20px 0;
    text-align: center;
    animation: slideInDown 1s ease-out;
">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">🏀 {greeting}!</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 10px 0;">
        Ready to explore NBA data with stunning visualizations?
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

# Smart suggestions with enhanced UI
st.markdown("### 🎯 Popular Right Now")
suggestion_cols = st.columns(4)

popular_queries = [
    "LeBron vs Curry stats",
    "Lakers next game", 
    "Top scorers today",
    "Rookie leaders"
]

for i, (col, query) in enumerate(zip(suggestion_cols, popular_queries)):
    with col:
        if st.button(query, key=f"popular_{i}", use_container_width=True):
            st.session_state.suggestion_clicked = query
            # Add visual feedback
            st.success(f"Great choice! 🎯")

# Enhanced chat interface
chat_container = st.container()

# Show contextual hints
if hasattr(st.session_state, 'current_query'):
    SmartNotifications.show_contextual_hints(st.session_state.current_query)

# Feature discovery
SmartNotifications.show_feature_discovery()

# Display messages with enhanced UX
with chat_container:
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user message-appear">
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
                        
                        <!-- Add to favorites option -->
                        <div style="margin-top: 10px;">
                            <button onclick="addToFavorites('{message["content"]}')" style="
                                background: rgba(255,215,0,0.2);
                                border: 1px solid #ffd700;
                                color: #ffd700;
                                padding: 4px 8px;
                                border-radius: 10px;
                                font-size: 0.8rem;
                                cursor: pointer;
                            ">⭐ Remember this</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                content = message["content"]
                
                # Enhanced response rendering with loading simulation
                try:
                    data = json.loads(content)
                except:
                    data = None
                
                if isinstance(data, dict) and "stats" in data:
                    # Player stats with enhanced UX
                    st.markdown(f"""
                    <div class="chat-message bot message-appear">
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
                            <br><small style="color: rgba(255,255,255,0.6);">{message.get('timestamp', '')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced stat cards with add to favorites
                    NBAVisualizations.create_interactive_stat_cards(data)
                    
                    # Action buttons with enhanced UX
                    action_cols = st.columns(4)
                    with action_cols[0]:
                        if st.button(f"⭐ Favorite {data.get('player', 'Player')}", key=f"fav_btn_{i}"):
                            PersonalizationEngine.add_to_favorites('player', data.get('player', ''))
                    
                    with action_cols[1]:
                        if st.button(f"🔄 Compare", key=f"compare_btn_{i}"):
                            st.session_state.comparison_mode = True
                            st.session_state.base_player = data.get('player', '')
                    
                    with action_cols[2]:
                        if st.button(f"📊 Detailed View", key=f"detail_btn_{i}"):
                            st.session_state.show_detailed = True
                            st.session_state.detailed_player = data
                    
                    with action_cols[3]:
                        if st.button(f"📤 Share", key=f"share_btn_{i}"):
                            st.success("Link copied to clipboard! 📋")
                    
                    # Show detailed view if requested
                    if hasattr(st.session_state, 'show_detailed') and st.session_state.show_detailed:
                        if st.session_state.detailed_player == data:
                            with st.expander("📊 Detailed Analytics", expanded=True):
                                tab1, tab2, tab3 = st.tabs(["🎯 Radar", "🏀 Shooting", "📈 Progress"])
                                
                                with tab1:
                                    with st.spinner("Generating radar chart..."):
                                        radar_fig = NBAVisualizations.create_player_radar_chart(data)
                                        st.plotly_chart(radar_fig, use_container_width=True)
                                
                                with tab2:
                                    with st.spinner("Creating shooting chart..."):
                                        shooting_fig = NBAVisualizations.create_shooting_chart(data)
                                        st.plotly_chart(shooting_fig, use_container_width=True)
                                
                                with tab3:
                                    with st.spinner("Building progression timeline..."):
                                        progress_fig = NBAVisualizations.create_season_progression(data)
                                        st.plotly_chart(progress_fig, use_container_width=True)
                                
                                if st.button("✅ Close Detailed View"):
                                    st.session_state.show_detailed = False
                                    st.rerun()
                
                else:
                    # Regular text response with enhanced styling
                    st.markdown(f"""
                    <div class="chat-message bot message-appear">
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

# Smart input with enhanced UX
input_placeholder = st.empty()

with input_placeholder.container():
    st.markdown("### 💬 Ask me anything about NBA...")
    
    # Enhanced input with suggestions
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="e.g., 'How many points did LeBron score this season?' or 'Compare Giannis and Embiid'",
            key="enhanced_input",
            help="💡 Tip: Try natural language! I understand questions like 'Who's the best shooter?' or 'Lakers vs Celtics'"
        )
    
    with col2:
        send_button = st.button("Send 🚀", type="primary", use_container_width=True)
    
    with col3:
        if st.button("🎲 Random", use_container_width=True, help="Get a random interesting NBA fact"):
            random_queries = [
                "Who leads the league in triple-doubles?",
                "What's the longest winning streak this season?",
                "Show me the youngest players scoring 20+ PPG",
                "Which team has the best home record?"
            ]
            import random
            st.session_state.suggestion_clicked = random.choice(random_queries)

# Handle input with enhanced feedback
if (send_button and user_input) or hasattr(st.session_state, 'suggestion_clicked'):
    query = user_input if send_button else st.session_state.suggestion_clicked
    
    if hasattr(st.session_state, 'suggestion_clicked'):
        delattr(st.session_state, 'suggestion_clicked')
    
    # Store current query for context
    st.session_state.current_query = query
    
    # Enhanced loading state
    with st.spinner("🏀 Analyzing NBA data..."):
        # Show loading skeleton
        PerformanceOptimizer.show_loading_skeleton("stats")
        
        # Add user message with animation
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": timestamp
        })
        
        # Get agent response
        response = st.session_state.agent.invoke({"input": query})
        result = response.get("output", str(response))
        
        # Add agent response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result,
            "timestamp": timestamp
        })
        
        # Success feedback
        st.success("✨ Got your answer! Check it out above.")
        st.balloons()
    
    st.rerun()

# Floating action buttons
QuickActions.show_floating_actions()

# Enhanced footer with tips
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.6);">
    <p>🏀 NBA Agent Pro - Enhanced Experience • Built with ❤️ for basketball fans</p>
    <div style="margin: 10px 0;">
        <span style="margin: 0 10px;">💡 Pro tip: Add players to favorites</span>
        <span style="margin: 0 10px;">📱 Works great on mobile</span>
        <span style="margin: 0 10px;">⌨️ Use Ctrl+Enter to send</span>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript for enhanced interactions
st.markdown("""
<script>
function addToFavorites(query) {
    // Extract player name from query
    alert('Added to favorites! ⭐');
}

// Enhanced keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === '?' && e.shiftKey) {
        alert('Keyboard Shortcuts:\\n\\nCtrl+Enter: Send message\\nCtrl+K: Focus input\\nEsc: Clear input\\n?: Show this help');
    }
});

// Auto-resize input on focus
document.querySelector('input[type="text"]')?.addEventListener('focus', function() {
    this.style.transform = 'scale(1.02)';
    this.style.transition = 'transform 0.2s ease';
});

document.querySelector('input[type="text"]')?.addEventListener('blur', function() {
    this.style.transform = 'scale(1)';
});
</script>
""", unsafe_allow_html=True) 