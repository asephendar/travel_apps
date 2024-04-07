from flask import request
from app_travel.models import app, db, User, Order, OrderSchedule, Schedule, Car

@app.route('/cars', methods=['GET'])
def get_cars():
    data = Car.query.order_by(Car.id_car.desc()).all()
    cars_list = []
    for el in data:
        cars_list.append({
            'id_car': el.id_car,
            'name': el.name,
            'specification': el.specification,
            'capacity': el.capacity,
            'rental_price': el.rental_price,
            'created_at': el.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': el.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return {'cars': cars_list}, 200

@app.route('/cars', methods=['POST'])
def create_car():
    data = Car(
        name=request.form['name'],
        specification=request.form['specification'],
        capacity=request.form['capacity'],
        rental_price=request.form['rental_price'],
    )
    db.session.add(data)
    db.session.commit()
    return {'message': 'Car created successfully'}, 201

@app.route('/cars/<int:id_car>', methods=['PUT'])
def update_car(id_car):
    data = Car.query.get(id_car)
    if data:
        data.name = request.form['name'],
        data.specification = request.form['specification'],
        data.capacity = request.form['capacity'],
        data.rental_price = request.form['rental_price']
        db.session.commit()
        return {'message': 'Car updated successfully'}
    else:
        return {'message': 'Car not found'}, 404

@app.route('/cars/<int:id_car>', methods=['DELETE'])
def delete_car(id_car):
    data = Car.query.get(id_car)
    if data:
        db.session.delete(data)
        db.session.commit()
        return {'message': 'Car deleted successfully'}
    else:
        return {'message': 'Car not found'}, 404