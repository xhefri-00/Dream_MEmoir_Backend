from flask import Blueprint, request, jsonify, Request
from extensions import db
from models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.

    Returns:
        Response object containing success or error message.
    """
    data = request.json
    if not all([data.get("username"), data.get("email"), data.get("password")]):
        return jsonify({"message": "All fields are required"}), 400

    # Check if the user already exists (by email or username)
    if User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first():
        return jsonify({"message": "User already exists"}), 400

    # Create new user and hash the password using the set_password method
    new_user = User(username=data["username"], email=data["email"], password=data["password"])

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Log in a user and return a JWT token.

    Returns:
        Response object containing the access token or error message.
    """
    data = request.json
    print(request.get_data())
    # Use email to query the user for authentication
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate a JWT token with email as identity
    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token, "username":user.username,"id":user.id}), 200