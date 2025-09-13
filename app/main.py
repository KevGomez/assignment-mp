from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import products, auth
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Management API",
    description="A secure API for managing product inventory with JWT authentication",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "Product Management API",
        "version": "1.0.0",
        "authentication": "JWT Bearer token required for product endpoints"
    }

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
