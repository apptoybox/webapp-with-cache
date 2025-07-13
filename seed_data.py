#!/usr/bin/env python3
"""
Seed script to populate the database with sample product data.
Run this script to add sample products for caching demonstration.
"""

import os
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Product

# Create tables
Base.metadata.create_all(bind=engine)

# Sample product data
SAMPLE_PRODUCTS = [
    {
        "name": "MacBook Pro 16-inch",
        "description": "Powerful laptop with M2 Pro chip, perfect for developers and creative professionals",
        "price": 2499.99,
        "category": "Electronics",
        "stock_quantity": 25
    },
    {
        "name": "Wireless Bluetooth Headphones",
        "description": "Premium noise-cancelling headphones with 30-hour battery life",
        "price": 299.99,
        "category": "Electronics",
        "stock_quantity": 150
    },
    {
        "name": "Python Programming Book",
        "description": "Comprehensive guide to Python programming for beginners and advanced users",
        "price": 49.99,
        "category": "Books",
        "stock_quantity": 75
    },
    {
        "name": "Design Patterns Book",
        "description": "Classic book on software design patterns and best practices",
        "price": 39.99,
        "category": "Books",
        "stock_quantity": 50
    },
    {
        "name": "Cotton T-Shirt",
        "description": "Comfortable 100% cotton t-shirt available in multiple colors",
        "price": 24.99,
        "category": "Clothing",
        "stock_quantity": 200
    },
    {
        "name": "Denim Jeans",
        "description": "Classic blue denim jeans with perfect fit",
        "price": 79.99,
        "category": "Clothing",
        "stock_quantity": 100
    },
    {
        "name": "Coffee Maker",
        "description": "Programmable coffee maker with 12-cup capacity",
        "price": 89.99,
        "category": "Home",
        "stock_quantity": 30
    },
    {
        "name": "Garden Tool Set",
        "description": "Complete set of essential gardening tools for home use",
        "price": 129.99,
        "category": "Home",
        "stock_quantity": 45
    },
    {
        "name": "Yoga Mat",
        "description": "Non-slip yoga mat perfect for home workouts and studio sessions",
        "price": 34.99,
        "category": "Sports",
        "stock_quantity": 80
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes with excellent cushioning and support",
        "price": 119.99,
        "category": "Sports",
        "stock_quantity": 60
    }
]

def seed_database():
    """Seed the database with sample products"""
    db = SessionLocal()

    try:
        # Check if products already exist
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} products.")
            print("Skipping seed data insertion.")
            return

        # Add sample products
        for product_data in SAMPLE_PRODUCTS:
            product = Product(**product_data)
            db.add(product)

        db.commit()
        print(f"Successfully added {len(SAMPLE_PRODUCTS)} sample products to the database.")
        print("\nSample products added:")
        for product in SAMPLE_PRODUCTS:
            print(f"- {product['name']} (${product['price']})")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with sample products...")
    seed_database()
    print("\nSeed script completed!")
