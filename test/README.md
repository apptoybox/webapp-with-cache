# Test Suite

This directory contains the test scripts for the cache example application.

## Test Files

| Test File                       | Description                                              |
|---------------------------------|----------------------------------------------------------|
| **test_cache.py**               | Tests caching functionality and performance improvements |
| **test_fix.py**                 | Tests the 500 error fix                                  |
| **test_form_validation.py**     | Tests form validation and identifies 422 errors          |
| **test_browser_debug.py**       | Tests browser-specific issues using the debug endpoint   |
| **test_frontend_simulation.py** | Simulates frontend form submission                       |

## Running Tests

You can run the tests using the Makefile commands:

```bash
# Test cache functionality
make test

# Test the 500 error fix
make test-fix

# Test form validation
make test-validation
```

Or run individual tests directly:

```bash
python test/test_cache.py
python test/test_fix.py
python test/test_form_validation.py
python test/test_browser_debug.py
python test/test_frontend_simulation.py
```

## Prerequisites

- The application must be running on <http://localhost:8000>
- Docker containers should be started with `docker-compose up --build`
