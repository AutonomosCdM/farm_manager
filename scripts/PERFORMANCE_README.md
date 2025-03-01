# Performance Testing for Farm Manager

## Overview
This script provides comprehensive performance testing for critical components of the Farm Manager system.

## Features
- Measure resource allocation performance
- Evaluate irrigation decision system efficiency
- Track execution time and memory usage
- Centralized logging of performance metrics

## Prerequisites
- Install dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

## Running Performance Tests
```bash
python scripts/performance_test.py
```

## Performance Metrics Tracked
- Total execution time
- Average time per iteration
- Memory consumption
- Resource allocation efficiency
- Irrigation decision system performance

## Logging
Performance and error logs are stored in the `logs/` directory with timestamped filenames.

## Customization
- Adjust `iterations` in test methods to fine-tune testing
- Modify test scenarios as needed

## Interpreting Results
The performance test generates detailed logs that include:
- Number of iterations
- Total execution time
- Average time per iteration
- Memory usage

### Example Log Output
```
Resource Allocation Performance:
Iterations: 100
Total Time: 0.5432 seconds
Average Time per Iteration: 0.005432 seconds
Memory Used: 2.35 MB

Irrigation Decision Performance:
Iterations: 50
Total Time: 0.2876 seconds
Average Time per Iteration: 0.005752 seconds
Memory Used: 1.87 MB
```

## Best Practices
- Run performance tests in a clean environment
- Close other applications to minimize interference
- Run multiple times to get consistent results
