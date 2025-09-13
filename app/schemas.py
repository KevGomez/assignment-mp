from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    sku: str
    brand: str
    slug: str
    name: str
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    brand: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    stock: Optional[int] = None

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    message: str
    product: Optional[Product] = None

class ProductListResponse(BaseModel):
    message: str
    products: list[Product]
    total: int

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
