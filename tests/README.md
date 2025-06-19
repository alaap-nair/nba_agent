# 🏀 NBA Agent Test Suite with Judgment Labs

Comprehensive testing and evaluation framework for the NBA Agent using [Judgment Labs](https://docs.judgmentlabs.ai/introduction) infrastructure.

## 🔧 Setup

1. **Install Dependencies**
   ```bash
   pip install judgeval
   ```

2. **Environment Setup**
   Make sure your `.env` file contains:
   ```
   OPENAI_API_KEY=your_openai_api_key
   JUDGMENT_API_KEY=your_judgment_labs_api_key  # Optional
   ```

3. **Activate Environment**
   ```bash
   source activate_env.sh
   source .venv/bin/activate
   ```

## 🚀 Quick Start

### Run All Tests
```bash
python run_judgment_tests.py all
```

### Run Specific Test Types
```bash
# Evaluation tests only
python run_judgment_tests.py evaluation

# Tracing tests only  
python run_judgment_tests.py tracing

# Performance tests only
python run_judgment_tests.py performance
```

### Custom Options
```bash
# Custom project name
python run_judgment_tests.py all --project-name "My NBA Agent Test"

# Different model
python run_judgment_tests.py evaluation --model gpt-3.5-turbo

# Verbose output
python run_judgment_tests.py all --verbose
```

## 📋 Test Suite Overview

### 1. Evaluation Tests (`test_agent_evaluation.py`)

Tests the **accuracy, relevancy, and faithfulness** of NBA agent responses.

#### Features:
- **Faithfulness Scoring**: Ensures responses are faithful to underlying data
- **Answer Relevancy**: Validates responses are relevant to questions
- **Factual Correctness**: Checks accuracy against known statistics
- **Coherence Testing**: Evaluates response structure and clarity
- **Hallucination Detection**: Identifies when agent creates false information

#### Example Usage:
```python
from tests.test_agent_evaluation import TestNBAAgentEvaluation

test_suite = TestNBAAgentEvaluation()
test_suite.setup_class()
test_suite.test_player_stats_faithfulness()
```

#### Sample Tests:
- Player statistics accuracy
- Schedule information correctness
- Complex query handling
- Error scenario responses

### 2. Tracing Tests (`test_agent_tracing.py`)

**Traces and monitors** NBA agent's tool calls, LLM interactions, and decision making.

#### Features:
- **Function Tracing**: Monitors agent decision flow
- **Tool Call Tracing**: Tracks individual tool usage
- **Performance Monitoring**: Measures response times
- **Error Handling**: Traces how agent handles edge cases
- **Online Evaluation**: Real-time quality scoring during tracing

#### Example Usage:
```python
from tests.test_agent_tracing import TestNBAAgentTracing

tracer = TestNBAAgentTracing()
results = tracer.run_comprehensive_tracing()
```

#### Trace Categories:
- Player stats queries
- Schedule lookups
- Complex reasoning chains
- Error scenarios
- Tool performance

### 3. Performance Tests (`test_agent_performance.py`)

Tests **response times, load handling, and production readiness**.

#### Features:
- **Response Time Benchmarks**: Measures latency across query types
- **Concurrent Load Testing**: Tests performance under multiple simultaneous requests
- **Accuracy Benchmarks**: Validates accuracy against known ground truth
- **Production Monitoring**: Simulates real-world usage patterns

#### Example Usage:
```python
from tests.test_agent_performance import TestNBAAgentPerformance

performance_tester = TestNBAAgentPerformance()
results = performance_tester.run_comprehensive_performance_tests()
```

#### Performance Categories:
- Simple stats queries: `< 3s`
- Complex reasoning: `< 8s`
- Schedule lookups: `< 2s`
- Concurrent success rate: `> 90%`

### 4. Dataset Builder (`test_dataset_builder.py`)

**Generates comprehensive test datasets** for evaluation and benchmarking.

#### Features:
- **Stats Dataset**: 50+ player statistics queries with ground truth
- **Schedule Dataset**: Team schedule and game information queries
- **Complex Dataset**: Multi-step reasoning and comparison queries
- **Edge Case Dataset**: Error handling and invalid input scenarios
- **Export Capabilities**: Saves datasets as JSON and to Judgment Labs

#### Example Usage:
```python
from tests.test_dataset_builder import NBAAgentDatasetBuilder

builder = NBAAgentDatasetBuilder()
datasets = builder.build_comprehensive_datasets()
```

## 📊 Judgment Labs Integration

### Scorers Used

| Scorer | Purpose | Threshold |
|--------|---------|-----------|
| `FaithfulnessScorer` | Data accuracy | 0.7 |
| `AnswerRelevancyScorer` | Response relevance | 0.8 |
| `FactualCorrectnessScorer` | Factual accuracy | 0.75 |
| `CoherenceScorer` | Response clarity | 0.8 |
| `HallucinationScorer` | False information | 0.3 |
| `LatencyScorer` | Response speed | 5.0s |

### Tracing Features

- **Span Types**: `function`, `tool`, `llm`, `error_handling`
- **Online Evaluation**: Real-time scoring during execution
- **Performance Monitoring**: Response time and accuracy tracking
- **Production Monitoring**: Simulated real-world scenarios

## 📈 Viewing Results

All test results are automatically sent to Judgment Labs dashboard:

1. **Visit**: https://app.judgmentlabs.ai
2. **Login** with your Judgment Labs account
3. **Navigate** to your project (e.g., "NBA Agent Tests - 2024-12-27 14:30")
4. **View** detailed results, traces, and metrics

### Dashboard Features:
- Real-time test execution monitoring
- Detailed trace visualization
- Performance metrics and trends
- Quality score breakdowns
- Dataset management

## 🔍 Test Categories

### Player Statistics
- Individual player stats (points, assists, rebounds, etc.)
- Comparative analysis between players
- Season-specific queries
- Comprehensive stat summaries

### Team Schedules
- Next game information
- Upcoming schedule queries
- Team-specific schedule requests

### Complex Reasoning
- Multi-player comparisons
- Statistical leadership queries
- Performance analysis
- Cross-category comparisons

### Edge Cases
- Retired player queries
- Invalid team names
- Future season requests
- Nonsensical inputs
- Ambiguous questions

## 🎯 Success Criteria

### Evaluation Metrics
- **Faithfulness**: > 80% of responses score ≥ 0.7
- **Relevancy**: > 90% of responses score ≥ 0.8
- **Factual Accuracy**: > 80% of responses score ≥ 0.75
- **Coherence**: > 85% of responses score ≥ 0.8
- **Hallucination**: < 30% hallucination score

### Performance Metrics
- **Simple Queries**: < 3 seconds average
- **Complex Queries**: < 8 seconds average
- **Concurrent Success**: > 90% success rate
- **Load Handling**: 24+ concurrent requests

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: `ModuleNotFoundError: No module named 'judgeval'`
   ```bash
   pip install judgeval
   ```

2. **API Key Missing**: `OPENAI_API_KEY environment variable not set`
   - Add your OpenAI API key to `.env` file

3. **Agent Import Error**: `ModuleNotFoundError: No module named 'agent'`
   - Ensure you're running from the correct directory
   - Check that `agent.py` exists

4. **Judgment Labs Connection**: Connection issues
   - Verify internet connection
   - Check Judgment Labs service status

### Debug Mode
```bash
python run_judgment_tests.py all --verbose
```

## 📁 File Structure

```
tests/
├── README.md                   # This file
├── test_agent_evaluation.py    # Evaluation tests
├── test_agent_tracing.py      # Tracing tests
├── test_agent_performance.py  # Performance tests
├── test_dataset_builder.py    # Dataset generation
└── __init__.py                # Test package

datasets/                      # Generated test datasets
├── nba_agent_stats_*.json
├── nba_agent_schedule_*.json
├── nba_agent_complex_*.json
└── nba_agent_comprehensive_*.json

run_judgment_tests.py          # Main test runner
```

## 🤝 Contributing

1. **Add New Tests**: Create new test methods in appropriate test files
2. **Extend Datasets**: Add new query templates in `test_dataset_builder.py`
3. **New Scorers**: Implement custom evaluation metrics
4. **Performance Benchmarks**: Add new performance test scenarios

## 📖 Documentation

- [Judgment Labs Documentation](https://docs.judgmentlabs.ai/introduction)
- [Evaluation Concepts](https://docs.judgmentlabs.ai/concepts/evaluation)
- [Tracing Guide](https://docs.judgmentlabs.ai/concepts/tracing)
- [Performance Monitoring](https://docs.judgmentlabs.ai/features/performance-monitoring)

## 🎉 Example Results

After running tests, you'll see output like:

```
🏀 NBA Agent Test Suite with Judgment Labs
============================================================
📊 Project: NBA Agent Tests - 2024-12-27 14:30
🤖 Model: gpt-4o
🔧 Test Type: all
============================================================

🎯 Running Evaluation Tests...
  📋 Initializing evaluation tests...
    🔄 Running Player Stats Faithfulness...
    ✅ Player Stats Faithfulness passed
    🔄 Running Answer Relevancy...
    ✅ Answer Relevancy passed
  📊 Evaluation Results: 6 passed, 0 failed

🔍 Running Tracing Tests...
  📊 Tracing Results:
    🏀 Player Stats: 4 queries
    📅 Schedule: 3 queries
    🧠 Complex: 4 queries
    ⚠️ Error Cases: 4 queries
    📈 Total: 15 traced interactions

⚡ Running Performance Tests...
  📊 Performance Results:
    ⏱️ Simple Stats: 2.1s avg
    ⏱️ Complex Stats: 5.8s avg
    ⏱️ Schedule: 1.9s avg
    🚀 Concurrent Success: 95.8%
    🎯 Content Accuracy: 87.5%

🎉 All tests completed successfully!
✨ View results at: https://app.judgmentlabs.ai
```

---

**Built with ❤️ using [Judgment Labs](https://judgmentlabs.ai) 💜** 