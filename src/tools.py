#!/usr/bin/env python3
"""
Updated NBA Tools using real-time nba_api data
Enhanced with structured logging, input validation, and proper error handling
"""

import json
import time
from langchain.tools import BaseTool
from typing import Dict, Optional
from nba_api.stats.endpoints import playercareerstats, commonteamroster, leaguestandings
from nba_api.stats.endpoints import scoreboardv2, teamgamelog
from nba_api.stats.static import players, teams
from nba_api.live.nba.endpoints import scoreboard
from cache import get as cache_get, set as cache_set
import datetime

# Import our new modules
from logger import get_logger, log_performance, log_api_call, log_error_with_context
from validation import InputValidator, ResponseValidator, ValidationError, safe_validate_input

# Initialize logger
logger = get_logger(__name__)


def _find_player_by_name(name: str) -> Dict | None:
    """Find player by name with fuzzy matching"""
    name = name.strip()
    
    # Try exact match first
    exact_match = players.find_players_by_full_name(name)
    if exact_match and exact_match[0]['is_active']:
        return exact_match[0]
    
    # Try partial matches
    all_players = players.get_active_players()
    
    # Check if name matches first or last name
    for player in all_players:
        if (name.lower() in player['full_name'].lower() or 
            name.lower() == player['first_name'].lower() or
            name.lower() == player['last_name'].lower()):
            return player
    
    return None


def _find_team_by_name(name: str) -> Dict | None:
    """Find team by name with fuzzy matching"""
    name = name.strip().lower()
    all_teams = teams.get_teams()
    
    for team in all_teams:
        if (name in team['full_name'].lower() or 
            name in team['nickname'].lower() or
            name in team['city'].lower() or
            name == team['abbreviation'].lower()):
            return team
    
    return None


class StatsTool(BaseTool):
    name: str = "nba_stats"
    description: str = (
        "Get real-time NBA player statistics. Input should be 'player_name stat_type season' "
        "(e.g., 'LeBron assists 2024-25') or just 'player_name'."
    )

    def _run(self, query: str) -> str:
        start_time = time.time()
        
        try:
            # Validate input query
            query_result = InputValidator.validate_query(query)
            if not query_result.is_valid:
                logger.warning(f"Invalid query received: {query_result.error_message}")
                return json.dumps({"error": f"Invalid query: {query_result.error_message}"})
            
            clean_query = query_result.cleaned_value
            parts = clean_query.split()
            
            # Extract player name, stat type, and season
            player_name, stat_type, season = self._parse_query_parts(parts)
            
            # Validate individual components
            player_result = InputValidator.validate_player_name(player_name)
            if not player_result.is_valid:
                logger.warning(f"Invalid player name: {player_name}")
                return json.dumps({"error": f"Invalid player name: {player_result.error_message}"})
            
            stat_result = InputValidator.validate_stat_type(stat_type)
            if not stat_result.is_valid:
                logger.warning(f"Invalid stat type: {stat_type}")
                return json.dumps({"error": f"Invalid stat type: {stat_result.error_message}"})
            
            season_result = InputValidator.validate_season(season)
            if not season_result.is_valid:
                logger.warning(f"Invalid season: {season}")
                return json.dumps({"error": f"Invalid season: {season_result.error_message}"})
            
            # Use cleaned values
            clean_player_name = player_result.cleaned_value
            clean_stat_type = stat_result.cleaned_value
            clean_season = season_result.cleaned_value
            
            logger.info(f"Processing stats request for {clean_player_name} ({clean_stat_type}, {clean_season})")
            
            # Find player
            player_info = _find_player_by_name(clean_player_name)
            if not player_info:
                logger.warning(f"Player not found: {clean_player_name}")
                return json.dumps({"error": f"Player '{clean_player_name}' not found"})
            
            # Get stats with caching
            stats = self._get_player_stats(player_info, clean_season)
            
            # Filter stats if specific type requested
            result_stats = self._filter_stats(stats, clean_stat_type)
            
            # Validate response
            response_data = {
                "player": player_info['full_name'],
                "season": clean_season,
                "stats": result_stats
            }
            
            validation_result = ResponseValidator.validate_player_stats(response_data)
            if not validation_result.is_valid:
                logger.error(f"Response validation failed: {validation_result.error_message}")
                return json.dumps({"error": "Invalid response data"})
            
            # Log performance
            duration = time.time() - start_time
            log_performance(logger, "player_stats_query", duration, 
                          player=player_info['full_name'], season=clean_season)
            
            return json.dumps(response_data)
            
        except ValidationError as e:
            log_error_with_context(logger, e, {"query": query})
            return json.dumps({"error": str(e)})
        except Exception as e:
            log_error_with_context(logger, e, {"query": query})
            return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
    
    def _parse_query_parts(self, parts: list) -> tuple[str, str, str]:
        """Parse query parts into player_name, stat_type, season"""
        player_name = parts[0]
        stat_type = "all"
        season = "2024-25"
        
        if len(parts) > 1:
            # Check if second part is a stat type or season
            if parts[1] in ["assists", "points", "rebounds", "steals", "blocks", "ppg", "apg", "rpg"]:
                stat_type = parts[1]
                if len(parts) > 2:
                    season = parts[2]
            elif parts[1] in ["2023-24", "2024-25", "2022-23"]:
                season = parts[1]
            else:
                # Assume it's part of the name
                player_name = " ".join(parts[:2])
                if len(parts) > 2:
                    if parts[2] in ["assists", "points", "rebounds", "steals", "blocks", "ppg", "apg", "rpg"]:
                        stat_type = parts[2]
                        if len(parts) > 3:
                            season = parts[3]
                    elif parts[2] in ["2023-24", "2024-25", "2022-23"]:
                        season = parts[2]
        
        return player_name, stat_type, season
    
    def _get_player_stats(self, player_info: Dict, season: str) -> Dict:
        """Get player statistics with caching and error handling"""
        player_id = player_info['id']
        cache_key = f"stats_{player_id}_{season}"
        
        # Check cache first
        cached_data = cache_get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {player_info['full_name']} {season}")
            return cached_data
        
        try:
            api_start = time.time()
            
            # Get career stats
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            df = career_stats.get_data_frames()[0]  # Season totals regular season
            
            api_duration = time.time() - api_start
            log_api_call(logger, "playercareerstats", "GET", 200, api_duration, 
                        player_id=player_id)
            
            # Find current season data
            current_season_data = df[df['SEASON_ID'].str.contains(season, na=False)]
            if current_season_data.empty:
                # If specific season not found, get the most recent
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
                "games_played": int(games_played)
            }
            
            # Cache the results
            cache_set(cache_key, stats)
            logger.debug(f"Cached stats for {player_info['full_name']} {season}")
            
            return stats
            
        except Exception as e:
            log_error_with_context(logger, e, {
                "player_id": player_id, 
                "player_name": player_info['full_name'],
                "season": season
            })
            raise
    
    def _filter_stats(self, stats: Dict, stat_type: str) -> Dict:
        """Filter stats based on requested type"""
        if stat_type in ["assists", "apg"]:
            return {"apg": stats.get("apg", 0)}
        elif stat_type in ["points", "ppg"]:
            return {"ppg": stats.get("ppg", 0)}
        elif stat_type in ["rebounds", "rpg"]:
            return {"rpg": stats.get("rpg", 0)}
        elif stat_type in ["steals", "spg"]:
            return {"spg": stats.get("spg", 0)}
        elif stat_type in ["blocks", "bpg"]:
            return {"bpg": stats.get("bpg", 0)}
        else:
            return stats


class ScheduleTool(BaseTool):
    name: str = "nba_schedule"
    description: str = "Get next scheduled game for an NBA team. Input should be the team name."

    def _run(self, team_name: str) -> str:
        team_info = _find_team_by_name(team_name)
        if not team_info:
            return f"Team '{team_name}' not found"
        
        cache_key = f"schedule_{team_info['id']}"
        cached_data = cache_get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            # Get live scoreboard for today's games
            board = scoreboard.ScoreBoard()
            games = board.get_dict()
            
            team_abbrev = team_info['abbreviation']
            
            # Check if team is playing today
            for game in games.get('scoreboard', {}).get('games', []):
                home_team = game.get('homeTeam', {}).get('teamTricode', '')
                away_team = game.get('awayTeam', {}).get('teamTricode', '')
                
                if team_abbrev in [home_team, away_team]:
                    game_status = game.get('gameStatus', 1)
                    if game_status == 1:  # Game hasn't started
                        opponent = home_team if team_abbrev == away_team else away_team
                        vs_or_at = "vs" if team_abbrev == home_team else "@"
                        result = f"Next {team_info['full_name']} game: {team_abbrev} {vs_or_at} {opponent} today"
                        cache_set(cache_key, result)
                        return result
            
            # If no game today, return a generic message
            result = f"Next {team_info['full_name']} game: Check NBA schedule for upcoming games"
            cache_set(cache_key, result)
            return result
            
        except Exception as e:
            return f"Error getting schedule for {team_info['full_name']}: {str(e)}"


class StandingsTool(BaseTool):
    name: str = "nba_standings"
    description: str = "Get current season standings for an NBA team. Input should be the team name."

    def _run(self, team_name: str) -> str:
        team_info = _find_team_by_name(team_name)
        if not team_info:
            return f"Team '{team_name}' not found"
        
        cache_key = f"standings_{team_info['id']}"
        cached_data = cache_get(cache_key)
        
        if cached_data:
            return json.dumps(cached_data)
        
        try:
            standings = leaguestandings.LeagueStandings()
            df = standings.get_data_frames()[0]
            
            # Find team in standings
            team_standing = df[df['TeamID'] == team_info['id']]
            if team_standing.empty:
                return json.dumps({"error": f"No standings data found for {team_info['full_name']}"})
            
            team_data = team_standing.iloc[0]
            
            result = {
                "team": team_info['full_name'],
                "wins": int(team_data.get('WINS', 0)),
                "losses": int(team_data.get('LOSSES', 0)),
                "win_pct": round(team_data.get('WinPCT', 0), 3),
                "conference_rank": int(team_data.get('ConferenceRank', 0)),
                "division_rank": int(team_data.get('DivisionRank', 0))
            }
            
            cache_set(cache_key, result)
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"error": f"Failed to get standings for {team_info['full_name']}: {str(e)}"})


class RosterTool(BaseTool):
    name: str = "nba_roster"
    description: str = "Get current roster for an NBA team. Input should be the team name."

    def _run(self, team_name: str) -> str:
        team_info = _find_team_by_name(team_name)
        if not team_info:
            return json.dumps({"error": f"Team '{team_name}' not found"})
        
        cache_key = f"roster_{team_info['id']}"
        cached_data = cache_get(cache_key)
        
        if cached_data:
            return json.dumps(cached_data)
        
        try:
            roster = commonteamroster.CommonTeamRoster(team_id=team_info['id'])
            df = roster.get_data_frames()[0]
            
            player_names = df['PLAYER'].tolist()
            
            result = {
                "team": team_info['full_name'],
                "roster": player_names
            }
            
            cache_set(cache_key, result)
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"error": f"Failed to get roster for {team_info['full_name']}: {str(e)}"})


class ArenaTool(BaseTool):
    name: str = "nba_arena"
    description: str = "Get arena information for an NBA team. Input should be the team name."

    def _run(self, team_name: str) -> str:
        team_info = _find_team_by_name(team_name)
        if not team_info:
            return json.dumps({"error": f"Team '{team_name}' not found"})
        
        # Basic arena info (this could be expanded with more detailed data)
        arenas = {
            1610612737: "State Farm Arena",  # Hawks
            1610612738: "TD Garden",  # Celtics
            1610612751: "Barclays Center",  # Nets
            1610612766: "Spectrum Center",  # Hornets
            1610612741: "United Center",  # Bulls
            1610612739: "Rocket Mortgage FieldHouse",  # Cavaliers
            1610612742: "American Airlines Center",  # Mavericks
            1610612743: "Ball Arena",  # Nuggets
            1610612765: "Little Caesars Arena",  # Pistons
            1610612744: "Chase Center",  # Warriors
            1610612745: "Toyota Center",  # Rockets
            1610612754: "Gainbridge Fieldhouse",  # Pacers
            1610612746: "Crypto.com Arena",  # Clippers
            1610612747: "Crypto.com Arena",  # Lakers
            1610612763: "FedExForum",  # Grizzlies
            1610612748: "Kaseya Center",  # Heat
            1610612749: "Fiserv Forum",  # Bucks
            1610612750: "Target Center",  # Timberwolves
            1610612740: "Smoothie King Center",  # Pelicans
            1610612752: "Madison Square Garden",  # Knicks
            1610612760: "Paycom Center",  # Thunder
            1610612753: "Kia Center",  # Magic
            1610612755: "Wells Fargo Center",  # 76ers
            1610612756: "Footprint Center",  # Suns
            1610612757: "Moda Center",  # Trail Blazers
            1610612758: "Golden 1 Center",  # Kings
            1610612759: "Frost Bank Center",  # Spurs
            1610612761: "Scotiabank Arena",  # Raptors
            1610612762: "Vivint Arena",  # Jazz
            1610612764: "Capital One Arena",  # Wizards
        }
        
        arena_name = arenas.get(team_info['id'], "Arena information not available")
        
        result = {
            "team": team_info['full_name'],
            "arena": arena_name,
            "city": team_info['city'],
            "state": team_info['state']
        }
        
        return json.dumps(result) 