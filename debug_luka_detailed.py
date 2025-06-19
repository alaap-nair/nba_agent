#!/usr/bin/env python3
"""
Debug Luka's assists calculation specifically
"""

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import json

def debug_luka_assists():
    """Debug exactly what happens when we query Luka's assists"""
    print("=== Debugging Luka Assists ===")
    
    # Find Luka
    luka_players = players.find_players_by_full_name("Luka Dončić")
    if not luka_players:
        print("Luka not found!")
        return
    
    luka_id = luka_players[0]['id']
    print(f"Luka ID: {luka_id}")
    
    try:
        # Get career stats exactly like in the tool
        career_stats = playercareerstats.PlayerCareerStats(player_id=luka_id)
        df = career_stats.get_data_frames()[0]  # Season totals regular season
        
        print(f"Dataframe shape: {df.shape}")
        print(f"Available seasons: {df['SEASON_ID'].tolist()}")
        
        # Find 2024-25 season data exactly like in the tool
        season = "2024-25"
        current_season_data = df[df['SEASON_ID'].str.contains(season, na=False)]
        
        print(f"\nCurrent season data shape: {current_season_data.shape}")
        
        if current_season_data.empty:
            print("No 2024-25 data found, using most recent")
            current_season_data = df.iloc[[-1]]
            print(f"Most recent season: {current_season_data.iloc[0]['SEASON_ID']}")
        
        season_stats = current_season_data.iloc[0]
        
        print(f"\nSeason stats for calculation:")
        print(f"GP (Games Played): {season_stats.get('GP')}")
        print(f"AST (Total Assists): {season_stats.get('AST')}")
        print(f"PTS (Total Points): {season_stats.get('PTS')}")
        print(f"REB (Total Rebounds): {season_stats.get('REB')}")
        
        # Calculate per-game averages exactly like the tool
        games_played = season_stats.get('GP', 1)
        if games_played == 0:
            games_played = 1
        
        print(f"\nPer-game calculations:")
        print(f"PPG: {season_stats.get('PTS', 0)} / {games_played} = {round(season_stats.get('PTS', 0) / games_played, 1)}")
        print(f"APG: {season_stats.get('AST', 0)} / {games_played} = {round(season_stats.get('AST', 0) / games_played, 1)}")
        print(f"RPG: {season_stats.get('REB', 0)} / {games_played} = {round(season_stats.get('REB', 0) / games_played, 1)}")
        
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
        
        print(f"\nFinal stats dict: {json.dumps(stats, indent=2)}")
        
        # Test filtering for assists only
        result_stats = {"apg": stats.get("apg", 0)}
        print(f"\nFiltered for assists: {json.dumps(result_stats, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_luka_assists() 