from dao import bus_dao


def create_database():
    return bus_dao.create_database()


def get_tickets(query_parameters):
    return bus_dao.get_tickets(query_parameters)


def put_tickets(request_json):
    get_seat_id = request_json['seat_id'] if 'seat_id' in request_json else ''
    get_status = request_json['status'] if 'status' in request_json else ''
    get_passenger_name = request_json['name'] if 'name' in request_json else ''
    get_passenger_phone = request_json['phone'] if 'phone' in request_json else ''
    if get_status == 'closed':
        return bus_dao.close_ticket(get_seat_id, get_passenger_name, get_passenger_phone, get_status)
    elif get_status == 'open':
        return bus_dao.open_ticket(get_seat_id)
    else:
        return make_response(jsonify({'error': 'Bad request'}), 400)


def get_passenger_details(query_parameters):
    return bus_dao.get_passenger_details(query_parameters)


def reset():
    return bus_dao.reset()
