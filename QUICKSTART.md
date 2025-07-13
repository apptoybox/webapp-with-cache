# Quick Start Guide

Get the cache example application running in minutes!

## 🚀 Quick Setup

1. **Create environment file**:

   ```bash
   cp env.example .env
   ```

2. **Start the application**:

   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - **Web Interface**: <http://localhost:8000>
   - **API Docs**: <http://localhost:8000/docs>

## 🎯 What You'll See

### Web Interface Features

- **Real-time cache statistics** (hits, misses, hit rate)
- **Product management** (add, view products)
- **Cache controls** (clear cache, performance test)
- **Visual indicators** showing cache hits vs database queries

### Caching Demonstration

1. **First Load**: Click "Load Products" - you'll see "Source: database"
2. **Second Load**: Click again - you'll see "Source: cache" (much faster!)
3. **Add Product**: Add a new product - cache automatically invalidates
4. **Performance Test**: Compare cached vs database response times

## 🧪 Test the Caching

Run the test script to verify everything works:

```bash
python test_cache.py
```

This will:

- Test basic caching functionality
- Verify cache invalidation
- Test individual product caching
- Compare performance improvements

## 📊 Expected Results

- **Cache Hit Rate**: Should increase with repeated requests
- **Response Time**: Cached requests should be 80-95% faster
- **Performance Improvement**: Typically 80-95% faster response times

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000, 5432, 6379 are available
2. **Database connection**: Wait 10-15 seconds for PostgreSQL to start
3. **Redis connection**: Check if Redis container is running

### Debug Commands

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs app

# Restart services
docker-compose restart
```

## 🎓 Learning Points

This application demonstrates:

- **Read-Through Caching**: Cache-first data retrieval
- **Write-Through Caching**: Cache invalidation on writes
- **Cache Expiration**: Automatic cleanup of stale data
- **Performance Monitoring**: Real-time cache statistics
- **Cache Key Strategy**: Hierarchical cache key management

## 📚 Next Steps

- Explore the API documentation at <http://localhost:8000/docs>
- Try different caching strategies
- Monitor cache performance in real-time
- Experiment with cache expiration times

Happy caching! 🚀
