from flask import request
from app_travel.Models import app, db, Car
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed
import os

# Inisialisasi UploadSet untuk mengelola jenis file gambar
photos = UploadSet('photos', IMAGES)

# Konfigurasi tempat penyimpanan file gambar
app.config['UPLOADED_PHOTOS_DEST'] = 'app_travel/images'

# Terapkan konfigurasi untuk unggahan
configure_uploads(app, photos)


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
        try:
            image = None
            if 'image' in request.files:
                filename = photos.save(request.files['image'])
                image = photos.url(filename)
            
            data = Car(
                name=request.form['name'],
                specification=request.form['specification'],
                capacity=request.form['capacity'],
                image=image 
            )
            db.session.add(data)
            db.session.commit()
            
            return {'message': 'Car created successfully'}, 201
        except UploadNotAllowed:
            return {'message': 'Invalid image format'}, 400
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
            data.capacity = request.form['capacity'],
            if 'image' in request.files:
                filename = photos.save(request.files['image'])
                data.image = photos.url(filename)
            db.session.commit()
            return {'message': 'Car updated successfully'}
        else:
            return {'message': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/cars/<int:id_car>', methods=['DELETE'])
@login_required
def delete_car(id_car):
    if any(role.role == 'admin' for role in current_user.user_roles):
        car = Car.query.get(id_car)
        if car:
            # Hapus file gambar jika ada
            if car.image:
                image_path = os.path.join(app.root_path, app.config['UPLOADED_PHOTOS_DEST'], car.image)
                if os.path.exists(image_path):
                    os.remove(image_path)

            db.session.delete(car)
            db.session.commit()
            
            return {'message': 'Car deleted successfully'}, 200
        else:
            return {'message': 'Car not found'}, 404
    else:
        return {'message': 'Access denied'}, 403





