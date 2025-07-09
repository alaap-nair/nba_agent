#!/usr/bin/env python3
"""
Test script to explore nba_api capabilities
"""

from nba_api.stats.endpoints import playergamelog, leaguegamefinder, teamgamelog
from nba_api.stats.endpoints import commonplayerinfo, teamdetails, leaguestandings
from nba_api.stats.endpoints import scoreboardv2, playercareerstats
from nba_api.stats.static import players, teams
from nba_api.live.nba.endpoints import scoreboard
import pandas as pd

def test_player_search():
    """Test finding players by name"""
    print("=== Testing Player Search ===")
    
    # Find Luka Dončić
    luka_players = players.find_players_by_full_name("Luka Dončić")
    print(f"Luka Dončić search: {luka_players}")
    
    # Alternative search
    luka_players2 = players.find_players_by_first_name("Luka")
    print(f"Players named Luka: {luka_players2}")
    
    # Find LeBron
    lebron = players.find_players_by_full_name("LeBron James")
    print(f"LeBron James: {lebron}")

def test_teams():
    """Test team data"""
    print("\n=== Testing Teams ===")
    
    # Get all teams
    nba_teams = teams.get_teams()
    print(f"Found {len(nba_teams)} teams")
    
    # Find Lakers
    lakers = [team for team in nba_teams if 'Lakers' in team['full_name']]
    print(f"Lakers: {lakers}")
    
    # Find Mavericks
    mavs = [team for team in nba_teams if 'Mavericks' in team['full_name']]
    print(f"Mavericks: {mavs}")

def test_live_scoreboard():
    """Test live game data"""
    print("\n=== Testing Live Scoreboard ===")
    
    try:
        board = scoreboard.ScoreBoard()
        games = board.get_dict()
        print(f"Live games today: {len(games.get('scoreboard', {}).get('games', []))}")
        
        # Show game info
        for game in games.get('scoreboard', {}).get('games', []):
            home_team = game.get('homeTeam', {}).get('teamTricode', 'Unknown')
            away_team = game.get('awayTeam', {}).get('teamTricode', 'Unknown')
            print(f"  {away_team} @ {home_team}")
            
    except Exception as e:
        print(f"Live scoreboard error: {e}")

def test_player_stats():
    """Test getting player stats"""
    print("\n=== Testing Player Stats ===")
    
    # Find Luka and get his stats
    luka_players = players.find_players_by_full_name("Luka Dončić")
    if luka_players:
        luka_id = luka_players[0]['id']
        print(f"Luka ID: {luka_id}")
        
        try:
            # Get current season stats
            career_stats = playercareerstats.PlayerCareerStats(player_id=luka_id)
            df = career_stats.get_data_frames()[0]  # Season totals regular season
            current_season = df.iloc[-1]  # Most recent season
            
            print(f"Luka this season:")
            print(f"  PPG: {current_season.get('PTS', 0)}")
            print(f"  APG: {current_season.get('AST', 0)}")
            print(f"  RPG: {current_season.get('REB', 0)}")
            
        except Exception as e:
            print(f"Error getting Luka stats: {e}")

if __name__ == "__main__":
    test_player_search()
    test_teams()
    test_live_scoreboard()
    test_player_stats() 