import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(user_id: int) -> str:
    """
    Create a new JWT token for a user
    """
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "user_id": user_id,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> int:
    """
    Verify a JWT token and return the user_id if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
