from flask import request
from app_travel.Models import app, db, Schedule, Car
from flask_login import login_required, current_user

@app.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.order_by(Schedule.id_schedule.desc()).all()
    schedules_list = []
    for schedule in schedules:
        schedules_list.append({
            'id_schedule': schedule.id_schedule,
            'id_car': schedule.id_car,
            'from_location': schedule.from_location,
            'to_location': schedule.to_location,
            'departure_time': schedule.departure_time.strftime("%H:%M"),
            'arrival_time': schedule.arrival_time.strftime("%H:%M"),
            'date_trip': schedule.date_trip.strftime("%d-%m-%Y"),
            'available_seats': schedule.available_seats,
            'status_still_available': schedule.status_still_available,
            'rental_price': f"IDR {schedule.rental_price:,}",
            'created_at': schedule.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': schedule.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'car': {
                'name': schedule.car.name,
                'specification': schedule.car.specification,
                'capacity': schedule.car.capacity,
                'image': schedule.car.image
            }
        })
    return {'schedules': schedules_list}, 200


@app.route('/schedules/<int:id_schedule>', methods=['GET'])
def get_schedule_by_id(id_schedule):
    schedule = Schedule.query.get(id_schedule)
    if schedule:
        return {'schedule': {
            'id_schedule': schedule.id_schedule,
            'id_car': schedule.id_car,
            'from_location': schedule.from_location,
            'to_location': schedule.to_location,
            'departure_time': schedule.departure_time.strftime("%H:%M"),
            'arrival_time': schedule.arrival_time.strftime("%H:%M"),
            'date_trip': schedule.date_trip.strftime("%d-%m-%Y"),
            'available_seats': schedule.available_seats,
            'status_still_available': schedule.status_still_available,
            'rental_price': f"IDR {schedule.rental_price:,}",
            'created_at': schedule.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': schedule.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'car': {
                'name': schedule.car.name,
                'specification': schedule.car.specification,
                'capacity': schedule.car.capacity,
                'image': schedule.car.image
            }
        }}, 200
    else:
        return {'message': 'Schedule not found'}, 404


@app.route('/schedules', methods=['POST'])
# @login_required
def create_schedule():
    if any(role.role == 'admin' for role in current_user.user_roles):
        car_name = request.form['car_name']
        car = Car.query.filter_by(name=car_name).first()

        if car:
            schedule = Schedule(
                id_car=car.id_car,
                from_location=request.form['from_location'],
                to_location=request.form['to_location'],
                departure_time=request.form['departure_time'],
                arrival_time=request.form['arrival_time'],
                date_trip=request.form['date_trip'],
                available_seats=request.form['available_seats'],
                rental_price=request.form['rental_price']
            )
            db.session.add(schedule)
            db.session.commit()

            return {'message': 'Schedule created successfully'}, 201
        else:
            return {'error': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403


@app.route('/schedules/<int:id_schedule>', methods=['PUT'])
# @login_required
def update_schedule(id_schedule):
    if any(role.role == 'admin' for role in current_user.user_roles):
        data = request.form
        schedule = Schedule.query.get(id_schedule)
        if schedule:
            schedule.from_location = data['from_location']
            schedule.to_location = data['to_location']
            schedule.departure_time = data['departure_time']
            schedule.arrival_time = data['arrival_time']
            schedule.date_trip = data['date_trip']
            schedule.available_seats = int(data['available_seats'])
            status = data['status_still_available'].lower()
            if status == 'true':
                schedule.status_still_available = True
            elif status == 'false':
                schedule.status_still_available = False
            else:
                return {'error': 'Invalid value for status_still_available'}, 400
            schedule.rental_price = float(data['rental_price'])
            db.session.commit()
            return {'message': 'Schedule updated successfully'}, 200
        else:
            return {'error': 'Schedule not found'}, 404
    else:
        return {'message': 'Access denied'}, 403



@app.route('/schedules/<int:id_schedule>', methods=['DELETE'])
@login_required
def delete_schedule(id_schedule):
    if any(role.role == 'admin' for role in current_user.user_roles):
        schedule = Schedule.query.get(id_schedule)
        if schedule:
            db.session.delete(schedule)
            db.session.commit()
            return {'message': 'Schedule deleted successfully'}, 200
        else:
            return {'error': 'Schedule not found'}, 404
    else:
        return {'message': 'Access denied'}, 403