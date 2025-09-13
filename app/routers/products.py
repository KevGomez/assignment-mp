from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=schemas.ProductListResponse)
def read_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    search: Optional[str] = Query(None, description="Search in product name or slug"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    products = crud.get_products(db, skip=skip, limit=limit, brand=brand, search=search)
    total = crud.get_products_count(db, brand=brand, search=search)
    return schemas.ProductListResponse(
        message="Products retrieved successfully",
        products=products,
        total=total
    )

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ProductResponse(
        message="Product retrieved successfully",
        product=db_product
    )

@router.get("/slug/{slug}", response_model=schemas.ProductResponse)
def read_product_by_slug(slug: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product_by_slug(db, slug=slug)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ProductResponse(
        message="Product retrieved successfully",
        product=db_product
    )

@router.get("/sku/{sku}", response_model=schemas.ProductResponse)
def read_product_by_sku(sku: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product_by_sku(db, sku=sku)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ProductResponse(
        message="Product retrieved successfully",
        product=db_product
    )

@router.post("/", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Check for duplicate SKU
    db_product_sku = crud.get_product_by_sku(db, sku=product.sku)
    if db_product_sku:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    # Check for duplicate slug
    db_product_slug = crud.get_product_by_slug(db, slug=product.slug)
    if db_product_slug:
        raise HTTPException(status_code=400, detail="Product with this slug already exists")
    
    created_product = crud.create_product(db=db, product=product)
    return schemas.ProductResponse(
        message="Product created successfully",
        product=created_product
    )

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int, 
    product_update: schemas.ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_update.slug and product_update.slug != db_product.slug:
        existing_product = crud.get_product_by_slug(db, slug=product_update.slug)
        if existing_product:
            raise HTTPException(status_code=400, detail="Product with this slug already exists")
    
    updated_product = crud.update_product(db=db, product_id=product_id, product_update=product_update)
    return schemas.ProductResponse(
        message="Product updated successfully",
        product=updated_product
    )

@router.delete("/{product_id}", response_model=schemas.ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    deleted_product = crud.delete_product(db=db, product_id=product_id)
    return schemas.ProductResponse(
        message="Product deleted successfully",
        product=deleted_product
    )

@router.get("/stock/low", response_model=schemas.ProductListResponse)
def get_low_stock_products(
    threshold: int = Query(10, ge=0, description="Stock threshold"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    products = crud.get_low_stock_products(db, threshold=threshold)
    return schemas.ProductListResponse(
        message="Low stock products retrieved successfully",
        products=products,
        total=len(products)
    )

@router.patch("/{product_id}/stock", response_model=schemas.ProductResponse)
def update_product_stock(
    product_id: int,
    stock: int = Query(..., ge=0, description="New stock quantity"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = crud.update_stock(db=db, product_id=product_id, new_stock=stock)
    return schemas.ProductResponse(
        message="Product stock updated successfully",
        product=updated_product
    )
