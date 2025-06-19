"""
NBA Agent Performance & Monitoring Tests using Judgment Labs
Tests response times, accuracy benchmarks, and production monitoring
"""

import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import (
    AnswerRelevancyScorer,
    AnswerCorrectnessScorer,  # Using this instead of FactualCorrectnessScorer
    FaithfulnessScorer,
    HallucinationScorer
)
from judgeval.tracer import Tracer
from agent import build_agent

class SimpleLatencyScorer:
    """Simple latency scorer since LatencyScorer is not available"""
    def __init__(self, threshold=5.0):
        self.threshold = threshold
    
    def score(self, response_time):
        """Score based on response time - lower is better"""
        if response_time <= self.threshold:
            return 1.0
        else:
            # Exponential decay for times over threshold
            return max(0.0, 1.0 - (response_time - self.threshold) / self.threshold)

class TestNBAAgentPerformance:
    """Performance and monitoring tests for NBA Agent"""
    
    def __init__(self):
        self.client = JudgmentClient()
        self.judgment = Tracer(project_name="NBA Agent Performance", deep_tracing=False)
        self.agent = build_agent()
        self.project_name = "NBA Agent Performance"
    
    def test_response_time_benchmarks(self):
        """Test response time performance across different query types"""
        
        benchmark_queries = {
            "simple_stats": [
                "What are LeBron's points?",
                "How many assists did Curry have?",
                "Show me Giannis rebounds"
            ],
            "complex_stats": [
                "What are all of LeBron's comprehensive stats this season?",
                "Compare Giannis and Luka across all statistical categories",
                "Who leads in each major statistical category?"
            ],
            "schedule": [
                "When do the Warriors play next?",
                "What is the Lakers next game?",
                "Show me the Celtics schedule"
            ]
        }
        
        performance_results = {}
        
        for category, queries in benchmark_queries.items():
            print(f"\n⏱️ Testing {category.replace('_', ' ').title()} Performance")
            
            times = []
            examples = []
            
            for query in queries:
                start_time = time.time()
                
                response = self.agent.invoke({"input": query})
                result = response.get("output", str(response))
                
                end_time = time.time()
                response_time = end_time - start_time
                times.append(response_time)
                
                print(f"  📊 Query: {query}")
                print(f"  ⏱️ Time: {response_time:.2f}s")
                
                # Create example for evaluation
                example = Example(
                    input=query,
                    actual_output=result,
                    metadata={"response_time": response_time, "category": category}
                )
                examples.append(example)
            
            # Calculate performance metrics
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)
            
            performance_results[category] = {
                "avg_time": avg_time,
                "max_time": max_time,
                "min_time": min_time,
                "times": times
            }
            
            print(f"  📈 Average: {avg_time:.2f}s")
            print(f"  🔴 Slowest: {max_time:.2f}s")
            print(f"  🟢 Fastest: {min_time:.2f}s")
            
            # Simple latency evaluation since LatencyScorer is not available
            latency_scorer = SimpleLatencyScorer(threshold=5.0)
            latency_scores = [latency_scorer.score(t) for t in times]
            avg_latency_score = statistics.mean(latency_scores)
            
            print(f"  ✅ Latency Score: {avg_latency_score:.3f} (avg)")
        
        return performance_results
    
    def test_concurrent_load(self):
        """Test agent performance under concurrent load"""
        
        print("\n🚀 Testing Concurrent Load Performance")
        
        # Test queries for concurrent execution
        concurrent_queries = [
            "What are LeBron's stats?",
            "How many assists did Haliburton have?",
            "When do the Warriors play next?",
            "Show me Giannis rebounds",
            "What are Curry's points this season?",
            "Compare Luka and Giannis stats",
            "Who had the most assists?",
            "What are Kevin Durant's stats?"
        ] * 3  # 24 total queries
        
        def execute_query(query):
            """Execute a single query and measure performance"""
            start_time = time.time()
            
            try:
                response = self.agent.invoke({"input": query})
                result = response.get("output", str(response))
                success = True
                error = None
            except Exception as e:
                result = f"Error: {str(e)}"
                success = False
                error = str(e)
            
            end_time = time.time()
            
            return {
                "query": query,
                "result": result,
                "time": end_time - start_time,
                "success": success,
                "error": error
            }
        
        # Execute queries concurrently
        print(f"  🔄 Executing {len(concurrent_queries)} concurrent queries...")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_query, query) for query in concurrent_queries]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_queries = [r for r in results if r["success"]]
        failed_queries = [r for r in results if not r["success"]]
        
        if successful_queries:
            avg_response_time = statistics.mean([r["time"] for r in successful_queries])
            max_response_time = max([r["time"] for r in successful_queries])
        else:
            avg_response_time = 0
            max_response_time = 0
        
        success_rate = len(successful_queries) / len(results)
        
        print(f"  📊 Total Execution Time: {total_time:.2f}s")
        print(f"  ✅ Success Rate: {success_rate:.1%}")
        print(f"  ⏱️ Average Response Time: {avg_response_time:.2f}s")
        print(f"  🔴 Max Response Time: {max_response_time:.2f}s")
        print(f"  ❌ Failed Queries: {len(failed_queries)}")
        
        # Create examples for evaluation
        examples = []
        for result in successful_queries:
            example = Example(
                input=result["query"],
                actual_output=result["result"],
                metadata={
                    "response_time": result["time"],
                    "concurrent_test": True
                }
            )
            examples.append(example)
        
        # Evaluate concurrent performance
        if examples:
            scorers = [
                AnswerRelevancyScorer(threshold=0.7)
            ]
            
            eval_results = self.client.run_evaluation(
                examples=examples[:10],  # Sample for evaluation
                scorers=scorers,
                model="gpt-4o",
                project_name=f"{self.project_name} - Concurrent Load"
            )
            
            print(f"  📈 Evaluation Results: {eval_results}")
        
        return {
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "max_response_time": max_response_time,
            "failed_queries": len(failed_queries)
        }
    
    @Tracer(project_name="NBA Agent Performance").observe(span_type="function")
    def test_accuracy_benchmarks(self):
        """Test accuracy against known benchmarks"""
        
        print("\n🎯 Testing Accuracy Benchmarks")
        
        # Benchmark test cases with known correct answers
        benchmark_cases = [
            {
                "query": "What is LeBron's PPG this season?",
                "expected_content": ["25.3", "points per game", "lebron"],
                "context": ["LeBron James averages 25.3 PPG in 2024-25"],
                "category": "exact_stats"
            },
            {
                "query": "How many assists does Tyrese Haliburton average?",
                "expected_content": ["10.9", "assists", "haliburton"],
                "context": ["Tyrese Haliburton averages 10.9 APG in 2023-24"],
                "category": "exact_stats"
            },
            {
                "query": "What are Giannis blocks per game?",
                "expected_content": ["1.1", "blocks", "giannis"],
                "context": ["Giannis Antetokounmpo averages 1.1 BPG in 2024-25"],
                "category": "exact_stats"
            }
        ]
        
        accuracy_results = []
        
        for case in benchmark_cases:
            print(f"\n  🔍 Testing: {case['query']}")
            
            response = self.agent.invoke({"input": case["query"]})
            result = response.get("output", str(response))
            
            print(f"  🤖 Response: {result}")
            
            # Check if expected content is present
            content_match = all(
                content.lower() in result.lower() 
                for content in case["expected_content"]
            )
            
            accuracy_results.append({
                "query": case["query"],
                "response": result,
                "content_match": content_match,
                "category": case["category"]
            })
            
            print(f"  ✅ Content Match: {content_match}")
            
            # Create example for detailed evaluation
            example = Example(
                input=case["query"],
                actual_output=result,
                retrieval_context=case["context"]
            )
            
            # Run accuracy evaluations
            scorers = [
                FaithfulnessScorer(threshold=0.8),
                AnswerCorrectnessScorer(threshold=0.8)
            ]
            
            eval_results = self.client.run_evaluation(
                examples=[example],
                scorers=scorers,
                model="gpt-4o",
                project_name=f"{self.project_name} - Accuracy"
            )
            
            print(f"  📊 Evaluation: {eval_results}")
        
        # Calculate overall accuracy
        content_accuracy = sum(r["content_match"] for r in accuracy_results) / len(accuracy_results)
        
        print(f"\n📈 Overall Content Accuracy: {content_accuracy:.1%}")
        
        return accuracy_results
    
    @Tracer(project_name="NBA Agent Performance").observe(span_type="function")
    def test_production_monitoring(self):
        """Test production monitoring scenarios"""
        
        print("\n🏭 Testing Production Monitoring Scenarios")
        
        # Simulate production traffic patterns
        production_queries = [
            "What are LeBron's stats this season?",
            "When do the Warriors play next?",
            "How many assists did Haliburton have?",
            "Compare Giannis and Luka stats",
            "Who leads in rebounds?",
            "What are Curry's shooting stats?",
            "Show me Lakers next games",
            "What are Kevin Durant's blocks?"
        ]
        
        monitoring_results = []
        
        for i, query in enumerate(production_queries):
            print(f"\n  📊 Production Query {i+1}: {query}")
            
            start_time = time.time()
            
            # Simulate production call with monitoring
            response = self.agent.invoke({"input": query})
            result = response.get("output", str(response))
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"  ⏱️ Response Time: {response_time:.2f}s")
            print(f"  📝 Response Length: {len(result)} chars")
            
            # Monitor for quality metrics
            monitoring_data = {
                "query": query,
                "response": result,
                "response_time": response_time,
                "response_length": len(result),
                "timestamp": time.time()
            }
            
            monitoring_results.append(monitoring_data)
            
            # Run online evaluation for production monitoring
            self.judgment.async_evaluate(
                scorers=[
                    AnswerRelevancyScorer(threshold=0.8)
                ],
                input=query,
                actual_output=result,
                model="gpt-4o"
            )
            
            # Simulate alert conditions
            if response_time > 10.0:
                print(f"  🚨 ALERT: High latency detected ({response_time:.2f}s)")
            
            if len(result) < 20:
                print(f"  ⚠️ WARNING: Short response detected ({len(result)} chars)")
            
            # Simulate brief delay between requests
            time.sleep(0.5)
        
        # Production metrics summary
        avg_response_time = statistics.mean([r["response_time"] for r in monitoring_results])
        avg_response_length = statistics.mean([r["response_length"] for r in monitoring_results])
        
        print(f"\n📈 Production Metrics Summary:")
        print(f"  ⏱️ Average Response Time: {avg_response_time:.2f}s")
        print(f"  📝 Average Response Length: {avg_response_length:.0f} chars")
        print(f"  📊 Total Requests: {len(monitoring_results)}")
        
        return monitoring_results
    
    def run_comprehensive_performance_tests(self):
        """Run all performance tests"""
        
        print("🏀 NBA Agent Performance Test Suite")
        print("Built with Judgment Labs 💜")
        print("=" * 60)
        
        results = {}
        
        # Response time benchmarks
        print("\n1️⃣ Response Time Benchmarks")
        results["response_times"] = self.test_response_time_benchmarks()
        
        # Concurrent load testing
        print("\n2️⃣ Concurrent Load Testing")
        results["concurrent_load"] = self.test_concurrent_load()
        
        # Accuracy benchmarks
        print("\n3️⃣ Accuracy Benchmarks")
        results["accuracy"] = self.test_accuracy_benchmarks()
        
        # Production monitoring
        print("\n4️⃣ Production Monitoring")
        results["production"] = self.test_production_monitoring()
        
        # Overall summary
        print(f"\n🎉 Performance Testing Complete!")
        print(f"✅ All performance data sent to Judgment Labs")
        
        return results

if __name__ == "__main__":
    # Initialize and run performance tests
    performance_tester = TestNBAAgentPerformance()
    
    print("⚡ NBA Agent Performance & Monitoring Test Suite")
    print("Built with Judgment Labs 💜")
    print("=" * 60)
    
    # Run comprehensive performance tests
    results = performance_tester.run_comprehensive_performance_tests()
    
    print(f"\n📈 Performance Test Summary:")
    
    # Response time summary
    if "response_times" in results:
        for category, metrics in results["response_times"].items():
            print(f"  ⏱️ {category.title()}: {metrics['avg_time']:.2f}s avg")
    
    # Concurrent load summary
    if "concurrent_load" in results:
        load_results = results["concurrent_load"]
        print(f"  🚀 Concurrent Success Rate: {load_results['success_rate']:.1%}")
        print(f"  🔄 Concurrent Avg Time: {load_results['avg_response_time']:.2f}s")
    
    # Accuracy summary
    if "accuracy" in results:
        accuracy = sum(r["content_match"] for r in results["accuracy"]) / len(results["accuracy"])
        print(f"  🎯 Content Accuracy: {accuracy:.1%}")
    
    print(f"\n✨ Detailed performance metrics available in Judgment Labs dashboard!")
    print(f"🔗 Visit: https://app.judgmentlabs.ai to view your performance data") 