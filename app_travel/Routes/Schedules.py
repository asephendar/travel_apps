from flask import request
from app_travel.Models import app, db, Schedule, Car

@app.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    schedules_list = []
    for schedule in schedules:
        car = Car.query.get(schedule.id_car)
        schedules_list.append({
            'id_schedule': schedule.id_schedule,
            'id_car': schedule.id_car,
            'from_location': schedule.from_location,
            'to_location': schedule.to_location,
            'departure_time': schedule.departure_time.strftime("%H:%M"),
            'arrival_time': schedule.arrival_time.strftime("%H:%M"),
            'day_of_week': schedule.day_of_week,
            'date_trip': schedule.date_trip.strftime("%Y-%m-%d"),
            'available_seats': schedule.available_seats,
            'status_still_available': schedule.status_still_available,
            'rental_price': f"Rp {schedule.rental_price:,}",
            'created_at': schedule.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': schedule.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'car': {
                'name': car.name,
                'specification': car.specification,
                'capacity': car.capacity
            }
        })
    return {'schedules': schedules_list}, 200

@app.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.json
    # Mencari mobil berdasarkan nama
    car_name = data['car_name']
    car = Car.query.filter_by(name=car_name).first()

    if car:
        # Jika mobil ditemukan, membuat objek jadwal perjalanan dengan id_car yang sesuai
        schedule = Schedule(
            id_car=car.id_car,
            from_location=data['from_location'],
            to_location=data['to_location'],
            departure_time=data['departure_time'],
            arrival_time=data['arrival_time'],
            day_of_week=data['day_of_week'],
            date_trip=data['date_trip'],
            available_seats=data['available_seats'],
            status_still_available=data['status_still_available'],
            rental_price=data['rental_price']
        )
        db.session.add(schedule)
        db.session.commit()

        return {'message': 'Schedule created successfully'}, 201
    else:
        return {'error': 'Car not found'}, 404