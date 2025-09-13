from sqlalchemy import Column, Integer, String
from ..database import Base

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_sku = Column(Integer, unique=True, index=True)
    brand_name = Column(String, index=True)
    product_slug = Column(String, unique=True, index=True)
    product_title = Column(String, index=True)
    quantity = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, product_sku={self.product_sku}, product_title='{self.product_title}', brand_name='{self.brand_name}', quantity={self.quantity})>"
