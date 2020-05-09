#!flask/bin/python
from collections import defaultdict
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
seats = {1: {'status': 'open', 'passenger_id' : 23}, 2: {'status':'open', 'passenger_id' : 35}, 3: {'status':'closed', 'passenger_id' : 40}, 4: {'status':'closed', 'passenger_id' : 55}}
passengers = {35: {'name': 'arjun', 'phone': 123}, 23: {'name':'chakra', 'phone': 134}, 40:{'name': 'shudh', 'phone':124},
              55: {'name':'test', 'phone': 1234}}

@app.route('/')
def index():
    return "Visit https://github.com/aReDDD/Ticket-Booking-App to learn more about this API!"

@app.route('/v1/')
@app.route('/v1/resources')
def not_found():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/v1/resources/tickets/', methods=['GET'])
def get_tickets():
    query_parameters = request.args
    get_status = query_parameters.get('status')
    tickets = {}
    if get_status in ['open', 'closed']:
        for x in seats:
            if get_status == seats[x]['status']:
                tickets[x] = seats[x]
    elif get_status:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        return jsonify(seats)
    return jsonify(tickets)


@app.route('/v1/resources/passengers/', methods=['GET'])
def get_passenger_details():
    query_parameters = request.args
    id = query_parameters.get('bus_ticket_id')
    if id and id.isdigit() and int(id) in seats:
        passenger_id = seats[int(id)]['passenger_id']
        return jsonify(passengers[passenger_id])
    elif not id:
        return jsonify(passengers)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)




if __name__ == '__main__':
    app.run(debug=True)

