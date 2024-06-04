from app_travel.Models import app, User
from app_travel.Routes.Cars import app
from app_travel.Routes.Schedules import app
from app_travel.Routes.Users import app
from app_travel.Routes.Orders import app
from app_travel.Routes.OrderSchedules import app
from app_travel.Routes.Reporting import app
from app_travel.Routes.Login import app
from flask_login import LoginManager, current_user

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

@app.route('/')
def index():
    return 'Hello, World!'

# @app.route('/profile')
# def profile():
#     if current_user.is_authenticated:
#         return f'{current_user.full_name}'
#     else:
#         return 'You are not logged in.'

if __name__ == '__main__':
    app.run(debug=True)