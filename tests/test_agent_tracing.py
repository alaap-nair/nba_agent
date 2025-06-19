"""
NBA Agent Tracing Tests using Judgment Labs
Tests and traces the NBA agent's tool calls, LLM interactions, and decision making
"""

from judgeval.tracer import Tracer
from judgeval.scorers import AnswerRelevancyScorer, AnswerCorrectnessScorer, HallucinationScorer
from agent import build_agent
import time

class TestNBAAgentTracing:
    """Tracing tests for NBA Agent tool calls and interactions"""
    
    def __init__(self):
        self.judgment = Tracer(project_name="NBA Agent Tracing", deep_tracing=False)
        self.agent = build_agent()
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function")
    def test_player_stats_tracing(self):
        """Trace player statistics queries and tool usage"""
        
        test_queries = [
            "What are LeBron's points this season?",
            "How many assists did Haliburton have?", 
            "Show me Giannis rebounds",
            "What are all of Luka's stats?"
        ]
        
        results = []
        for query in test_queries:
            print(f"\n🔍 Tracing Query: {query}")
            
            # Trace the agent call
            traced_result = self._trace_agent_call(query)
            results.append(traced_result)
            
            # Run online evaluation during tracing
            self.judgment.async_evaluate(
                scorers=[AnswerRelevancyScorer(threshold=0.8)],
                input=query,
                actual_output=traced_result,
                model="gpt-4o"
            )
        
        return results
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="tool")
    def _trace_agent_call(self, query):
        """Trace individual agent calls"""
        
        start_time = time.time()
        
        # Call the agent
        response = self.agent.invoke({"input": query})
        result = response.get("output", str(response))
        
        end_time = time.time()
        
        # Log tracing information
        print(f"  📊 Response Time: {end_time - start_time:.2f}s")
        print(f"  🤖 Agent Response: {result}")
        
        return result
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function")
    def test_schedule_queries_tracing(self):
        """Trace team schedule queries"""
        
        schedule_queries = [
            "When do the Warriors play next?",
            "What is the Lakers next game?",
            "Show me the Celtics upcoming schedule"
        ]
        
        results = []
        for query in schedule_queries:
            print(f"\n📅 Tracing Schedule Query: {query}")
            
            traced_result = self._trace_schedule_call(query)
            results.append(traced_result)
            
            # Evaluate schedule accuracy
            self.judgment.async_evaluate(
                scorers=[AnswerCorrectnessScorer(threshold=0.7)],
                input=query,
                actual_output=traced_result,
                model="gpt-4o"
            )
        
        return results
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="tool")
    def _trace_schedule_call(self, query):
        """Trace schedule tool calls"""
        
        response = self.agent.invoke({"input": query})
        result = response.get("output", str(response))
        
        print(f"  📅 Schedule Response: {result}")
        return result
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function") 
    def test_complex_queries_tracing(self):
        """Trace complex multi-step queries"""
        
        complex_queries = [
            "Who had the most combined points, rebounds, and assists this season?",
            "Compare LeBron and Giannis stats across all categories",
            "What player leads in each major statistical category?",
            "How do the top 3 scorers compare in other stats?"
        ]
        
        results = []
        for query in complex_queries:
            print(f"\n🧠 Tracing Complex Query: {query}")
            
            traced_result = self._trace_complex_reasoning(query)
            results.append(traced_result)
            
            # Evaluate reasoning quality
            self.judgment.async_evaluate(
                scorers=[
                    AnswerRelevancyScorer(threshold=0.8),
                    AnswerCorrectnessScorer(threshold=0.7)
                ],
                input=query,
                actual_output=traced_result,
                model="gpt-4o"
            )
        
        return results
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="llm")
    def _trace_complex_reasoning(self, query):
        """Trace complex reasoning and multi-tool usage"""
        
        print(f"  🧠 Processing complex query...")
        
        response = self.agent.invoke({"input": query})
        result = response.get("output", str(response))
        
        print(f"  📋 Complex Response: {result[:200]}...")
        return result
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function")
    def test_error_handling_tracing(self):
        """Trace error handling and edge cases"""
        
        edge_case_queries = [
            "What are Michael Jordan's stats this season?",  # Retired player
            "How many points did LeBron score in 2030?",     # Future season
            "What team does Santa Claus play for?",          # Invalid player
            "Show me the stats for the year 1800"           # Invalid year
        ]
        
        results = []
        for query in edge_case_queries:
            print(f"\n⚠️ Tracing Edge Case: {query}")
            
            traced_result = self._trace_error_handling(query)
            results.append(traced_result)
            
            # Check for hallucinations in error responses
            self.judgment.async_evaluate(
                scorers=[HallucinationScorer(threshold=0.3)],
                input=query,
                actual_output=traced_result,
                model="gpt-4o"
            )
        
        return results
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="error_handling")
    def _trace_error_handling(self, query):
        """Trace how agent handles invalid queries"""
        
        try:
            response = self.agent.invoke({"input": query})
            result = response.get("output", str(response))
            
            print(f"  ⚠️ Error Response: {result}")
            return result
            
        except Exception as e:
            error_msg = f"Agent error: {str(e)}"
            print(f"  ❌ Exception: {error_msg}")
            return error_msg
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function")
    def test_tool_performance_tracing(self):
        """Trace individual tool performance"""
        
        # Test stats tool directly
        stats_queries = [
            "LeBron points 2024-25",
            "Curry assists",
            "Giannis rebounds", 
            "Luka all stats"
        ]
        
        # Test schedule tool directly  
        schedule_queries = [
            "Warriors",
            "Lakers", 
            "Celtics"
        ]
        
        print("\n🔧 Testing Stats Tool Performance:")
        for query in stats_queries:
            self._trace_stats_tool_performance(query)
        
        print("\n📅 Testing Schedule Tool Performance:")
        for query in schedule_queries:
            self._trace_schedule_tool_performance(query)
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="tool")
    def _trace_stats_tool_performance(self, query):
        """Trace stats tool performance"""
        from tools import StatsTool
        
        start_time = time.time()
        
        tool = StatsTool()
        result = tool._run(query)
        
        end_time = time.time()
        
        print(f"  📊 Query: {query}")
        print(f"  ⏱️ Time: {end_time - start_time:.3f}s")
        print(f"  📈 Result: {result}")
        
        return result
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="tool")
    def _trace_schedule_tool_performance(self, query):
        """Trace schedule tool performance"""
        from tools import ScheduleTool
        
        start_time = time.time()
        
        tool = ScheduleTool()
        result = tool._run(query)
        
        end_time = time.time()
        
        print(f"  📅 Query: {query}")
        print(f"  ⏱️ Time: {end_time - start_time:.3f}s") 
        print(f"  🏀 Result: {result}")
        
        return result
    
    @Tracer(project_name="NBA Agent Tracing").observe(span_type="function")
    def run_comprehensive_tracing(self):
        """Run all tracing tests"""
        
        print("🏀 Starting Comprehensive NBA Agent Tracing")
        print("=" * 60)
        
        # Player stats tracing
        print("\n1️⃣ Player Stats Tracing")
        stats_results = self.test_player_stats_tracing()
        
        # Schedule tracing
        print("\n2️⃣ Schedule Queries Tracing") 
        schedule_results = self.test_schedule_queries_tracing()
        
        # Complex queries tracing
        print("\n3️⃣ Complex Queries Tracing")
        complex_results = self.test_complex_queries_tracing()
        
        # Error handling tracing
        print("\n4️⃣ Error Handling Tracing")
        error_results = self.test_error_handling_tracing()
        
        # Tool performance tracing
        print("\n5️⃣ Tool Performance Tracing")
        self.test_tool_performance_tracing()
        
        # Summary
        total_tests = len(stats_results) + len(schedule_results) + len(complex_results) + len(error_results)
        
        print(f"\n🎉 Tracing Complete!")
        print(f"📊 Total Traced Queries: {total_tests}")
        print(f"✅ All traces sent to Judgment Labs")
        
        return {
            "stats_results": stats_results,
            "schedule_results": schedule_results, 
            "complex_results": complex_results,
            "error_results": error_results,
            "total_tests": total_tests
        }

if __name__ == "__main__":
    # Initialize and run tracing tests
    tracer = TestNBAAgentTracing()
    
    print("🔍 NBA Agent Tracing Test Suite")
    print("Built with Judgment Labs 💜")
    print("=" * 50)
    
    # Run comprehensive tracing
    results = tracer.run_comprehensive_tracing()
    
    print(f"\n📈 Tracing Summary:")
    print(f"  🏀 Player Stats Queries: {len(results['stats_results'])}")
    print(f"  📅 Schedule Queries: {len(results['schedule_results'])}")
    print(f"  🧠 Complex Queries: {len(results['complex_results'])}")
    print(f"  ⚠️ Error Cases: {len(results['error_results'])}")
    print(f"  📊 Total: {results['total_tests']} traced interactions")
    
    print(f"\n✨ All traces and evaluations are available in Judgment Labs dashboard!")
    print(f"🔗 Visit: https://app.judgmentlabs.ai to view your traces") 