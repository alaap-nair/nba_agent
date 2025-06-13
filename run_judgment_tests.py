#!/usr/bin/env python3
"""
NBA Agent Test Runner using Judgment Labs
Comprehensive test suite runner for evaluation, tracing, and performance testing
"""

import argparse
import sys
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description="🏀 NBA Agent Test Suite with Judgment Labs",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        'test_type',
        choices=['all', 'evaluation', 'tracing', 'performance'],
        help="""Choose test type to run:
  all         - Run all test suites
  evaluation  - Run evaluation tests (accuracy, relevancy, faithfulness)
  tracing     - Run tracing tests (tool calls, LLM interactions)
  performance - Run performance tests (latency, load testing)"""
    )
    
    parser.add_argument(
        '--project-name',
        default=f"NBA Agent Tests - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        help='Project name for Judgment Labs (default: timestamped)'
    )
    
    parser.add_argument(
        '--model',
        default='gpt-4o',
        help='Model to use for evaluations (default: gpt-4o)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print("🏀 NBA Agent Test Suite with Judgment Labs")
    print("=" * 60)
    print(f"📊 Project: {args.project_name}")
    print(f"🤖 Model: {args.model}")
    print(f"🔧 Test Type: {args.test_type}")
    print("=" * 60)
    
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Please add your OpenAI API key to the .env file")
        return 1
    
    try:
        # Run selected tests
        if args.test_type == 'evaluation' or args.test_type == 'all':
            print("\n🎯 Running Evaluation Tests...")
            run_evaluation_tests(args)
        
        if args.test_type == 'tracing' or args.test_type == 'all':
            print("\n🔍 Running Tracing Tests...")
            run_tracing_tests(args)
        
        if args.test_type == 'performance' or args.test_type == 'all':
            print("\n⚡ Running Performance Tests...")
            run_performance_tests(args)
        
        print("\n🎉 All tests completed successfully!")
        print("✨ View results at: https://app.judgmentlabs.ai")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def run_evaluation_tests(args):
    """Run evaluation test suite"""
    try:
        from tests.test_agent_evaluation import TestNBAAgentEvaluation
        
        print("  📋 Initializing evaluation tests...")
        test_suite = TestNBAAgentEvaluation()
        test_suite.setup_class()
        
        # Override project name if provided
        if args.project_name:
            test_suite.project_name = f"{args.project_name} - Evaluation"
        
        tests = [
            ("Player Stats Faithfulness", test_suite.test_player_stats_faithfulness),
            ("Answer Relevancy", test_suite.test_answer_relevancy),
            ("Factual Correctness", test_suite.test_factual_correctness),
            ("Response Coherence", test_suite.test_response_coherence),
            ("Hallucination Detection", test_suite.test_hallucination_detection),
            ("Comprehensive Evaluation", test_suite.test_comprehensive_evaluation)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                print(f"    🔄 Running {test_name}...")
                test_func()
                print(f"    ✅ {test_name} passed")
                passed += 1
            except Exception as e:
                print(f"    ❌ {test_name} failed: {e}")
                failed += 1
                if args.verbose:
                    import traceback
                    traceback.print_exc()
        
        print(f"\n  📊 Evaluation Results: {passed} passed, {failed} failed")
        
    except ImportError as e:
        print(f"  ❌ Failed to import evaluation tests: {e}")
        print("     Make sure judgeval is installed: pip install judgeval")

def run_tracing_tests(args):
    """Run tracing test suite"""
    try:
        from tests.test_agent_tracing import TestNBAAgentTracing
        
        print("  🔍 Initializing tracing tests...")
        tracer = TestNBAAgentTracing()
        
        # Override project name if provided
        if args.project_name:
            tracer.judgment.project_name = f"{args.project_name} - Tracing"
        
        print("    🔄 Running comprehensive tracing...")
        results = tracer.run_comprehensive_tracing()
        
        print(f"  📊 Tracing Results:")
        print(f"    🏀 Player Stats: {len(results['stats_results'])} queries")
        print(f"    📅 Schedule: {len(results['schedule_results'])} queries")
        print(f"    🧠 Complex: {len(results['complex_results'])} queries")
        print(f"    ⚠️ Error Cases: {len(results['error_results'])} queries")
        print(f"    📈 Total: {results['total_tests']} traced interactions")
        
    except ImportError as e:
        print(f"  ❌ Failed to import tracing tests: {e}")
        print("     Make sure judgeval is installed: pip install judgeval")

def run_performance_tests(args):
    """Run performance test suite"""
    try:
        from tests.test_agent_performance import TestNBAAgentPerformance
        
        print("  ⚡ Initializing performance tests...")
        performance_tester = TestNBAAgentPerformance()
        
        # Override project name if provided
        if args.project_name:
            performance_tester.project_name = f"{args.project_name} - Performance"
        
        print("    🔄 Running comprehensive performance tests...")
        results = performance_tester.run_comprehensive_performance_tests()
        
        print(f"  📊 Performance Results:")
        
        # Response time summary
        if "response_times" in results:
            for category, metrics in results["response_times"].items():
                print(f"    ⏱️ {category.replace('_', ' ').title()}: {metrics['avg_time']:.2f}s avg")
        
        # Concurrent load summary
        if "concurrent_load" in results:
            load_results = results["concurrent_load"]
            print(f"    🚀 Concurrent Success: {load_results['success_rate']:.1%}")
            print(f"    🔄 Concurrent Avg: {load_results['avg_response_time']:.2f}s")
        
        # Accuracy summary
        if "accuracy" in results:
            accuracy = sum(r["content_match"] for r in results["accuracy"]) / len(results["accuracy"])
            print(f"    🎯 Content Accuracy: {accuracy:.1%}")
        
    except ImportError as e:
        print(f"  ❌ Failed to import performance tests: {e}")
        print("     Make sure judgeval is installed: pip install judgeval")

def print_usage_examples():
    """Print usage examples"""
    print("""
🏀 NBA Agent Test Suite Examples:

# Run all tests
python run_judgment_tests.py all

# Run only evaluation tests
python run_judgment_tests.py evaluation

# Run tracing tests with custom project name
python run_judgment_tests.py tracing --project-name "My NBA Agent Test"

# Run performance tests with verbose output
python run_judgment_tests.py performance --verbose

# Run all tests with different model
python run_judgment_tests.py all --model gpt-3.5-turbo

🔗 View results at: https://app.judgmentlabs.ai
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_usage_examples()
        sys.exit(0)
    
    exit_code = main()
    sys.exit(exit_code) 