#!/usr/bin/env python3
"""
NBA Agent Visualization Demo
Showcases the enhanced visualization capabilities
"""

import streamlit as st
import json
from visualizations import NBAVisualizations, LiveGameWidget, add_enhanced_css
from smart_interface import SmartInterface, QueryOptimizer
import plotly.graph_objects as go
from datetime import datetime
import time

def main():
    st.set_page_config(
        page_title="🏀 NBA Agent - Visualization Demo",
        page_icon="🏀",
        layout="wide"
    )
    
    add_enhanced_css()
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); border-radius: 20px; margin: 1rem 0;">
        <h1 style="color: white; margin: 0;">🏀 NBA Agent Visualization Demo</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">
            Experience the future of NBA data visualization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo navigation
    demo_section = st.selectbox(
        "Choose a demo section:",
        [
            "🎯 Interactive Player Stats",
            "📊 Advanced Charts",
            "🔍 Smart Interface",
            "⚡ Live Game Experience",
            "🤖 AI-Powered Insights",
            "📱 Mobile-Optimized Views"
        ]
    )
    
    if demo_section == "🎯 Interactive Player Stats":
        demo_interactive_stats()
    elif demo_section == "📊 Advanced Charts":
        demo_advanced_charts()
    elif demo_section == "🔍 Smart Interface":
        demo_smart_interface()
    elif demo_section == "⚡ Live Game Experience":
        demo_live_experience()
    elif demo_section == "🤖 AI-Powered Insights":
        demo_ai_insights()
    elif demo_section == "📱 Mobile-Optimized Views":
        demo_mobile_views()

def demo_interactive_stats():
    """Demo interactive player statistics"""
    st.markdown("## 🎯 Interactive Player Statistics")
    st.markdown("Experience player stats like never before with interactive cards and real-time comparisons.")
    
    # Mock player data
    lebron_data = {
        "player": "LeBron James",
        "season": "2024-25",
        "stats": {
            "ppg": 25.8,
            "apg": 8.2,
            "rpg": 7.1,
            "spg": 1.3,
            "bpg": 0.6,
            "fg_pct": 52.4,
            "fg3_pct": 35.8,
            "ft_pct": 75.2,
            "games_played": 42
        }
    }
    
    curry_data = {
        "player": "Stephen Curry",
        "season": "2024-25", 
        "stats": {
            "ppg": 28.4,
            "apg": 5.1,
            "rpg": 4.3,
            "spg": 1.8,
            "bpg": 0.4,
            "fg_pct": 45.8,
            "fg3_pct": 42.1,
            "ft_pct": 91.3,
            "games_played": 40
        }
    }
    
    # Interactive stat cards
    st.markdown("### 🃏 Interactive Stat Cards")
    selected_player = st.selectbox("Select a player:", ["LeBron James", "Stephen Curry"])
    
    if selected_player == "LeBron James":
        NBAVisualizations.create_interactive_stat_cards(lebron_data)
    else:
        NBAVisualizations.create_interactive_stat_cards(curry_data)
    
    # Comparison mode
    st.markdown("### ⚔️ Player Comparison")
    if st.button("🔄 Compare LeBron vs Curry"):
        comparison_fig = NBAVisualizations.create_stat_comparison_chart(lebron_data, curry_data)
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        st.markdown("""
        **Key Insights:**
        - 🏀 Curry leads in scoring and 3-point shooting
        - 🤝 LeBron dominates in assists and rebounds  
        - 🎯 Both are elite performers in their specialties
        """)

def demo_advanced_charts():
    """Demo advanced chart visualizations"""
    st.markdown("## 📊 Advanced Chart Visualizations")
    st.markdown("Dive deep into player performance with sophisticated data visualizations.")
    
    # Mock data
    giannis_data = {
        "player": "Giannis Antetokounmpo",
        "season": "2024-25",
        "stats": {
            "ppg": 31.2,
            "apg": 6.8,
            "rpg": 11.3,
            "spg": 1.2,
            "bpg": 1.4,
            "fg_pct": 58.9,
            "fg3_pct": 28.4,
            "ft_pct": 65.8,
            "games_played": 38
        }
    }
    
    chart_type = st.selectbox(
        "Choose chart type:",
        ["🎯 Radar Chart", "🏀 Shooting Chart", "📈 Season Progression", "🗺️ Performance Heatmap"]
    )
    
    if chart_type == "🎯 Radar Chart":
        st.markdown("### Player Performance Radar")
        radar_fig = NBAVisualizations.create_player_radar_chart(giannis_data)
        st.plotly_chart(radar_fig, use_container_width=True)
        
        st.info("💡 The radar chart shows how Giannis performs across all major statistical categories, normalized to league standards.")
    
    elif chart_type == "🏀 Shooting Chart":
        st.markdown("### Basketball Court Shooting Analysis")
        shooting_fig = NBAVisualizations.create_shooting_chart(giannis_data)
        st.plotly_chart(shooting_fig, use_container_width=True)
        
        st.info("🎯 Visual representation of shooting efficiency from different court areas.")
    
    elif chart_type == "📈 Season Progression":
        st.markdown("### Season Performance Timeline")
        progression_fig = NBAVisualizations.create_season_progression(giannis_data)
        st.plotly_chart(progression_fig, use_container_width=True)
        
        st.info("📊 Track performance trends and consistency throughout the season.")
    
    elif chart_type == "🗺️ Performance Heatmap":
        st.markdown("### Team Performance Heatmap")
        
        # Mock team data
        teams_data = [
            {"team": "Bucks", "wins": 28, "losses": 14, "rank": 2},
            {"team": "Celtics", "wins": 32, "losses": 10, "rank": 1},
            {"team": "76ers", "wins": 24, "losses": 18, "rank": 5},
            {"team": "Heat", "wins": 22, "losses": 20, "rank": 7}
        ]
        
        heatmap_fig = NBAVisualizations.create_team_heatmap(teams_data)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        st.info("🔥 Compare multiple teams across key performance metrics.")

def demo_smart_interface():
    """Demo smart interface features"""
    st.markdown("## 🔍 Smart Interface Features")
    st.markdown("Experience AI-powered query assistance and intelligent autocomplete.")
    
    interface_feature = st.selectbox(
        "Try these smart features:",
        ["🎯 Query Builder", "🤖 Auto-complete", "💡 Smart Suggestions", "🔍 Intent Analysis"]
    )
    
    if interface_feature == "🎯 Query Builder":
        st.markdown("### Interactive Query Builder")
        st.markdown("Build complex queries without typing!")
        
        built_query = SmartInterface.create_smart_query_builder()
        if built_query:
            st.success(f"Generated query: **{built_query}**")
            st.markdown("🚀 This query would now be sent to the NBA Agent for processing!")
    
    elif interface_feature == "🤖 Auto-complete":
        st.markdown("### Intelligent Auto-complete")
        st.markdown("Type partial names and get instant suggestions.")
        
        col1, col2 = st.columns(2)
        with col1:
            player_input = SmartInterface.create_autocomplete_input("Player Name:", "demo_player", "player")
        with col2:
            team_input = SmartInterface.create_autocomplete_input("Team Name:", "demo_team", "team")
        
        if player_input or team_input:
            st.success("✨ Auto-complete makes data entry fast and error-free!")
    
    elif interface_feature == "💡 Smart Suggestions":
        st.markdown("### Contextual Query Suggestions")
        test_input = st.text_input("Type something NBA-related:", placeholder="LeBron points...")
        
        suggestions = SmartInterface.generate_smart_suggestions(test_input)
        st.markdown("**Smart suggestions based on your input:**")
        
        for i, suggestion in enumerate(suggestions):
            st.markdown(f"💭 {suggestion}")
    
    elif interface_feature == "🔍 Intent Analysis":
        st.markdown("### AI Query Intent Analysis")
        test_query = st.text_input("Enter a query to analyze:", 
                                 placeholder="Compare LeBron and Curry points this season")
        
        if test_query:
            intent = SmartInterface.parse_query_intent(test_query)
            
            st.json({
                "Query Type": intent["type"],
                "Detected Players": intent["entities"]["players"],
                "Detected Teams": intent["entities"]["teams"],
                "Detected Stats": intent["entities"]["stats"],
                "Is Comparison": intent["comparison"],
                "Confidence": f"{intent['confidence']:.1%}"
            })
            
            enhanced = QueryOptimizer.enhance_query(test_query)
            if enhanced != test_query:
                st.info(f"🔧 Enhanced query: **{enhanced}**")

def demo_live_experience():
    """Demo live game experience"""
    st.markdown("## ⚡ Live Game Experience")
    st.markdown("Experience NBA games in real-time with dynamic visualizations.")
    
    # Live game widget
    st.markdown("### 🔴 Live Game Widget")
    LiveGameWidget.create_live_score_widget({})
    
    # Simulated live stats
    st.markdown("### 📊 Live Player Performance")
    
    if st.button("🔄 Simulate Live Update"):
        # Create animated progress bars
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏀 LeBron James**")
            points_progress = st.progress(0)
            for i in range(28):
                points_progress.progress((i + 1) / 40)
                time.sleep(0.05)
            st.markdown("28 PTS • 7 REB • 6 AST")
        
        with col2:
            st.markdown("**🎯 Stephen Curry**")
            points_progress = st.progress(0)
            for i in range(32):
                points_progress.progress((i + 1) / 40)
                time.sleep(0.05)
            st.markdown("32 PTS • 4 REB • 8 AST")
        
        with col3:
            st.markdown("**⚡ Giannis**")
            points_progress = st.progress(0)
            for i in range(35):
                points_progress.progress((i + 1) / 40)
                time.sleep(0.05)
            st.markdown("35 PTS • 12 REB • 5 AST")
    
    # Game momentum chart
    st.markdown("### 📈 Game Momentum")
    
    # Mock momentum data
    import numpy as np
    time_points = list(range(48))  # 48 minutes
    team_a_momentum = 50 + np.cumsum(np.random.normal(0, 2, 48))
    team_b_momentum = 100 - team_a_momentum
    
    momentum_fig = go.Figure()
    momentum_fig.add_trace(go.Scatter(
        x=time_points, y=team_a_momentum,
        mode='lines', name='Lakers',
        line=dict(color='#552583', width=3),
        fill='tonexty'
    ))
    momentum_fig.add_trace(go.Scatter(
        x=time_points, y=team_b_momentum,
        mode='lines', name='Warriors',
        line=dict(color='#FFC72C', width=3)
    ))
    
    momentum_fig.update_layout(
        title="Game Momentum Over Time",
        xaxis_title="Minutes",
        yaxis_title="Momentum %",
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(momentum_fig, use_container_width=True)

def demo_ai_insights():
    """Demo AI-powered insights"""
    st.markdown("## 🤖 AI-Powered Insights")
    st.markdown("Discover hidden patterns and get intelligent recommendations.")
    
    insight_type = st.selectbox(
        "Choose insight type:",
        ["🔮 Performance Predictions", "📊 Statistical Anomalies", "🏆 Award Predictions", "📈 Trend Analysis"]
    )
    
    if insight_type == "🔮 Performance Predictions":
        st.markdown("### AI Performance Predictions")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.1)); 
                   padding: 20px; border-radius: 15px; margin: 20px 0;">
            <h4>🤖 AI Analysis: LeBron James</h4>
            <p><strong>Predicted next 10 games:</strong></p>
            <ul>
                <li>🏀 <strong>Points:</strong> 26.2 ± 4.1 (based on recent form and matchups)</li>
                <li>🤝 <strong>Assists:</strong> 7.8 ± 2.3 (trending upward)</li>
                <li>🔄 <strong>Rebounds:</strong> 7.5 ± 1.8 (consistent performance)</li>
            </ul>
            <p><strong>Key factors:</strong> Rest days, opponent defensive rating, home/away splits</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif insight_type == "📊 Statistical Anomalies":
        st.markdown("### Unusual Statistical Patterns")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(247,147,30,0.1)); 
                   padding: 20px; border-radius: 15px; margin: 20px 0;">
            <h4>🔍 Anomaly Detection</h4>
            <p><strong>Unusual patterns detected:</strong></p>
            <ul>
                <li>⚠️ <strong>Giannis 3P%:</strong> 38% in last 5 games (season avg: 28%)</li>
                <li>📈 <strong>Curry assists:</strong> 8.2 APG increase vs last month</li>
                <li>🔻 <strong>Embiid minutes:</strong> 5 min decrease, possible load management</li>
            </ul>
            <p><strong>Recommendation:</strong> Monitor these trends for fantasy/betting insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif insight_type == "🏆 Award Predictions":
        st.markdown("### 2024-25 Award Predictions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: rgba(255,215,0,0.2); border-radius: 15px;">
                <h4>🏆 MVP Race</h4>
                <p><strong>1. Giannis</strong> (35%)</p>
                <p><strong>2. Luka</strong> (28%)</p>
                <p><strong>3. Tatum</strong> (18%)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: rgba(192,192,192,0.2); border-radius: 15px;">
                <h4>🛡️ DPOY Race</h4>
                <p><strong>1. Gobert</strong> (42%)</p>
                <p><strong>2. Bam</strong> (25%)</p>
                <p><strong>3. Draymond</strong> (15%)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: rgba(205,127,50,0.2); border-radius: 15px;">
                <h4>🌟 ROY Race</h4>
                <p><strong>1. Wembanyama</strong> (65%)</p>
                <p><strong>2. Chet</strong> (22%)</p>
                <p><strong>3. Brandon Miller</strong> (8%)</p>
            </div>
            """, unsafe_allow_html=True)

def demo_mobile_views():
    """Demo mobile-optimized views"""
    st.markdown("## 📱 Mobile-Optimized Experience")
    st.markdown("See how the interface adapts for mobile users.")
    
    # Simulate mobile view
    st.markdown("### 📱 Mobile Interface Preview")
    
    mobile_col = st.columns([1, 2, 1])[1]  # Center column for mobile simulation
    
    with mobile_col:
        st.markdown("""
        <div style="border: 3px solid #333; border-radius: 25px; padding: 20px; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: white; margin: 0;">🏀 NBA Agent</h3>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 15px; margin: 10px 0;">
                <p style="color: white; margin: 0;"><strong>You:</strong> LeBron stats?</p>
            </div>
            
            <div style="background: rgba(255,107,53,0.2); padding: 15px; border-radius: 15px; margin: 10px 0;">
                <p style="color: white; margin: 0;"><strong>🏀 Agent:</strong> LeBron James 2024-25:</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0;">
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;">
                        <div style="color: #ffd700; font-size: 1.5rem; font-weight: bold;">25.8</div>
                        <div style="color: white; font-size: 0.8rem;">PPG</div>
                    </div>
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;">
                        <div style="color: #ffd700; font-size: 1.5rem; font-weight: bold;">8.2</div>
                        <div style="color: white; font-size: 0.8rem;">APG</div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 5px; margin: 15px 0;">
                <button style="flex: 1; background: rgba(255,255,255,0.2); border: none; 
                              padding: 10px; border-radius: 10px; color: white;">Compare</button>
                <button style="flex: 1; background: rgba(255,255,255,0.2); border: none; 
                              padding: 10px; border-radius: 10px; color: white;">Details</button>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; 
                       display: flex; align-items: center; gap: 10px;">
                <span style="color: white;">Ask me anything...</span>
                <div style="margin-left: auto; background: #ff6b35; width: 40px; height: 40px; 
                           border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    🎤
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Mobile-First Features")
    st.markdown("""
    **Optimizations for mobile users:**
    - 👆 Touch-friendly interface with large buttons
    - 📱 Responsive design that adapts to screen size
    - ⚡ Fast loading with progressive data display
    - 🎤 Voice input for hands-free operation
    - 📊 Simplified charts optimized for small screens
    - 💾 Offline capability for cached data
    """)

if __name__ == "__main__":
    main() 