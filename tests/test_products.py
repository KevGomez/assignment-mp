import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models import Product

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
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_product_data():
    return {
        "brand": "TestBrand",
        "slug": "test-product-slug",
        "name": "Test Product",
        "stock": 50
    }

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_product(setup_database, sample_product_data):
    response = client.post("/api/v1/products/", json=sample_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Product created successfully"
    assert data["product"]["brand"] == sample_product_data["brand"]
    assert data["product"]["slug"] == sample_product_data["slug"]

def test_create_duplicate_product(setup_database, sample_product_data):
    client.post("/api/v1/products/", json=sample_product_data)
    response = client.post("/api/v1/products/", json=sample_product_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_products(setup_database, sample_product_data):
    client.post("/api/v1/products/", json=sample_product_data)
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Products retrieved successfully"
    assert len(data["products"]) == 1
    assert data["total"] == 1

def test_read_product_by_id(setup_database, sample_product_data):
    create_response = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_response.json()["product"]["id"]
    
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["id"] == product_id

def test_read_product_by_slug(setup_database, sample_product_data):
    client.post("/api/v1/products/", json=sample_product_data)
    
    response = client.get(f"/api/v1/products/slug/{sample_product_data['slug']}")
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["slug"] == sample_product_data["slug"]

def test_read_nonexistent_product(setup_database):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_product(setup_database, sample_product_data):
    create_response = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_response.json()["product"]["id"]
    
    update_data = {"name": "Updated Product Name", "stock": 75}
    response = client.put(f"/api/v1/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["name"] == "Updated Product Name"
    assert data["product"]["stock"] == 75

def test_delete_product(setup_database, sample_product_data):
    create_response = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_response.json()["product"]["id"]
    
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 404

def test_get_low_stock_products(setup_database):
    low_stock_product = {
        "brand": "TestBrand",
        "slug": "low-stock-product",
        "name": "Low Stock Product",
        "stock": 5
    }
    high_stock_product = {
        "brand": "TestBrand",
        "slug": "high-stock-product",
        "name": "High Stock Product",
        "stock": 50
    }
    
    client.post("/api/v1/products/", json=low_stock_product)
    client.post("/api/v1/products/", json=high_stock_product)
    
    response = client.get("/api/v1/products/stock/low?threshold=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 1
    assert data["products"][0]["stock"] <= 10

def test_update_product_stock(setup_database, sample_product_data):
    create_response = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_response.json()["product"]["id"]
    
    response = client.patch(f"/api/v1/products/{product_id}/stock?stock=100")
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["stock"] == 100

def test_search_products(setup_database):
    products = [
        {"brand": "Nike", "slug": "nike-shirt", "name": "Nike Shirt", "stock": 10},
        {"brand": "Adidas", "slug": "adidas-shoes", "name": "Adidas Shoes", "stock": 20},
        {"brand": "Nike", "slug": "nike-pants", "name": "Nike Pants", "stock": 15}
    ]
    
    for product in products:
        client.post("/api/v1/products/", json=product)
    
    response = client.get("/api/v1/products/?brand=Nike")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 2
    
    response = client.get("/api/v1/products/?search=shoes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 1
    assert "shoes" in data["products"][0]["name"].lower()

def test_pagination(setup_database):
    for i in range(15):
        product_data = {
            "brand": f"Brand{i}",
            "slug": f"product-{i}",
            "name": f"Product {i}",
            "stock": i * 10
        }
        client.post("/api/v1/products/", json=product_data)
    
    response = client.get("/api/v1/products/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 10
    assert data["total"] == 15
    
    response = client.get("/api/v1/products/?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 5
