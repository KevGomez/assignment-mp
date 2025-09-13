from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    product_sku: int
    brand_name: str
    product_slug: str
    product_title: str
    quantity: int = 0
    is_deleted: bool = False

class ProductCreate(BaseModel):
    product_sku: int
    brand_name: str
    product_title: str
    quantity: int

class ProductUpdate(BaseModel):
    product_sku: Optional[int] = None
    brand_name: Optional[str] = None
    product_slug: Optional[str] = None
    product_title: Optional[str] = None
    quantity: Optional[int] = None
    is_deleted: Optional[bool] = None

class Product(ProductBase):
    product_id: int
    
    model_config = ConfigDict(from_attributes=True)

class ProductListItem(BaseModel):
    """Product list item with only required fields for listing"""
    product_id: int
    product_sku: int
    product_title: str
    brand_name: str
    product_slug: str
    
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    message: str
    product: Optional[Product] = None

class ProductListResponse(BaseModel):
    message: str
    products: list[Product]
    total: int
