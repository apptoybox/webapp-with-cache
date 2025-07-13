# Cache Example Application

A comprehensive demonstration of caching with FastAPI, PostgreSQL, and Redis. This application showcases various caching patterns and strategies commonly used in web applications.

## 🚀 Features

- **FastAPI Backend**: Modern, fast web framework for building APIs
- **PostgreSQL Database**: Robust relational database for data persistence
- **Redis Cache**: High-performance in-memory cache for improved response times
- **Docker Compose**: Easy development environment setup
- **Modern Frontend**: Beautiful, responsive web interface
- **Cache Statistics**: Real-time monitoring of cache performance
- **Performance Comparison**: Side-by-side comparison of cached vs non-cached responses

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   PostgreSQL    │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Redis Cache   │
                       └─────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🛠️ Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create environment file**:

   ```bash
   cp env.example .env
   ```

3. **Start the application**:

   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: <http://localhost:8000>
   - API Documentation: <http://localhost:8000/docs>
   - Alternative API Docs: <http://localhost:8000/redoc>

## 🎯 Usage Examples

### 1. Basic Caching Demonstration

1. Open <http://localhost:8000> in your browser
2. Click "Load Products" to see the initial database query
3. Click "Load Products" again to see the cached response
4. Notice the difference in response times and source indicators

### 2. Cache Statistics

- View real-time cache statistics on the dashboard
- Monitor hit rates and performance metrics
- Use the "Performance Test" button to compare cached vs database queries

### 3. Cache Invalidation

1. Add a new product using the form
2. Notice that the cache is automatically invalidated
3. Load products again to see the updated data

### 4. API Endpoints

#### Product Management

```bash
# Get all products (with caching)
GET /products

# Get product by ID (with caching)
GET /products/{id}

# Create new product
POST /products
{
  "name": "Sample Product",
  "description": "A sample product",
  "price": 29.99,
  "category": "Electronics",
  "stock_quantity": 100
}

# Update product
PUT /products/{id}

# Delete product
DELETE /products/{id}
```

#### Cache Management

```bash
# Get cache statistics
GET /cache/stats

# Clear all cache
POST /cache/clear

# Performance comparison
GET /cache/performance
```

## 🔧 Caching Strategies Demonstrated

### 1. Read-Through Caching

- Data is fetched from cache first
- On cache miss, data is retrieved from database and cached
- Subsequent requests are served from cache

### 2. Write-Through Caching

- When data is modified, cache is invalidated
- Ensures data consistency between cache and database

### 3. Cache Expiration

- Products list: 5 minutes
- Individual products: 10 minutes
- Automatic cleanup of stale data

### 4. Cache Key Strategy

- `all_products`: Cached list of all products
- `product:{id}`: Individual product cache keys
- Hierarchical invalidation on updates

## 📊 Performance Benefits

The application demonstrates significant performance improvements:

- **First Request**: Database query (slower)
- **Subsequent Requests**: Cache hit (much faster)
- **Typical Improvement**: 80-95% faster response times

## 🐳 Docker Services

### Application Service (`app`)

- **Port**: 8000
- **Dependencies**: PostgreSQL, Redis
- **Features**: FastAPI application with hot reload

### PostgreSQL Service (`db`)

- **Port**: 5432
- **Image**: postgres:14
- **Persistence**: Docker volume for data storage

### Redis Service (`redis`)

- **Port**: 6379
- **Image**: valkey/valkey:8.1-alpine
- **Features**: AOF persistence enabled

## 🔍 Monitoring and Debugging

### Cache Statistics

- Hit rate monitoring
- Request counting
- Performance metrics

### Database Monitoring

- Connection pooling
- Query performance
- Data consistency

### Redis Monitoring

- Memory usage
- Connection status
- Cache hit/miss ratios

## 🧪 Testing the Caching

1. **Initial Load**: First request hits the database
2. **Cache Hit**: Subsequent requests use cached data
3. **Cache Miss**: After expiration or invalidation
4. **Performance Test**: Compare response times

## 📁 Project Structure

```
├── docker-compose.yml      # Docker services configuration
├── Dockerfile             # Python application container
├── requirements.txt       # Python dependencies
├── main.py               # FastAPI application entry point
├── database.py           # Database configuration
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── cache_service.py      # Redis cache service
├── database_service.py   # Database operations
├── static/
│   └── index.html        # Frontend application
└── README.md             # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 8000, 5432, and 6379 are available
2. **Database Connection**: Wait for PostgreSQL to fully start before accessing the app
3. **Redis Connection**: Check Redis container logs for connection issues
4. **Cache Not Working**: Verify Redis is running and accessible

### Debug Commands

```bash
# Check container status
docker-compose ps

# View application logs
docker-compose logs app

# Access database
docker-compose exec db psql -U postgres -d cache_example

# Access Redis CLI
docker-compose exec redis redis-cli

# Restart services
docker-compose restart
```

## 🔄 Development

### Adding New Features

1. **New Cache Patterns**: Extend `cache_service.py`
2. **Additional Models**: Add to `models.py` and `schemas.py`
3. **New Endpoints**: Add to `main.py`
4. **Frontend Updates**: Modify `static/index.html`

### Environment Variables

```bash
DB_USER=postgres
DB_PASSWORD=password123
DB_NAME=cache_example
```

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes and demonstrates caching best practices in web applications.
