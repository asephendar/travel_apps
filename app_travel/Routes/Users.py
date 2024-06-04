from flask import request
from app_travel.Models import app, db, User, UserRole
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    if any(role.role == 'admin' for role in current_user.user_roles):
        # .filter(UserRole.role == 'member')
        role_users = UserRole.query.join(User).order_by(User.id_user.desc()).all()
        user_list = []
        for user in role_users:
            user_list.append({
                'id_user': user.user.id_user,
                'username': user.user.username,
                'password': user.user.password,
                'full_name': user.user.full_name,
                'address': user.user.address,
                'email': user.user.email,
                'phone_number': user.user.phone_number,
                'role': user.role,
                'created_at': user.user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return {'users': user_list}
    else:
        return {'message': 'Access denied'}, 403
    

@app.route('/users/<int:id_user>', methods=['GET'])
# @login_required
def get_user(id_user):
    # if any(role.role == 'admin' for role in current_user.user_roles):
        user = User.query.get(id_user)
        if not user:
            return {'message': 'User not found'}, 404
        return {
            'id_user': user.id_user,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'address': user.address,
            'phone_number': user.phone_number,
            'role': user.user_roles[0].role
        }
    # else:
    #     return {'message': 'Access denied'}, 403

@app.route('/profile', methods=['GET'])
def get_profile():
    if current_user.is_authenticated:
        return {
            'id_user': current_user.id_user,
            'username': current_user.username,
            'full_name': current_user.full_name,
            'address': current_user.address,
            'email': current_user.email,
            'phone_number': current_user.phone_number,
            'password': current_user.password,
            'role': current_user.user_roles[0].role
        }
    else:
        return {'message': 'You must be logged in to view your profile'}, 401

@app.route('/profile/<int:id_user>', methods=['PUT'])
def update_profile(id_user):
    if current_user.is_authenticated:
        user = User.query.get(id_user)
        if not user:
            return {'message': 'User not found'}, 404
        user.full_name = request.form.get('full_name', user.full_name)
        user.address = request.form.get('address', user.address)
        user.email = request.form.get('email', user.email)
        user.phone_number = request.form.get('phone_number', user.phone_number)
        db.session.commit()
        return {'message': 'Profile updated successfully'}
    else:
        return {'message': 'You must be logged in to update your profile'}, 401

@app.route('/users/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return {'message': 'User not found'}, 404

    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
            user.username = request.form.get('username', user.username)
            password = request.form.get('password')
            if password:
                user.password = generate_password_hash(password)
            user.full_name = request.form.get('full_name', user.full_name)
            user.address = request.form.get('address', user.address)
            user.email = request.form.get('email', user.email)
            user.phone_number = request.form.get('phone_number', user.phone_number)
            user.user_roles[0].role = request.form.get('role', user.user_roles[0].role)

            db.session.commit()
            return {'message': 'User updated successfully'}
        else:
            if current_user.id_user == id_user:
                user.username = request.form.get('username', user.username)
                password = request.form.get('password')
                if password:
                    user.password = generate_password_hash(password)
                user.full_name = request.form.get('full_name', user.full_name)
                user.address = request.form.get('address', user.address)
                user.email = request.form.get('email', user.email)
                user.phone_number = request.form.get('phone_number', user.phone_number)

                db.session.commit()
                return {'message': 'User updated successfully'}
            else:
                return {'message': 'Access denied'}, 403
    else:
        return {'message': 'You must be logged in to update user profiles'}, 401

@app.route('/users/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return {'message': 'User not found'}, 404

    if current_user.is_authenticated and any(role.role == 'admin' for role in current_user.user_roles):
        try:
            # Delete related user roles first
            UserRole.query.filter_by(id_user=id_user).delete()

            # Now delete the user
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500
    else:
        return {'message': 'Access denied'}, 403

