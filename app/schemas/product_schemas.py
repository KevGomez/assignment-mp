from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    product_sku: int
    brand_name: str
    product_slug: str
    product_title: str
    quantity: int = 0

class ProductCreate(BaseModel):
    product_sku: int
    brand_name: str
    product_title: str
    quantity: int = 0

class ProductUpdate(BaseModel):
    product_sku: Optional[int] = None
    brand_name: Optional[str] = None
    product_slug: Optional[str] = None
    product_title: Optional[str] = None
    quantity: Optional[int] = None

class Product(ProductBase):
    product_id: int
    
    class Config:
        from_attributes = True

class ProductListItem(BaseModel):
    """Product list item with only required fields for listing"""
    product_id: int
    product_sku: int
    product_title: str
    brand_name: str
    product_slug: str
    
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    message: str
    product: Optional[Product] = None

class ProductListResponse(BaseModel):
    message: str
    products: list[Product]
    total: int
