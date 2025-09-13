import subprocess
import sys
import os

def run_seed_data():
    """Load initial data from CSV"""
    print("Loading initial data from CSV...")
    try:
        subprocess.run([sys.executable, "seed_data.py"], check=True)
        print("✓ Data loaded successfully!")
    except subprocess.CalledProcessError:
        print("✗ Failed to load data")
        return False
    return True

def start_server():
    """Start the FastAPI server"""
    print("Starting Product Management API server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
    except subprocess.CalledProcessError:
        print("✗ Failed to start server")

def main():
    print("=== Product Management API Setup ===")
    
    # Check if database exists
    if not os.path.exists("products.db"):
        print("Database not found. Setting up initial data...")
        if not run_seed_data():
            sys.exit(1)
    else:
        print("✓ Database found")
    
    print("\nAPI will be available at:")
    print("  - Main API: http://localhost:8000")
    print("  - Documentation: http://localhost:8000/docs")
    print("  - Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    start_server()

if __name__ == "__main__":
    main()
