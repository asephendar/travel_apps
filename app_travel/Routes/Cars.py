from flask import request
from app_travel.Models import app, db, Car, User, UserRole
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return {'message': 'User not found'}, 404

    user_role = UserRole.query.filter_by(id_user=current_user_id).first()

    if user_role and user_role.role == 'admin':
        data = Car.query.order_by(Car.id_car.desc()).all()
        cars_list = []
        for car in data:
            cars_list.append({
                'id_car': car.id_car,
                'name': car.name,
                'specification': car.specification,
                'capacity': car.capacity,
                'created_at': car.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': car.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return {'cars': cars_list}, 200
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars', methods=['POST'])
@login_required
def create_car():
    if any(role.role == 'admin' for role in current_user.user_roles):
        data = Car(
            name=request.form['name'],
            specification=request.form['specification'],
            capacity=request.form['capacity']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Car created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars/<int:id_car>', methods=['PUT'])
@login_required
def update_car(id_car):
    if any(role.role == 'admin' for role in current_user.user_roles):
        data = Car.query.get(id_car)
        if data:
            data.name = request.form['name'],
            data.specification = request.form['specification'],
            data.capacity = request.form['capacity']
            db.session.commit()
            return {'message': 'Car updated successfully'}
        else:
            return {'message': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars/<int:id_car>', methods=['DELETE'])
@login_required
def delete_car(id_car):
    if any(role.role == 'admin' for role in current_user.user_roles):
        data = Car.query.get(id_car)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Car deleted successfully'}
        else:
            return {'message': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403