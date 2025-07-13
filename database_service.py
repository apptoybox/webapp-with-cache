from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductUpdate
from typing import List, Optional

class DatabaseService:
    def get_all_products(self, db: Session) -> List[dict]:
        """Get all products from database"""
        products = db.query(Product).all()
        return [product.to_dict() for product in products]

    def get_product_by_id(self, db: Session, product_id: int) -> Optional[dict]:
        """Get product by ID from database"""
        product = db.query(Product).filter(Product.id == product_id).first()
        return product.to_dict() if product else None

    def create_product(self, db: Session, product_data: ProductCreate) -> dict:
        """Create a new product"""
        db_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            stock_quantity=product_data.stock_quantity
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product.to_dict()

    def update_product(self, db: Session, product_id: int, product_data: ProductCreate) -> Optional[dict]:
        """Update an existing product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None

        # Update fields
        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.price = product_data.price
        db_product.category = product_data.category
        db_product.stock_quantity = product_data.stock_quantity

        db.commit()
        db.refresh(db_product)
        return db_product.to_dict()

    def delete_product(self, db: Session, product_id: int) -> bool:
        """Delete a product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return False

        db.delete(db_product)
        db.commit()
        return True

    def get_products_by_category(self, db: Session, category: str) -> List[dict]:
        """Get products by category"""
        products = db.query(Product).filter(Product.category == category).all()
        return [product.to_dict() for product in products]

    def search_products(self, db: Session, search_term: str) -> List[dict]:
        """Search products by name or description"""
        products = db.query(Product).filter(
            Product.name.ilike(f"%{search_term}%") |
            Product.description.ilike(f"%{search_term}%")
        ).all()
        return [product.to_dict() for product in products]
