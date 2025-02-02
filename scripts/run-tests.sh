#!/bin/bash
set -e

# Build and run the test containers
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test

# Clean up
docker compose -f docker-compose.test.yml down 