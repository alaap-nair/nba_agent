import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List
import json

class NBAVisualizations:
    """Enhanced NBA visualizations for better user experience"""
    
    @staticmethod
    def create_player_radar_chart(player_data: Dict) -> go.Figure:
        """Create a radar chart for player stats"""
        stats = player_data.get('stats', {})
        
        # Normalize stats to 0-100 scale for radar chart
        max_values = {
            'ppg': 35, 'apg': 12, 'rpg': 15, 'spg': 3, 'bpg': 3,
            'fg_pct': 60, 'fg3_pct': 50, 'ft_pct': 95
        }
        
        categories = ['Points/Game', 'Assists/Game', 'Rebounds/Game', 
                     'Steals/Game', 'Blocks/Game', 'FG%', '3P%', 'FT%']
        
        values = []
        stat_keys = ['ppg', 'apg', 'rpg', 'spg', 'bpg', 'fg_pct', 'fg3_pct', 'ft_pct']
        
        for i, key in enumerate(stat_keys):
            stat_value = stats.get(key, 0)
            if key.endswith('_pct'):
                normalized = min(stat_value, max_values[key])
            else:
                normalized = min((stat_value / max_values[key]) * 100, 100)
            values.append(normalized)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_data.get('player', 'Player'),
            line_color='rgb(255, 107, 53)',
            fillcolor='rgba(255, 107, 53, 0.25)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=20,
                    gridcolor='rgba(255, 255, 255, 0.3)',
                    linecolor='rgba(255, 255, 255, 0.3)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255, 255, 255, 0.3)',
                    linecolor='rgba(255, 255, 255, 0.3)'
                )
            ),
            showlegend=True,
            title=f"{player_data.get('player', 'Player')} - {player_data.get('season', '2024-25')} Stats",
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_stat_comparison_chart(player1_data: Dict, player2_data: Dict) -> go.Figure:
        """Create side-by-side stat comparison"""
        categories = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'FG%', '3P%', 'FT%']
        
        player1_stats = player1_data.get('stats', {})
        player2_stats = player2_data.get('stats', {})
        
        stat_keys = ['ppg', 'apg', 'rpg', 'spg', 'bpg', 'fg_pct', 'fg3_pct', 'ft_pct']
        
        player1_values = [player1_stats.get(key, 0) for key in stat_keys]
        player2_values = [player2_stats.get(key, 0) for key in stat_keys]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name=player1_data.get('player', 'Player 1'),
            x=categories,
            y=player1_values,
            marker_color='rgb(255, 107, 53)',
            text=player1_values,
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name=player2_data.get('player', 'Player 2'),
            x=categories,
            y=player2_values,
            marker_color='rgb(102, 126, 234)',
            text=player2_values,
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Player Comparison',
            xaxis_title='Statistics',
            yaxis_title='Value',
            barmode='group',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)')
        )
        
        return fig
    
    @staticmethod
    def create_shooting_chart(player_data: Dict) -> go.Figure:
        """Create a basketball court with shooting percentages"""
        # Basketball court coordinates (simplified)
        court_x = [-250, 250, 250, -250, -250]
        court_y = [-47.5, -47.5, 422.5, 422.5, -47.5]
        
        fig = go.Figure()
        
        # Draw court outline
        fig.add_trace(go.Scatter(
            x=court_x, y=court_y,
            mode='lines',
            line=dict(color='white', width=2),
            showlegend=False,
            name='Court'
        ))
        
        # Add three-point line (simplified arc)
        theta = np.linspace(-np.pi/2, np.pi/2, 50)
        three_point_x = 237.5 * np.cos(theta)
        three_point_y = 237.5 * np.sin(theta) + 53
        
        fig.add_trace(go.Scatter(
            x=three_point_x, y=three_point_y,
            mode='lines',
            line=dict(color='white', width=2),
            showlegend=False,
            name='3-Point Line'
        ))
        
        # Add shooting zones with percentages
        stats = player_data.get('stats', {})
        
        # Paint area (close range)
        fig.add_trace(go.Scatter(
            x=[0], y=[100],
            mode='markers+text',
            marker=dict(
                size=60,
                color=stats.get('fg_pct', 0),
                colorscale='RdYlGn',
                cmin=0, cmax=70,
                showscale=True,
                colorbar=dict(title="FG%", titlefont=dict(color='white'))
            ),
            text=f"Paint<br>{stats.get('fg_pct', 0):.1f}%",
            textposition='middle center',
            textfont=dict(color='white', size=12),
            showlegend=False
        ))
        
        # Three-point area
        fig.add_trace(go.Scatter(
            x=[0], y=[300],
            mode='markers+text',
            marker=dict(
                size=60,
                color=stats.get('fg3_pct', 0),
                colorscale='RdYlGn',
                cmin=0, cmax=50,
                showscale=False
            ),
            text=f"3-Point<br>{stats.get('fg3_pct', 0):.1f}%",
            textposition='middle center',
            textfont=dict(color='white', size=12),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"{player_data.get('player', 'Player')} Shooting Chart",
            xaxis=dict(
                range=[-300, 300],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="y",
                scaleratio=1
            ),
            yaxis=dict(
                range=[-100, 500],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            showlegend=False,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_season_progression(player_data: Dict) -> go.Figure:
        """Create a timeline showing season progression"""
        # Mock data for demonstration - in real app, this would come from game logs
        games = list(range(1, 21))  # First 20 games
        stats = player_data.get('stats', {})
        base_ppg = stats.get('ppg', 20)
        
        # Generate some realistic variation
        np.random.seed(42)
        points_per_game = base_ppg + np.random.normal(0, 5, 20)
        points_per_game = np.maximum(points_per_game, 0)  # No negative points
        
        # Calculate rolling average
        rolling_avg = pd.Series(points_per_game).rolling(window=5).mean()
        
        fig = go.Figure()
        
        # Individual game points
        fig.add_trace(go.Scatter(
            x=games,
            y=points_per_game,
            mode='markers',
            name='Game Points',
            marker=dict(color='rgb(255, 107, 53)', size=8),
            text=[f"Game {g}: {p:.1f} pts" for g, p in zip(games, points_per_game)],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        # Rolling average
        fig.add_trace(go.Scatter(
            x=games,
            y=rolling_avg,
            mode='lines',
            name='5-Game Average',
            line=dict(color='rgb(102, 126, 234)', width=3)
        ))
        
        # Season average line
        fig.add_hline(
            y=base_ppg,
            line_dash="dash",
            line_color="rgb(255, 215, 0)",
            annotation_text=f"Season Avg: {base_ppg:.1f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title=f"{player_data.get('player', 'Player')} Season Progression",
            xaxis_title='Game Number',
            yaxis_title='Points Per Game',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.3)')
        )
        
        return fig
    
    @staticmethod
    def create_team_heatmap(teams_data: List[Dict]) -> go.Figure:
        """Create a heatmap comparing multiple teams"""
        if not teams_data:
            return go.Figure()
        
        team_names = [team.get('team', f'Team {i}') for i, team in enumerate(teams_data)]
        stats_categories = ['Wins', 'Losses', 'Win %', 'Rank']
        
        # Create matrix of team stats
        heatmap_data = []
        for team in teams_data:
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            win_pct = wins / (wins + losses) if (wins + losses) > 0 else 0
            rank = team.get('rank', 15)
            
            heatmap_data.append([wins, losses, win_pct * 100, 31 - rank])  # Invert rank for coloring
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=stats_categories,
            y=team_names,
            colorscale='RdYlGn',
            text=[[f"{val:.1f}" for val in row] for row in heatmap_data],
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Team Performance Comparison',
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_interactive_stat_cards(player_data: Dict) -> None:
        """Create interactive stat cards with animations"""
        stats = player_data.get('stats', {})
        player_name = player_data.get('player', 'Player')
        
        # Create columns for stat cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; animation: slideInUp 0.5s ease-out;">
                <h3 style="color: #ff6b35; margin: 0;">🏀 POINTS</h3>
                <h1 style="color: white; margin: 5px 0; font-size: 2.5rem;">{stats.get('ppg', 0):.1f}</h1>
                <p style="color: #ccc; margin: 0;">per game</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; animation: slideInUp 0.6s ease-out;">
                <h3 style="color: #667eea; margin: 0;">🤝 ASSISTS</h3>
                <h1 style="color: white; margin: 5px 0; font-size: 2.5rem;">{stats.get('apg', 0):.1f}</h1>
                <p style="color: #ccc; margin: 0;">per game</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; animation: slideInUp 0.7s ease-out;">
                <h3 style="color: #ffd700; margin: 0;">🔄 REBOUNDS</h3>
                <h1 style="color: white; margin: 5px 0; font-size: 2.5rem;">{stats.get('rpg', 0):.1f}</h1>
                <p style="color: #ccc; margin: 0;">per game</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; animation: slideInUp 0.8s ease-out;">
                <h3 style="color: #28a745; margin: 0;">🎯 FG%</h3>
                <h1 style="color: white; margin: 5px 0; font-size: 2.5rem;">{stats.get('fg_pct', 0):.1f}%</h1>
                <p style="color: #ccc; margin: 0;">field goal</p>
            </div>
            """, unsafe_allow_html=True)

class LiveGameWidget:
    """Widget for displaying live game information"""
    
    @staticmethod
    def create_live_score_widget(game_data: Dict) -> None:
        """Create a live score widget"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 8px 16px rgba(255, 107, 53, 0.3);
            animation: pulse 2s infinite;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="text-align: center; flex: 1;">
                    <h3 style="color: white; margin: 0;">🏀 LIVE</h3>
                    <h2 style="color: white; margin: 5px 0;">LAL vs GSW</h2>
                    <p style="color: rgba(255,255,255,0.8); margin: 0;">Q3 8:42</p>
                </div>
                <div style="text-align: center; flex: 1;">
                    <h1 style="color: white; margin: 0; font-size: 3rem;">108</h1>
                    <p style="color: rgba(255,255,255,0.8);">Lakers</p>
                </div>
                <div style="text-align: center; flex: 1;">
                    <h1 style="color: white; margin: 0; font-size: 3rem;">112</h1>
                    <p style="color: rgba(255,255,255,0.8);">Warriors</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def add_enhanced_css():
    """Add enhanced CSS animations and styling"""
    st.markdown("""
    <style>
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
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #ffd700;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
    }
    
    .interactive-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
    }
    
    .interactive-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True) 