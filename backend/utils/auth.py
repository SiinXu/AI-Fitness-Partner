from functools import wraps
from flask import request, jsonify
from .jwt_utils import verify_token

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
            
        try:
            # Remove 'Bearer ' prefix if present
            token = auth_header.replace('Bearer ', '')
            user_id = verify_token(token)
            
            if not user_id:
                return jsonify({'error': 'Invalid token'}), 401
                
            # Add user_id to request object
            request.user_id = user_id
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 401
            
    return decorated
