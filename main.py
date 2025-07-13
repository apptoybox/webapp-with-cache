from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import time
import json

from database import get_db, engine
from models import Base, Product
from schemas import (
    ProductCreate, ProductResponse, CacheStats,
    ProductResponseWithMetadata, ProductsResponseWithMetadata,
    DeleteResponse, PerformanceResponse
)
from cache_service import CacheService
from database_service import DatabaseService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cache Example Application",
    description="A demonstration of caching with FastAPI, PostgreSQL, and Redis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
cache_service = CacheService()
db_service = DatabaseService()

@app.get("/")
async def root():
    """Serve the frontend application"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "database": "connected",
            "cache": "connected"
        }
    }

@app.get("/products", response_model=ProductsResponseWithMetadata)
async def get_products(db: Session = Depends(get_db)):
    """Get all products with caching"""
    start_time = time.time()

    # Try to get from cache first
    cached_products = cache_service.get("all_products")
    if cached_products:
        cache_service.increment_hits()
        return {
            "products": cached_products,
            "source": "cache",
            "response_time": time.time() - start_time
        }

    # Cache miss - get from database
    cache_service.increment_misses()
    products = db_service.get_all_products(db)

    # Cache the result for 5 minutes
    cache_service.set("all_products", products, expire=300)

    return {
        "products": products,
        "source": "database",
        "response_time": time.time() - start_time
    }

@app.get("/products/{product_id}", response_model=ProductResponseWithMetadata)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID with caching"""
    start_time = time.time()

    # Try to get from cache first
    cache_key = f"product:{product_id}"
    cached_product = cache_service.get(cache_key)
    if cached_product:
        cache_service.increment_hits()
        return {
            "product": cached_product,
            "source": "cache",
            "response_time": time.time() - start_time
        }

    # Cache miss - get from database
    cache_service.increment_misses()
    product = db_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Cache the result for 10 minutes
    cache_service.set(cache_key, product, expire=600)

    return {
        "product": product,
        "source": "database",
        "response_time": time.time() - start_time
    }

@app.post("/products", response_model=ProductResponseWithMetadata)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product and invalidate cache"""
    start_time = time.time()

    # Create product in database
    new_product = db_service.create_product(db, product)

    # Invalidate cache
    cache_service.delete("all_products")

    return {
        "product": new_product,
        "source": "database",
        "response_time": time.time() - start_time
    }

@app.put("/products/{product_id}", response_model=ProductResponseWithMetadata)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """Update a product and invalidate cache"""
    start_time = time.time()

    # Update product in database
    updated_product = db_service.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Invalidate cache
    cache_service.delete("all_products")
    cache_service.delete(f"product:{product_id}")

    return {
        "product": updated_product,
        "source": "database",
        "response_time": time.time() - start_time
    }

@app.delete("/products/{product_id}", response_model=DeleteResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product and invalidate cache"""
    start_time = time.time()

    # Delete product from database
    success = db_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")

    # Invalidate cache
    cache_service.delete("all_products")
    cache_service.delete(f"product:{product_id}")

    return {
        "message": "Product deleted successfully",
        "source": "database",
        "response_time": time.time() - start_time
    }

@app.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get cache statistics"""
    return cache_service.get_stats()

@app.post("/cache/clear")
async def clear_cache():
    """Clear all cache"""
    cache_service.clear_all()
    return {"message": "Cache cleared successfully"}

@app.get("/cache/performance", response_model=PerformanceResponse)
async def compare_performance(db: Session = Depends(get_db)):
    """Compare cached vs non-cached performance"""
    # Test with cached request
    cache_start = time.time()
    cached_products = cache_service.get("all_products")
    cache_time = time.time() - cache_start

    # Test with database request
    db_start = time.time()
    db_products = db_service.get_all_products(db)
    db_time = time.time() - db_start

    return {
        "cached_response_time": cache_time,
        "database_response_time": db_time,
        "performance_improvement": f"{((db_time - cache_time) / db_time * 100):.2f}%"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
