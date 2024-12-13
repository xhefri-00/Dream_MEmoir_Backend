"""
Initialize Flask extensions for the application.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Initialize the extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
