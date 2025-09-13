from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...models.user import User
from ...schemas import product_schemas as schemas
from ...utils.auth_utils import get_current_user
from ...database import get_db
from ...services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[schemas.ProductListItem])
def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(10, ge=1, le=1000, description="Number of products to return (default 10)"),
    brand: Optional[str] = Query(None, description="Filter by brand name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List products - returns 10 products by default with Product ID, SKU, Product Title, Brand Name, Product Slug"""
    return ProductService.get_products_list(db, skip=skip, limit=limit, brand=brand)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Get a single product using product ID - returns all fields"""
    return ProductService.get_product_by_id_direct(db, product_id)


@router.post("/", response_model=schemas.Product, status_code=201)
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create new product - accepts Product SKU, Brand Name, Product Title, Quantity"""
    return ProductService.create_product_direct(db, product)

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Delete a product using product ID"""
    ProductService.delete_product_direct(db, product_id)
    return None
