#!/usr/bin/env python3
"""
Enhanced NBA Agent Chat with Flexible Query Parsing
Demonstrates natural language query capabilities and improved user experience
"""

import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from enhanced_agent import build_enhanced_agent, build_smart_processor
from query_parser import query_parser, query_enhancer

def print_banner():
    """Print a beautiful banner for the enhanced chat"""
    print("🏀" * 20)
    print("   NBA Agent Pro - Enhanced Chat")
    print("   Natural Language Query Support")
    print("🏀" * 20)
    print()

def print_query_examples():
    """Print example queries to help users"""
    print("💡 **Natural Language Query Examples:**")
    print()
    
    examples = {
        "Player Stats": [
            "LeBron's points this season",
            "Curry shooting percentages", 
            "Giannis assists and rebounds",
            "Embiid stats now",
            "Luka's detailed performance"
        ],
        "Comparisons": [
            "Compare LeBron and Curry",
            "Giannis vs Embiid",
            "Who's better: Luka or Jokic?",
            "LeBron vs Durant shooting"
        ],
        "Team Info": [
            "When do the Warriors play next?",
            "Lakers schedule this week",
            "Celtics upcoming games",
            "Heat next game"
        ],
        "Advanced": [
            "LeBron's shooting efficiency this season",
            "Curry's detailed stats with games played",
            "Giannis vs Embiid head to head",
            "Show me visual charts for LeBron's performance"
        ]
    }
    
    for category, queries in examples.items():
        print(f"📊 **{category}:**")
        for query in queries:
            print(f"   • {query}")
        print()

def print_query_help():
    """Print detailed query help"""
    print("🔍 **Query Flexibility Features:**")
    print()
    print("✅ **Natural Language Support:**")
    print("   • Use conversational queries")
    print("   • No rigid format required")
    print("   • Fuzzy name matching")
    print()
    print("✅ **Smart Suggestions:**")
    print("   • Similar player/team suggestions")
    print("   • Query expansion options")
    print("   • Context-aware responses")
    print()
    print("✅ **Flexible Stat Types:**")
    print("   • Points, assists, rebounds, steals, blocks")
    print("   • Shooting percentages (FG%, 3P%, FT%)")
    print("   • Efficiency metrics")
    print("   • All stats or specific categories")
    print()
    print("✅ **Time Period Support:**")
    print("   • This season, last season, next season")
    print("   • Specific years (2024-25, 2023-24)")
    print("   • Current, previous, upcoming")
    print()

def format_response(response):
    """Format the enhanced response for display"""
    if isinstance(response, dict):
        output = response.get("output", str(response))
        
        # Add parsed query info if available
        if "parsed_query" in response:
            parsed = response["parsed_query"]
            print(f"\n🔍 **Query Analysis:**")
            print(f"   Type: {parsed.get('query_type', 'Unknown')}")
            print(f"   Entities: {', '.join(parsed.get('entities', []))}")
            if parsed.get('stat_type'):
                print(f"   Stat Type: {parsed['stat_type']}")
            if parsed.get('season'):
                print(f"   Season: {parsed['season']}")
            if parsed.get('comparison'):
                print(f"   Comparison: Yes")
            print()
        
        # Add confidence score if available
        if "query_confidence" in response:
            confidence = response["query_confidence"]
            print(f"🎯 **Query Confidence:** {confidence:.1%}")
            print()
        
        # Add suggestions if available
        if "suggestions" in response and response["suggestions"]:
            print(f"💡 **Related Queries:**")
            for suggestion in response["suggestions"]:
                print(f"   • {suggestion}")
            print()
        
        # Add visual suggestions if available
        if "visual_suggestions" in response and response["visual_suggestions"]:
            print(f"📊 **Visual Suggestions:**")
            for suggestion in response["visual_suggestions"]:
                print(f"   • {suggestion}")
            print()
        
        return output
    else:
        return str(response)

def main():
    """Main enhanced chat interface"""
    print_banner()
    print_query_examples()
    
    # Ask user if they want to see detailed help
    help_choice = input("📚 Would you like to see detailed query help? (y/n): ").strip().lower()
    if help_choice in ['y', 'yes']:
        print_query_help()
    
    print("🚀 **Starting Enhanced NBA Agent...**")
    print("   (This may take a moment to initialize)")
    print()
    
    # Initialize the enhanced agent
    try:
        # Use smart processor for better performance
        processor = build_smart_processor()
        print("✅ Enhanced agent loaded successfully!")
        print()
    except Exception as e:
        print(f"❌ Error loading enhanced agent: {e}")
        print("Falling back to basic agent...")
        processor = build_enhanced_agent()
    
    print("🎯 **Ready for natural language queries!**")
    print("Type 'help' for query examples, 'quit' to exit.")
    print("=" * 60)
    print()
    
    while True:
        try:
            # Get user input
            query = input("🤔 Ask me anything: ").strip()
            
            # Check for exit commands
            if query.lower() in ['quit', 'exit', 'bye', 'stop']:
                print("👋 Thanks for using the Enhanced NBA Agent!")
                break
            
            if query.lower() in ['help', 'examples']:
                print_query_examples()
                continue
            
            if not query:
                continue
            
            # Process the query
            print("🤖 Processing your query...")
            response = processor.process_query(query)
            
            # Format and display the response
            output = format_response(response)
            print(f"📊 {output}")
            print()
            
            # Show query confidence and suggestions
            if isinstance(response, dict):
                if "query_confidence" in response:
                    confidence = response["query_confidence"]
                    if confidence < 0.7:
                        print("⚠️  **Low confidence query detected.**")
                        print("   Try being more specific or check spelling.")
                        print()
                
                if "suggestions" in response and response["suggestions"]:
                    print("💡 **Try these related queries:**")
                    for i, suggestion in enumerate(response["suggestions"][:3], 1):
                        print(f"   {i}. {suggestion}")
                    print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Sorry, I encountered an error: {e}")
            print("Please try rephrasing your query.")
            print()

def demo_mode():
    """Run a demonstration of the enhanced query capabilities"""
    print("🎬 **Enhanced NBA Agent Demo Mode**")
    print("=" * 50)
    print()
    
    # Initialize processor
    processor = build_smart_processor()
    
    # Demo queries
    demo_queries = [
        "LeBron's points this season",
        "Compare Curry and Giannis",
        "When do the Warriors play next?",
        "Embiid shooting percentages",
        "Luka vs Jokic stats"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"🎯 **Demo Query {i}:** {query}")
        print("-" * 40)
        
        try:
            response = processor.process_query(query)
            output = format_response(response)
            print(f"📊 Response: {output}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        input("Press Enter for next demo query...")
        print()
    
    print("🎉 **Demo completed!**")
    print("Try the interactive mode for your own queries.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        main() 