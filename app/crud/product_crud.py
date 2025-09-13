from sqlalchemy.orm import Session
from sqlalchemy import func, String
from typing import Optional
from ..models.product import Product
from ..schemas.product_schemas import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()

def get_product_by_slug(db: Session, product_slug: str):
    return db.query(Product).filter(Product.product_slug == product_slug).first()

def get_product_by_sku(db: Session, product_sku: int):
    return db.query(Product).filter(Product.product_sku == product_sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, brand: Optional[str] = None, search: Optional[str] = None):
    query = db.query(Product)
    
    if brand:
        query = query.filter(Product.brand_name.ilike(f"%{brand}%"))
    
    if search:
        query = query.filter(
            Product.product_title.ilike(f"%{search}%") |
            Product.product_slug.ilike(f"%{search}%") |
            Product.product_sku.cast(String).ilike(f"%{search}%")
        )
    
    return query.offset(skip).limit(limit).all()

def get_products_count(db: Session, brand: Optional[str] = None, search: Optional[str] = None):
    query = db.query(func.count(Product.product_id))
    
    if brand:
        query = query.filter(Product.brand_name.ilike(f"%{brand}%"))
    
    if search:
        query = query.filter(
            Product.product_title.ilike(f"%{search}%") |
            Product.product_slug.ilike(f"%{search}%") |
            Product.product_sku.cast(String).ilike(f"%{search}%")
        )
    
    return query.scalar()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_low_stock_products(db: Session, threshold: int = 10):
    return db.query(Product).filter(Product.quantity <= threshold).all()

def update_stock(db: Session, product_id: int, new_quantity: int):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        db_product.quantity = new_quantity
        db.commit()
        db.refresh(db_product)
    return db_product
