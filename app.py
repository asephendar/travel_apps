from app_travel.Models import app
from app_travel.Routes.Cars import app

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)