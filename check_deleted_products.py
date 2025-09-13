import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.product import Product

def check_deleted_products():
    """Check all products including soft deleted ones"""
    db = SessionLocal()
    try:
        print("=== ALL PRODUCTS (INCLUDING DELETED) ===")
        all_products = db.query(Product).all()
        
        if not all_products:
            print("No products found in database.")
            return
            
        print(f"Total products in database: {len(all_products)}")
        print()
        
        # Separate active and deleted products
        active_products = [p for p in all_products if not p.is_deleted]
        deleted_products = [p for p in all_products if p.is_deleted]
        
        print(f"📊 SUMMARY:")
        print(f"  Active products: {len(active_products)}")
        print(f"  Deleted products: {len(deleted_products)}")
        print()
        
        # Show active products
        if active_products:
            print("✅ ACTIVE PRODUCTS:")
            for product in active_products:
                print(f"  ID: {product.product_id}, SKU: {product.product_sku}, "
                      f"Title: '{product.product_title}', is_deleted: {product.is_deleted}")
            print()
        
        # Show deleted products
        if deleted_products:
            print("🗑️  SOFT DELETED PRODUCTS:")
            for product in deleted_products:
                print(f"  ID: {product.product_id}, SKU: {product.product_sku}, "
                      f"Title: '{product.product_title}', is_deleted: {product.is_deleted}")
            print()
        else:
            print("🗑️  No soft deleted products found.")
            print()
            
        # Show what the API would return (only active products)
        print("🔍 WHAT API RETURNS (active products only):")
        api_products = db.query(Product).filter(Product.is_deleted == False).all()
        if api_products:
            for product in api_products:
                print(f"  ID: {product.product_id}, SKU: {product.product_sku}, Title: '{product.product_title}'")
        else:
            print("  No active products visible to API.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

def check_specific_product(product_id):
    """Check a specific product by ID (including if it's deleted)"""
    db = SessionLocal()
    try:
        # Query without filtering by is_deleted to see the actual state
        product = db.query(Product).filter(Product.product_id == product_id).first()
        
        if product:
            print(f"=== PRODUCT ID {product_id} ===")
            print(f"SKU: {product.product_sku}")
            print(f"Title: {product.product_title}")
            print(f"Brand: {product.brand_name}")
            print(f"Quantity: {product.quantity}")
            print(f"is_deleted: {product.is_deleted}")
            print(f"Status: {'DELETED' if product.is_deleted else 'ACTIVE'}")
        else:
            print(f"Product with ID {product_id} not found in database.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            product_id = int(sys.argv[1])
            check_specific_product(product_id)
        except ValueError:
            print("Please provide a valid product ID number.")
    else:
        check_deleted_products()
