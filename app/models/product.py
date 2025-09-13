from sqlalchemy import Column, Integer, String, Boolean, Index
from ..database import Base

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_sku = Column(Integer, index=True)  # Removed unique=True, will use conditional constraint
    brand_name = Column(String, index=True)
    product_slug = Column(String, index=True)  # Removed unique=True, will use conditional constraint
    product_title = Column(String, index=True)
    quantity = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False, index=True)
    
    # Conditional unique constraints - only for non-deleted products
    __table_args__ = (
        # SKU uniqueness only for active products
        Index('idx_unique_sku_active', 'product_sku', unique=True, 
              sqlite_where=Column('is_deleted') == False),
        # Slug uniqueness only for active products  
        Index('idx_unique_slug_active', 'product_slug', unique=True,
              sqlite_where=Column('is_deleted') == False),
    )
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, product_sku={self.product_sku}, product_title='{self.product_title}', brand_name='{self.brand_name}', quantity={self.quantity})>"
