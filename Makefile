# Cache Example Application Makefile
# Provides easy commands for building, testing, and operating the application

.PHONY: help build up down restart logs clean test seed shell-app shell-db shell-redis status health-check lint format docs

# Default target
help:
	@echo "Cache Example Application - Available Commands:"
	@echo ""
	@echo "🚀 Setup & Deployment:"
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make clean     - Stop services and remove volumes"
	@echo ""
	@echo "📊 Monitoring & Debugging:"
	@echo "  make logs      - View application logs"
	@echo "  make status    - Check service status"
	@echo "  make health    - Health check for all services"
	@echo ""
	@echo "🧪 Testing & Development:"
	@echo "  make test      - Run cache functionality tests"
	@echo "  make test-fix  - Test the 500 error fix"
	@echo "  make test-validation - Test form validation"
	@echo "  make seed      - Seed database with sample data"
	@echo "  make lint      - Lint Python code"
	@echo "  make format    - Format Python code"
	@echo ""
	@echo "🔧 Shell Access:"
	@echo "  make shell-app - Access application container shell"
	@echo "  make shell-db  - Access PostgreSQL container shell"
	@echo "  make shell-redis - Access Redis container shell"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  make docs      - Open API documentation"
	@echo ""
	@echo "💡 Quick Start:"
	@echo "  make quick     - Quick start (build + up + seed)"

# Environment setup
setup:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "✅ Created .env file from env.example"; \
	else \
		echo "✅ .env file already exists"; \
	fi

# Build Docker images
build: setup
	@echo "🔨 Building Docker images..."
	docker-compose build --no-cache
	@echo "✅ Build completed"

# Start all services
up: setup
	@echo "🚀 Starting all services..."
	docker-compose up -d
	@echo "✅ Services started"
	@echo "📱 Access the application at: http://localhost:8000"
	@echo "📚 API docs at: http://localhost:8000/docs"

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker-compose down
	@echo "✅ Services stopped"

# Restart all services
restart: down up

# Clean up (stop services and remove volumes)
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup completed"

# View logs
logs:
	@echo "📋 Viewing application logs..."
	docker-compose logs -f app

# Check service status
status:
	@echo "📊 Service Status:"
	docker-compose ps
	@echo ""
	@echo "🔍 Container Details:"
	docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Health check for all services
health:
	@echo "🏥 Performing health checks..."
	@echo ""
	@echo "🔍 Checking application health endpoint..."
	@if curl -s http://localhost:8000/health > /dev/null; then \
		echo "✅ Application health endpoint is responding"; \
	else \
		echo "❌ Application health endpoint is not responding"; \
	fi
	@echo ""
	@echo "🔍 Checking application..."
	@if curl -s http://localhost:8000/ > /dev/null; then \
		echo "✅ Application is running"; \
	else \
		echo "❌ Application is not responding"; \
	fi
	@echo ""
	@echo "🔍 Checking PostgreSQL..."
	@if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then \
		echo "✅ PostgreSQL is ready"; \
	else \
		echo "❌ PostgreSQL is not ready"; \
	fi
	@echo ""
	@echo "🔍 Checking Redis..."
	@if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then \
		echo "✅ Redis is ready"; \
	else \
		echo "❌ Redis is not ready"; \
	fi

# Run cache functionality tests
test:
	@echo "🧪 Running cache functionality tests..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make setup' first"; \
		exit 1; \
	fi
	@echo "Waiting for application to be ready..."
	@sleep 5
	@python test_cache.py

# Test the 500 error fix
test-fix:
	@echo "🔧 Testing the 500 error fix..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make setup' first"; \
		exit 1; \
	fi
	@echo "Waiting for application to be ready..."
	@sleep 5
	@python test_fix.py

# Test form validation
test-validation:
	@echo "🧪 Testing form validation..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make setup' first"; \
		exit 1; \
	fi
	@echo "Waiting for application to be ready..."
	@sleep 5
	@python test_form_validation.py

# Seed database with sample data
seed:
	@echo "🌱 Seeding database with sample data..."
	docker-compose exec app python seed_data.py

# Quick start (build + up + seed)
quick: build up
	@echo "⏳ Waiting for services to be ready..."
	@sleep 15
	@echo "🌱 Seeding database..."
	@make seed
	@echo ""
	@echo "🎉 Application is ready!"
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "📚 API docs: http://localhost:8000/docs"

# Shell access to application container
shell-app:
	@echo "🐚 Accessing application container shell..."
	docker-compose exec app bash

# Shell access to PostgreSQL container
shell-db:
	@echo "🐚 Accessing PostgreSQL container shell..."
	docker-compose exec db psql -U postgres -d cache_example

# Shell access to Redis container
shell-redis:
	@echo "🐚 Accessing Redis container shell..."
	docker-compose exec redis redis-cli

# Lint Python code
lint:
	@echo "🔍 Linting Python code..."
	@if command -v flake8 > /dev/null; then \
		flake8 . --exclude=venv,__pycache__,.git; \
	else \
		echo "⚠️  flake8 not installed. Install with: pip install flake8"; \
	fi

# Format Python code
format:
	@echo "🎨 Formatting Python code..."
	@if command -v black > /dev/null; then \
		black . --exclude=venv,__pycache__,.git; \
	else \
		echo "⚠️  black not installed. Install with: pip install black"; \
	fi

# Open API documentation
docs:
	@echo "📚 Opening API documentation..."
	@if command -v open > /dev/null; then \
		open http://localhost:8000/docs; \
	elif command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:8000/docs; \
	else \
		echo "📚 API documentation available at: http://localhost:8000/docs"; \
	fi

# Development mode (with hot reload)
dev:
	@echo "🔧 Starting development mode..."
	docker-compose up --build

# Production mode (without hot reload)
prod:
	@echo "🚀 Starting production mode..."
	docker-compose -f docker-compose.yml up -d --build

# View cache statistics
cache-stats:
	@echo "📊 Cache Statistics:"
	@curl -s http://localhost:8000/cache/stats | python -m json.tool

# Clear cache
clear-cache:
	@echo "🗑️  Clearing cache..."
	@curl -X POST http://localhost:8000/cache/clear
	@echo "✅ Cache cleared"

# Performance test
perf-test:
	@echo "⚡ Running performance test..."
	@curl -s http://localhost:8000/cache/performance | python -m json.tool

# Database backup
backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker-compose exec db pg_dump -U postgres cache_example > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

# Database restore
restore:
	@echo "📥 Restoring database from backup..."
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify backup file: make restore BACKUP_FILE=backups/backup_20231201_120000.sql"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U postgres cache_example < $(BACKUP_FILE)
	@echo "✅ Database restored from $(BACKUP_FILE)"

# Monitor all services
monitor:
	@echo "📊 Monitoring all services..."
	@echo "Press Ctrl+C to stop monitoring"
	@watch -n 2 'docker-compose ps && echo "" && curl -s http://localhost:8000/cache/stats | python -c "import sys, json; data=json.load(sys.stdin); print(f\"Cache Hits: {data[\"hits\"]}, Misses: {data[\"misses\"]}, Hit Rate: {data[\"hit_rate\"]}%\")"'

# Show application info
info:
	@echo "ℹ️  Cache Example Application Information:"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  ├── main.py              # FastAPI application"
	@echo "  ├── cache_service.py     # Redis cache service"
	@echo "  ├── database_service.py  # Database operations"
	@echo "  ├── models.py            # SQLAlchemy models"
	@echo "  ├── schemas.py           # Pydantic schemas"
	@echo "  ├── static/index.html    # Frontend interface"
	@echo "  └── docker-compose.yml   # Docker services"
	@echo ""
	@echo "🌐 Services:"
	@echo "  - Application: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/docs"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - Redis: localhost:6379"
	@echo ""
	@echo "🔧 Environment Variables:"
	@echo "  - DB_USER=postgres"
	@echo "  - DB_PASSWORD=password123"
	@echo "  - DB_NAME=cache_example"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  - README.md: Complete documentation"
	@echo "  - QUICKSTART.md: Quick start guide"
