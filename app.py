import datetime
import random
import os
import uuid
import json
import boto3

from flask import Flask, jsonify, request

# Utils
from utils.geocode import GoogleGeocodeAPI
from utils.boto import create_record, get_item, filter_dynamodb

app = Flask(__name__)

GOOGLE_GEOCODING_API_KEY = os.environ['GOOGLE_GEOCODING_API_KEY']
USERS_TABLE = os.environ['USERS_TABLE']
GEOCODE_TABLE = os.environ['GEOCODE_TABLE']

client = boto3.client('dynamodb')


@app.route("/hi-team", methods=["GET"])
def hello():
    names = [
        "jonathan",
        "andres",
        "cristian",
        "diego",
        "cathe",
        "yuli",
        "mateo",
        "deivys",
    ]
    return f"Hi {random.choice(names).title()}."


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    create_record(table_name=USERS_TABLE, item={
        'userId': {'S': user_id},
        'name': {'S': name},
        'created': {'S': datetime.datetime.utcnow().isoformat()}
    })

    return jsonify({
        'userId': user_id,
        'name': name,
    })


@app.route("/users/<string:user_id>")
def get_user(user_id):
    item = get_item(table_name=USERS_TABLE, key={'userId': {'S': user_id}})
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    data = filter_dynamodb(table_name=GEOCODE_TABLE, index_name="user-id-index", key_name="user_id", key_value=user_id)

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S'),
        'geodata': data.get('Items', [])
    })


@app.route("/geocode/<string:user_id>", methods=["POST"])
def geocode(user_id):
    item = get_item(table_name=USERS_TABLE, key={'userId': {'S': user_id}})
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    address = request.json.get('address', "")
    address = address.replace(" ", "+")

    zoom = request.json.get('zoom', "10.5z")

    geocode_api = GoogleGeocodeAPI()
    gmaps_data = geocode_api.get_reverse_geocode(address=address)

    try:
        latitude = gmaps_data['results'][0]['geometry']['location']['lat']
        longitude = gmaps_data['results'][0]['geometry']['location']['lng']
        maps_link = f"https://www.google.com/maps/@{latitude},{longitude},{zoom}"
    except Exception as e:
        return jsonify({
            'error': "Error occurred getting gmaps data.",
            'additional_info': gmaps_data,
            'address': address,
            'exception_info': str(e),
            'api_key': geocode_api.API_KEY
        })

    data = {
        'maps_link': maps_link,
        'latitude': str(latitude),
        'longitude': str(longitude),
    }

    create_record(
        table_name=GEOCODE_TABLE,
        item={
            'id': {'S': str(uuid.uuid4())},
            'user_id': {'S': user_id},
            'latitude': {'S': str(latitude)},
            'longitude': {'S': str(longitude)},
            'address': {'S': address},
            'maps_link': {'S': maps_link},
            'created': {'S': datetime.datetime.utcnow().isoformat()},
            'metadata': {'S': json.dumps(gmaps_data)},
        }
    )
    return data
