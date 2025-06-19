"""
NBA Agent Dataset Builder using Judgment Labs
Creates comprehensive datasets for testing and evaluation
"""

import json
import random
from datetime import datetime, timedelta
from judgeval import JudgmentClient
from judgeval.data import Example
from agent import build_agent

class NBAAgentDatasetBuilder:
    """Build comprehensive datasets for NBA agent testing"""
    
    def __init__(self):
        self.client = JudgmentClient()
        self.agent = build_agent()
        
        # Ground truth data for validation
        self.ground_truth_stats = {
            "LeBron James": {
                "points": 25.3, "assists": 7.8, "rebounds": 8.1,
                "steals": 1.3, "blocks": 0.6, "season": "2024-25"
            },
            "Giannis Antetokounmpo": {
                "points": 32.7, "assists": 6.1, "rebounds": 11.5,
                "steals": 1.2, "blocks": 1.1, "season": "2024-25"
            },
            "Luka Dončić": {
                "points": 28.1, "assists": 8.3, "rebounds": 8.8,
                "steals": 1.4, "blocks": 0.5, "season": "2024-25"
            },
            "Stephen Curry": {
                "points": 22.4, "assists": 6.8, "rebounds": 5.0,
                "steals": 1.3, "blocks": 0.4, "season": "2024-25"
            },
            "Tyrese Haliburton": {
                "points": 20.1, "assists": 10.9, "rebounds": 4.4,
                "steals": 1.3, "blocks": 0.7, "season": "2023-24"
            },
            "Tyler Herro": {
                "points": 20.8, "assists": 4.5, "rebounds": 5.6,
                "steals": 0.8, "blocks": 0.4, "season": "2023-24"
            },
            "Kevin Durant": {
                "points": 27.3, "assists": 5.0, "rebounds": 6.7,
                "steals": 0.9, "blocks": 1.5, "season": "2024-25"
            }
        }
        
        self.team_schedules = {
            "Warriors": ["vs Lakers 2024-12-28", "@ Celtics 2024-12-30", "vs Suns 2025-01-02"],
            "Lakers": ["@ Warriors 2024-12-28", "vs Nuggets 2024-12-31", "@ Heat 2025-01-03"],
            "Celtics": ["vs Heat 2024-12-29", "vs Warriors 2024-12-30", "@ Knicks 2025-01-01"]
        }
    
    def create_stats_dataset(self, size=50):
        """Create a comprehensive stats testing dataset"""
        
        print(f"📊 Creating Stats Dataset (size: {size})")
        
        examples = []
        query_templates = [
            "What are {player}'s stats this season?",
            "How many {stat} did {player} have?",
            "Show me {player} {stat} numbers",
            "What is {player}'s {stat} per game?",
            "Compare {player1} and {player2} {stat}",
            "Who has more {stat}, {player1} or {player2}?",
            "What are all of {player}'s statistics?",
            "Tell me {player}'s season averages"
        ]
        
        stat_types = ["points", "assists", "rebounds", "steals", "blocks"]
        players = list(self.ground_truth_stats.keys())
        
        for i in range(size):
            template = random.choice(query_templates)
            
            if "{player1}" in template and "{player2}" in template:
                # Comparison query
                player1, player2 = random.sample(players, 2)
                stat = random.choice(stat_types)
                query = template.format(player1=player1, player2=player2, stat=stat)
                
                # Create expected output
                p1_stat = self.ground_truth_stats[player1][stat]
                p2_stat = self.ground_truth_stats[player2][stat]
                expected = f"{player1}: {p1_stat} {stat}, {player2}: {p2_stat} {stat}"
                context = [f"{player1} averages {p1_stat} {stat} per game", 
                          f"{player2} averages {p2_stat} {stat} per game"]
                
            elif "{stat}" in template:
                # Single player, specific stat
                player = random.choice(players)
                stat = random.choice(stat_types)
                query = template.format(player=player, stat=stat)
                
                stat_value = self.ground_truth_stats[player][stat]
                expected = f"{player} averages {stat_value} {stat} per game"
                context = [f"{player}: {stat_value} {stat} per game in {self.ground_truth_stats[player]['season']}"]
                
            else:
                # All stats query
                player = random.choice(players)
                query = template.format(player=player)
                
                stats = self.ground_truth_stats[player]
                expected = f"{player} averages {stats['points']} PPG, {stats['assists']} APG, {stats['rebounds']} RPG"
                context = [f"{player} season stats: {stats['points']} PPG, {stats['assists']} APG, {stats['rebounds']} RPG, {stats['steals']} SPG, {stats['blocks']} BPG"]
            
            # Get actual agent response
            response = self.agent.invoke({"input": query})
            actual_output = response.get("output", str(response))
            
            example = Example(
                input=query,
                actual_output=actual_output,
                expected_output=expected,
                retrieval_context=context,
                metadata={
                    "category": "stats",
                    "players": [player] if "{player1}" not in template else [player1, player2],
                    "stat_type": stat if "{stat}" in template else "comprehensive",
                    "query_type": template
                }
            )
            
            examples.append(example)
            
            if i % 10 == 0:
                print(f"  📈 Generated {i+1}/{size} examples")
        
        print(f"✅ Stats dataset created with {len(examples)} examples")
        return examples
    
    def create_schedule_dataset(self, size=20):
        """Create a schedule testing dataset"""
        
        print(f"📅 Creating Schedule Dataset (size: {size})")
        
        examples = []
        query_templates = [
            "When do the {team} play next?",
            "What is the {team} next game?",
            "Show me {team} upcoming schedule",
            "When is the next {team} game?",
            "What are the {team} next 3 games?"
        ]
        
        teams = list(self.team_schedules.keys())
        
        for i in range(size):
            template = random.choice(query_templates)
            team = random.choice(teams)
            query = template.format(team=team)
            
            # Create expected output based on schedule
            next_games = self.team_schedules[team]
            expected = f"Next {team} games: " + ", ".join(next_games[:3])
            context = [f"{team} upcoming schedule: {', '.join(next_games)}"]
            
            # Get actual agent response
            response = self.agent.invoke({"input": query})
            actual_output = response.get("output", str(response))
            
            example = Example(
                input=query,
                actual_output=actual_output,
                expected_output=expected,
                retrieval_context=context,
                metadata={
                    "category": "schedule",
                    "team": team,
                    "query_type": template
                }
            )
            
            examples.append(example)
            
            if i % 5 == 0:
                print(f"  📅 Generated {i+1}/{size} examples")
        
        print(f"✅ Schedule dataset created with {len(examples)} examples")
        return examples
    
    def create_complex_dataset(self, size=30):
        """Create a dataset with complex, multi-step queries"""
        
        print(f"🧠 Creating Complex Query Dataset (size: {size})")
        
        examples = []
        complex_templates = [
            "Who has the highest combined points, rebounds, and assists?",
            "Compare the top 3 scorers and their other stats",
            "Which player is more well-rounded, {player1} or {player2}?",
            "Who leads in each major statistical category?",
            "What player has the best overall performance this season?",
            "Find the player with the most balanced stat line",
            "Who contributes more to their team, {player1} or {player2}?",
            "Show me the statistical leaders in each category",
            "Which players are averaging a triple-double?",
            "Compare defensive stats across all players"
        ]
        
        players = list(self.ground_truth_stats.keys())
        
        for i in range(size):
            template = random.choice(complex_templates)
            
            if "{player1}" in template and "{player2}" in template:
                player1, player2 = random.sample(players, 2)
                query = template.format(player1=player1, player2=player2)
                
                # Complex expected output
                p1_stats = self.ground_truth_stats[player1]
                p2_stats = self.ground_truth_stats[player2]
                expected = f"Comparing {player1} and {player2} across multiple statistical categories"
                context = [
                    f"{player1}: {p1_stats['points']} PPG, {p1_stats['assists']} APG, {p1_stats['rebounds']} RPG",
                    f"{player2}: {p2_stats['points']} PPG, {p2_stats['assists']} APG, {p2_stats['rebounds']} RPG"
                ]
            else:
                query = template
                expected = "Analysis of multiple players across various statistical categories"
                context = []
                for player, stats in self.ground_truth_stats.items():
                    context.append(f"{player}: {stats['points']} PPG, {stats['assists']} APG, {stats['rebounds']} RPG")
            
            # Get actual agent response
            response = self.agent.invoke({"input": query})
            actual_output = response.get("output", str(response))
            
            example = Example(
                input=query,
                actual_output=actual_output,
                expected_output=expected,
                retrieval_context=context,
                metadata={
                    "category": "complex",
                    "complexity": "multi-step",
                    "query_type": template
                }
            )
            
            examples.append(example)
            
            if i % 5 == 0:
                print(f"  🧠 Generated {i+1}/{size} examples")
        
        print(f"✅ Complex dataset created with {len(examples)} examples")
        return examples
    
    def create_edge_case_dataset(self, size=20):
        """Create a dataset with edge cases and error scenarios"""
        
        print(f"⚠️ Creating Edge Case Dataset (size: {size})")
        
        examples = []
        edge_cases = [
            # Retired/Invalid players
            "What are Michael Jordan's stats this season?",
            "How many points did Kobe Bryant score this year?",
            "Show me Magic Johnson's current stats",
            
            # Future/Invalid seasons
            "What were LeBron's stats in 2030?",
            "How did Curry perform in the 2025-26 season?",
            "Show me next year's MVP stats",
            
            # Invalid teams
            "When do the Seattle SuperSonics play next?",
            "What is the Vancouver Grizzlies schedule?",
            "Show me the Baltimore Bullets games",
            
            # Nonsensical queries
            "What team does Superman play for?",
            "How many assists did my dog have?",
            "Show me the stats for the year 1800",
            "What are the basketball stats for Mars?",
            
            # Ambiguous queries
            "What are the stats?",
            "When is the game?",
            "Who won?",
            "Show me the numbers",
            
            # Impossible stats
            "Who scored 200 points in a game?",
            "What player has 50 assists per game?",
            "Show me someone with 100 rebounds per game"
        ]
        
        for query in edge_cases[:size]:
            # Get actual agent response
            response = self.agent.invoke({"input": query})
            actual_output = response.get("output", str(response))
            
            # Determine edge case type
            if any(name in query.lower() for name in ["jordan", "kobe", "magic"]):
                case_type = "retired_player"
                expected = "This player is retired and does not have current season stats"
            elif any(year in query for year in ["2030", "2025-26", "next year"]):
                case_type = "future_season"
                expected = "This season has not occurred yet"
            elif any(team in query for team in ["supersonic", "grizzlies", "bullets"]):
                case_type = "invalid_team"
                expected = "This team does not currently exist in the NBA"
            elif any(word in query.lower() for word in ["superman", "dog", "mars"]):
                case_type = "nonsensical"
                expected = "This query does not relate to valid NBA entities"
            elif len(query.split()) < 4:
                case_type = "ambiguous"
                expected = "This query is too ambiguous to provide specific information"
            else:
                case_type = "impossible_stat"
                expected = "These statistical values are not realistic for NBA players"
            
            example = Example(
                input=query,
                actual_output=actual_output,
                expected_output=expected,
                retrieval_context=[],
                metadata={
                    "category": "edge_case",
                    "edge_case_type": case_type,
                    "should_handle_gracefully": True
                }
            )
            
            examples.append(example)
        
        print(f"✅ Edge case dataset created with {len(examples)} examples")
        return examples
    
    def save_dataset(self, examples, name, description=""):
        """Save dataset to JSON file and optionally to Judgment Labs"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"datasets/nba_agent_{name}_{timestamp}.json"
        
        # Create datasets directory if it doesn't exist
        import os
        os.makedirs("datasets", exist_ok=True)
        
        # Convert examples to JSON-serializable format
        dataset_data = {
            "name": name,
            "description": description,
            "created_at": timestamp,
            "size": len(examples),
            "examples": []
        }
        
        for example in examples:
            example_data = {
                "input": example.input,
                "actual_output": example.actual_output,
                "expected_output": example.expected_output,
                "retrieval_context": example.retrieval_context,
                "metadata": example.metadata
            }
            dataset_data["examples"].append(example_data)
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(dataset_data, f, indent=2)
        
        print(f"💾 Dataset saved to {filename}")
        
        # Note: Judgment Labs dataset upload would be done here
        # when Dataset class becomes available in future versions
        print(f"📝 Dataset ready for use with Judgment Labs evaluations")
        
        return filename
    
    def build_comprehensive_datasets(self):
        """Build all datasets for comprehensive testing"""
        
        print("🏀 NBA Agent Comprehensive Dataset Builder")
        print("=" * 60)
        
        datasets = {}
        
        # Stats dataset
        print("\n1️⃣ Building Stats Dataset...")
        stats_examples = self.create_stats_dataset(50)
        stats_file = self.save_dataset(
            stats_examples, 
            "stats", 
            "Comprehensive player statistics queries and responses"
        )
        datasets["stats"] = {"examples": stats_examples, "file": stats_file}
        
        # Schedule dataset
        print("\n2️⃣ Building Schedule Dataset...")
        schedule_examples = self.create_schedule_dataset(20)
        schedule_file = self.save_dataset(
            schedule_examples,
            "schedule",
            "Team schedule and game information queries"
        )
        datasets["schedule"] = {"examples": schedule_examples, "file": schedule_file}
        
        # Complex dataset
        print("\n3️⃣ Building Complex Query Dataset...")
        complex_examples = self.create_complex_dataset(30)
        complex_file = self.save_dataset(
            complex_examples,
            "complex",
            "Multi-step reasoning and comparison queries"
        )
        datasets["complex"] = {"examples": complex_examples, "file": complex_file}
        
        # Edge case dataset
        print("\n4️⃣ Building Edge Case Dataset...")
        edge_examples = self.create_edge_case_dataset(20)
        edge_file = self.save_dataset(
            edge_examples,
            "edge_cases",
            "Error handling and edge case scenarios"
        )
        datasets["edge_cases"] = {"examples": edge_examples, "file": edge_file}
        
        # Combined dataset
        print("\n5️⃣ Building Combined Dataset...")
        all_examples = stats_examples + schedule_examples + complex_examples + edge_examples
        combined_file = self.save_dataset(
            all_examples,
            "comprehensive",
            "Complete NBA agent testing dataset with all categories"
        )
        datasets["comprehensive"] = {"examples": all_examples, "file": combined_file}
        
        print(f"\n🎉 Dataset Building Complete!")
        print(f"📊 Total Examples: {len(all_examples)}")
        print(f"  📈 Stats: {len(stats_examples)}")
        print(f"  📅 Schedule: {len(schedule_examples)}")
        print(f"  🧠 Complex: {len(complex_examples)}")
        print(f"  ⚠️ Edge Cases: {len(edge_examples)}")
        
        return datasets

if __name__ == "__main__":
    # Build comprehensive datasets
    builder = NBAAgentDatasetBuilder()
    
    print("📊 NBA Agent Dataset Builder")
    print("Built with Judgment Labs 💜")
    print("=" * 50)
    
    datasets = builder.build_comprehensive_datasets()
    
    print(f"\n✨ All datasets created and ready for testing!")
    print(f"📁 Datasets saved in 'datasets/' directory")
    print(f"🔗 Use these datasets with Judgment Labs for comprehensive evaluation") 