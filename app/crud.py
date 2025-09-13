from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_slug(db: Session, slug: str):
    return db.query(models.Product).filter(models.Product.slug == slug).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, brand: Optional[str] = None, search: Optional[str] = None):
    query = db.query(models.Product)
    
    if brand:
        query = query.filter(models.Product.brand.ilike(f"%{brand}%"))
    
    if search:
        query = query.filter(
            models.Product.name.ilike(f"%{search}%") |
            models.Product.slug.ilike(f"%{search}%") |
            models.Product.sku.ilike(f"%{search}%")
        )
    
    return query.offset(skip).limit(limit).all()

def get_products_count(db: Session, brand: Optional[str] = None, search: Optional[str] = None):
    query = db.query(func.count(models.Product.id))
    
    if brand:
        query = query.filter(models.Product.brand.ilike(f"%{brand}%"))
    
    if search:
        query = query.filter(
            models.Product.name.ilike(f"%{search}%") |
            models.Product.slug.ilike(f"%{search}%") |
            models.Product.sku.ilike(f"%{search}%")
        )
    
    return query.scalar()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_low_stock_products(db: Session, threshold: int = 10):
    return db.query(models.Product).filter(models.Product.stock <= threshold).all()

def update_stock(db: Session, product_id: int, new_stock: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.stock = new_stock
        db.commit()
        db.refresh(db_product)
    return db_product
