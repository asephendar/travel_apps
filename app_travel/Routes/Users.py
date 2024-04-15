from flask import request
from app_travel.Models import app, db, User
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    if current_user.role == 'admin':
        users = User.query.filter_by(role='member').order_by(User.id_user.desc()).all()
        user_list = []
        for user in users:
            user_list.append({
                'id_user': user.id_user,
                'username': user.username,
                'password': user.password,
                'full_name': user.full_name,
                'address': user.address,
                'email': user.email,
                'phone_number': user.phone_number,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return {'users': user_list}
    else:
        return {'message': 'Access denied'}, 403

@app.route('/users/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    if current_user.role == 'admin':
        user = User.query.get(id_user)
        if user:
            user.username=request.form['username']
            user.password=generate_password_hash(request.form['password'])
            user.full_name=request.form['full_name']
            user.address=request.form['address']
            user.email=request.form['email']
            user.phone_number=request.form['phone_number']

            db.session.commit()
            return {'message': 'User updated successfully'}
        else:
            return {'message': 'User not found'}, 404
    else:
        if current_user.id_user == id_user:
            user = User.query.get(id_user)
            if user:
                user.password=generate_password_hash(request.form['password'])
                user.full_name=request.form['full_name']
                user.address=request.form['address']

                db.session.commit()
                return {'message': 'User updated successfully'}
            else:
                return {'message': 'User not found'}, 404
        else:
            return {'message': 'Access denied'}, 403