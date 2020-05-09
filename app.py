#!flask/bin/python
from collections import defaultdict
from flask import Flask, jsonify, make_response, request
global c
c = 56
app = Flask(__name__)

seats = {1: {'status': 'open', 'passenger_id' : None}, 2: {'status':'open', 'passenger_id' : None}, 3: {'status':'closed', 'passenger_id' : 40}, 4: {'status':'closed', 'passenger_id' : 55}}
passengers = {35: {'name': 'arjun', 'phone': 123}, 23: {'name':'chakra', 'phone': 134}, 40:{'name': 'shudh', 'phone':124},
              55: {'name':'test', 'phone': 1234}}

def add_passenger(name, phone):
    global c
    passengers[c] = {'name': name, 'phone': phone}
    c += 1
    return c - 1

@app.route('/')
def index():
    return "Visit https://github.com/aReDDD/Ticket-Booking-App to learn more about this API!"

@app.route('/v1/')
@app.route('/v1/resources')
def not_found():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/v1/resources/tickets/', methods=['GET', 'PUT'])
def tickets():
    if request.method == 'GET':
        query_parameters = request.args
        get_id = query_parameters.get('id')
        get_status = query_parameters.get('status')
        tickets = {}
        if get_id:
            if get_id.isdigit() and int(get_id) in seats:
                return jsonify(seats[int(get_id)])
            else:
                return make_response(jsonify({'error': 'Bad request'}), 400)
        else:
            if get_status in ['open', 'closed']:
                for x in seats:
                    if get_status == seats[x]['status']:
                        tickets[x] = seats[x]
                return jsonify(tickets)
            elif get_status:
                return make_response(jsonify({'error': 'Bad request'}), 400)
            else:
                return jsonify(seats)
    else:
        get_seat_id = request.json['seat_id'] if 'seat_id' in request.json else ''
        get_status = request.json['status'] if 'status' in request.json else ''
        get_passenger_name = request.json['name'] if 'name' in request.json else ''
        get_passenger_phone = request.json['phone'] if 'phone' in request.json else ''
        if get_status == 'closed':
            if get_seat_id.isdigit() and int(get_seat_id) in seats and seats[int(get_seat_id)]['status'] == 'open' and get_passenger_phone and get_passenger_name:
                passenger_id = add_passenger(get_passenger_name, get_passenger_phone)
                seats[int(get_seat_id)]['passenger_id'] = passenger_id
                seats[int(get_seat_id)]['status'] = get_status
                return jsonify(seats[(int(get_seat_id))])
            else:
                return make_response(jsonify({'error': 'Bad request/seat already closed'}), 400)
        elif get_status == 'open':
            if get_seat_id.isdigit() and int(get_seat_id) in seats and seats[int(get_seat_id)]['status'] == 'closed':
                seats[int(get_seat_id)]['passenger_id'] = None
                seats[int(get_seat_id)]['status'] = get_status
                return jsonify(seats[(int(get_seat_id))])
            else:
                return make_response(jsonify({'error': 'Bad request/seat already open'}), 400)
        else:
            return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/v1/resources/passengers/', methods=['GET'])
def get_passenger_details():
    query_parameters = request.args
    id = query_parameters.get('bus_ticket_id')
    if id and id.isdigit() and int(id) in seats and seats[int(id)]['passenger_id']:
        passenger_id = seats[int(id)]['passenger_id']
        return jsonify(passengers[passenger_id])
    elif not id:
        return jsonify(passengers)
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)





if __name__ == '__main__':
    app.run(debug=True)