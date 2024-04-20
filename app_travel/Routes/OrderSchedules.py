from app_travel.Models import app, db, OrderSchedule
from flask_login import login_required, current_user

@app.route('/order_schedules', methods=['GET'])
@login_required
def get_order_schedules():
    if any(role.role == 'admin' for role in current_user.user_roles):
        order_schedules = OrderSchedule.query.order_by(OrderSchedule.id_order.desc()).all()
        order_list = []
        for el in order_schedules:
            order_list.append({
                'id_order': el.id_order,
                'id_schedule': el.id_schedule,
                'order': {
                    'id_user': el.order.id_user,
                    'date': el.order.date.strftime('%Y-%m-%d'),
                    'number_participants': el.order.number_participants,
                    'total_amount': f"Rp {el.order.total_amount:,}",
                    'status_payment': el.order.status_payment,
                    'payment_gateway': el.order.payment_gateway,
                    'user': {
                        'username': el.order.user.username,
                        'full_name': el.order.user.full_name
                    }
                },
                'schedule': {
                    'from_location': el.schedule.from_location,
                    'to_location': el.schedule.to_location,
                    'departure_time': el.schedule.departure_time.strftime('%H:%M'),
                    'arrival_time': el.schedule.arrival_time.strftime('%H:%M'),
                    'day_of_week': el.schedule.day_of_week,
                    'date_trip': el.schedule.date_trip.strftime('%Y-%m-%d'),
                    'rental_price': f"Rp {el.schedule.rental_price:,}"
                }
            })
        return {'orders': order_list}
    else:
        order_schedules = OrderSchedule.query.filter(OrderSchedule.order.has(id_user=current_user.id_user)).order_by(OrderSchedule.id_order.desc()).all()
        order_list = []
        for el in order_schedules:
            order_list.append({
                'id_order': el.id_order,
                'id_schedule': el.id_schedule,
                'order': {
                    'id_user': el.order.id_user,
                    'date': el.order.date.strftime('%Y-%m-%d'),
                    'number_participants': el.order.number_participants,
                    'total_amount': f"Rp {el.order.total_amount:,}",
                    'status_payment': el.order.status_payment,
                    'payment_gateway': el.order.payment_gateway,
                    'user': {
                        'username': el.order.user.username,
                        'full_name': el.order.user.full_name
                    }
                },
                'schedule': {
                    'from_location': el.schedule.from_location,
                    'to_location': el.schedule.to_location,
                    'departure_time': el.schedule.departure_time.strftime('%H:%M'),
                    'arrival_time': el.schedule.arrival_time.strftime('%H:%M'),
                    'day_of_week': el.schedule.day_of_week,
                    'date_trip': el.schedule.date_trip.strftime('%Y-%m-%d'),
                    'rental_price': f"Rp {el.schedule.rental_price:,}"
                }
            })
        return {'orders': order_list}

@app.route('/order_schedules/<int:id_order>', methods=['DELETE'])
def delete_order_schedule(id_order):
    if any(role.role == 'admin' for role in current_user.user_roles):
        order_schedules = OrderSchedule.query.filter_by(id_order=id_order).all()
        if order_schedules:
            for order_schedule in order_schedules:
                db.session.delete(order_schedule)
            db.session.commit()
            return {'message': 'Order Schedules with id_order {} deleted successfully'.format(id_order)}, 200
        else:
            return {'error': 'Order Schedules with id_order {} not found'.format(id_order)}, 404
    else:
        return {'message': 'Access denied'}, 403