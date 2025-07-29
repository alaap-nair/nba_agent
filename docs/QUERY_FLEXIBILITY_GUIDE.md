# 🎯 Enhanced Query Flexibility Guide

## Overview

The NBA Agent now supports **natural language queries** with flexible parsing, fuzzy matching, and intelligent suggestions. This guide explains how the enhanced query system works and how to extend it further.

## 🚀 Key Improvements

### Before (Rigid Format)
```
❌ "LeBron James assists 2024-25"  # Exact format required
❌ "Curry points"                   # Missing season
❌ "Lebron"                        # Wrong spelling
❌ "Compare LeBron and Curry"      # Not supported
```

### After (Natural Language)
```
✅ "LeBron's points this season"
✅ "Curry shooting percentages"
✅ "Giannis assists and rebounds"
✅ "Compare LeBron and Curry"
✅ "Who's better: Luka or Jokic?"
✅ "When do the Warriors play next?"
```

## 🏗️ Architecture

### Core Components

1. **Query Parser** (`src/query_parser.py`)
   - Natural language understanding
   - Entity extraction (players, teams)
   - Intent classification
   - Context awareness

2. **Enhanced Tools** (`src/enhanced_tools.py`)
   - Flexible stat retrieval
   - Fuzzy name matching
   - Smart suggestions
   - Comparison support

3. **Smart Agent** (`src/enhanced_agent.py`)
   - Intelligent query routing
   - Confidence scoring
   - Context enhancement
   - Response formatting

## 📊 Query Types Supported

### Player Statistics
```python
# Basic stats
"LeBron's points this season"
"Curry shooting percentages"
"Giannis assists and rebounds"

# Specific stats
"Embiid blocks per game"
"Luka steals this season"
"Jokic field goal percentage"

# Detailed requests
"LeBron's detailed performance"
"Curry's complete stats"
"Giannis efficiency metrics"
```

### Player Comparisons
```python
# Direct comparisons
"Compare LeBron and Curry"
"Giannis vs Embiid"
"Luka vs Jokic stats"

# Specific stat comparisons
"LeBron vs Durant shooting"
"Curry vs Giannis assists"
"Embiid vs Jokic rebounds"

# Question format
"Who's better: Luka or Jokic?"
"Which player scores more: LeBron or Curry?"
```

### Team Information
```python
# Schedule queries
"When do the Warriors play next?"
"Lakers schedule this week"
"Celtics upcoming games"

# Team abbreviations
"GSW next game"
"LAL vs BOS"
"BOS schedule"
```

### Advanced Features
```python
# Time context
"LeBron stats now"           # Current/urgent
"Curry last season"          # Historical
"Giannis next season"        # Future

# Format preferences
"Show me visual charts for LeBron's performance"
"Give me a summary of Curry's stats"
"Detailed breakdown of Giannis vs Embiid"
```

## 🔧 How to Extend Query Flexibility

### 1. Add New Stat Types

Edit `src/query_parser.py`:

```python
class StatType(Enum):
    # Existing types...
    ADVANCED = "advanced"
    EFFICIENCY = "efficiency"
    DEFENSE = "defense"
    CLUTCH = "clutch"

# Add synonyms
self.stat_synonyms = {
    # Existing synonyms...
    "advanced": ["advanced", "advanced stats", "per", "vorp", "bpm"],
    "efficiency": ["efficiency", "efficient", "true shooting", "ts%"],
    "defense": ["defense", "defensive", "defensive rating", "drtg"],
    "clutch": ["clutch", "clutch time", "late game", "pressure"]
}
```

### 2. Add New Query Types

```python
class QueryType(Enum):
    # Existing types...
    PLAYER_HISTORY = "player_history"
    TEAM_ANALYTICS = "team_analytics"
    GAME_PREDICTIONS = "game_predictions"

# Add patterns
self.query_type_patterns = {
    # Existing patterns...
    QueryType.PLAYER_HISTORY: [
        r"(career|history|past|previous)",
        r"(how long|since when|years)"
    ],
    QueryType.TEAM_ANALYTICS: [
        r"(team stats|team performance|team analytics)",
        r"(offense|defense|efficiency)"
    ]
}
```

### 3. Enhance Entity Recognition

```python
def _extract_entities(self, query: str) -> List[str]:
    # Add more player nicknames
    nicknames = {
        "king": "LeBron James",
        "steph": "Stephen Curry", 
        "greek freak": "Giannis Antetokounmpo",
        "the process": "Joel Embiid",
        "luka magic": "Luka Doncic"
    }
    
    # Add team variations
    team_variations = {
        "dubs": "Warriors",
        "lake show": "Lakers",
        "green team": "Celtics",
        "sixers": "76ers"
    }
```

### 4. Add Context Awareness

```python
def _extract_context(self, query: str) -> Dict[str, Any]:
    context = {}
    
    # Add new context types
    if any(word in query for word in ["playoff", "postseason"]):
        context["playoff"] = True
    
    if any(word in query for word in ["home", "away", "road"]):
        context["venue"] = "home" if "home" in query else "away"
    
    if any(word in query for word in ["rookie", "veteran", "young"]):
        context["experience"] = "rookie" if "rookie" in query else "veteran"
    
    return context
```

### 5. Create New Tools

```python
class AdvancedStatsTool(BaseTool):
    name: str = "advanced_nba_stats"
    description: str = "Get advanced NBA statistics and analytics"
    
    def _run(self, query: str) -> str:
        parsed = query_parser.parse(query)
        # Implement advanced stats logic
        return self._get_advanced_stats(parsed)

class PredictionTool(BaseTool):
    name: str = "nba_predictions"
    description: str = "Get game predictions and odds"
    
    def _run(self, query: str) -> str:
        parsed = query_parser.parse(query)
        # Implement prediction logic
        return self._get_predictions(parsed)
```

## 🧪 Testing New Features

### 1. Unit Tests

```python
def test_new_stat_type():
    query = "LeBron advanced stats"
    parsed = query_parser.parse(query)
    assert parsed.stat_type == StatType.ADVANCED
    assert "lebron" in parsed.entities

def test_new_query_type():
    query = "LeBron career history"
    parsed = query_parser.parse(query)
    assert parsed.query_type == QueryType.PLAYER_HISTORY
```

### 2. Integration Tests

```python
def test_enhanced_tool():
    tool = AdvancedStatsTool()
    result = tool._run("LeBron advanced stats this season")
    assert "per" in result.lower() or "vorp" in result.lower()
```

### 3. Performance Tests

```python
def test_query_speed():
    start_time = time.time()
    for _ in range(100):
        query_parser.parse("LeBron stats")
    duration = time.time() - start_time
    assert duration < 1.0  # Should be fast
```

## 📈 Performance Optimizations

### 1. Caching

```python
# Cache parsed queries
@lru_cache(maxsize=1000)
def parse_query_cached(query: str) -> ParsedQuery:
    return query_parser.parse(query)
```

### 2. Preprocessing

```python
def preprocess_query(query: str) -> str:
    # Normalize common variations
    query = query.lower()
    query = re.sub(r"lebron's", "lebron", query)
    query = re.sub(r"curry's", "curry", query)
    return query
```

### 3. Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_multiple_queries(queries: List[str]) -> List[ParsedQuery]:
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(query_parser.parse, queries))
```

## 🎯 Best Practices

### 1. Query Design

- **Be specific**: "LeBron's points this season" vs "LeBron stats"
- **Use natural language**: "Compare LeBron and Curry" vs "LeBron vs Curry"
- **Include context**: "Curry shooting percentages" vs "Curry stats"

### 2. Error Handling

```python
def safe_parse_query(query: str) -> ParsedQuery:
    try:
        return query_parser.parse(query)
    except Exception as e:
        logger.error(f"Query parsing failed: {e}")
        return ParsedQuery(
            query_type=QueryType.UNKNOWN,
            entities=[],
            stat_type=StatType.ALL,
            season="2024-25"
        )
```

### 3. User Feedback

```python
def provide_suggestions(parsed: ParsedQuery) -> List[str]:
    suggestions = []
    
    if not parsed.entities:
        suggestions.append("Try specifying a player name")
    
    if parsed.query_confidence < 0.7:
        suggestions.append("Try being more specific")
    
    if parsed.stat_type == StatType.ALL:
        suggestions.append("Try asking for specific stats")
    
    return suggestions
```

## 🚀 Usage Examples

### Basic Usage

```python
from src.enhanced_agent import build_smart_processor

# Initialize
processor = build_smart_processor()

# Process queries
response = processor.process_query("LeBron's points this season")
print(response["output"])
```

### Advanced Usage

```python
from src.query_parser import query_parser

# Parse queries manually
parsed = query_parser.parse("Compare LeBron and Curry")
print(f"Query type: {parsed.query_type}")
print(f"Entities: {parsed.entities}")
print(f"Comparison: {parsed.comparison}")
```

### Testing

```bash
# Run the test suite
python test_enhanced_queries.py

# Run demo mode
python test_enhanced_queries.py demo

# Test specific features
python apps/enhanced_chat.py
```

## 🔮 Future Enhancements

### 1. Machine Learning Integration

- **Intent Classification**: Use ML models for better query understanding
- **Entity Recognition**: Named entity recognition for players/teams
- **Query Embeddings**: Semantic similarity for better suggestions

### 2. Advanced Features

- **Multi-turn Conversations**: "What about his assists?" (referring to previous player)
- **Voice Queries**: Speech-to-text integration
- **Visual Queries**: Image-based player identification

### 3. Personalization

- **User Preferences**: Remember favorite players/teams
- **Query History**: Learn from user patterns
- **Custom Alerts**: "Notify me when LeBron scores 30+"

### 4. Real-time Features

- **Live Game Data**: Real-time statistics during games
- **Push Notifications**: Important game events
- **Social Integration**: Share stats on social media

## 📚 Additional Resources

- [Query Parser Documentation](src/query_parser.py)
- [Enhanced Tools Documentation](src/enhanced_tools.py)
- [Enhanced Agent Documentation](src/enhanced_agent.py)
- [Test Suite](test_enhanced_queries.py)
- [Demo Interface](apps/enhanced_chat.py)

---

**🎯 The enhanced query flexibility system provides a much more natural and user-friendly experience for NBA data queries, making the agent accessible to users of all technical levels.** 