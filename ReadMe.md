# Product Management API

A secure FastAPI-based REST API for managing product inventory with JWT authentication. This API provides full CRUD operations for products with features like search, filtering, pagination, and stock management.

## Features

- **JWT Authentication**: Secure API access with JSON Web Tokens
- **Complete CRUD Operations**: Create, Read, Update, and Delete products
- **Auto-Generated IDs**: Database generates unique integer IDs for products (separate from SKU)
- **SKU Management**: Store and search products by SKU from CSV data
- **Advanced Search**: Search products by name, slug, or SKU
- **Brand Filtering**: Filter products by brand name
- **Pagination**: Efficient pagination for large datasets
- **Stock Management**: Track and update product stock levels
- **Low Stock Alerts**: Identify products with low inventory
- **Data Validation**: Comprehensive input validation using Pydantic
- **Database Integration**: SQLAlchemy ORM with SQLite (configurable for PostgreSQL/MySQL)
- **Security**: All product endpoints require valid JWT tokens
- **Testing**: Comprehensive test suite with pytest
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
│   ├── auth.py              # JWT authentication utilities
│   ├── database.py          # Database configuration and connection
│   ├── models.py            # SQLAlchemy models (Product, User)
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Database CRUD operations
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       └── products.py      # Product management endpoints
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
- OpenAPI ReadOnly Docs: `http://localhost:8000/api/v1/redoc`

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

| Method | Endpoint                       | Description                                    | Parameters                         |
| ------ | ------------------------------ | ---------------------------------------------- | ---------------------------------- |
| GET    | `/api/v1/products/`            | Get all products with filtering and pagination | `skip`, `limit`, `brand`, `search` |
| GET    | `/api/v1/products/{id}`        | Get product by ID                              | `id` (path parameter)              |
| GET    | `/api/v1/products/slug/{slug}` | Get product by slug                            | `slug` (path parameter)            |
| GET    | `/api/v1/products/sku/{sku}`   | Get product by SKU                             | `sku` (path parameter)             |
| POST   | `/api/v1/products/`            | Create new product                             | Product data in request body       |
| PUT    | `/api/v1/products/{id}`        | Update product                                 | `id` (path), update data in body   |
| DELETE | `/api/v1/products/{id}`        | Delete product                                 | `id` (path parameter)              |
| GET    | `/api/v1/products/stock/low`   | Get low stock products                         | `threshold` (query parameter)      |
| PATCH  | `/api/v1/products/{id}/stock`  | Update product stock                           | `id` (path), `stock` (query)       |

### Query Parameters

- **skip**: Number of records to skip (pagination)
- **limit**: Maximum number of records to return (1-1000)
- **brand**: Filter by brand name (case-insensitive)
- **search**: Search in product name, slug, or SKU (case-insensitive)
- **threshold**: Stock threshold for low stock alerts

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
       "sku": "NIKE-AM90-001",
       "brand": "Nike",
       "slug": "nike-air-max-90",
       "name": "Nike Air Max 90",
       "stock": 50
     }'
```

Request Body:

```json
{
  "sku": "NIKE-AM90-001",
  "brand": "Nike",
  "slug": "nike-air-max-90",
  "name": "Nike Air Max 90",
  "stock": 50
}
```

Response:

```json
{
  "message": "Product created successfully",
  "product": {
    "id": 21,
    "sku": "NIKE-AM90-001",
    "brand": "Nike",
    "slug": "nike-air-max-90",
    "name": "Nike Air Max 90",
    "stock": 50
  }
}
```

### 4. Get Products with Filtering (with JWT)

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?brand=Nike&limit=10&skip=0"
```

### 5. Search Products (with JWT)

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/?search=shirt"
```

### 6. Update Product Stock (with JWT)

```bash
curl -X PATCH \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     "http://localhost:8000/api/v1/products/1/stock?stock=25"
```

## Data Model

### Product Schema

```json
{
  "id": 1,
  "sku": "NIKE-AM90-001",
  "brand": "Nike",
  "slug": "nike-air-max-90",
  "name": "Nike Air Max 90",
  "stock": 50
}
```

### Response Format

All API responses follow a consistent format:

```json
{
  "message": "Operation successful",
  "product": {
    /* product data */
  },
  "products": [
    /* array of products */
  ],
  "total": 100
}
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

**API Version**: 1.0.0  
**Last Updated**: September 2025  
**Implemented by**: Kevin Gomez - kevingomez890@gmail.com
