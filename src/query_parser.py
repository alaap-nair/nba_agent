#!/usr/bin/env python3
"""
Advanced Query Parser for NBA Agent
Provides flexible, natural language query parsing with context awareness
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)

class QueryType(Enum):
    PLAYER_STATS = "player_stats"
    TEAM_SCHEDULE = "team_schedule"
    TEAM_STANDINGS = "team_standings"
    TEAM_ROSTER = "team_roster"
    TEAM_ARENA = "team_arena"
    PLAYER_COMPARISON = "player_comparison"
    TEAM_COMPARISON = "team_comparison"
    UNKNOWN = "unknown"

class StatType(Enum):
    POINTS = "points"
    ASSISTS = "assists"
    REBOUNDS = "rebounds"
    STEALS = "steals"
    BLOCKS = "blocks"
    ALL = "all"
    SHOOTING = "shooting"
    EFFICIENCY = "efficiency"

@dataclass
class ParsedQuery:
    query_type: QueryType
    entities: List[str]  # Players, teams, etc.
    stat_type: Optional[StatType] = None
    season: Optional[str] = None
    comparison: bool = False
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

class FlexibleQueryParser:
    """Advanced query parser with natural language understanding"""
    
    def __init__(self):
        # Common variations and synonyms
        self.stat_synonyms = {
            "points": ["points", "ppg", "scoring", "pts", "points per game"],
            "assists": ["assists", "apg", "assist", "passing", "dimes"],
            "rebounds": ["rebounds", "rpg", "rebound", "boards"],
            "steals": ["steals", "spg", "steal", "theft"],
            "blocks": ["blocks", "bpg", "block", "rejection"],
            "shooting": ["shooting", "fg%", "3p%", "ft%", "field goal", "three point", "free throw"],
            "efficiency": ["efficiency", "efficient", "fg%", "3p%", "ft%", "shooting percentage"]
        }
        
        self.season_patterns = [
            r"(\d{4}-\d{2})",  # 2024-25
            r"(\d{4})",         # 2024
            r"(this season|current season|now)",
            r"(last season|previous season)",
            r"(next season|upcoming season)"
        ]
        
        self.comparison_keywords = [
            "compare", "vs", "versus", "against", "head to head", "matchup",
            "who's better", "who is better", "difference between"
        ]
        
        self.query_type_patterns = {
            QueryType.PLAYER_STATS: [
                r"(stats|statistics|numbers|averages|performance)",
                r"(how many|what are|show me|get)",
                r"(points|assists|rebounds|steals|blocks|ppg|apg|rpg|spg|bpg)"
            ],
            QueryType.TEAM_SCHEDULE: [
                r"(schedule|next game|upcoming|when do|play next)",
                r"(game|match|fixture)",
                r"(tomorrow|next week|this week)"
            ],
            QueryType.TEAM_STANDINGS: [
                r"(standings|ranking|position|record)",
                r"(how good|where are|what place)",
                r"(conference|division|league)"
            ],
            QueryType.TEAM_ROSTER: [
                r"(roster|players|team members|squad)",
                r"(who plays|who's on|team list)"
            ],
            QueryType.TEAM_ARENA: [
                r"(arena|stadium|venue|home court)",
                r"(where do|play at|home games)"
            ]
        }
    
    def parse(self, query: str) -> ParsedQuery:
        """Parse a natural language query into structured components"""
        query = query.lower().strip()
        
        # Initialize result
        parsed = ParsedQuery(
            query_type=QueryType.UNKNOWN,
            entities=[],
            stat_type=None,
            season=None,
            comparison=False,
            context={}
        )
        
        # Detect query type
        parsed.query_type = self._detect_query_type(query)
        
        # Extract entities (players, teams)
        parsed.entities = self._extract_entities(query)
        
        # Detect comparison
        parsed.comparison = self._detect_comparison(query)
        
        # Extract stat type
        parsed.stat_type = self._extract_stat_type(query)
        
        # Extract season
        parsed.season = self._extract_season(query)
        
        # Extract additional context
        parsed.context = self._extract_context(query)
        
        logger.debug(f"Parsed query: {parsed}")
        return parsed
    
    def _detect_query_type(self, query: str) -> QueryType:
        """Detect the type of query based on keywords"""
        for query_type, patterns in self.query_type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return query_type
        
        # Default to player stats if we can't determine
        return QueryType.PLAYER_STATS
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract player names and team names from query"""
        entities = []
        
        # Common NBA team names and abbreviations
        team_patterns = [
            r"\b(lakers|warriors|celtics|heat|bulls|knicks|nets|clippers|spurs|mavericks|rockets|thunder|blazers|jazz|nuggets|timberwolves|pelicans|kings|suns|hawks|hornets|magic|pistons|cavaliers|raptors|76ers|bucks|pacers|wizards|knicks)\b",
            r"\b(gsw|lal|bos|mia|chi|nyk|bkn|lac|sa|dal|hou|okc|por|uta|den|min|nop|sac|phx|atl|cha|orl|det|cle|tor|phi|mil|ind|was)\b"
        ]
        
        # Extract team names
        for pattern in team_patterns:
            matches = re.findall(pattern, query)
            entities.extend(matches)
        
        # Extract potential player names (words that could be names)
        words = query.split()
        potential_names = []
        
        for i, word in enumerate(words):
            # Skip common words that aren't names
            if word in ["the", "and", "or", "vs", "versus", "compare", "stats", "this", "that", "what", "how", "when", "where", "who"]:
                continue
            
            # Look for multi-word names
            if i < len(words) - 1:
                potential_name = f"{word} {words[i+1]}"
                if self._looks_like_name(potential_name):
                    potential_names.append(potential_name)
            
            # Single word names (common players)
            if self._looks_like_name(word):
                potential_names.append(word)
        
        entities.extend(potential_names)
        
        return list(set(entities))  # Remove duplicates
    
    def _looks_like_name(self, text: str) -> bool:
        """Check if text looks like a player name"""
        # Common player name patterns
        name_patterns = [
            r"^[A-Z][a-z]+$",  # Single capitalized word
            r"^[A-Z][a-z]+ [A-Z][a-z]+$",  # Two capitalized words
            r"^[A-Z][a-z]+-[A-Z][a-z]+$",  # Hyphenated name
        ]
        
        for pattern in name_patterns:
            if re.match(pattern, text):
                return True
        
        # Common player nicknames
        nicknames = ["lebron", "curry", "giannis", "jokic", "embiid", "durant", "harden", "luka", "zion", "ja"]
        if text.lower() in nicknames:
            return True
        
        return False
    
    def _detect_comparison(self, query: str) -> bool:
        """Detect if this is a comparison query"""
        for keyword in self.comparison_keywords:
            if keyword in query:
                return True
        return False
    
    def _extract_stat_type(self, query: str) -> Optional[StatType]:
        """Extract the requested stat type from query"""
        for stat_type, synonyms in self.stat_synonyms.items():
            for synonym in synonyms:
                if synonym in query:
                    return StatType(stat_type)
        
        # Default to all stats if no specific stat mentioned
        return StatType.ALL
    
    def _extract_season(self, query: str) -> Optional[str]:
        """Extract season information from query"""
        # Look for specific season patterns
        for pattern in self.season_patterns:
            match = re.search(pattern, query)
            if match:
                season = match.group(1)
                if season == "this season" or season == "current season" or season == "now":
                    return "2024-25"
                elif season == "last season" or season == "previous season":
                    return "2023-24"
                elif season == "next season" or season == "upcoming season":
                    return "2025-26"
                else:
                    return season
        
        # Default to current season
        return "2024-25"
    
    def _extract_context(self, query: str) -> Dict[str, Any]:
        """Extract additional context from query"""
        context = {}
        
        # Detect urgency/timing
        if any(word in query for word in ["now", "today", "live", "current"]):
            context["urgent"] = True
        
        # Detect detailed vs summary request
        if any(word in query for word in ["detailed", "full", "complete", "all"]):
            context["detailed"] = True
        elif any(word in query for word in ["summary", "overview", "quick"]):
            context["summary"] = True
        
        # Detect format preferences
        if any(word in query for word in ["chart", "graph", "visual", "plot"]):
            context["visual"] = True
        
        return context

class QueryEnhancer:
    """Enhances queries with context and suggestions"""
    
    def __init__(self):
        self.common_queries = {
            "player_stats": [
                "What are {player}'s stats this season?",
                "How many points does {player} average?",
                "Show me {player}'s shooting percentages",
                "What are {player}'s assists and rebounds?"
            ],
            "team_schedule": [
                "When do the {team} play next?",
                "What's the {team} schedule?",
                "When is the next {team} game?"
            ],
            "comparison": [
                "Compare {player1} and {player2}",
                "Who's better: {player1} or {player2}?",
                "{player1} vs {player2} stats"
            ]
        }
    
    def suggest_queries(self, parsed_query: ParsedQuery) -> List[str]:
        """Suggest related queries based on the parsed query"""
        suggestions = []
        
        if parsed_query.query_type == QueryType.PLAYER_STATS and parsed_query.entities:
            player = parsed_query.entities[0]
            suggestions.extend([
                f"What are {player}'s shooting percentages?",
                f"How many assists does {player} average?",
                f"Show me {player}'s complete stats"
            ])
        
        return suggestions
    
    def expand_query(self, query: str) -> List[str]:
        """Expand a simple query into multiple related queries"""
        expanded = [query]
        
        # Add variations for common patterns
        if "stats" in query.lower():
            expanded.append(query.replace("stats", "shooting percentages"))
            expanded.append(query.replace("stats", "assists and rebounds"))
        
        return expanded

# Global parser instance
query_parser = FlexibleQueryParser()
query_enhancer = QueryEnhancer() 