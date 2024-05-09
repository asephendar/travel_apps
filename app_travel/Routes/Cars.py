from flask import request
from app_travel.Models import app, db, Car
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'app_travel/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cars', methods=['GET'])
@login_required
def get_cars():
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
                'created_at': el.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': el.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return {'cars': cars_list}, 200
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars', methods=['POST'])
@login_required
def create_car():
    if any(role.role == 'admin' for role in current_user.user_roles):
        # Check if the post request has the file part
        if 'image' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['image']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            data = Car(
                name=request.form['name'],
                specification=request.form['specification'],
                capacity=request.form['capacity'],
                image=file_path  # Save the path to the image file
            )
            db.session.add(data)
            db.session.commit()
            return {'message': 'Car created successfully'}, 201
        else:
            return {'message': 'Invalid file type'}, 400
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars/<int:id_car>', methods=['PUT'])
@login_required
def update_car(id_car):
    if any(role.role == 'admin' for role in current_user.user_roles):
        data = Car.query.get(id_car)
        if data:
            data.name = request.form['name'],
            data.specification = request.form['specification'],
            data.capacity = request.form['capacity']
            db.session.commit()
            return {'message': 'Car updated successfully'}
        else:
            return {'message': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars/<int:car_id>', methods=['DELETE'])
@login_required
def delete_car(car_id):
    car = Car.query.get(car_id)

    if not car:
        return {'message': 'Car not found'}, 404

    if any(role.role == 'admin' for role in current_user.user_roles):
        # Hapus file gambar jika ada
        if car.image:
            try:
                os.remove(car.image)
            except OSError as e:
                print("Error: %s : %s" % (car.image, e.strerror))

        db.session.delete(car)
        db.session.commit()
        return {'message': 'Car deleted successfully'}, 200
    else:
        return {'message': 'Access denied'}, 403





