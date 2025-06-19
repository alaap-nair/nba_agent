"""
NBA Agent Test Suite using Judgment Labs
Comprehensive testing framework for evaluation, tracing, and performance monitoring
"""

# Export main test classes
from .test_agent_evaluation import TestNBAAgentEvaluation
from .test_agent_tracing import TestNBAAgentTracing  
from .test_agent_performance import TestNBAAgentPerformance
from .test_dataset_builder import NBAAgentDatasetBuilder

__version__ = "1.0.0"
__author__ = "NBA Agent Team"
__description__ = "Comprehensive test suite for NBA Agent using Judgment Labs"

# Available test classes
__all__ = [
    "TestNBAAgentEvaluation",
    "TestNBAAgentTracing", 
    "TestNBAAgentPerformance",
    "NBAAgentDatasetBuilder"
]
