import streamlit as st
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class OnboardingFlow:
    """Enhanced onboarding experience for new users"""
    
    @staticmethod
    def show_welcome_tour():
        """Interactive welcome tour for first-time users"""
        # Use the same first_visit logic as the rest of the app
        if st.session_state.user_preferences.get('first_visit', True):
            with st.container():
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 20px;
                    text-align: center;
                    margin: 20px 0;
                    border: 2px solid rgba(255,255,255,0.2);
                    animation: slideInDown 1s ease-out;
                ">
                    <h1 style="color: white; margin: 0;">🏀 Welcome to NBA Agent Pro!</h1>
                    <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 15px 0;">
                        Your AI-powered basketball companion with stunning visualizations
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
                
                # Tour steps
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div style="
                        background: rgba(255,107,53,0.2);
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
                        <h3 style="color: white; margin: 0;">Step 1: Ask Anything</h3>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            Type any NBA question or use our smart suggestions
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="
                        background: rgba(102,126,234,0.2);
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                        <h3 style="color: white; margin: 0;">Step 2: Explore</h3>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            Get beautiful charts and interactive visualizations
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div style="
                        background: rgba(255,215,0,0.2);
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🏆</div>
                        <h3 style="color: white; margin: 0;">Step 3: Discover</h3>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            Find insights and compare your favorite players
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Quick start examples
                st.markdown("### 🚀 Try these examples to get started:")
                
                example_cols = st.columns(2)
                with example_cols[0]:
                    if st.button("🏀 'What are LeBron's stats this season?'", use_container_width=True):
                        st.session_state.suggestion_clicked = "What are LeBron's stats this season?"
                        st.session_state.user_preferences['first_visit'] = False
                        st.rerun()
                
                with example_cols[1]:
                    if st.button("📅 'When do the Warriors play next?'", use_container_width=True):
                        st.session_state.suggestion_clicked = "When do the Warriors play next?"
                        st.session_state.user_preferences['first_visit'] = False
                        st.rerun()
                
                # Skip tour option
                skip_col1, skip_col2, skip_col3 = st.columns([1, 1, 1])
                with skip_col2:
                    if st.button("Skip Tour →", type="secondary", use_container_width=True):
                        st.session_state.user_preferences['first_visit'] = False
                        st.rerun()
                
                return True
        
        return False

class PersonalizationEngine:
    """User personalization and preferences"""
    
    @staticmethod
    def init_user_preferences():
        """Initialize user preferences"""
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {
                'favorite_teams': [],
                'favorite_players': [],
                'recent_queries': [],
                'preferred_stats': ['ppg', 'apg', 'rpg'],
                'theme': 'dark',
                'visualization_mode': 'interactive',
                'query_history': [],
                'first_visit': True
            }
    
    @staticmethod
    def add_to_favorites(item_type: str, item_name: str):
        """Add player or team to favorites"""
        PersonalizationEngine.init_user_preferences()
        
        if item_type == 'player':
            favorites = st.session_state.user_preferences['favorite_players']
        else:
            favorites = st.session_state.user_preferences['favorite_teams']
        
        if item_name not in favorites:
            favorites.append(item_name)
            st.success(f"Added {item_name} to favorites! ⭐")
    
    @staticmethod
    def get_personalized_suggestions() -> List[str]:
        """Get personalized query suggestions based on user preferences"""
        PersonalizationEngine.init_user_preferences()
        prefs = st.session_state.user_preferences
        
        suggestions = []
        
        # Suggestions based on favorite players
        for player in prefs['favorite_players'][:2]:
            suggestions.append(f"How is {player} performing this season?")
        
        # Suggestions based on favorite teams
        for team in prefs['favorite_teams'][:2]:
            suggestions.append(f"What's {team}'s next game?")
        
        # Time-based suggestions
        current_hour = datetime.now().hour
        if 18 <= current_hour <= 23:  # Evening
            suggestions.extend([
                "What games are on tonight?",
                "Show me today's top performers"
            ])
        elif 9 <= current_hour <= 17:  # Daytime
            suggestions.extend([
                "Who are the scoring leaders?",
                "Show me yesterday's highlights"
            ])
        
        # Fallback suggestions
        if not suggestions:
            suggestions = [
                "What are LeBron's stats this season?",
                "Who leads the league in assists?",
                "When do the Lakers play next?",
                "Compare Giannis and Embiid"
            ]
        
        return suggestions[:4]
    
    @staticmethod
    def show_favorites_sidebar():
        """Show user's favorites in sidebar"""
        PersonalizationEngine.init_user_preferences()
        prefs = st.session_state.user_preferences
        
        if prefs['favorite_players'] or prefs['favorite_teams']:
            st.markdown("### ⭐ Your Favorites")
            
            if prefs['favorite_players']:
                st.markdown("**👤 Players:**")
                for player in prefs['favorite_players']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"📊 {player}", key=f"fav_player_{player}"):
                            st.session_state.quick_query = f"Show me {player}'s stats"
                    with col2:
                        if st.button("×", key=f"remove_player_{player}", help="Remove"):
                            prefs['favorite_players'].remove(player)
                            st.rerun()
            
            if prefs['favorite_teams']:
                st.markdown("**🏀 Teams:**")
                for team in prefs['favorite_teams']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"📅 {team}", key=f"fav_team_{team}"):
                            st.session_state.quick_query = f"When do the {team} play next?"
                    with col2:
                        if st.button("×", key=f"remove_team_{team}", help="Remove"):
                            prefs['favorite_teams'].remove(team)
                            st.rerun()

class PerformanceOptimizer:
    """Performance enhancements and loading states"""
    
    @staticmethod
    def show_loading_skeleton(content_type: str = "general"):
        """Show skeleton loading animation"""
        if content_type == "stats":
            st.markdown("""
            <div style="animation: pulse 1.5s ease-in-out infinite;">
                <div style="
                    background: rgba(255,255,255,0.1);
                    height: 60px;
                    border-radius: 10px;
                    margin: 10px 0;
                "></div>
                <div style="display: flex; gap: 10px;">
                    <div style="
                        background: rgba(255,255,255,0.1);
                        height: 80px;
                        border-radius: 10px;
                        flex: 1;
                    "></div>
                    <div style="
                        background: rgba(255,255,255,0.1);
                        height: 80px;
                        border-radius: 10px;
                        flex: 1;
                    "></div>
                    <div style="
                        background: rgba(255,255,255,0.1);
                        height: 80px;
                        border-radius: 10px;
                        flex: 1;
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif content_type == "chart":
            st.markdown("""
            <div style="animation: pulse 1.5s ease-in-out infinite;">
                <div style="
                    background: rgba(255,255,255,0.1);
                    height: 300px;
                    border-radius: 15px;
                    margin: 20px 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="color: rgba(255,255,255,0.5); font-size: 1.2rem;">
                        📊 Generating visualization...
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def progressive_data_loading(data_chunks: List, render_func):
        """Load and render data progressively"""
        placeholder = st.empty()
        
        for i, chunk in enumerate(data_chunks):
            progress_percent = (i + 1) / len(data_chunks)
            
            with placeholder.container():
                # Show progress
                st.progress(progress_percent)
                st.write(f"Loading... {int(progress_percent * 100)}%")
                
                # Render available data
                render_func(chunk)
                
                # Small delay for demonstration
                time.sleep(0.5)
        
        # Clear progress indicator
        placeholder.empty()

class AccessibilityFeatures:
    """Accessibility and inclusive design features"""
    
    @staticmethod
    def add_keyboard_shortcuts():
        """Add keyboard navigation support"""
        st.markdown("""
        <div style="
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 0.8rem;
            z-index: 1000;
            opacity: 0.7;
        ">
            <strong>⌨️ Shortcuts:</strong><br>
            <kbd>Ctrl</kbd>+<kbd>Enter</kbd> Send<br>
            <kbd>Ctrl</kbd>+<kbd>K</kbd> Focus search<br>
            <kbd>Esc</kbd> Clear input
        </div>
        
        <script>
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                // Trigger send button
                const sendBtn = document.querySelector('[data-testid="baseButton-secondary"]');
                if (sendBtn) sendBtn.click();
            }
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                // Focus on input
                const input = document.querySelector('input[type="text"]');
                if (input) input.focus();
            }
            if (e.key === 'Escape') {
                // Clear input
                const input = document.querySelector('input[type="text"]');
                if (input) input.value = '';
            }
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_high_contrast_mode():
        """Add high contrast mode option"""
        if st.sidebar.checkbox("🔆 High Contrast Mode"):
            st.markdown("""
            <style>
            .stApp {
                filter: contrast(1.5) brightness(1.2);
            }
            .chat-message {
                border: 2px solid white !important;
            }
            </style>
            """, unsafe_allow_html=True)

class SmartNotifications:
    """Contextual notifications and helpful hints"""
    
    @staticmethod
    def show_contextual_hints(query: str = ""):
        """Show helpful hints based on context"""
        hints = []
        
        if not query:
            hints.append("💡 Try asking about your favorite player's stats!")
        elif "compare" in query.lower():
            hints.append("📊 Tip: Comparison charts work best with 2-3 players")
        elif any(word in query.lower() for word in ["schedule", "next", "game"]):
            hints.append("📅 Pro tip: You can ask for multiple games ahead!")
        elif any(word in query.lower() for word in ["stats", "points", "assists"]):
            hints.append("🎯 Try switching to 'Detailed Charts' mode for deeper insights")
        
        if hints:
            st.info(hints[0])
    
    @staticmethod
    def show_feature_discovery():
        """Help users discover new features"""
        features = [
            "🎯 Did you know? You can compare any two players by saying 'compare X and Y'",
            "📱 Tip: This app works great on mobile - try it on your phone!",
            "⭐ Pro tip: Add players to favorites for quick access",
            "🎨 Try different visualization modes in the sidebar",
            "🔍 Use the query builder for complex questions"
        ]
        
        if 'feature_tip_index' not in st.session_state:
            st.session_state.feature_tip_index = 0
        
        # Show a rotating tip every few interactions
        message_count = len(st.session_state.get('messages', []))
        if message_count > 0 and message_count % 3 == 0:
            tip = features[st.session_state.feature_tip_index % len(features)]
            st.sidebar.info(tip)
            st.session_state.feature_tip_index += 1

class MicroInteractions:
    """Small delightful interactions and feedback"""
    
    @staticmethod
    def add_success_animations():
        """Add success animations for completed actions"""
        st.markdown("""
        <style>
        @keyframes celebration {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .success-pulse {
            animation: celebration 0.6s ease-in-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .message-appear {
            animation: slideInUp 0.5s ease-out;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_hover_effects():
        """Enhanced hover effects for better interactivity"""
        st.markdown("""
        <style>
        .stButton > button {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            transition: all 0.1s;
        }
        
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.5);
            border-color: #ffd700;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(255, 215, 0, 0.2);
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)

class QuickActions:
    """Quick action shortcuts and floating action buttons"""
    
    @staticmethod
    def show_floating_actions():
        """Show floating action buttons for quick access"""
        st.markdown("""
        <div style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        ">
            <button onclick="scrollToTop()" style="
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                ↑
            </button>
            
            <button onclick="clearChat()" style="
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(45deg, #ff6b35, #f7931e);
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                🗑️
            </button>
        </div>
        
        <script>
        function scrollToTop() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        
        function clearChat() {
            if (confirm('Clear chat history?')) {
                // This would need to be integrated with Streamlit's session state
                alert('Chat cleared!');
            }
        }
        </script>
        """, unsafe_allow_html=True)

def enhance_user_experience():
    """Apply all UX enhancements"""
    # Initialize all enhancement systems
    PersonalizationEngine.init_user_preferences()
    
    # Add CSS enhancements
    MicroInteractions.add_success_animations()
    MicroInteractions.add_hover_effects()
    
    # Add accessibility features
    AccessibilityFeatures.add_keyboard_shortcuts()
    
    # Show floating actions
    QuickActions.show_floating_actions()
    
    return True 