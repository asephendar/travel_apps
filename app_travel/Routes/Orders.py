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
                'date': order.date.strftime("%d-%m-%Y"),
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
                'date': order.date.strftime("%d-%m-%Y"),
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

    schedules = Schedule.query.filter(
        Schedule.from_location.ilike(f"%{from_location}%"),
        Schedule.to_location.ilike(f"%{to_location}%"),
        Schedule.date_trip == date_trip
    ).all()

    schedules_list = [{
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
    } for schedule in schedules]

    return {'schedules': schedules_list}, 200

# @app.route('/search_schedule', methods=['GET'])
# def search_schedule():
#     from_location = request.args.get('from_location')
#     to_location = request.args.get('to_location')
#     date_trip = request.args.get('date_trip')

#     schedules = Schedule.query.filter_by(from_location=from_location, to_location=to_location, date_trip=date_trip).all()
    
#     if not schedules:
#         return {'message': 'Tidak ada jadwal yang ditemukan'}, 404

#     response = []
#     for schedule in schedules:
#         response.append({
#             'id_schedule': schedule.id_schedule,
#             'id_car': schedule.id_car,
#             'from_location': schedule.from_location,
#             'to_location': schedule.to_location,
#             'departure_time': schedule.departure_time.strftime('%H:%M'),
#             'arrival_time': schedule.arrival_time.strftime('%H:%M'),
#             'date_trip': schedule.date_trip.strftime("%d-%m-%Y"),
#             'available_seats': schedule.available_seats,
#             'status_still_available': schedule.status_still_available,
#             'rental_price': f"Rp {schedule.rental_price:,}",
#             'car': {
#                 'name': schedule.car.name,
#                 'specification': schedule.car.specification,
#                 'capacity': schedule.car.capacity
#             }
#         })

#     return {'schedules': response}, 200

@app.route('/orders/<int:id_order>', methods=['GET'])
# @login_required
def get_order(id_order):
    # order = Order.query.filter_by(id_order=id_order, id_user=current_user.id_user).first()
    order = Order.query.filter_by(id_order=id_order).first()
    if order:
        return {'order': {
            'id_order': order.id_order,
            # 'id_user': order.id_user,
            # 'date': order.date.strftime("%d-%m-%Y"),
            # 'number_participants': order.number_participants,
            # 'total_amount': f"Rp {order.total_amount:,}",
            'status_payment': order.status_payment,
            'status_order': order.order_status
            # 'payment_gateway': order.payment_gateway
        }}
    else:
        return {'message': 'Order not found'}, 404
    
@app.route('/orders', methods=['POST'])
# @login_required
def create_order():
    if any(role.role == 'member' for role in current_user.user_roles):
        # Ambil data dari formulir
        number_participants = int(request.form['number_participants'])
        payment_gateway = request.form['payment_gateway']

        try:
            date_trip = datetime.strptime(request.form['date_trip'], '%d-%m-%Y').date()
        except ValueError:
            return {'message': 'Invalid date format. Expected format is YYYY-MM-DD.'}, 400

        try:
            departure_time = datetime.strptime(request.form['departure_time'], '%H:%M').time()
            arrival_time = datetime.strptime(request.form['arrival_time'], '%H:%M').time()
        except ValueError:
            return {'message': 'Invalid time format. Expected format is HH:MM.'}, 400

        schedule_data = {
            'from_location': request.form['from_location'],
            'to_location': request.form['to_location'],
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'date_trip': date_trip
        }

        order = Order(
            id_user=current_user.id_user,
            date=datetime.now().date(),
            number_participants=number_participants,
            payment_gateway=payment_gateway
        )
        db.session.add(order)
        db.session.commit()

        total_amount = 0
        
        # Ambil jadwal berdasarkan input dari formulir
        schedule = Schedule.query.filter_by(
            from_location=schedule_data['from_location'],
            to_location=schedule_data['to_location'],
            date_trip=schedule_data['date_trip']
        ).first()
        if schedule:
            total_amount += number_participants * schedule.rental_price
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
    
# @app.route('/orders', methods=['POST'])
# # @login_required
# def create_order():
#     if any(role.role == 'member' for role in current_user.user_roles):
#         # Ambil data dari formulir
#         number_participants = int(request.form['number_participants'])
#         payment_gateway = request.form['payment_gateway']
#         schedule_data = {
#             'from_location': request.form['from_location'],
#             'to_location': request.form['to_location'],
#             'date_trip': datetime.strptime(request.form['date_trip'], '%Y-%m-%d').date()
#         }

#         order = Order(
#             id_user=current_user.id_user,
#             date=datetime.now().date(),
#             number_participants=number_participants,
#             payment_gateway=payment_gateway
#         )
#         db.session.add(order)
#         db.session.commit()

#         total_amount = 0
        
#         # Ambil jadwal berdasarkan input dari formulir
#         schedule = Schedule.query.filter_by(
#             from_location=schedule_data['from_location'],
#             to_location=schedule_data['to_location'],
#             date_trip=schedule_data['date_trip']
#         ).first()
#         if schedule:
#             total_amount += number_participants * schedule.rental_price
#             order_schedule = OrderSchedule(
#                 id_order=order.id_order,
#                 id_schedule=schedule.id_schedule
#             )
#             db.session.add(order_schedule)
                
#         order.total_amount = total_amount
#         db.session.commit()

#         return {'message': 'Order created successfully'}, 201
#     else:
#         return {'message': 'Access denied'}, 403

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