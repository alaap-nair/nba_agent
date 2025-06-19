"""
NBA Agent Evaluation Tests using Judgment Labs
Tests the accuracy, relevancy, and faithfulness of NBA agent responses
"""

import pytest
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import (
    FaithfulnessScorer, 
    AnswerRelevancyScorer, 
    AnswerCorrectnessScorer,
    HallucinationScorer
)
from agent import build_agent
import time
import uuid

class TestNBAAgentEvaluation:
    """Comprehensive evaluation tests for the NBA Agent"""
    
    @classmethod
    def setup_class(cls):
        """Setup the NBA agent and Judgment client"""
        cls.client = JudgmentClient()
        cls.agent = build_agent()
        cls.project_name = "NBA Agent Evaluation"
        
    def create_example(self, input_query, expected_context=None, ground_truth=None):
        """Helper to create an example and get agent response"""
        response = self.agent.invoke({"input": input_query})
        actual_output = response.get("output", str(response))
        
        return Example(
            input=input_query,
            actual_output=actual_output,
            retrieval_context=expected_context or [],
            expected_output=ground_truth
        )
    
    def get_unique_run_name(self, base_name):
        """Generate unique run name to avoid conflicts"""
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"{base_name}_{timestamp}_{unique_id}"
    
    def test_player_stats_faithfulness(self):
        """Test if player stats responses are faithful to the underlying data"""
        
        # Test cases for player stats
        test_cases = [
            {
                "query": "What are LeBron's stats this season?",
                "context": ["LeBron James averages 25.3 PPG, 7.8 APG, 8.1 RPG in 2024-25 season"],
                "description": "LeBron comprehensive stats"
            },
            {
                "query": "How many assists did Tyler Herro have this season?",
                "context": ["Tyler Herro averages 4.5 assists per game in the 2023-24 season"],
                "description": "Tyler Herro assists"
            },
            {
                "query": "What were Giannis rebounds in 2024-25?",
                "context": ["Giannis Antetokounmpo averages 11.5 rebounds per game in 2024-25 season"],
                "description": "Giannis rebounds"
            }
        ]
        
        examples = []
        for case in test_cases:
            example = self.create_example(case["query"], case["context"])
            examples.append(example)
            print(f"Testing: {case['description']}")
            print(f"Query: {case['query']}")
            print(f"Response: {example.actual_output}")
            print("---")
        
        # Run faithfulness evaluation with unique name
        scorer = FaithfulnessScorer(threshold=0.7)
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=[scorer],
            model="gpt-4o",
            project_name=self.project_name
        )
        
        print(f"\nFaithfulness Results: {len(results)} examples evaluated")
        
        # Count successful results
        success_count = sum(1 for result in results if result.success and len(result.scorers_data) > 0 and result.scorers_data[0].score >= 0.7)
        assert success_count >= len(examples) * 0.8
        
    def test_answer_relevancy(self):
        """Test if agent responses are relevant to the questions asked"""
        
        test_cases = [
            "Who had the most points this season?",
            "When do the Warriors play next?", 
            "What are all of Luka's stats?",
            "How many blocks did Kevin Durant get?",
            "Show me Curry's assists numbers",
            "What were the Pacers last game stats?"
        ]
        
        examples = []
        for query in test_cases:
            example = self.create_example(query)
            examples.append(example)
            print(f"Query: {query}")
            print(f"Response: {example.actual_output}")
            print("---")
        
        # Run answer relevancy evaluation
        scorer = AnswerRelevancyScorer(threshold=0.8)
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=[scorer],
            model="gpt-4o", 
            project_name=self.project_name
        )
        
        print(f"\nAnswer Relevancy Results: {len(results)} examples evaluated")
        
        # Count successful results
        success_count = sum(1 for result in results if result.success and len(result.scorers_data) > 0 and result.scorers_data[0].score >= 0.8)
        assert success_count >= len(examples) * 0.9
        
    def test_factual_correctness(self):
        """Test factual correctness of NBA statistics"""
        
        test_cases = [
            {
                "query": "What is LeBron's PPG this season?",
                "ground_truth": "LeBron James averages 25.3 points per game this season",
                "context": ["LeBron James: 25.3 PPG in 2024-25"]
            },
            {
                "query": "How many assists does Tyrese Haliburton average?",
                "ground_truth": "Tyrese Haliburton averages 10.9 assists per game",
                "context": ["Tyrese Haliburton: 10.9 APG in 2023-24"]
            },
            {
                "query": "What are Giannis blocks per game?",
                "ground_truth": "Giannis Antetokounmpo averages 1.1 blocks per game",
                "context": ["Giannis Antetokounmpo: 1.1 BPG in 2024-25"]
            }
        ]
        
        examples = []
        for case in test_cases:
            example = self.create_example(
                case["query"], 
                case["context"], 
                case["ground_truth"]
            )
            examples.append(example)
        
        # Run factual correctness evaluation using AnswerCorrectnessScorer
        scorer = AnswerCorrectnessScorer(threshold=0.75)
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=[scorer],
            model="gpt-4o",
            project_name=self.project_name
        )
        
        print(f"\nFactual Correctness Results: {len(results)} examples evaluated")
        
        # Count successful results
        success_count = sum(1 for result in results if result.success and len(result.scorers_data) > 0 and result.scorers_data[0].score >= 0.75)
        assert success_count >= len(examples) * 0.8
        
    def test_response_coherence(self):
        """Test if agent responses are coherent and well-structured"""
        
        test_cases = [
            "Compare LeBron and Giannis stats this season",
            "Who are the top 3 scorers in the NBA right now?",
            "What makes Luka Dončić such a good player statistically?",
            "Explain the difference between Curry and Haliburton's assist numbers"
        ]
        
        examples = []
        for query in test_cases:
            example = self.create_example(query)
            examples.append(example)
        
        # Run coherence evaluation using AnswerCorrectnessScorer as a proxy
        scorer = AnswerCorrectnessScorer(threshold=0.8)
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=[scorer],
            model="gpt-4o",
            project_name=self.project_name
        )
        
        print(f"\nCoherence Results: {len(results)} examples evaluated")
        
        # Count successful results  
        success_count = sum(1 for result in results if result.success and len(result.scorers_data) > 0 and result.scorers_data[0].score >= 0.8)
        assert success_count >= len(examples) * 0.85
        
    def test_hallucination_detection(self):
        """Test for hallucinations in agent responses"""
        
        # Test with queries that might lead to hallucinations
        test_cases = [
            {
                "query": "What are Michael Jordan's stats this season?", 
                "context": ["Michael Jordan retired from professional basketball"],
                "description": "Retired player query"
            },
            {
                "query": "How many points did LeBron score in the 2025-26 season?",
                "context": ["The 2025-26 season has not occurred yet"],
                "description": "Future season query"
            },
            {
                "query": "What team does Kobe Bryant play for currently?",
                "context": ["Kobe Bryant passed away in 2020"],
                "description": "Deceased player query"
            }
        ]
        
        examples = []
        for case in test_cases:
            example = self.create_example(case["query"], case["context"])
            examples.append(example)
            print(f"Testing: {case['description']}")
            print(f"Response: {example.actual_output}")
        
        # Run hallucination detection
        scorer = HallucinationScorer(threshold=0.2)  # Lower threshold for hallucination
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=[scorer],
            model="gpt-4o",
            project_name=self.project_name
        )
        
        print(f"\nHallucination Results: {len(results)} examples evaluated")
        
        # Count good results (low hallucination scores)
        success_count = sum(1 for result in results if result.success and len(result.scorers_data) > 0 and result.scorers_data[0].score <= 0.3)
        assert success_count >= len(examples) * 0.7
        
    def test_comprehensive_evaluation(self):
        """Run a comprehensive evaluation with multiple scorers"""
        
        comprehensive_queries = [
            "What are all of LeBron James' 2024-25 season statistics?",
            "How do Tyler Herro's assists compare to other guards?",
            "When is the next Warriors game scheduled?",
            "Who leads the league in rebounds this season?",
            "Compare Giannis and Luka's overall performance"
        ]
        
        examples = []
        for query in comprehensive_queries:
            example = self.create_example(query)
            examples.append(example)
        
        # Multiple scorers for comprehensive evaluation
        scorers = [
            FaithfulnessScorer(threshold=0.7),
            AnswerRelevancyScorer(threshold=0.8),
            AnswerCorrectnessScorer(threshold=0.8),
            HallucinationScorer(threshold=0.3)
        ]
        
        results = self.client.run_evaluation(
            examples=examples,
            scorers=scorers,
            model="gpt-4o",
            project_name=f"{self.project_name} - Comprehensive"
        )
        
        print(f"\nComprehensive Evaluation Results: {len(results)} examples evaluated")
        
        # Count overall success (at least 75% of scorer-example combinations should pass)
        total_scorer_results = 0
        successful_scorer_results = 0
        
        for result in results:
            if result.success:
                for scorer_data in result.scorers_data:
                    total_scorer_results += 1
                    if scorer_data.score >= 0.7:  # General threshold
                        successful_scorer_results += 1
        
        success_rate = successful_scorer_results / total_scorer_results if total_scorer_results > 0 else 0
        
        print(f"Overall Success Rate: {success_rate:.2%}")
        assert success_rate >= 0.75  # 75% success rate threshold

if __name__ == "__main__":
    # Run the tests
    test_suite = TestNBAAgentEvaluation()
    test_suite.setup_class()
    
    print("🏀 Starting NBA Agent Evaluation Tests")
    print("=" * 50)
    
    try:
        test_suite.test_player_stats_faithfulness()
        print("✅ Player Stats Faithfulness Test Passed")
    except Exception as e:
        print(f"❌ Player Stats Faithfulness Test Failed: {e}")
    
    try:
        test_suite.test_answer_relevancy()
        print("✅ Answer Relevancy Test Passed") 
    except Exception as e:
        print(f"❌ Answer Relevancy Test Failed: {e}")
    
    try:
        test_suite.test_factual_correctness()
        print("✅ Factual Correctness Test Passed")
    except Exception as e:
        print(f"❌ Factual Correctness Test Failed: {e}")
    
    try:
        test_suite.test_response_coherence()
        print("✅ Response Coherence Test Passed")
    except Exception as e:
        print(f"❌ Response Coherence Test Failed: {e}")
    
    try:
        test_suite.test_hallucination_detection()
        print("✅ Hallucination Detection Test Passed")
    except Exception as e:
        print(f"❌ Hallucination Detection Test Failed: {e}")
    
    try:
        test_suite.test_comprehensive_evaluation()
        print("✅ Comprehensive Evaluation Test Passed")
    except Exception as e:
        print(f"❌ Comprehensive Evaluation Test Failed: {e}")
    
    print("\n🎉 NBA Agent Evaluation Complete!") 