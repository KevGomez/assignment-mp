from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..utils.auth_schemas import UserCreate, User as UserSchema, Token
from ..utils import auth_utils

class AuthService:
    
    @staticmethod
    def register_user(db: Session, user: UserCreate) -> UserSchema:
        """Register a new user"""
        db_user = auth_utils.get_user(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        hashed_password = auth_utils.get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def login_user(db: Session, user_credentials: UserCreate) -> Token:
        """Authenticate user and return JWT token"""
        user = auth_utils.authenticate_user(db, user_credentials.username, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
