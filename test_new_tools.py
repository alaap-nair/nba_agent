#!/usr/bin/env python3
"""
Test the new real-time NBA tools
"""

from tools import StatsTool, ScheduleTool, StandingsTool, RosterTool, ArenaTool
import json

def test_stats_tool():
    """Test the stats tool with Luka"""
    print("=== Testing StatsTool ===")
    
    tool = StatsTool()
    
    # Test Luka assists
    result = tool._run("Luka assists")
    print(f"Luka assists: {result}")
    
    # Test LeBron all stats
    result = tool._run("LeBron James")
    print(f"LeBron all stats: {result}")

def test_roster_tool():
    """Test the roster tool with Mavericks"""
    print("\n=== Testing RosterTool ===")
    
    tool = RosterTool()
    
    # Test Mavericks roster
    result = tool._run("Dallas Mavericks")
    print(f"Mavericks roster: {result}")

def test_standings_tool():
    """Test the standings tool with Lakers"""
    print("\n=== Testing StandingsTool ===")
    
    tool = StandingsTool()
    
    # Test Lakers standings
    result = tool._run("Lakers")
    print(f"Lakers standings: {result}")

def test_schedule_tool():
    """Test the schedule tool"""
    print("\n=== Testing ScheduleTool ===")
    
    tool = ScheduleTool()
    
    # Test Lakers schedule
    result = tool._run("Lakers")
    print(f"Lakers schedule: {result}")

if __name__ == "__main__":
    test_stats_tool()
    test_roster_tool()
    test_standings_tool()
    test_schedule_tool() 