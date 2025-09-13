from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.auth_schemas import UserCreate, User, Token
from ...database import get_db
from ...services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=User)
def register_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """Register a new user"""
    return AuthService.register_user(db, user)

@router.post("/token", response_model=Token)
def login_for_access_token(
    user_credentials: UserCreate,
    db: Session = Depends(get_db)
):
    """Login and get JWT access token"""
    return AuthService.login_user(db, user_credentials)
