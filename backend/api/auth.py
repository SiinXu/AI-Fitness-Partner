from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from backend.models import db
from backend.models.user import User
import os
import logging
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        current_app.logger.info("Starting registration process")
        data = request.get_json()
        current_app.logger.info(f"Received registration data: {data}")
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                current_app.logger.error(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            current_app.logger.error(f"Username {data['username']} already exists")
            return jsonify({'error': 'Username already exists'}), 400
            
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            current_app.logger.error(f"Email {data['email']} already exists")
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user with bcrypt password hash
        current_app.logger.info("Creating new user")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt).decode('utf-8')
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=password_hash,
            fitness_level=data.get('fitness_level', 'beginner'),
            modelscope_api_key=data.get('modelscope_api_key'),
            fish_audio_api_key=data.get('fish_audio_api_key')
        )
        
        # Save to database
        current_app.logger.info("Saving user to database")
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"User created with ID: {new_user.id}")
        
        # Generate token
        current_app.logger.info("Generating JWT token")
        token = jwt.encode(
            {
                'user_id': new_user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            },
            os.getenv('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
        current_app.logger.info("JWT token generated successfully")
        
        response_data = {
            'message': 'Registration successful',
            'token': token,
            'user': new_user.to_dict()
        }
        current_app.logger.info("Registration completed successfully")
        return jsonify(response_data), 201
        
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        current_app.logger.error(f"Error type: {type(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'error': f'Failed to register: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        current_app.logger.info("Starting login process")
        data = request.get_json()
        current_app.logger.info(f"Received login data: {data}")
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            current_app.logger.error("Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        current_app.logger.info(f"Looking up user with email: {data['email']}")
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            current_app.logger.error("User not found")
            return jsonify({'error': 'Invalid email or password'}), 401
            
        # Verify password using bcrypt
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            current_app.logger.error("Invalid password")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        current_app.logger.info("Generating JWT token")
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            },
            os.getenv('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
        current_app.logger.info("JWT token generated successfully")
        
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }
        current_app.logger.info("Login completed successfully")
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        current_app.logger.error(f"Error type: {type(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Failed to login: {str(e)}'}), 500

@auth_bp.route('/api-keys', methods=['GET', 'POST'])
def manage_api_keys():
    try:
        current_app.logger.info("Starting API keys management")
        
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            current_app.logger.error("No valid authorization header")
            return jsonify({'error': 'No valid authorization header'}), 401
            
        token = auth_header.split(' ')[1]
        
        try:
            # Decode JWT token
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            current_app.logger.error("Token has expired")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            current_app.logger.error("Invalid token")
            return jsonify({'error': 'Invalid token'}), 401
            
        # Find user
        user = User.query.get(user_id)
        if not user:
            current_app.logger.error("User not found")
            return jsonify({'error': 'User not found'}), 404
            
        if request.method == 'GET':
            # Return API keys
            return jsonify({
                'modelscope_api_key': user.modelscope_api_key or '',
                'fish_audio_api_key': user.fish_audio_api_key or ''
            }), 200
        else:  # POST
            data = request.get_json()
            
            # Update API keys
            if 'modelscope_api_key' in data:
                user.modelscope_api_key = data['modelscope_api_key']
            if 'fish_audio_api_key' in data:
                user.fish_audio_api_key = data['fish_audio_api_key']
                
            db.session.commit()
            
            current_app.logger.info("API keys updated successfully")
            return jsonify({
                'message': 'API keys updated successfully',
                'modelscope_api_key': user.modelscope_api_key or '',
                'fish_audio_api_key': user.fish_audio_api_key or ''
            }), 200
        
    except Exception as e:
        current_app.logger.error(f"API keys management error: {str(e)}")
        return jsonify({'error': f'Failed to manage API keys: {str(e)}'}), 500

@auth_bp.route('/modelscope-key', methods=['POST'])
def update_modelscope_key():
    try:
        current_app.logger.info("Starting ModelScope API key update")
        data = request.get_json()
        
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            current_app.logger.error("No valid authorization header")
            return jsonify({'error': 'No valid authorization header'}), 401
            
        token = auth_header.split(' ')[1]
        
        try:
            # Decode JWT token
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            current_app.logger.error("Token has expired")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            current_app.logger.error("Invalid token")
            return jsonify({'error': 'Invalid token'}), 401
            
        # Find user
        user = User.query.get(user_id)
        if not user:
            current_app.logger.error("User not found")
            return jsonify({'error': 'User not found'}), 404
            
        # Update API key
        user.modelscope_api_key = data.get('api_key')
        db.session.commit()
        
        current_app.logger.info("ModelScope API key updated successfully")
        return jsonify({
            'message': 'ModelScope API key updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"ModelScope API key update error: {str(e)}")
        return jsonify({'error': f'Failed to update ModelScope API key: {str(e)}'}), 500
