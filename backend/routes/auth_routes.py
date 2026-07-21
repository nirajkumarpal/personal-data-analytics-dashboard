from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Success
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200