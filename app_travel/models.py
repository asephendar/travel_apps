from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/travel_apps'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.Enum('admin', 'member', name='user_role_enum'), nullable=False, default='member')
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Order(db.Model):
    __tablename__ = 'orders'

    id_order = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    number_participants = db.Column(db.Integer, nullable=False, default=1)
    total_amount = db.Column(db.Integer, nullable=False, default=0)
    status_payment = db.Column(db.Boolean, nullable=False, default=False)
    order_status = db.Column(db.Enum('pending', 'processing', 'completed', name='order_status_enum'), nullable=False, default='pending') 
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class OrderSchedule(db.Model):
    __tablename__ = 'order_schedules'

    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), primary_key=True)
    id_schedule = db.Column(db.Integer, db.ForeignKey('schedules.id_schedule'), primary_key=True)

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id_schedule = db.Column(db.Integer, primary_key=True)
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car'))
    from_location = db.Column(db.String(255), nullable=False)
    to_location = db.Column(db.String(255), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.String(255), nullable=False)
    date_trip = db.Column(db.Date, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    status_still_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Car(db.Model):
    __tablename__ = 'cars'

    id_car = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specification = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    rental_price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
