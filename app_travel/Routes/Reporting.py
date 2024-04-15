from sqlalchemy import func
from app_travel.Models import app, db, Order, Schedule, User

@app.route('/report/most-popular-route', methods=['GET'])
def most_popular_route():
    schedules = Schedule.query.with_entities(
        Schedule.from_location,
        Schedule.to_location
    ).all()

    route_counts = {}
    for schedule in schedules:
        route = (schedule.from_location, schedule.to_location)
        if route in route_counts:
            route_counts[route] += 1
        else:
            route_counts[route] = 1

    most_popular_route = max(route_counts, key=route_counts.get)

    return {'most_popular_route': most_popular_route}

@app.route('/report/most-popular-schedule', methods=['GET'])
def most_popular_schedule():
    schedules = Schedule.query.with_entities(
        Schedule.from_location,
        Schedule.to_location,
        Schedule.departure_time,
        Schedule.arrival_time
    ).all()

    schedule_counts = {}
    for schedule in schedules:
        schedule_info = (schedule.from_location, schedule.to_location, schedule.departure_time, schedule.arrival_time)
        if schedule_info in schedule_counts:
            schedule_counts[schedule_info] += 1
        else:
            schedule_counts[schedule_info] = 1

    most_popular_schedule = max(schedule_counts, key=schedule_counts.get)

    most_popular_schedule = list(most_popular_schedule)
    most_popular_schedule[2] = most_popular_schedule[2].strftime('%H:%M:%S')
    most_popular_schedule[3] = most_popular_schedule[3].strftime('%H:%M:%S')

    return {'most_popular_schedule': most_popular_schedule}

@app.route('/report/top-users', methods=['GET'])
def top_users():
    orders = db.session.query(
        Order.id_user,
        func.count().label('order_count')
    ).group_by(Order.id_user).order_by(func.count().desc()).limit(1).all()

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





