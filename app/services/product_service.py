from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException
from .. import crud
from ..schemas import product_schemas as schemas
from ..models.product import Product

class ProductService:
    
    @staticmethod
    def _generate_brand_specific_slug(brand_name: str, product_title: str) -> str:
        """Generate slug based on brand-specific rules with GLOBAL 4-TOKEN RULE"""
        import re
        
        # Normalize title to tokens
        title_clean = product_title.lower().strip()
        title_clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title_clean)  # Remove special chars
        tokens = [token for token in title_clean.split() if token]  # Split and remove empty
        
        brand_lower = brand_name.lower().strip()
        
        # GLOBAL RULE: Apply 4-token limit first if >4 tokens
        if len(tokens) > 4:
            tokens = tokens[:4]  # Truncate to first 4 tokens
        
        # Apply brand-specific rules based on token count
        if brand_lower == "tommy":
            # Tommy rule: If only 3 tokens → insert "solid" before last word
            if len(tokens) == 3:
                tokens.insert(-1, "solid")  # Insert "solid" before last token
            # If 4 tokens, keep as-is (like "tall stripped black shirt")
            
        elif brand_lower == "shein":
            # Shein rule: If ends with "shirt" → drop "shirt", insert "curved" before last word
            if tokens and tokens[-1] == "shirt":
                tokens = tokens[:-1]  # Remove "shirt" 
                if len(tokens) >= 1:
                    tokens.insert(-1, "curved")  # Insert "curved" before last token
            # For dresses and others, use normal rule (no changes needed)
            
        elif brand_lower == "reiss":
            # Reiss rule: Drop "shirt" if present (handles >4 token case)
            if tokens and tokens[-1] == "shirt":
                tokens = tokens[:-1]  # Remove "shirt"
                
        elif brand_lower == "next":
            # Next rule: Straightforward title → slug conversion (no special rules)
            pass
        
        else:
            # Default rule for unknown brands: simple title → slug conversion
            pass
        
        # GLOBAL RULE: Ensure exactly 4 tokens (pad if needed)
        while len(tokens) < 4:
            # If less than 4 tokens, this shouldn't happen with proper brand rules
            # But as fallback, pad with generic terms
            tokens.append("item")
        
        # Final safety: ensure exactly 4 tokens
        tokens = tokens[:4]
        
        # Convert tokens back to slug
        slug = "-".join(tokens) if tokens else ""
        return slug
    
    @staticmethod
    def get_products_list(
        db: Session, 
        skip: int = 0, 
        limit: int = 10, 
        brand: Optional[str] = None
    ) -> List[schemas.ProductListItem]:
        """List products - returns 10 products by default with only required fields"""
        products = crud.get_products(db, skip=skip, limit=limit, brand=brand, search=None)
        return [schemas.ProductListItem.from_orm(product) for product in products]
    
    @staticmethod
    def get_product_by_id_direct(db: Session, product_id: int) -> schemas.Product:
        """Get a single product using product ID - returns all fields directly"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return schemas.Product.from_orm(db_product)
    
    @staticmethod
    def create_product_direct(db: Session, product: schemas.ProductCreate) -> schemas.Product:
        """Create new product - accepts Product SKU, Brand Name, Product Title, Quantity. Slug is auto-generated."""
        # Check for duplicate SKU
        db_product_sku = crud.get_product_by_sku(db, product_sku=product.product_sku)
        if db_product_sku:
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")
        
        # Generate slug from title using brand-specific rules
        slug = ProductService._generate_brand_specific_slug(product.brand_name, product.product_title)
        
        # Ensure slug is not empty
        if not slug:
            slug = f"product-{product.product_sku}"
        
        # Business validation: Check if same brand + title combination exists
        existing_products = crud.get_products(db, skip=0, limit=1000, brand=product.brand_name, search=None)
        for existing_product in existing_products:
            if (existing_product.brand_name.lower() == product.brand_name.lower() and 
                existing_product.product_title.lower() == product.product_title.lower()):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Product '{product.product_title}' already exists for brand '{product.brand_name}'. Use a different title or update the existing product."
                )
        
        # Check for duplicate slug (should not happen with business validation above, but safety check)
        db_product_slug = crud.get_product_by_slug(db, product_slug=slug)
        if db_product_slug:
            raise HTTPException(
                status_code=400, 
                detail="Product slug conflict detected. Please use a different product title."
            )
        
        # Create full product data
        full_product_data = schemas.ProductBase(
            product_sku=product.product_sku,
            brand_name=product.brand_name,
            product_slug=slug,
            product_title=product.product_title,
            quantity=product.quantity
        )
        
        created_product = crud.create_product(db=db, product=full_product_data)
        return schemas.Product.from_orm(created_product)
    
    @staticmethod
    def delete_product_direct(db: Session, product_id: int) -> None:
        """Delete a product using product ID - returns 204 No Content"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        crud.delete_product(db=db, product_id=product_id)
        return None
    
    @staticmethod
    def get_products(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        brand: Optional[str] = None, 
        search: Optional[str] = None
    ) -> schemas.ProductListResponse:
        """Get all products with filtering and pagination"""
        products = crud.get_products(db, skip=skip, limit=limit, brand=brand, search=search)
        total = crud.get_products_count(db, brand=brand, search=search)
        return schemas.ProductListResponse(
            message="Products retrieved successfully",
            products=products,
            total=total
        )
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> schemas.ProductResponse:
        """Get product by ID"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return schemas.ProductResponse(
            message="Product retrieved successfully",
            product=db_product
        )
    
    @staticmethod
    def get_product_by_slug(db: Session, product_slug: str) -> schemas.ProductResponse:
        """Get product by slug"""
        db_product = crud.get_product_by_slug(db, product_slug=product_slug)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return schemas.ProductResponse(
            message="Product retrieved successfully",
            product=db_product
        )
    
    @staticmethod
    def get_product_by_sku(db: Session, product_sku: int) -> schemas.ProductResponse:
        """Get product by SKU"""
        db_product = crud.get_product_by_sku(db, product_sku=product_sku)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return schemas.ProductResponse(
            message="Product retrieved successfully",
            product=db_product
        )
    
    @staticmethod
    def create_product(db: Session, product: schemas.ProductCreate) -> schemas.ProductResponse:
        """Create a new product"""
        # Check for duplicate SKU
        db_product_sku = crud.get_product_by_sku(db, product_sku=product.product_sku)
        if db_product_sku:
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")
        
        # Check for duplicate slug
        db_product_slug = crud.get_product_by_slug(db, product_slug=product.product_slug)
        if db_product_slug:
            raise HTTPException(status_code=400, detail="Product with this slug already exists")
        
        created_product = crud.create_product(db=db, product=product)
        return schemas.ProductResponse(
            message="Product created successfully",
            product=created_product
        )
    
    @staticmethod
    def update_product(
        db: Session, 
        product_id: int, 
        product_update: schemas.ProductUpdate
    ) -> schemas.ProductResponse:
        """Update an existing product"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Check for duplicate SKU if being updated
        if product_update.product_sku and product_update.product_sku != db_product.product_sku:
            existing_product = crud.get_product_by_sku(db, product_sku=product_update.product_sku)
            if existing_product:
                raise HTTPException(status_code=400, detail="Product with this SKU already exists")
        
        # Check for duplicate slug if being updated
        if product_update.product_slug and product_update.product_slug != db_product.product_slug:
            existing_product = crud.get_product_by_slug(db, product_slug=product_update.product_slug)
            if existing_product:
                raise HTTPException(status_code=400, detail="Product with this slug already exists")
        
        updated_product = crud.update_product(db=db, product_id=product_id, product_update=product_update)
        return schemas.ProductResponse(
            message="Product updated successfully",
            product=updated_product
        )
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> schemas.ProductResponse:
        """Delete a product"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        deleted_product = crud.delete_product(db=db, product_id=product_id)
        return schemas.ProductResponse(
            message="Product deleted successfully",
            product=deleted_product
        )
    
    @staticmethod
    def get_low_stock_products(db: Session, threshold: int = 10) -> schemas.ProductListResponse:
        """Get products with low stock"""
        products = crud.get_low_stock_products(db, threshold=threshold)
        return schemas.ProductListResponse(
            message="Low stock products retrieved successfully",
            products=products,
            total=len(products)
        )
    
    @staticmethod
    def update_product_stock(
        db: Session, 
        product_id: int, 
        new_quantity: int
    ) -> schemas.ProductResponse:
        """Update product stock quantity"""
        db_product = crud.get_product(db, product_id=product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        updated_product = crud.update_stock(db=db, product_id=product_id, new_quantity=new_quantity)
        return schemas.ProductResponse(
            message="Product stock updated successfully",
            product=updated_product
        )
