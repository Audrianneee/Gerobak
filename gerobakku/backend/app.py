from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerobakku.db'
db = SQLAlchemy(app)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    van_id = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_seller = Seller(name=data['name'], van_id=data['van_id'], latitude=data['latitude'], longitude=data['longitude'])
    db.session.add(new_seller)
    db.session.commit()
    return jsonify({'message': 'Seller registered successfully'})

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    seller = Seller.query.filter_by(van_id=data['van_id']).first()
    if seller:
        seller.latitude = data['latitude']
        seller.longitude = data['longitude']
        db.session.commit()
        return jsonify({'message': 'Location updated successfully'})
    return jsonify({'message': 'Seller not found'}), 404

@app.route('/get_sellers', methods=['GET'])
def get_sellers():
    sellers = Seller.query.all()
    return jsonify([{'van_id': seller.van_id, 'latitude': seller.latitude, 'longitude': seller.longitude} for seller in sellers])

@app.route('/get_seller_details', methods=['GET'])
def get_seller_details():
    van_id = request.args.get('van_id')
    seller = Seller.query.filter_by(van_id=van_id).first()
    if seller:
        return jsonify({'name': seller.name, 'van_id': seller.van_id})
    return jsonify({'message': 'Seller not found'}), 404

if __name__ == '__main__':
    db.create_all()
    
    # Add initial data if the database is empty
    if Seller.query.count() == 0:
        initial_data = [
            {"name": "Van 1", "van_id": "van1", "latitude": -6.200000, "longitude": 106.816666},
            {"name": "Van 2", "van_id": "van2", "latitude": -6.210000, "longitude": 106.826666},
            {"name": "Van 3", "van_id": "van3", "latitude": -6.220000, "longitude": 106.836666},
        ]
        for data in initial_data:
            new_seller = Seller(name=data['name'], van_id=data['van_id'], latitude=data['latitude'], longitude=data['longitude'])
            db.session.add(new_seller)
        db.session.commit()
    
    app.run(debug=True)
