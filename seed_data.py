import csv
import os
from app.database import SessionLocal, engine, Base
from app.models import Product, User
from app.utils.auth_utils import get_password_hash

def load_products_from_csv():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create a default admin user for testing
        existing_user = db.query(User).filter(User.username == "admin").first()
        if not existing_user:
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123")
            )
            db.add(admin_user)
            print("Created default admin user (username: admin, password: admin123)")
        
        csv_file_path = os.path.join(os.path.dirname(__file__), "data", "products.csv")
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            for row in csv_reader:
                if len(row) >= 5:
                    # CSV columns: SKU, Brand, Slug, Title, Quantity
                    sku, brand, slug, title, quantity = row
                    
                    # Check if product with this SKU or slug already exists
                    existing_product = db.query(Product).filter(
                        (Product.product_sku == int(sku.strip())) | (Product.product_slug == slug.strip())
                    ).first()
                    if not existing_product:
                        product = Product(
                            product_sku=int(sku.strip()),
                            brand_name=brand.strip(),
                            product_slug=slug.strip(),
                            product_title=title.strip(),
                            quantity=int(quantity),
                            is_deleted=False
                        )
                        db.add(product)
                        print(f"Added product: {title.strip()} (SKU: {sku})")
        
        db.commit()
        print("Products loaded successfully from CSV!")
        
        total_products = db.query(Product).count()
        print(f"Total products in database: {total_products}")
        
    except Exception as e:
        print(f"Error loading products: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_products_from_csv()
