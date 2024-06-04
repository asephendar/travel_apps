from sqlalchemy import func
from app_travel.Models import app, db, Order, Schedule, User, OrderSchedule

@app.route('/report/popular_route', methods=['GET'])
def report_popular_route():
    popular_routes = db.session.query(
        Schedule.from_location,
        Schedule.to_location,
        func.count(Order.id_order).label('order_count')
    ).select_from(Schedule).join(OrderSchedule).join(Order).group_by(
        Schedule.from_location,
        Schedule.to_location
    ).order_by(
        func.count(Order.id_order).desc()
    ).limit(3).all()

    result = []
    for route in popular_routes:
        result.append({
            'from_location': route.from_location,
            'to_location': route.to_location,
            'order_count': route.order_count
        })

    return result

@app.route('/report/popular_schedule', methods=['GET'])
def report_popular_schedule():
    # Query the database to get the most popular schedule orders
    popular_schedules = db.session.query(
        Schedule,
        func.count(OrderSchedule.id_order).label('order_count')
    ).join(OrderSchedule).group_by(Schedule).order_by(func.count(OrderSchedule.id_order).desc()).limit(3).all()

    # Check if there are popular schedules
    if popular_schedules:
        response = []
        for popular_schedule in popular_schedules:
            schedule = popular_schedule[0]
            order_count = popular_schedule[1]

            # Append the schedule information to the response list
            response.append({
                'id_schedule': schedule.id_schedule,
                'from_location': schedule.from_location,
                'to_location': schedule.to_location,
                'departure_time': schedule.departure_time.strftime('%H:%M'),
                'arrival_time': schedule.arrival_time.strftime('%H:%M'),
                'order_count': order_count
            })

        # Return the response as JSON
        return response
    else:
        return {
            'message': 'No popular schedules found'
        }


@app.route('/report/top_users', methods=['GET'])
def top_users():
    orders = db.session.query(
        Order.id_user,
        func.count().label('order_count')
    ).group_by(Order.id_user).order_by(func.count().desc()).limit(3).all()

    top_users = []
    for order in orders:
        user = User.query.get(order.id_user)
        top_users.append({
            'user_id': order.id_user,
            'username': user.username,
            'full_name': user.full_name,
            'order_count': order.order_count
        })

    return {'top_users': top_users}
# ambil url seacrh, per-halaman limit=10, page untuk halaman berapa




