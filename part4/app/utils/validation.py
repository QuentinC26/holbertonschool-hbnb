from flask import jsonify

def validate_price(price):
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"error": "Invalid price"}), 400

def validate_latitude(lat):
    if not isinstance(lat, (int, float)) or not -90 <= lat <= 90:
        return jsonify({"error": "Invalid latitude"}), 400

def validate_longitude(lng):
    if not isinstance(lng, (int, float)) or not -180 <= lng <= 180:
        return jsonify({"error": "Invalid longitude"}), 400
