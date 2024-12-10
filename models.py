# Import what we need from app.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Create User model
class User(db.Model):
    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username must be unique
    password_hash = db.Column(db.String(120), nullable=False)  # Store hashed password, never plain text!
    role = db.Column(db.String(20), nullable=False, default='user')  # Role can be 'user' or 'admin'

    @staticmethod
    def is_password_strong(password):
        """Check if password meets security requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        return True, "Password is strong"

    # Method to set password - this will hash it before saving
    def set_password(self, password):
        is_strong, message = self.is_password_strong(password)
        if not is_strong:
            raise ValueError(message)
        self.password_hash = generate_password_hash(password)

    # Method to check if password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # String representation of our user
    def __repr__(self):
        return f'<User: {self.username}>'
