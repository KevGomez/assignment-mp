import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models.product import Product
from app.models.user import User
from app.utils.auth_utils import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    
    # Create test admin user
    db = TestingSessionLocal()
    admin_user = User(
        username="testadmin",
        hashed_password=get_password_hash("testpass123")
    )
    db.add(admin_user)
    db.commit()
    db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_headers(setup_database):
    """Get JWT token for authenticated requests"""
    login_data = {
        "username": "testadmin",
        "password": "testpass123"
    }
    response = client.post("/api/v1/auth/token", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_product_data():
    return {
        "product_sku": 12345,
        "brand_name": "Tommy",
        "product_title": "High split shirt",
        "quantity": 50
    }

class TestAuthentication:
    def test_register_user(self, setup_database):
        user_data = {
            "username": "newuser",
            "password": "newpass123"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data

    def test_login_user(self, setup_database):
        login_data = {
            "username": "testadmin",
            "password": "testpass123"
        }
        response = client.post("/api/v1/auth/token", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, setup_database):
        login_data = {
            "username": "testadmin",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/token", json=login_data)
        assert response.status_code == 401

class TestProductAPI:
    def test_create_product(self, auth_headers, sample_product_data):
        response = client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["product_sku"] == 12345
        assert data["brand_name"] == "Tommy"
        assert data["product_title"] == "High split shirt"
        assert data["product_slug"] == "high-split-solid-shirt"  # Tommy brand rule
        assert data["quantity"] == 50
        assert "product_id" in data

    def test_create_product_duplicate_sku(self, auth_headers, sample_product_data):
        # Create first product
        client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        
        # Try to create with same SKU
        duplicate_data = sample_product_data.copy()
        duplicate_data["product_title"] = "Different title"
        response = client.post("/api/v1/products/", json=duplicate_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Product with this SKU already exists" in response.json()["detail"]

    def test_create_product_duplicate_brand_title(self, auth_headers, sample_product_data):
        # Create first product
        client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        
        # Try to create with same brand + title but different SKU
        duplicate_data = sample_product_data.copy()
        duplicate_data["product_sku"] = 99999
        response = client.post("/api/v1/products/", json=duplicate_data, headers=auth_headers)
        assert response.status_code == 400
        assert "already exists for brand" in response.json()["detail"]

    def test_create_product_same_title_different_brand(self, auth_headers, sample_product_data):
        # Create first product
        client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        
        # Create with same title but different brand (should be allowed)
        different_brand_data = {
            "product_sku": 99999,
            "brand_name": "Shein",
            "product_title": "High split shirt",
            "quantity": 25
        }
        response = client.post("/api/v1/products/", json=different_brand_data, headers=auth_headers)
        assert response.status_code == 201

    def test_list_products_default(self, auth_headers, sample_product_data):
        # Create a product first
        client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        
        response = client.get("/api/v1/products/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        
        product = data[0]
        assert "product_id" in product
        assert "product_sku" in product
        assert "product_title" in product
        assert "brand_name" in product
        assert "product_slug" in product
        # List response should NOT include quantity

    def test_list_products_with_pagination(self, auth_headers):
        # Create multiple products
        for i in range(15):
            product_data = {
                "product_sku": 10000 + i,
                "brand_name": "Tommy",
                "product_title": f"Test product {i}",
                "quantity": 10
            }
            client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        
        # Test default limit (10)
        response = client.get("/api/v1/products/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        
        # Test custom limit
        response = client.get("/api/v1/products/?limit=5", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Test skip
        response = client.get("/api/v1/products/?skip=10&limit=5", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_list_products_brand_filter(self, auth_headers):
        # Create products with different brands
        tommy_product = {
            "product_sku": 11111,
            "brand_name": "Tommy",
            "product_title": "Tommy shirt",
            "quantity": 10
        }
        shein_product = {
            "product_sku": 22222,
            "brand_name": "Shein",
            "product_title": "Shein dress",
            "quantity": 15
        }
        
        client.post("/api/v1/products/", json=tommy_product, headers=auth_headers)
        client.post("/api/v1/products/", json=shein_product, headers=auth_headers)
        
        # Filter by Tommy
        response = client.get("/api/v1/products/?brand=Tommy", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["brand_name"] == "Tommy"
        
        # Filter by Shein (case-insensitive)
        response = client.get("/api/v1/products/?brand=shein", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["brand_name"] == "Shein"

    def test_get_single_product(self, auth_headers, sample_product_data):
        # Create product first
        create_response = client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        product_id = create_response.json()["product_id"]
        
        # Get single product
        response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Should include ALL fields
        assert data["product_id"] == product_id
        assert data["product_sku"] == 12345
        assert data["brand_name"] == "Tommy"
        assert data["product_title"] == "High split shirt"
        assert data["product_slug"] == "high-split-solid-shirt"
        assert data["quantity"] == 50

    def test_get_nonexistent_product(self, auth_headers):
        response = client.get("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_product(self, auth_headers, sample_product_data):
        # Create product first
        create_response = client.post("/api/v1/products/", json=sample_product_data, headers=auth_headers)
        product_id = create_response.json()["product_id"]
        
        # Delete product
        response = client.delete(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify product is deleted (should return 404)
        response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_nonexistent_product(self, auth_headers):
        response = client.delete("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404

class TestSlugGeneration:
    def test_tommy_brand_slug_generation(self, auth_headers):
        # Test Tommy 3-token rule
        product_data = {
            "product_sku": 30001,
            "brand_name": "Tommy",
            "product_title": "High split shirt",  # 3 tokens
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "high-split-solid-shirt"
        
        # Test Tommy 4-token rule
        product_data = {
            "product_sku": 30002,
            "brand_name": "Tommy",
            "product_title": "Tall stripped black shirt",  # 4 tokens
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "tall-stripped-black-shirt"

    def test_shein_brand_slug_generation(self, auth_headers):
        # Test Shein shirt rule
        product_data = {
            "product_sku": 30003,
            "brand_name": "Shein",
            "product_title": "Tall buttoned black shirt",
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "tall-buttoned-curved-black"
        
        # Test Shein dress rule (no change)
        product_data = {
            "product_sku": 30004,
            "brand_name": "Shein",
            "product_title": "Solid split red dress",
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "solid-split-red-dress"

    def test_reiss_brand_slug_generation(self, auth_headers):
        # Test Reiss shirt removal
        product_data = {
            "product_sku": 30005,
            "brand_name": "Reiss",
            "product_title": "Roll up sleeve black shirt",
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "roll-up-sleeve-black"

    def test_next_brand_slug_generation(self, auth_headers):
        # Test Next direct conversion
        product_data = {
            "product_sku": 30006,
            "brand_name": "Next",
            "product_title": "Cold shoulder red dress",
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "cold-shoulder-red-dress"

    def test_global_4_token_rule(self, auth_headers):
        # Test >4 tokens gets truncated
        product_data = {
            "product_sku": 30007,
            "brand_name": "Tommy",
            "product_title": "Rare max dress end white extra",  # 6 tokens
            "quantity": 10
        }
        response = client.post("/api/v1/products/", json=product_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["product_slug"] == "rare-max-dress-end"  # First 4 tokens

class TestAPIAuthentication:
    def test_unauthenticated_requests(self):
        # All product endpoints should require authentication
        response = client.get("/api/v1/products/")
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
        
        response = client.get("/api/v1/products/1")
        assert response.status_code == 403
        
        response = client.post("/api/v1/products/", json={})
        assert response.status_code == 403
        
        response = client.delete("/api/v1/products/1")
        assert response.status_code == 403

class TestSystemEndpoints:
    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Product Management API" in data["message"]