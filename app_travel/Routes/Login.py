from flask import request, session
from flask_login import login_user, logout_user, login_required, current_user
from app_travel.Models import app, db, User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import jwt_required, get_jwt_identity

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username).first()
#     if user and check_password_hash(user.password, password):
#         login_user(user)
#         access_token = user.generate_access_token()
#         return {'message': 'Login successful', 'access_token': access_token}, 200
#     else:
#         return {'message': 'Invalid username or password'}, 401

@app.route('/check_login')
# @login_required
def check_login():
    # return {'loggedIn': True}
    if 'username' in session:
        return {'authenticated': True}
    else:
        return {'authenticated': False}, 401

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        # Mengambil role user sebagai string
        role = 'member'  # Default role
        for user_role in user.user_roles:
            if user_role.role == 'admin':
                role = 'admin'
                break
        return {'message': 'Login successful', 'role': role}
    else:
        return {'message': 'Invalid username or password'}, 401

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     user = User.query.get(current_user)
#     return {'user_id': user.id_user, 'username': user.username}, 200

@app.route('/logout', methods=['POST'])  # Ubah metode menjadi POST
@login_required
def logout():
    logout_user()
    return {'message': 'Logout successful'}

# @app.route("/logout", methods=["GET"])
# @login_required
# def logout():
#     logout_user()
#     return {'message': 'Logout successful'}

@app.route("/registers", methods=["POST"])
def register():
    user = User(
        username=request.form.get('username'),
        password=generate_password_hash(request.form.get('password')),
        full_name=request.form.get('full_name'),
        address=request.form.get('address'),
        email=request.form.get('email'),
        phone_number=request.form.get('phone_number')
    )

    db.session.add(user)
    db.session.commit()

    user_role = UserRole(
        role='member',
        id_user=user.id_user
    )

    db.session.add(user_role)
    db.session.commit()

    return {'message': 'User created successfully'}, 201

@app.route('/add_admin', methods=['POST'])
@login_required
def add_admin():
    user = User(
        username=request.form.get('username'),
        password=generate_password_hash(request.form.get('password')),
        full_name=request.form.get('full_name'),
        address=request.form.get('address'),
        email=request.form.get('email'),
        phone_number=request.form.get('phone_number')
    )

    db.session.add(user)
    db.session.commit()

    user_role = UserRole(
        role=request.form.get('role'),
        id_user=user.id_user
    )

    db.session.add(user_role)
    db.session.commit()

    return {'message': 'User created successfully'}, 201