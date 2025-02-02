# Running Tests

Tests can be run using the provided `run-tests.sh` script in the scripts directory:

```bash
chmod +x scripts/run-tests.sh
./scripts/run-tests.sh
```

This script will:
1. Build the test containers using docker-compose.test.yml
2. Run all tests in an isolated environment
3. Clean up containers after completion


## Test Structure

The test suite includes:
- Unit tests: Testing individual components
- Integration tests: Testing API endpoints and database interactions
- WebSocket tests: Testing real-time collaboration features

Test files are located in the `app/tests/` directory:
- `app/tests/unit/`: Unit tests
- `app/tests/integration/`: Integration tests
- `app/tests/conftest.py`: Test fixtures and configuration
