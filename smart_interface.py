import streamlit as st
import re
from typing import List, Dict, Tuple
from difflib import get_close_matches
import json

class SmartInterface:
    """Smart interface features for enhanced user experience"""
    
    # NBA player names for autocomplete (subset for demo)
    POPULAR_PLAYERS = [
        "LeBron James", "Stephen Curry", "Giannis Antetokounmpo", "Luka Doncic",
        "Jayson Tatum", "Kevin Durant", "Nikola Jokic", "Joel Embiid", 
        "Damian Lillard", "Anthony Davis", "Kawhi Leonard", "Jimmy Butler",
        "Paul George", "Devin Booker", "Trae Young", "Ja Morant",
        "Zion Williamson", "Tyler Herro", "Bam Adebayo", "Scottie Barnes"
    ]
    
    NBA_TEAMS = [
        "Lakers", "Warriors", "Celtics", "Heat", "Nets", "76ers", "Bucks",
        "Nuggets", "Suns", "Clippers", "Mavericks", "Grizzlies", "Pelicans",
        "Trail Blazers", "Kings", "Timberwolves", "Thunder", "Rockets",
        "Spurs", "Jazz", "Hawks", "Hornets", "Bulls", "Cavaliers",
        "Pistons", "Pacers", "Magic", "Knicks", "Raptors", "Wizards"
    ]
    
    STAT_TYPES = [
        "points", "assists", "rebounds", "steals", "blocks", "field goal percentage",
        "three point percentage", "free throw percentage", "minutes", "turnovers"
    ]
    
    @staticmethod
    def suggest_players(partial_name: str, limit: int = 5) -> List[str]:
        """Suggest player names based on partial input"""
        if not partial_name:
            return SmartInterface.POPULAR_PLAYERS[:limit]
        
        matches = get_close_matches(
            partial_name, 
            SmartInterface.POPULAR_PLAYERS, 
            n=limit, 
            cutoff=0.3
        )
        
        # Also include starts-with matches
        starts_with = [name for name in SmartInterface.POPULAR_PLAYERS 
                      if name.lower().startswith(partial_name.lower())]
        
        # Combine and deduplicate
        combined = list(dict.fromkeys(starts_with + matches))
        return combined[:limit]
    
    @staticmethod
    def suggest_teams(partial_name: str, limit: int = 5) -> List[str]:
        """Suggest team names based on partial input"""
        if not partial_name:
            return SmartInterface.NBA_TEAMS[:limit]
        
        matches = get_close_matches(
            partial_name, 
            SmartInterface.NBA_TEAMS, 
            n=limit, 
            cutoff=0.3
        )
        
        starts_with = [name for name in SmartInterface.NBA_TEAMS 
                      if name.lower().startswith(partial_name.lower())]
        
        combined = list(dict.fromkeys(starts_with + matches))
        return combined[:limit]
    
    @staticmethod
    def generate_smart_suggestions(user_input: str = "") -> List[str]:
        """Generate contextual query suggestions"""
        base_suggestions = [
            "What are LeBron's points this season?",
            "When do the Warriors play next?",
            "Who leads the league in assists?",
            "Lakers vs Celtics head to head",
            "Top 5 scorers this week",
            "Giannis shooting percentage",
            "Heat upcoming schedule",
            "Rookie of the year candidates"
        ]
        
        if not user_input:
            return base_suggestions[:4]
        
        # Generate contextual suggestions based on input
        contextual = []
        
        # If user mentions a player
        for player in SmartInterface.POPULAR_PLAYERS:
            if player.lower() in user_input.lower():
                contextual.extend([
                    f"Compare {player} to other stars",
                    f"{player} season progression",
                    f"{player} vs team average"
                ])
                break
        
        # If user mentions a team
        for team in SmartInterface.NBA_TEAMS:
            if team.lower() in user_input.lower():
                contextual.extend([
                    f"{team} next 5 games",
                    f"{team} top performers",
                    f"{team} season record"
                ])
                break
        
        # If user mentions stats
        if any(stat in user_input.lower() for stat in ["points", "assists", "rebounds"]):
            contextual.extend([
                "League leaders in this stat",
                "Compare top 3 players",
                "Rookie leaders"
            ])
        
        return contextual[:3] if contextual else base_suggestions[:3]
    
    @staticmethod
    def parse_query_intent(query: str) -> Dict[str, any]:
        """Parse user query to understand intent and extract entities"""
        intent = {
            "type": "general",
            "entities": {
                "players": [],
                "teams": [],
                "stats": [],
                "timeframe": None
            },
            "comparison": False,
            "confidence": 0.5
        }
        
        query_lower = query.lower()
        
        # Detect comparison queries
        comparison_keywords = ["vs", "versus", "compare", "against", "between"]
        if any(keyword in query_lower for keyword in comparison_keywords):
            intent["comparison"] = True
            intent["type"] = "comparison"
            intent["confidence"] += 0.2
        
        # Extract players
        for player in SmartInterface.POPULAR_PLAYERS:
            if player.lower() in query_lower:
                intent["entities"]["players"].append(player)
                intent["confidence"] += 0.3
        
        # Extract teams
        for team in SmartInterface.NBA_TEAMS:
            if team.lower() in query_lower:
                intent["entities"]["teams"].append(team)
                intent["confidence"] += 0.2
        
        # Extract stat types
        for stat in SmartInterface.STAT_TYPES:
            if stat in query_lower:
                intent["entities"]["stats"].append(stat)
                intent["confidence"] += 0.1
        
        # Detect query types
        if any(word in query_lower for word in ["schedule", "next", "game", "when"]):
            intent["type"] = "schedule"
        elif any(word in query_lower for word in ["stats", "points", "assists", "rebounds"]):
            intent["type"] = "stats"
        elif any(word in query_lower for word in ["standings", "rank", "record"]):
            intent["type"] = "standings"
        
        return intent
    
    @staticmethod
    def create_autocomplete_input(label: str, key: str, data_type: str = "player") -> str:
        """Create an autocomplete-style input field"""
        
        # Create the input field
        user_input = st.text_input(label, key=key)
        
        if user_input:
            # Generate suggestions based on input
            if data_type == "player":
                suggestions = SmartInterface.suggest_players(user_input)
            elif data_type == "team":
                suggestions = SmartInterface.suggest_teams(user_input)
            else:
                suggestions = []
            
            if suggestions:
                st.markdown("**Suggestions:**")
                suggestion_cols = st.columns(min(len(suggestions), 3))
                
                for i, suggestion in enumerate(suggestions[:3]):
                    with suggestion_cols[i]:
                        if st.button(f"📝 {suggestion}", key=f"{key}_suggest_{i}"):
                            st.session_state[key] = suggestion
                            st.rerun()
        
        return user_input
    
    @staticmethod
    def create_smart_query_builder() -> str:
        """Create an interactive query builder"""
        st.markdown("### 🎯 Smart Query Builder")
        
        # Query type selection
        query_type = st.selectbox(
            "What would you like to know?",
            ["Player Stats", "Team Info", "Compare Players", "Schedule", "League Leaders"]
        )
        
        built_query = ""
        
        if query_type == "Player Stats":
            col1, col2 = st.columns(2)
            with col1:
                player = SmartInterface.create_autocomplete_input("Player Name:", "qb_player", "player")
            with col2:
                stat = st.selectbox("Stat Type:", ["All Stats"] + SmartInterface.STAT_TYPES)
            
            if player:
                if stat == "All Stats":
                    built_query = f"What are {player}'s stats this season?"
                else:
                    built_query = f"How many {stat} does {player} have this season?"
        
        elif query_type == "Compare Players":
            col1, col2 = st.columns(2)
            with col1:
                player1 = SmartInterface.create_autocomplete_input("First Player:", "qb_player1", "player")
            with col2:
                player2 = SmartInterface.create_autocomplete_input("Second Player:", "qb_player2", "player")
            
            if player1 and player2:
                built_query = f"Compare {player1} and {player2} stats"
        
        elif query_type == "Team Info":
            team = SmartInterface.create_autocomplete_input("Team Name:", "qb_team", "team")
            info_type = st.selectbox("Information Type:", ["Schedule", "Standings", "Roster"])
            
            if team:
                if info_type == "Schedule":
                    built_query = f"When do the {team} play next?"
                elif info_type == "Standings":
                    built_query = f"What are the {team} standings?"
                else:
                    built_query = f"Show me the {team} roster"
        
        elif query_type == "League Leaders":
            stat = st.selectbox("Stat Category:", SmartInterface.STAT_TYPES)
            built_query = f"Who leads the league in {stat}?"
        
        if built_query:
            st.markdown(f"**Generated Query:** `{built_query}`")
            if st.button("🚀 Use This Query", use_container_width=True):
                return built_query
        
        return ""

class VoiceInterface:
    """Voice interface capabilities (placeholder for future implementation)"""
    
    @staticmethod
    def create_voice_input_button():
        """Create a voice input button (UI only for now)"""
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <button class="voice-input" onclick="alert('Voice input coming soon!')">
                🎤
            </button>
            <p style="color: rgba(255,255,255,0.6); margin: 10px 0;">
                Voice input (Coming Soon!)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def simulate_voice_commands() -> List[str]:
        """Simulate popular voice commands"""
        return [
            "Hey NBA Agent, what are LeBron's stats?",
            "Show me Warriors next game",
            "Compare Giannis and Embiid",
            "Who's leading in scoring?"
        ]

class QueryOptimizer:
    """Optimize user queries for better agent performance"""
    
    @staticmethod
    def enhance_query(original_query: str) -> str:
        """Enhance user query with context and specificity"""
        enhanced = original_query.strip()
        
        # Add current season context if not specified
        if not any(season in enhanced for season in ["2024-25", "2023-24", "2022-23"]):
            if any(word in enhanced.lower() for word in ["stats", "points", "assists", "rebounds"]):
                enhanced += " for the 2024-25 season"
        
        # Expand abbreviations
        abbreviations = {
            "pts": "points",
            "ast": "assists", 
            "reb": "rebounds",
            "stl": "steals",
            "blk": "blocks"
        }
        
        for abbr, full in abbreviations.items():
            enhanced = re.sub(rf'\b{abbr}\b', full, enhanced, flags=re.IGNORECASE)
        
        # Add specificity hints
        if "compare" in enhanced.lower() and "stats" not in enhanced.lower():
            enhanced += " stats"
        
        return enhanced
    
    @staticmethod
    def suggest_refinements(query: str, query_result: str) -> List[str]:
        """Suggest query refinements based on results"""
        refinements = []
        
        intent = SmartInterface.parse_query_intent(query)
        
        if intent["type"] == "stats" and len(intent["entities"]["players"]) == 1:
            player = intent["entities"]["players"][0]
            refinements.extend([
                f"Compare {player} to league average",
                f"{player} game-by-game stats",
                f"{player} vs position peers"
            ])
        
        elif intent["type"] == "schedule":
            refinements.extend([
                "Show full month schedule",
                "Include game times and TV",
                "Show strength of upcoming opponents"
            ])
        
        return refinements[:3] 