#!flask/bin/python
from flask import Flask, jsonify, make_response, request
from services import bus_service

app = Flask(__name__)


@app.route('/')
def index():
    return "Visit https://github.com/aReDDD/Ticket-Booking-App to learn more about this API!"


@app.route('/v1/resources/tickets/', methods=['GET'])
def get_tickets():
    query_parameters = request.args
    return bus_service.get_tickets(query_parameters)


@app.route('/v1/resources/tickets/', methods=['PUT'])
def put_tickets():
    return bus_service.put_tickets(request.json)


@app.route('/v1/resources/passengers/', methods=['GET'])
def get_passenger_details():
    return bus_service.get_passenger_details(request.args)


@app.route('/v1/reset/', methods=['GET'])
def reset():
    return bus_service.reset()


@app.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed_error(error):
    return make_response(jsonify({'error': 'Not Allowed'}), 405)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)


if __name__ == '__main__':
    bus_service.create_database()
    app.run(debug=True)
