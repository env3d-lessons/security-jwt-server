# Store test results
import json

test_results = []

def pytest_runtest_logreport(report):
    """Collect test results from each test execution."""
    if report.when == "call":  # Only log actual test call results, not setup/teardown
        test_results.append({
            "nodeid": report.nodeid,
            "outcome": report.outcome,  # "passed", "failed", "skipped"
            "duration": report.duration
        })

def pytest_sessionfinish(session, exitstatus):
    """Write collected test results to a JSON file at the end of the test session."""
    results_file = "result.json"
    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=4)

    print(f"\nTest results written to {results_file}")