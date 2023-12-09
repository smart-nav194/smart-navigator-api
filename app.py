# type: ignore
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


class CoordinatesSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


coordinates = {
    'latitude': 14.0833428,
    'longitude': 121.1440427,
    'updated_at': datetime.now().isoformat(),
}


coordinates_schema = CoordinatesSchema()


@app.route('/api/coordinates', methods=['GET', 'POST'])
def handle_coordinates():
    global coordinates

    if request.method == 'GET':
        return jsonify(coordinates), 200

    elif request.method == 'POST':
        try:
            secret_key = os.getenv('SECRET_KEY')
            print(f"Loaded Secret Key: {secret_key}")

            if request.headers.get('Secret-Key') != secret_key:
                return 'Unauthorized', 401

            data = coordinates_schema.load(request.json)
            coordinates.update(data)
            coordinates['updated_at'] = datetime.now().isoformat()
            return 'Coordinates updated successfully', 200
        except ValidationError as err:
            return str(err), 400


if __name__ == '__main__':
    app.run(debug=True)
