#!/usr/bin/env python3
"""
Debug script to understand nba_api data structure
"""

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd

def debug_luka_stats():
    """Debug Luka's stats structure"""
    print("=== Debugging Luka Stats ===")
    
    # Find Luka
    luka_players = players.find_players_by_full_name("Luka Dončić")
    if not luka_players:
        print("Luka not found!")
        return
    
    luka_id = luka_players[0]['id']
    print(f"Luka ID: {luka_id}")
    
    try:
        # Get career stats
        career_stats = playercareerstats.PlayerCareerStats(player_id=luka_id)
        dataframes = career_stats.get_data_frames()
        
        print(f"Number of dataframes returned: {len(dataframes)}")
        
        for i, df in enumerate(dataframes):
            print(f"\nDataframe {i} columns: {list(df.columns)}")
            print(f"Shape: {df.shape}")
            if not df.empty:
                print(f"First row:\n{df.iloc[0]}")
                print(f"Last row (most recent season):\n{df.iloc[-1]}")
                
                # Check for 2024-25 season
                season_2024 = df[df['SEASON_ID'].str.contains('2024-25', na=False)]
                if not season_2024.empty:
                    print(f"\n2024-25 season data:\n{season_2024.iloc[0]}")
                else:
                    print("\nNo 2024-25 season data found")
                    print(f"Available seasons: {df['SEASON_ID'].tolist()}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_luka_stats() 