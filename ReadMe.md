# Product Management API

A secure FastAPI-based REST API for product management with JWT authentication and smart brand-specific slug generation. Built with domain-driven architecture following exact assignment requirements.

## Features

- **JWT Authentication**: Secure API access with JSON Web Tokens
- **REST API Compliance**: Exact implementation of assignment requirements
- **Auto-Generated IDs**: Database generates unique integer IDs for products (separate from SKU)
- **Smart Slug Generation**: Brand-specific slug generation with global 4-token rule
- **Product Management**: Create, Read, Delete operations (as per requirements)
- **Advanced Filtering**: Filter products by brand name (case-insensitive)
- **Pagination**: Support for `limit` and `skip` query parameters
- **Data Validation**: Comprehensive input validation using Pydantic
- **Domain-Driven Architecture**: Clean separation of concerns with layered design
- **Database Integration**: SQLAlchemy ORM with SQLite (configurable for PostgreSQL/MySQL)
- **Security**: All product endpoints require valid JWT tokens
- **OpenAPI Documentation**: Interactive API documentation with Swagger UI
- **Containerization**: Docker support with Colima compatibility

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for database operations
- **Pydantic**: Data validation and serialization using Python type annotations
- **JWT (JSON Web Tokens)**: Secure authentication and authorization
- **SQLite**: Lightweight database (easily configurable for PostgreSQL/MySQL)
- **Uvicorn**: High-performance ASGI server for running the application
- **Pytest**: Comprehensive testing framework with fixtures and mocking
- **Docker & Colima**: Containerization for consistent development and deployment
- **Passlib & Bcrypt**: Secure password hashing
- **Python-Jose**: JWT token creation and validation

## Project Structure

```
product-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and connection
│   ├── models/              # Domain-specific models
│   │   ├── __init__.py
│   │   ├── product.py       # Product SQLAlchemy model
│   │   └── user.py          # User SQLAlchemy model
│   ├── schemas/             # Domain-specific schemas
│   │   ├── __init__.py
│   │   └── product_schemas.py # Product Pydantic schemas
│   ├── crud/                # Domain-specific CRUD operations
│   │   ├── __init__.py
│   │   └── product_crud.py  # Product database operations
│   ├── utils/               # Utilities and helpers
│   │   ├── __init__.py
│   │   ├── auth_utils.py    # JWT authentication utilities
│   │   └── auth_schemas.py  # Authentication Pydantic schemas
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication business logic
│   │   └── product_service.py # Product business logic
│   └── routers/             # API route handlers
│       └── v1/              # API version 1
│           ├── __init__.py
│           ├── auth.py      # Authentication endpoints
│           └── products.py  # Product management endpoints
├── data/
│   └── products.csv         # Initial product data (SKU, Brand, Slug, Title, Quantity)
├── tests/
│   └── test_products.py     # Comprehensive test suite
├── seed_data.py             # Script to load CSV data and create admin user
├── start.py                 # Convenient startup script
├── requirements.txt         # Python dependencies with versions
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── ReadMe.md               # This comprehensive documentation
```

## Installation & Setup

### Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Docker & Colima** (for containerized deployment) OR **Docker Desktop**
- **Git** (for version control)

### Local Development Setup

1. **Clone the repository and navigate to the project directory**

   ```bash
   cd product-api
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Load initial data and create admin user**

   ```bash
   python seed_data.py
   ```

   This will:

   - Create database tables
   - Load all products from `data/products.csv`
   - Create default admin user as below

5. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

   Or use the convenient startup script:

   ```bash
   python start.py
   ```

**The API will be available at:**

- Main API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/api/v1/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### Docker Setup (with Colima or Docker Desktop)

#### Prerequisites

- **Colima**: `brew install colima docker docker-compose`
- **Docker Desktop**: Install from Docker website

#### Using Colima

1. **Start Colima**

   ```bash
   colima start
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

3. **Load initial data and create admin user (in a separate terminal)**

   ```bash
   docker-compose exec api python seed_data.py
   ```

   This creates the admin user and loads all CSV products.

4. **Stop Colima when done**
   ```bash
   colima stop
   ```

#### Using Docker Desktop

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

2. **Load initial data and create admin user (in a separate terminal)**
   ```bash
   docker-compose exec api python seed_data.py
   ```

## CSV Data Structure

The `data/products.csv` file contains product information with the following columns:

| Column | Type    | Description      | Example                  |
| ------ | ------- | ---------------- | ------------------------ |
| 1      | Integer | Product SKU      | `2842534`                |
| 2      | String  | Brand Name       | `Tommy`                  |
| 3      | String  | Product Slug     | `high-split-solid-shirt` |
| 4      | String  | Product Title    | `High split shirt`       |
| 5      | Integer | Quantity (Stock) | `101`                    |

**Note**: The database auto-generates unique integer IDs separate from the SKU values.

## Architecture Overview

The application follows a **layered architecture** with clear separation of concerns:

### **🏗️ Layer Structure:**

1. ** API Layer (`routers/v1/`)**

   - Handles HTTP requests and responses
   - Manages authentication and authorization
   - Input validation and error handling
   - Clean, focused route handlers

2. ** Service Layer (`services/`)**

   - Contains all business logic
   - Data validation and processing
   - Error handling and business rules
   - Coordinates between routers and data layer

3. ** Data Layer (`crud/`, `models/`)**

   - Database operations and queries
   - Domain-specific CRUD operations
   - Data models organized by domain
   - Raw database interactions

4. ** Support Layers:**
   - **`schemas/`**: Domain-specific Pydantic models
   - **`utils/`**: Shared utilities and helpers
   - **`database.py`**: Database configuration

### **📋 Benefits:**

- **Domain-Driven Design**: Code organized by business domains (Product, User)
- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Business logic is isolated and easily testable
- **Maintainability**: Changes in one layer don't affect others
- **API Versioning**: Easy to add v2, v3 APIs alongside v1
- **Reusability**: Services can be used by multiple routers
- **Scalability**: Easy to add new domains (Orders, Inventory, etc.)
- **Clean Imports**: Clear dependency structure and imports

## Authentication Flow

1. **Register** a new user or use the default admin account
2. **Login** to get a JWT token
3. **Include the JWT token** in the `Authorization: Bearer <token>` header for all product requests
4. **Token expires** after 30 minutes (configurable)

**Default Admin Account:**

- Username: `admin`
- Password: `admin123`

## API Documentation

Once the application is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/api/v1/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/api/v1/redoc`
- **Health Check**: `http://localhost:8000/api/v1/health`
- **OpenAPI JSON Schema**: `http://localhost:8000/openapi.json`

## API Endpoints

### System Routes

- **Root**: `GET /` - Welcome message and API information
- **Health Check**: `GET /api/v1/health` - API health status

### Authentication (`/api/v1/auth`)

| Method | Endpoint                | Description             | Parameters                       |
| ------ | ----------------------- | ----------------------- | -------------------------------- |
| POST   | `/api/v1/auth/register` | Register new user       | User credentials in request body |
| POST   | `/api/v1/auth/token`    | Login and get JWT token | User credentials in request body |

### Product Management (`/api/v1/products`) - **Requires JWT Authentication**

| Method | Endpoint                | Description                               | Parameters                   |
| ------ | ----------------------- | ----------------------------------------- | ---------------------------- |
| GET    | `/api/v1/products/`     | List products (default 10) with filtering | `skip`, `limit`, `brand`     |
| GET    | `/api/v1/products/{id}` | Get single product by ID (all fields)     | `id` (path parameter)        |
| POST   | `/api/v1/products/`     | Create new product (auto-generates slug)  | Product data in request body |
| DELETE | `/api/v1/products/{id}` | Delete product by ID                      | `id` (path parameter)        |

### Query Parameters

- **skip**: Number of records to skip (pagination) - Default: 0

  - Example: `skip=10` skips the first 10 products
  - Used for pagination: page 2 with limit 10 = `skip=10&limit=10`

- **limit**: Maximum number of records to return (1-1000) - Default: 10

  - Example: `limit=5` returns maximum 5 products
  - Validation: Must be between 1 and 1000

- **brand**: Filter by brand name (case-insensitive partial matching)
  - Example: `brand=Tommy` returns products where brand contains "Tommy"
  - Case-insensitive: `brand=tommy` works the same as `brand=Tommy`
  - Partial matching: `brand=Tom` matches "Tommy" brand products
  - Available brands: Tommy, Shein, Reiss, Next

## Request/Response Examples

### 1. Register New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "password": "securepassword123"
     }'
```

Request Body:

```json
{
  "username": "newuser",
  "password": "securepassword123"
}
```

Response:

```json
{
  "id": 2,
  "username": "newuser"
}
```

### 2. Get JWT Token (Login)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "admin123"
     }'
```

Request Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create Product (with JWT)

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "product_sku": 12345,
       "brand_name": "Tommy",
       "product_title": "High split shirt",
       "quantity": 50
     }'
```

**🔒 Business Validation Rules:**

- **SKU Uniqueness**: Each `product_sku` must be unique across all products
- **Brand + Title Uniqueness**: Same brand cannot have duplicate product titles
- **Case-Insensitive**: `"High Split Shirt"` = `"high split shirt"`

**Examples:**

```bash
# ✅ ALLOWED: Different brands, same title
POST {"product_sku": 1001, "brand_name": "Tommy", "product_title": "Red Shirt", "quantity": 10}
POST {"product_sku": 1002, "brand_name": "Shein", "product_title": "Red Shirt", "quantity": 15}

# ✅ ALLOWED: Same brand, different titles
POST {"product_sku": 1003, "brand_name": "Tommy", "product_title": "Red Shirt", "quantity": 10}
POST {"product_sku": 1004, "brand_name": "Tommy", "product_title": "Blue Shirt", "quantity": 20}

# 🚫 BLOCKED: Same brand + same title
POST {"product_sku": 1005, "brand_name": "Tommy", "product_title": "Red Shirt", "quantity": 10}
POST {"product_sku": 1006, "brand_name": "Tommy", "product_title": "Red Shirt", "quantity": 25}
# Error: "Product 'Red Shirt' already exists for brand 'Tommy'"
```

**🔧 Smart Brand-Specific Slug Generation:**

The `product_slug` is automatically generated using **GLOBAL 4-TOKEN RULE** + **brand-specific rules**:

### **🌐 GLOBAL RULE: All slugs have exactly 4 tokens**

- **>4 tokens**: Truncate to first 4 tokens
- **<4 tokens**: Apply brand-specific padding
- **=4 tokens**: Apply brand-specific modifications

### **🏷️ Brand Rules:**

**Tommy:**

- 3 tokens → insert "solid" before last word
- 4+ tokens → keep first 4 as-is
- Examples:
  - `"High split shirt"` → `"high-split-solid-shirt"`
  - `"Rare max dress end white"` → `"rare-max-dress-end"`

**Shein:**

- Ends with "shirt" → drop "shirt", insert "curved" before last word
- Examples: `"Tall buttoned black shirt"` → `"tall-buttoned-curved-black"`

**Reiss:**

- Drop "shirt" suffix if present
- Examples: `"Roll up sleeve black shirt"` → `"roll-up-sleeve-black"`

**Next:**

- Direct 4-token conversion
- Examples: `"Cold shoulder red dress"` → `"cold-shoulder-red-dress"`

**Other Brands:**

- Default: first 4 tokens with lowercase + hyphens

Request Body:

```json
{
  "product_sku": 12345,
  "brand_name": "Tommy",
  "product_title": "High split shirt",
  "quantity": 50
}
```

Response:

```json
{
  "product_id": 21,
  "product_sku": 12345,
  "brand_name": "Tommy",
  "product_slug": "high-split-solid-shirt",
  "product_title": "High split shirt",
  "quantity": 50
}
```

### 4. List Products with Filtering and Pagination (with JWT)

```bash
# Get first 10 products (default)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/"

# Pagination: Get 5 products, skip first 10
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?limit=5&skip=10"

# Brand filtering: Get all Tommy products
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?brand=Tommy"

# Brand filtering (case-insensitive): Get all tommy products
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?brand=tommy"

# Combined: Get 3 Shein products, skip first 2
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?brand=Shein&limit=3&skip=2"

# Partial brand matching: Get products containing "Tom"
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?brand=Tom"
```

**Query Parameter Examples:**

| URL                                     | Description                      |
| --------------------------------------- | -------------------------------- |
| `/api/v1/products/`                     | Default: First 10 products       |
| `/api/v1/products/?limit=5`             | First 5 products                 |
| `/api/v1/products/?skip=10`             | Skip first 10, get next 10       |
| `/api/v1/products/?limit=3&skip=5`      | Skip 5, get next 3               |
| `/api/v1/products/?brand=Tommy`         | All Tommy brand products         |
| `/api/v1/products/?brand=tommy`         | Case-insensitive: Tommy products |
| `/api/v1/products/?brand=Tom`           | Partial match: Tommy products    |
| `/api/v1/products/?brand=Shein&limit=5` | First 5 Shein products           |

**Pagination Examples:**

```bash
# Page 1: First 10 products (default)
GET /api/v1/products/

# Page 2: Next 10 products
GET /api/v1/products/?skip=10&limit=10

# Page 3: Next 10 products
GET /api/v1/products/?skip=20&limit=10

# Custom page size: 5 products per page
# Page 1: GET /api/v1/products/?limit=5
# Page 2: GET /api/v1/products/?skip=5&limit=5
# Page 3: GET /api/v1/products/?skip=10&limit=5
```

### 5. Get Single Product (with JWT)

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/1"
```

### 6. Delete Product (with JWT)

```bash
curl -X DELETE \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/1"
```

## Data Model

### Product Schema

```json
{
  "product_id": 1,
  "product_sku": 2842534,
  "brand_name": "Tommy",
  "product_slug": "high-split-solid-shirt",
  "product_title": "High split shirt",
  "quantity": 101
}
```

### Response Formats

**List Products Response (GET /products/):**

```json
[
  {
    "product_id": 1,
    "product_sku": 2842534,
    "product_title": "High split shirt",
    "brand_name": "Tommy",
    "product_slug": "high-split-solid-shirt"
  },
  {
    "product_id": 2,
    "product_sku": 2842633,
    "product_title": "Tall stripped black shirt",
    "brand_name": "Tommy",
    "product_slug": "tall-stripped-black-shirt"
  }
]
```

**Filtered Response (GET /products/?brand=Tommy&limit=2):**

```json
[
  {
    "product_id": 1,
    "product_sku": 2842534,
    "product_title": "High split shirt",
    "brand_name": "Tommy",
    "product_slug": "high-split-solid-shirt"
  },
  {
    "product_id": 2,
    "product_sku": 2842633,
    "product_title": "Tall stripped black shirt",
    "brand_name": "Tommy",
    "product_slug": "tall-stripped-black-shirt"
  }
]
```

**Single Product Response (GET /products/{id}):**

```json
{
  "product_id": 1,
  "product_sku": 2842534,
  "brand_name": "Tommy",
  "product_slug": "high-split-solid-shirt",
  "product_title": "High split shirt",
  "quantity": 101
}
```

**Delete Response (DELETE /products/{id}):**

```
204 No Content
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## Database Configuration

The application uses SQLite by default. To use a different database:

1. **Create a `.env` file** (copy from `.env.example`)
2. **Set the DATABASE_URL**:
   - PostgreSQL: `postgresql://username:password@localhost/dbname`
   - MySQL: `mysql://username:password@localhost/dbname`
   - SQLite: `sqlite:///./products.db`

## Development Guidelines

### Code Structure

- **Models**: Database models using SQLAlchemy ORM
- **Schemas**: Pydantic models for request/response validation
- **CRUD**: Database operations separated from API logic
- **Routers**: API endpoints organized by functionality
- **Tests**: Comprehensive test coverage for all endpoints

### Adding New Features

1. Update the database model in `models.py`
2. Create/update Pydantic schemas in `schemas.py`
3. Add CRUD operations in `crud.py`
4. Implement API endpoints in appropriate router
5. Write tests for new functionality

## Deployment

### Production Considerations

- Use a production database (PostgreSQL, MySQL)
- Set up proper environment variables
- Configure CORS settings appropriately
- Use a reverse proxy (nginx)
- Set up SSL/TLS certificates
- Implement proper logging and monitoring

### Environment Variables

- `DATABASE_URL`: Database connection string
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Support

For questions or issues, please create an issue in the repository or contact the development team.

---

## Implementation Status

✅ **Complete Assignment Implementation**

- ✅ **List Products**: Returns 10 products by default with Product ID, SKU, Title, Brand, Slug
- ✅ **Get Product**: Single product by ID with all fields
- ✅ **Create Product**: Accepts SKU, Brand, Title, Quantity (auto-generates slug)
- ✅ **Delete Product**: Removes product by ID (returns 404 after deletion)
- ✅ **Query Parameters**: Full support for `limit`, `skip`, and `brand` filtering
- ✅ **JWT Authentication**: All product endpoints secured
- ✅ **Smart Slug Generation**: Brand-specific rules with global 4-token constraint
- ✅ **Docker Integration**: Full containerization support
- ✅ **OpenAPI Documentation**: Interactive API docs
- ✅ **Domain Architecture**: Clean, maintainable code structure

**API Version**: 1.0.0  
**Last Updated**: September 2025  
**Status**: Production Ready ✨
