from flask import request, url_for
from app_travel.Models import app, db, Car, UPLOAD_FOLDER
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

# UPLOAD_FOLDER = 'app_travel/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cars', methods=['GET'])
# @login_required
def get_cars():
    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
            data = Car.query.order_by(Car.id_car.desc()).all()
            cars_list = []
            for el in data:
                cars_list.append({
                    'id_car': el.id_car,
                    'name': el.name,
                    'specification': el.specification,
                    'capacity': el.capacity,
                    'image': el.image,
                    # 'image': url_for('get_uploaded_image', filename=el.image),
                    'created_at': el.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': el.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                })
            return {'cars': cars_list}, 200
        else:
            return {'message': 'Access denied'}, 403
    else:
        return {'message': 'Unauthorized'}, 401

@app.route('/cars', methods=['POST'])
# @login_required
def create_car():
    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
   
            if 'image' not in request.files:
                return {'message': 'No file part'}, 400

            file = request.files['image']

            if file.filename == '':
                return {'message': 'No selected file'}, 400

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join('app_travel', UPLOAD_FOLDER, filename)

                file.save(file_path)

                image_url = url_for('get_uploaded_image', filename=filename, _external=True)

                data = Car(
                    name=request.form['name'],
                    specification=request.form['specification'],
                    capacity=request.form['capacity'],
                    image=image_url  # Save the URL to the image file
                )
                db.session.add(data)
                db.session.commit()

                return {'message': 'Car created successfully'}, 201
            else:
                return {'message': 'Invalid file type'}, 400
        else:
            return {'message': 'Access denied'}, 403
    else:
        return {'message': 'Unauthorized'}, 401
    
@app.route('/cars/<int:car_id>', methods=['GET'])
# @login_required
def get_car(car_id):
    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
            car = Car.query.get(car_id)
            if car:
                return {
                    'id_car': car.id_car,
                    'name': car.name,
                    'specification': car.specification,
                    'capacity': car.capacity,
                    'image': car.image,
                    'created_at': car.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': car.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }, 200
            else:
                return {'message': 'Car not found'}, 404
        else:
            return {'message': 'Access denied'}, 403
    else:
        return {'message': 'Unauthorized'}, 401

@app.route('/cars/<int:car_id>', methods=['PUT'])
# @login_required
def update_car(car_id):
    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
            car = Car.query.get(car_id)
            if car:
                # Update the car details based on the request data
                if 'image' in request.files:
                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join('app_travel', UPLOAD_FOLDER, filename)
                        file.save(file_path)
                        image_url = url_for('get_uploaded_image', filename=filename, _external=True)
                        car.image = image_url

                if 'name' in request.form:
                    car.name = request.form['name']
                if 'specification' in request.form:
                    car.specification = request.form['specification']
                if 'capacity' in request.form:
                    car.capacity = request.form['capacity']

                db.session.commit()
                return {'message': 'Car updated successfully'}, 200
            else:
                return {'message': 'Car not found'}, 404
        else:
            return {'message': 'Access denied'}, 403
    else:
        return {'message': 'Unauthorized'}, 401


@app.route('/cars/<int:car_id>', methods=['DELETE'])
# @login_required
def delete_car(car_id):
    if current_user.is_authenticated:
        if any(role.role == 'admin' for role in current_user.user_roles):
            car = Car.query.get(car_id)
            if car:
                # Menghapus file terkait jika ada
                if car.image:
                    file_path = os.path.join('../images', UPLOAD_FOLDER, car.image)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    # else:
                    #     return {'message': 'File not found'}, 404

                db.session.delete(car)
                db.session.commit()
                return {'message': 'Car deleted successfully'}, 200
            else:
                return {'message': 'Car not found'}, 404
        else:
            return {'message': 'Access denied'}, 403
    else:
        return {'message': 'Unauthorized'}, 401






