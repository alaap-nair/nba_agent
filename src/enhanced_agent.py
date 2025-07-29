#!/usr/bin/env python3
"""
Enhanced NBA Agent with Flexible Query Parsing
Provides natural language understanding and improved user experience
"""

import os
import json
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage
from enhanced_tools import EnhancedStatsTool, EnhancedScheduleTool
from query_parser import query_parser, query_enhancer, ParsedQuery, QueryType
from logger import get_logger

logger = get_logger(__name__)

class EnhancedNBAAgent:
    """Enhanced NBA Agent with flexible query parsing and natural language understanding"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.query_parser = query_parser
        self.query_enhancer = query_enhancer
        
        # Initialize tools
        self.tools = [
            EnhancedStatsTool(),
            EnhancedScheduleTool()
        ]
        
        # Initialize agent
        self.agent = self._build_agent()
    
    def _build_agent(self):
        """Build the enhanced agent with better configuration"""
        agent_kwargs = {
            "tools": self.tools,
            "llm": self.llm,
            "agent": AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            "verbose": True,
            "max_iterations": 8,  # Increased for complex queries
            "max_execution_time": 45,  # More time for parsing
            "early_stopping_method": "generate",
            "handle_parsing_errors": True,
            "memory": self.memory,
        }
        
        # Add Judgment tracing if available
        try:
            from judgeval.common.tracer import Tracer
            if os.getenv("JUDGMENT_API_KEY"):
                tracer = Tracer(project_name="enhanced_nba_agent", deep_tracing=False)
                agent_kwargs["tracer"] = tracer
                logger.info("✅ Judgment tracing enabled for enhanced agent")
            else:
                logger.info("⚠️  Running enhanced agent without Judgment tracing")
        except Exception as e:
            logger.warning(f"⚠️  Running enhanced agent without Judgment tracing: {e}")
        
        return initialize_agent(**agent_kwargs)
    
    def invoke(self, inputs: dict) -> dict:
        """Process a query with enhanced parsing and context awareness"""
        query = inputs.get("input", "")
        
        try:
            # Parse the query to understand intent
            parsed_query = self.query_parser.parse(query)
            logger.info(f"Enhanced agent parsed query: {parsed_query}")
            
            # Generate suggestions for similar queries
            suggestions = self.query_enhancer.suggest_queries(parsed_query)
            
            # Process with the agent
            response = self.agent.invoke({"input": query})
            
            # Enhance response with context
            enhanced_response = self._enhance_response(response, parsed_query, suggestions)
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error in enhanced agent: {e}")
            return {
                "output": f"Sorry, I encountered an error processing your query: {str(e)}",
                "error": True,
                "suggestions": self._get_fallback_suggestions(query)
            }
    
    def _enhance_response(self, response: dict, parsed_query: ParsedQuery, suggestions: list) -> dict:
        """Enhance the agent response with additional context and suggestions"""
        enhanced = {
            "output": response.get("output", ""),
            "parsed_query": {
                "query_type": parsed_query.query_type.value,
                "entities": parsed_query.entities,
                "stat_type": parsed_query.stat_type.value if parsed_query.stat_type else None,
                "season": parsed_query.season,
                "comparison": parsed_query.comparison,
                "context": parsed_query.context
            },
            "suggestions": suggestions,
            "query_confidence": self._calculate_confidence(parsed_query)
        }
        
        # Add context-specific enhancements
        if parsed_query.context.get("urgent"):
            enhanced["urgent"] = True
            enhanced["output"] = f"🚨 {enhanced['output']}"
        
        if parsed_query.context.get("detailed"):
            enhanced["detailed"] = True
        
        if parsed_query.context.get("visual"):
            enhanced["visual_suggestions"] = self._get_visual_suggestions(parsed_query)
        
        return enhanced
    
    def _calculate_confidence(self, parsed_query: ParsedQuery) -> float:
        """Calculate confidence score for the parsed query"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence for clear entities
        if parsed_query.entities:
            confidence += 0.2
        
        # Boost for specific stat types
        if parsed_query.stat_type and parsed_query.stat_type != "all":
            confidence += 0.1
        
        # Boost for specific seasons
        if parsed_query.season and parsed_query.season != "2024-25":
            confidence += 0.1
        
        # Boost for comparison queries
        if parsed_query.comparison:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _get_visual_suggestions(self, parsed_query: ParsedQuery) -> list:
        """Get suggestions for visual representations"""
        suggestions = []
        
        if parsed_query.query_type == QueryType.PLAYER_STATS:
            suggestions.extend([
                "📊 Bar chart of key stats",
                "📈 Trend line of performance over time",
                "🎯 Radar chart of shooting percentages"
            ])
        elif parsed_query.query_type == QueryType.PLAYER_COMPARISON:
            suggestions.extend([
                "⚖️ Side-by-side comparison chart",
                "📊 Radar chart comparison",
                "📈 Performance trend comparison"
            ])
        
        return suggestions
    
    def _get_fallback_suggestions(self, query: str) -> list:
        """Get fallback suggestions when query fails"""
        return [
            "Try asking about a specific player: 'LeBron James stats'",
            "Ask about team schedules: 'When do the Warriors play next?'",
            "Compare players: 'LeBron vs Curry'",
            "Get shooting stats: 'Curry shooting percentages'"
        ]
    
    def get_query_examples(self) -> dict:
        """Get example queries for different categories"""
        return {
            "player_stats": [
                "What are LeBron's stats this season?",
                "How many points does Curry average?",
                "Show me Giannis' shooting percentages",
                "Embiid rebounds and assists"
            ],
            "comparisons": [
                "Compare LeBron and Curry",
                "Who's better: Giannis or Embiid?",
                "LeBron vs Durant stats",
                "Jokic vs Luka comparison"
            ],
            "team_info": [
                "When do the Warriors play next?",
                "Lakers schedule this week",
                "Celtics upcoming games",
                "Heat next game"
            ],
            "advanced": [
                "LeBron's shooting efficiency this season",
                "Curry's detailed stats with games played",
                "Giannis vs Embiid head to head",
                "Show me visual charts for LeBron's performance"
            ]
        }

def build_enhanced_agent() -> EnhancedNBAAgent:
    """Create an enhanced NBA agent with flexible query parsing"""
    return EnhancedNBAAgent()

class SmartQueryProcessor:
    """Processes queries with intelligent routing and enhancement"""
    
    def __init__(self):
        self.enhanced_agent = build_enhanced_agent()
        self.query_parser = query_parser
        self.query_enhancer = query_enhancer
    
    def process_query(self, query: str) -> dict:
        """Process a query with smart routing and enhancement"""
        # Parse the query
        parsed = self.query_parser.parse(query)
        
        # Determine if this is a simple query that can be handled directly
        if self._is_simple_query(parsed):
            return self._handle_simple_query(parsed)
        else:
            # Use the enhanced agent for complex queries
            return self.enhanced_agent.invoke({"input": query})
    
    def _is_simple_query(self, parsed: ParsedQuery) -> bool:
        """Determine if a query is simple enough for direct processing"""
        # Simple queries have clear entities and specific stat types
        return (
            len(parsed.entities) == 1 and
            parsed.query_type in [QueryType.PLAYER_STATS, QueryType.TEAM_SCHEDULE] and
            parsed.stat_type != "all" and
            not parsed.comparison
        )
    
    def _handle_simple_query(self, parsed: ParsedQuery) -> dict:
        """Handle simple queries directly without agent overhead"""
        try:
            if parsed.query_type == QueryType.PLAYER_STATS:
                # Use the enhanced stats tool directly
                tool = EnhancedStatsTool()
                result = tool._run(f"{parsed.entities[0]} {parsed.stat_type.value} {parsed.season}")
                return {
                    "output": result,
                    "direct_processing": True,
                    "parsed_query": {
                        "query_type": parsed.query_type.value,
                        "entities": parsed.entities,
                        "stat_type": parsed.stat_type.value,
                        "season": parsed.season
                    }
                }
            else:
                # Fall back to agent for other query types
                return self.enhanced_agent.invoke({"input": " ".join(parsed.entities)})
        except Exception as e:
            logger.error(f"Error in simple query processing: {e}")
            return self.enhanced_agent.invoke({"input": " ".join(parsed.entities)})
    
    def get_query_help(self) -> dict:
        """Get help information for different query types"""
        return {
            "player_stats": {
                "description": "Get player statistics and performance data",
                "examples": [
                    "LeBron's points this season",
                    "Curry shooting percentages",
                    "Giannis assists and rebounds",
                    "Embiid stats now"
                ],
                "tips": [
                    "Use first names for common players (LeBron, Curry, Giannis)",
                    "Specify stat types: points, assists, rebounds, shooting",
                    "Add 'this season' or 'last season' for specific time periods"
                ]
            },
            "comparisons": {
                "description": "Compare players head-to-head",
                "examples": [
                    "Compare LeBron and Curry",
                    "Giannis vs Embiid",
                    "Who's better: Luka or Jokic?",
                    "LeBron vs Durant stats"
                ],
                "tips": [
                    "Use 'vs', 'versus', or 'compare' for comparisons",
                    "Compare specific stats: 'LeBron vs Curry shooting'",
                    "Ask 'who's better' for overall comparisons"
                ]
            },
            "team_info": {
                "description": "Get team schedules and information",
                "examples": [
                    "When do the Warriors play next?",
                    "Lakers schedule this week",
                    "Celtics upcoming games",
                    "Heat next game"
                ],
                "tips": [
                    "Use team names or abbreviations (Warriors, GSW)",
                    "Ask about 'next game', 'schedule', or 'upcoming'",
                    "Specify time periods: 'this week', 'next week'"
                ]
            }
        }

def build_smart_processor() -> SmartQueryProcessor:
    """Create a smart query processor with intelligent routing"""
    return SmartQueryProcessor() 