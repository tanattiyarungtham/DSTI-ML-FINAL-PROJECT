# Makefile

# Start Docker services (e.g., PostgreSQL)
up:
	docker-compose up -d

# Stop all running Docker services
down:
	docker-compose down

# Run all unit and integration tests using pytest
test:
	pytest tests/

# Start Docker and run all tests (useful for CI or full testing pipeline)
test-all: up
	sleep 2  # wait briefly for PostgreSQL container to initialize
	pytest tests/