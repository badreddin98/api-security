# Import needed modules
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models import User
import time
from collections import defaultdict

# Our secret key - in real projects, this should be in environment variables!
SECRET_KEY = 'my-super-secret-key'

# Simple rate limiting
RATE_LIMIT = 5  # requests
RATE_LIMIT_PERIOD = 60  # seconds
request_counts = defaultdict(list)

def is_rate_limited(ip):
    """Check if an IP is rate limited"""
    now = time.time()
    # Clean old requests
    request_counts[ip] = [req_time for req_time in request_counts[ip] 
                         if now - req_time < RATE_LIMIT_PERIOD]
    # Add new request
    request_counts[ip].append(now)
    # Check if too many requests
    return len(request_counts[ip]) > RATE_LIMIT

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        if is_rate_limited(ip):
            return jsonify({
                'message': 'Too many requests. Please try again later.'
            }), 429
        return f(*args, **kwargs)
    return wrapper

def create_token(user_id):
    """
    Creates a JWT token for a user
    """
    # Token will expire in 24 hours
    expiration = datetime.utcnow() + timedelta(days=1)
    
    # Create the token with user info
    token = jwt.encode(
        {
            'user_id': user_id,
            'exp': expiration
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    return token

def check_token(token):
    """
    Checks if a token is valid
    """
    try:
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['user_id']
    except:
        return None

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get token from header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'No token provided'}), 401
        
        # Remove 'Bearer ' from token
        token = token.split(' ')[1]
        
        # Check if token is valid
        user_id = check_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
            
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 401
            
        return f(user, *args, **kwargs)
    return wrapper

# Decorator to check user role
def admin_required(f):
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return wrapper
