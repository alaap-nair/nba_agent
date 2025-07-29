#!/usr/bin/env python3
"""
Enhanced NBA Tools with Flexible Query Parsing
Provides natural language query support and improved user experience
"""

import json
import time
from langchain.tools import BaseTool
from typing import Dict, Optional, List, Any
from nba_api.stats.endpoints import playercareerstats, commonteamroster, leaguestandings
from nba_api.stats.endpoints import scoreboardv2, teamgamelog
from nba_api.stats.static import players, teams
from nba_api.live.nba.endpoints import scoreboard
from cache import get as cache_get, set as cache_set
import datetime

# Import our modules
from logger import get_logger, log_performance, log_api_call, log_error_with_context
from validation import InputValidator, ResponseValidator, ValidationError, safe_validate_input
from query_parser import query_parser, query_enhancer, ParsedQuery, QueryType, StatType

# Initialize logger
logger = get_logger(__name__)

class EnhancedStatsTool(BaseTool):
    name: str = "enhanced_nba_stats"
    description: str = (
        "Get NBA player statistics with natural language support. "
        "Examples: 'LeBron's points this season', 'Curry shooting percentages', "
        "'Giannis assists and rebounds', 'Embiid stats now'"
    )

    def _run(self, query: str) -> str:
        start_time = time.time()
        
        try:
            # Parse the natural language query
            parsed = query_parser.parse(query)
            logger.info(f"Parsed query: {parsed}")
            
            # Handle different query types
            if parsed.query_type == QueryType.PLAYER_STATS:
                return self._handle_player_stats(parsed)
            elif parsed.query_type == QueryType.PLAYER_COMPARISON:
                return self._handle_player_comparison(parsed)
            else:
                return json.dumps({"error": f"Unsupported query type: {parsed.query_type}"})
                
        except Exception as e:
            log_error_with_context(logger, e, {"query": query})
            return json.dumps({"error": f"Error processing query: {str(e)}"})
        finally:
            log_performance(logger, "enhanced_stats_tool", time.time() - start_time)

    def _handle_player_stats(self, parsed: ParsedQuery) -> str:
        """Handle player statistics queries"""
        if not parsed.entities:
            return json.dumps({"error": "No player name found in query"})
        
        player_name = parsed.entities[0]
        player_info = self._find_player_by_name(player_name)
        
        if not player_info:
            # Try fuzzy matching
            suggestions = self._suggest_similar_players(player_name)
            return json.dumps({
                "error": f"Player '{player_name}' not found",
                "suggestions": suggestions
            })
        
        # Get player stats
        stats = self._get_player_stats(player_info, parsed.season)
        
        # Filter based on requested stat type
        filtered_stats = self._filter_stats_by_type(stats, parsed.stat_type)
        
        # Format response based on context
        response = self._format_player_response(player_info, filtered_stats, parsed)
        
        return json.dumps(response)

    def _handle_player_comparison(self, parsed: ParsedQuery) -> str:
        """Handle player comparison queries"""
        if len(parsed.entities) < 2:
            return json.dumps({"error": "Need at least two players for comparison"})
        
        player1_name = parsed.entities[0]
        player2_name = parsed.entities[1]
        
        player1_info = self._find_player_by_name(player1_name)
        player2_info = self._find_player_by_name(player2_name)
        
        if not player1_info or not player2_info:
            return json.dumps({"error": "One or both players not found"})
        
        # Get stats for both players
        stats1 = self._get_player_stats(player1_info, parsed.season)
        stats2 = self._get_player_stats(player2_info, parsed.season)
        
        # Compare stats
        comparison = self._compare_player_stats(player1_info, stats1, player2_info, stats2, parsed.stat_type)
        
        return json.dumps(comparison)

    def _find_player_by_name(self, name: str) -> Dict | None:
        """Find player by name with enhanced fuzzy matching"""
        name = name.strip()
        
        # Try exact match first
        exact_match = players.find_players_by_full_name(name)
        if exact_match and exact_match[0]['is_active']:
            return exact_match[0]
        
        # Try partial matches with fuzzy matching
        all_players = players.get_active_players()
        best_match = None
        best_score = 0
        
        for player in all_players:
            # Check full name
            score = self._fuzzy_match(name.lower(), player['full_name'].lower())
            if score > best_score and score > 0.6:  # Threshold for good match
                best_score = score
                best_match = player
            
            # Check first name
            score = self._fuzzy_match(name.lower(), player['first_name'].lower())
            if score > best_score and score > 0.8:
                best_score = score
                best_match = player
            
            # Check last name
            score = self._fuzzy_match(name.lower(), player['last_name'].lower())
            if score > best_score and score > 0.8:
                best_score = score
                best_match = player
        
        return best_match

    def _fuzzy_match(self, query: str, target: str) -> float:
        """Calculate fuzzy match score between query and target"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, query, target).ratio()

    def _suggest_similar_players(self, name: str) -> List[str]:
        """Suggest similar player names"""
        all_players = players.get_active_players()
        suggestions = []
        
        for player in all_players:
            score = self._fuzzy_match(name.lower(), player['full_name'].lower())
            if score > 0.3:  # Lower threshold for suggestions
                suggestions.append(player['full_name'])
        
        return suggestions[:5]  # Return top 5 suggestions

    def _get_player_stats(self, player_info: Dict, season: str) -> Dict:
        """Get player statistics with caching"""
        player_id = player_info['id']
        cache_key = f"enhanced_stats_{player_id}_{season}"
        
        # Check cache first
        cached_data = cache_get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {player_info['full_name']} {season}")
            return cached_data
        
        try:
            api_start = time.time()
            
            # Get career stats
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            df = career_stats.get_data_frames()[0]
            
            api_duration = time.time() - api_start
            log_api_call(logger, "playercareerstats", "GET", 200, api_duration, 
                        player_id=player_id)
            
            # Find current season data
            current_season_data = df[df['SEASON_ID'].str.contains(season, na=False)]
            if current_season_data.empty:
                current_season_data = df.iloc[[-1]]
            
            if current_season_data.empty:
                raise ValueError(f"No stats found for {player_info['full_name']}")
            
            season_stats = current_season_data.iloc[0]
            
            # Calculate per-game averages
            games_played = season_stats.get('GP', 1)
            if games_played == 0:
                games_played = 1
            
            stats = {
                "ppg": round(season_stats.get('PTS', 0) / games_played, 1),
                "apg": round(season_stats.get('AST', 0) / games_played, 1),
                "rpg": round(season_stats.get('REB', 0) / games_played, 1),
                "spg": round(season_stats.get('STL', 0) / games_played, 1),
                "bpg": round(season_stats.get('BLK', 0) / games_played, 1),
                "fg_pct": round(season_stats.get('FG_PCT', 0) * 100, 1) if season_stats.get('FG_PCT') else 0,
                "fg3_pct": round(season_stats.get('FG3_PCT', 0) * 100, 1) if season_stats.get('FG3_PCT') else 0,
                "ft_pct": round(season_stats.get('FT_PCT', 0) * 100, 1) if season_stats.get('FT_PCT') else 0,
                "games_played": int(games_played),
                "total_points": int(season_stats.get('PTS', 0)),
                "total_assists": int(season_stats.get('AST', 0)),
                "total_rebounds": int(season_stats.get('REB', 0))
            }
            
            # Cache the results
            cache_set(cache_key, stats)
            logger.debug(f"Cached enhanced stats for {player_info['full_name']} {season}")
            
            return stats
            
        except Exception as e:
            log_error_with_context(logger, e, {
                "player_id": player_id, 
                "player_name": player_info['full_name'],
                "season": season
            })
            raise

    def _filter_stats_by_type(self, stats: Dict, stat_type: StatType) -> Dict:
        """Filter stats based on requested type"""
        if stat_type == StatType.POINTS:
            return {"ppg": stats.get("ppg", 0), "total_points": stats.get("total_points", 0)}
        elif stat_type == StatType.ASSISTS:
            return {"apg": stats.get("apg", 0), "total_assists": stats.get("total_assists", 0)}
        elif stat_type == StatType.REBOUNDS:
            return {"rpg": stats.get("rpg", 0), "total_rebounds": stats.get("total_rebounds", 0)}
        elif stat_type == StatType.STEALS:
            return {"spg": stats.get("spg", 0)}
        elif stat_type == StatType.BLOCKS:
            return {"bpg": stats.get("bpg", 0)}
        elif stat_type == StatType.SHOOTING:
            return {
                "fg_pct": stats.get("fg_pct", 0),
                "fg3_pct": stats.get("fg3_pct", 0),
                "ft_pct": stats.get("ft_pct", 0)
            }
        elif stat_type == StatType.EFFICIENCY:
            return {
                "fg_pct": stats.get("fg_pct", 0),
                "fg3_pct": stats.get("fg3_pct", 0),
                "ft_pct": stats.get("ft_pct", 0),
                "ppg": stats.get("ppg", 0)
            }
        else:  # ALL
            return stats

    def _format_player_response(self, player_info: Dict, stats: Dict, parsed: ParsedQuery) -> Dict:
        """Format player response based on context"""
        response = {
            "player": player_info['full_name'],
            "team": player_info.get('team_name', 'Unknown'),
            "season": parsed.season,
            "stats": stats,
            "query_type": parsed.query_type.value,
            "stat_type": parsed.stat_type.value if parsed.stat_type else None
        }
        
        # Add context-specific formatting
        if parsed.context.get("detailed"):
            response["detailed"] = True
            response["games_played"] = stats.get("games_played", 0)
        
        if parsed.context.get("summary"):
            response["summary"] = True
            # Keep only key stats for summary
        
        if parsed.context.get("visual"):
            response["visual_data"] = True
            # Add data suitable for charts
        
        return response

    def _compare_player_stats(self, player1_info: Dict, stats1: Dict, 
                            player2_info: Dict, stats2: Dict, stat_type: StatType) -> Dict:
        """Compare two players' statistics"""
        comparison = {
            "player1": {
                "name": player1_info['full_name'],
                "team": player1_info.get('team_name', 'Unknown'),
                "stats": stats1
            },
            "player2": {
                "name": player2_info['full_name'],
                "team": player2_info.get('team_name', 'Unknown'),
                "stats": stats2
            },
            "comparison": {}
        }
        
        # Compare key metrics
        if stat_type == StatType.ALL:
            metrics = ["ppg", "apg", "rpg", "spg", "bpg", "fg_pct", "fg3_pct", "ft_pct"]
        elif stat_type == StatType.SHOOTING:
            metrics = ["fg_pct", "fg3_pct", "ft_pct"]
        else:
            metrics = [stat_type.value]
        
        for metric in metrics:
            if metric in stats1 and metric in stats2:
                val1 = stats1[metric]
                val2 = stats2[metric]
                comparison["comparison"][metric] = {
                    "player1": val1,
                    "player2": val2,
                    "difference": round(val1 - val2, 1),
                    "winner": player1_info['full_name'] if val1 > val2 else player2_info['full_name']
                }
        
        return comparison

class EnhancedScheduleTool(BaseTool):
    name: str = "enhanced_nba_schedule"
    description: str = (
        "Get NBA team schedules with natural language support. "
        "Examples: 'When do the Warriors play next?', 'Lakers schedule this week', "
        "'Next Celtics game', 'Upcoming Heat games'"
    )

    def _run(self, query: str) -> str:
        start_time = time.time()
        
        try:
            # Parse the natural language query
            parsed = query_parser.parse(query)
            logger.info(f"Parsed schedule query: {parsed}")
            
            if not parsed.entities:
                return json.dumps({"error": "No team name found in query"})
            
            team_name = parsed.entities[0]
            team_info = self._find_team_by_name(team_name)
            
            if not team_info:
                suggestions = self._suggest_similar_teams(team_name)
                return json.dumps({
                    "error": f"Team '{team_name}' not found",
                    "suggestions": suggestions
                })
            
            # Get team schedule
            schedule = self._get_team_schedule(team_info, parsed.context)
            
            return json.dumps(schedule)
            
        except Exception as e:
            log_error_with_context(logger, e, {"query": query})
            return json.dumps({"error": f"Error processing schedule query: {str(e)}"})
        finally:
            log_performance(logger, "enhanced_schedule_tool", time.time() - start_time)

    def _find_team_by_name(self, name: str) -> Dict | None:
        """Find team by name with fuzzy matching"""
        name = name.strip().lower()
        all_teams = teams.get_teams()
        
        # Try exact match first
        for team in all_teams:
            if (name == team['full_name'].lower() or 
                name == team['nickname'].lower() or
                name == team['abbreviation'].lower()):
                return team
        
        # Try fuzzy matching
        best_match = None
        best_score = 0
        
        for team in all_teams:
            score = self._fuzzy_match(name, team['full_name'].lower())
            if score > best_score and score > 0.6:
                best_score = score
                best_match = team
        
        return best_match

    def _fuzzy_match(self, query: str, target: str) -> float:
        """Calculate fuzzy match score"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, query, target).ratio()

    def _suggest_similar_teams(self, name: str) -> List[str]:
        """Suggest similar team names"""
        all_teams = teams.get_teams()
        suggestions = []
        
        for team in all_teams:
            score = self._fuzzy_match(name.lower(), team['full_name'].lower())
            if score > 0.3:
                suggestions.append(team['full_name'])
        
        return suggestions[:5]

    def _get_team_schedule(self, team_info: Dict, context: Dict) -> Dict:
        """Get team schedule with context awareness"""
        team_id = team_info['id']
        cache_key = f"schedule_{team_id}_enhanced"
        
        # Check cache first
        cached_data = cache_get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Get team schedule
            schedule_data = scoreboardv2.ScoreboardV2()
            games = schedule_data.get_data_frames()[0]
            
            # Filter for team's games
            team_games = games[
                (games['TEAM_ABBREVIATION_A'] == team_info['abbreviation']) |
                (games['TEAM_ABBREVIATION_H'] == team_info['abbreviation'])
            ]
            
            # Format schedule
            schedule = {
                "team": team_info['full_name'],
                "abbreviation": team_info['abbreviation'],
                "upcoming_games": []
            }
            
            for _, game in team_games.iterrows():
                game_info = {
                    "date": game.get('GAME_DATE_EST', 'Unknown'),
                    "home_team": game.get('TEAM_NAME_HOME', 'Unknown'),
                    "away_team": game.get('TEAM_NAME_AWAY', 'Unknown'),
                    "home_score": game.get('PTS_HOME', 0),
                    "away_score": game.get('PTS_AWAY', 0),
                    "status": game.get('GAME_STATUS_TEXT', 'Unknown')
                }
                schedule["upcoming_games"].append(game_info)
            
            # Cache the results
            cache_set(cache_key, schedule)
            
            return schedule
            
        except Exception as e:
            log_error_with_context(logger, e, {
                "team_id": team_id,
                "team_name": team_info['full_name']
            })
            raise 