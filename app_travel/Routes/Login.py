from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app_travel.Models import app, db, User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {'message': 'You are already logged in'}
    
    username = request.headers.get('username')
    password = request.headers.get('password')

    user = User.query.filter_by(username = username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return {'message': 'Login successful'}
    else:
        return {'message': 'Invalid username or password'}, 401

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {'message': 'Logout successful'}

@app.route("/registers", methods=["POST"])
def register():
    user = User(
        username=request.form['username'],
        password=generate_password_hash(request.form['password']),
        full_name=request.form['full_name'],
        address=request.form['address'],
        email=request.form['email'],
        phone_number=request.form['phone_number'],
        role='member'
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'User created successfully'}, 201

@app.route('/add_admin', methods=['POST'])
@login_required
def add_admin():
    if current_user.role == 'admin':
        user = User(
            username=request.form['username'],
            password=request.form['password'],
            full_name=request.form['full_name'],
            address=request.form['address'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403