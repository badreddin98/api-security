# Import what we need
from flask import jsonify, request
from app import app, db
from models import User
from utils.util import create_token, login_required, admin_required, rate_limit

# Route to create a new user
@app.route('/register', methods=['POST'])
@rate_limit
def register():
    # Get data from request
    data = request.get_json()
    
    # Check if we have all the info we need
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Check if username is already taken
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    # Create new user
    try:
        new_user = User(
            username=data['username'],
            role=data.get('role', 'user')  # Default to 'user' if no role provided
        )
        new_user.set_password(data['password'])
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
    # Save to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!'}), 201

# Route to login
@app.route('/login', methods=['POST'])
@rate_limit
def login():
    # Get login info
    data = request.get_json()
    
    # Check if we have username and password
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Find user in database
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Wrong username or password'}), 401
    
    # Create token
    token = create_token(user.id)
    
    return jsonify({
        'message': 'Logged in successfully!',
        'token': token,
        'role': user.role
    }), 200

# Example of a protected route - needs login
@app.route('/profile', methods=['GET'])
@login_required
def profile(current_user):
    return jsonify({
        'username': current_user.username,
        'role': current_user.role
    }), 200

# Example of an admin-only route
@app.route('/admin-only', methods=['GET'])
@login_required
@admin_required
def admin_only(current_user):
    return jsonify({
        'message': f'Welcome admin {current_user.username}!'
    }), 200
