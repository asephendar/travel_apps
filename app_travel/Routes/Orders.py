from flask import request
from app_travel.Models import app, db, Order, Schedule, OrderSchedule
from datetime import datetime
from flask_login import login_required, current_user

@app.route('/orders', methods=['GET'])
@login_required
def get_orders():
    if any(role.role == 'admin' for role in current_user.user_roles):
        orders = Order.query.order_by(Order.id_order.desc()).all()
        order_list = []
        for order in orders:
            order_list.append({
                'id_order': order.id_order,
                'id_user': order.id_user,
                'date': order.date.strftime('%Y-%m-%d'),
                'number_participants': order.number_participants,
                'total_amount': f"Rp {order.total_amount:,}",
                'status_payment': order.status_payment,
                'status_order': order.order_status,
                'payment_gateway': order.payment_gateway,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user': {
                    'username': order.user.username,
                    'full_name': order.user.full_name
                }
            })
        return {'orders': order_list}
    else:
        orders = Order.query.filter_by(id_user=current_user.id_user).order_by(Order.id_order.desc()).all()
        order_list = []
        for order in orders:
            order_list.append({
                'id_order': order.id_order,
                'id_user': order.id_user,
                'date': order.date.strftime('%Y-%m-%d'),
                'number_participants': order.number_participants,
                'total_amount': f"Rp {order.total_amount:,}",
                'status_payment': order.status_payment,
                'status_order': order.order_status,
                'payment_gateway': order.payment_gateway,
                'user': {
                    'username': order.user.username,
                    'full_name': order.user.full_name
                }
            })
        return {'orders': order_list}

@app.route('/search_schedule', methods=['GET'])
def search_schedule():
    from_location = request.args.get('from_location')
    to_location = request.args.get('to_location')
    date_trip = request.args.get('date_trip')

    schedules = Schedule.query.filter_by(from_location=from_location, to_location=to_location, date_trip=date_trip).all()
    
    if not schedules:
        return {'message': 'Tidak ada jadwal yang ditemukan'}, 404

    response = []
    for schedule in schedules:
        response.append({
            'id_schedule': schedule.id_schedule,
            'id_car': schedule.id_car,
            'from_location': schedule.from_location,
            'to_location': schedule.to_location,
            'departure_time': schedule.departure_time.strftime('%H:%M'),
            'arrival_time': schedule.arrival_time.strftime('%H:%M'),
            'day_of_week': schedule.day_of_week,
            'date_trip': schedule.date_trip.strftime('%Y-%m-%d'),
            'available_seats': schedule.available_seats,
            'status_still_available': schedule.status_still_available,
            'rental_price': f"Rp {schedule.rental_price:,}",
            'car': {
                'name': schedule.car.name,
                'specification': schedule.car.specification,
                'capacity': schedule.car.capacity
            }
        })

    return {'schedules': response}, 200

@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    if any(role.role == 'member' for role in current_user.user_roles):
        data = request.json

        order = Order(
            id_user=current_user.id_user,
            date=datetime.now().date(),
            number_participants=data['number_participants'],
            payment_gateway=data['payment_gateway']
        )
        db.session.add(order)
        db.session.commit()

        total_amount = 0
        
        for schedule_data in data['schedule']:
            schedule = Schedule.query.filter_by(
                from_location=schedule_data['from_location'],
                to_location=schedule_data['to_location'],
                date_trip=schedule_data['date_trip']
            ).first()
            if schedule:
                total_amount += data['number_participants'] * schedule.rental_price
                order_schedule = OrderSchedule(
                    id_order=order.id_order,
                    id_schedule=schedule.id_schedule
                )
                db.session.add(order_schedule)
                
        order.total_amount = total_amount
        db.session.commit()

        return {'message': 'Order created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/orders/<int:id_order>', methods=['PUT'])
@login_required
def update_order(id_order):
    if any(role.role == 'admin' for role in current_user.user_roles):
        order = Order.query.get(id_order)
        if order:
            order.order_status = request.form['order_status'].lower()
            order.status_payment = request.form['status_payment'].lower() == 'true'
            db.session.commit()
            return {'message': 'Order updated successfully'}
        else:
            return {'message': 'Order not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/orders/<int:id_order>', methods=['DELETE'])
@login_required
def delete_order(id_order):
    if any(role.role == 'admin' for role in current_user.user_roles):
        order = Order.query.get(id_order)
        if order:
            db.session.delete(order)
            db.session.commit()
            return {'message': 'Order deleted successfully'}
        else:
            return {'message': 'Order not found'}, 404
    else:
        return {'message': 'Access denied'}, 403