from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# New schemas for caching demonstration with metadata
class ProductResponseWithMetadata(BaseModel):
    product: ProductResponse
    source: str
    response_time: float

class ProductsResponseWithMetadata(BaseModel):
    products: List[ProductResponse]
    source: str
    response_time: float

class DeleteResponse(BaseModel):
    message: str
    source: str
    response_time: float

class CacheStats(BaseModel):
    hits: int
    misses: int
    hit_rate: float
    total_requests: int

class PerformanceResponse(BaseModel):
    cached_response_time: float
    database_response_time: float
    performance_improvement: str
