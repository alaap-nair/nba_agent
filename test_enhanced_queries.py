#!/usr/bin/env python3
"""
Test Enhanced Query Flexibility
Demonstrates the improved natural language query capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from query_parser import query_parser, query_enhancer, ParsedQuery, QueryType, StatType
from enhanced_agent import build_smart_processor

def test_query_parsing():
    """Test the enhanced query parser with various natural language queries"""
    print("🧪 **Testing Enhanced Query Parser**")
    print("=" * 50)
    print()
    
    test_queries = [
        # Player stats queries
        "LeBron's points this season",
        "Curry shooting percentages",
        "Giannis assists and rebounds",
        "Embiid stats now",
        "Luka's detailed performance",
        
        # Comparison queries
        "Compare LeBron and Curry",
        "Giannis vs Embiid",
        "Who's better: Luka or Jokic?",
        "LeBron vs Durant shooting",
        
        # Team queries
        "When do the Warriors play next?",
        "Lakers schedule this week",
        "Celtics upcoming games",
        "Heat next game",
        
        # Edge cases
        "Lebron James",  # Simple name
        "Curry",  # Single name
        "GSW next game",  # Abbreviation
        "LAL vs BOS",  # Team comparison
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🎯 **Test {i}:** {query}")
        print("-" * 40)
        
        try:
            parsed = query_parser.parse(query)
            print(f"✅ Parsed successfully!")
            print(f"   Query Type: {parsed.query_type.value}")
            print(f"   Entities: {parsed.entities}")
            print(f"   Stat Type: {parsed.stat_type.value if parsed.stat_type else 'None'}")
            print(f"   Season: {parsed.season}")
            print(f"   Comparison: {parsed.comparison}")
            print(f"   Context: {parsed.context}")
            
            # Test suggestions
            suggestions = query_enhancer.suggest_queries(parsed)
            if suggestions:
                print(f"   Suggestions: {suggestions[:2]}")
            
        except Exception as e:
            print(f"❌ Error parsing: {e}")
        
        print()

def test_fuzzy_matching():
    """Test fuzzy matching capabilities"""
    print("🔍 **Testing Fuzzy Matching**")
    print("=" * 50)
    print()
    
    # Test player name variations
    player_variations = [
        "Lebron", "LeBron", "LeBron James", "LBJ",
        "Curry", "Stephen Curry", "Steph",
        "Giannis", "Giannis Antetokounmpo", "Greek Freak",
        "Embiid", "Joel Embiid",
        "Luka", "Luka Doncic", "Doncic"
    ]
    
    for name in player_variations:
        print(f"🎯 Testing: '{name}'")
        try:
            # This would normally use the actual player database
            # For demo purposes, we'll just show the parsing
            parsed = query_parser.parse(f"{name} stats")
            print(f"   ✅ Parsed as: {parsed.entities}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

def test_query_enhancement():
    """Test query enhancement and suggestions"""
    print("💡 **Testing Query Enhancement**")
    print("=" * 50)
    print()
    
    base_queries = [
        "LeBron stats",
        "Curry shooting",
        "Giannis vs Embiid"
    ]
    
    for query in base_queries:
        print(f"🎯 Base Query: {query}")
        try:
            parsed = query_parser.parse(query)
            suggestions = query_enhancer.suggest_queries(parsed)
            expanded = query_enhancer.expand_query(query)
            
            print(f"   Suggestions: {suggestions}")
            print(f"   Expanded: {expanded}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

def test_smart_processor():
    """Test the smart query processor"""
    print("🧠 **Testing Smart Query Processor**")
    print("=" * 50)
    print()
    
    # Initialize processor
    try:
        processor = build_smart_processor()
        print("✅ Smart processor initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ Error initializing processor: {e}")
        return
    
    # Test queries
    test_queries = [
        "LeBron's points this season",
        "Compare Curry and Giannis",
        "When do the Warriors play next?"
    ]
    
    for query in test_queries:
        print(f"🎯 Processing: {query}")
        try:
            response = processor.process_query(query)
            print(f"   ✅ Response received")
            print(f"   Output length: {len(str(response.get('output', '')))} chars")
            
            if "parsed_query" in response:
                parsed = response["parsed_query"]
                print(f"   Query Type: {parsed.get('query_type', 'Unknown')}")
                print(f"   Entities: {parsed.get('entities', [])}")
            
            if "query_confidence" in response:
                confidence = response["query_confidence"]
                print(f"   Confidence: {confidence:.1%}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

def run_demo():
    """Run a comprehensive demo of the enhanced query capabilities"""
    print("🎬 **Enhanced Query Flexibility Demo**")
    print("=" * 60)
    print()
    
    print("This demo showcases the improved natural language query capabilities")
    print("of the NBA Agent, including:")
    print("• Flexible query parsing")
    print("• Fuzzy name matching")
    print("• Smart suggestions")
    print("• Context awareness")
    print("• Query enhancement")
    print()
    
    # Run all tests
    test_query_parsing()
    test_fuzzy_matching()
    test_query_enhancement()
    test_smart_processor()
    
    print("🎉 **Demo completed!**")
    print()
    print("💡 **Key Improvements:**")
    print("✅ Natural language queries (no rigid format)")
    print("✅ Fuzzy name matching (handles typos and variations)")
    print("✅ Smart suggestions for similar queries")
    print("✅ Context-aware responses")
    print("✅ Query confidence scoring")
    print("✅ Intelligent query routing")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        print("🧪 **Enhanced Query Flexibility Tests**")
        print("Run with 'demo' argument for full demonstration")
        print()
        test_query_parsing()
        test_fuzzy_matching()
        test_query_enhancement() 