#!flask/bin/python
from collections import defaultdict
from flask import Flask, jsonify, make_response, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


def create_database():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        conn.execute('''CREATE TABLE IF NOT EXISTS Passenger
                             (ID INTEGER PRIMARY KEY NOT NULL ,
                             NAME          TEXT    NOT NULL,
                             PHONE         INT NOT NULL
                             );''')
        conn.execute('''CREATE TABLE IF NOT EXISTS Seat
                     (ID INT PRIMARY KEY     NOT NULL,
                     STATUS          TEXT    NOT NULL,
                     PASSENGER_ID    INT,
                     FOREIGN KEY (PASSENGER_ID)
       REFERENCES Passenger (id)
                     );''')
        conn.execute('''CREATE TABLE IF NOT EXISTS Counter
                             (ID INT PRIMARY KEY     NOT NULL,
                             c INT NOT NULL
                             );''')
        for x in range(1, 41):
            l = [x, 'open', None]
            conn.execute("INSERT or IGNORE INTO Seat values(?, ?, ?);", l)
        conn.execute("INSERT or IGNORE INTO Counter values(1,1);")
        conn.commit()
    except Error as e:
        return (jsonify({'error': e}))
    finally:
        if conn:
            conn.close()


def add_passenger(name, phone):
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        cur = conn.execute('''Select  c from Counter where id = 1''')
        mx = next(cur)[0]
        conn.execute('''INSERT or IGNORE INTO Passenger(id, name, phone) values(?, ?, ?);''', [mx, name, phone])
        cur = conn.execute('''Update Counter set c = ? where id = 1''', [mx + 1])
        conn.commit()
        return mx
    except Error as e:
        return make_response({'error': repr(e)}, 500)
    finally:
        if conn:
            conn.close()


@app.route('/')
def index():
    return "Visit https://github.com/aReDDD/Ticket-Booking-App to learn more about this API!"


@app.route('/v1/resources/tickets/', methods=['GET'])
def tickets_get():
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        query_parameters = request.args
        get_id = query_parameters.get('id')
        get_status = query_parameters.get('status')
        if get_id:
            if str(get_id).isdigit() and int(get_id) >= 1 and int(get_id) <= 40:
                cursor = conn.execute("Select * from seat where id = ?", [get_id])
                d = {}
                for row in cursor:
                    d[row[0]] = {'status': row[1], 'passenger_id': row[2]}
                return jsonify(d)
            else:
                return make_response(jsonify({'error': 'Bad request'}), 400)
        else:
            if get_status in ['open', 'closed']:
                cursor = conn.execute("Select * from seat where status = ?", [get_status])
                d = {}
                for row in cursor:
                    d[row[0]] = {'status': row[1], 'passenger_id': row[2]}
                return jsonify(d)
            elif get_status:
                return make_response(jsonify({'error': 'Bad request'}), 400)
            else:
                cursor = conn.execute("Select * from seat;")
                d = {}
                for row in cursor:
                    d[row[0]] = {'status': row[1], 'passenger_id': row[2]}
                return jsonify(d)
    except Error as e:
        return make_response({'error': repr(e)}, 400)
    finally:
        if conn:
            conn.close()


@app.route('/v1/resources/tickets/', methods=['PUT'])
def tickets_put():
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        get_seat_id = request.json['seat_id'] if 'seat_id' in request.json else ''
        get_status = request.json['status'] if 'status' in request.json else ''
        get_passenger_name = request.json['name'] if 'name' in request.json else ''
        get_passenger_phone = request.json['phone'] if 'phone' in request.json else ''
        if get_status == 'closed':
            if str(get_seat_id).isdigit() and int(get_seat_id) >= 1 and int(
                    get_seat_id) <= 40 and get_passenger_phone and get_passenger_name:
                cursor = conn.execute("Select status from seat where id = ?", [get_seat_id])
                if next(cursor)[0] == "open":
                    passenger_id = add_passenger(get_passenger_name, get_passenger_phone)
                    cursor = conn.execute("Update seat set passenger_id = ?, status = ? where id = ?",
                                          [passenger_id, get_status, get_seat_id])
                    conn.commit()
                    d = {}
                    cursor = conn.execute("Select * from seat where id = ?", [get_seat_id])
                    row = next(cursor)
                    d[row[0]] = {'status': row[1], 'passenger_id': row[2]}
                    return jsonify(d)
                else:
                    return make_response(jsonify({'error': 'Bad request/seat already closed'}), 400)
            else:
                return make_response(jsonify({'error': 'Bad request'}), 400)
        elif get_status == 'open':
            if get_seat_id.isdigit() and int(get_seat_id) >= 1 and int(get_seat_id) <= 40:
                cursor = conn.execute("Select status from seat where id = ?", [get_seat_id])
                if next(cursor)[0] == "closed":
                    cursor = conn.execute("Update seat set passenger_id = ?, status = ? where id = ?",
                                          [None, get_status, get_seat_id])
                    conn.commit()
                    d = {}
                    cursor = conn.execute("Select id, passenger_id, status from seat where id = ?", [get_seat_id])
                    row = next(cursor)
                    d[row[0]] = {'status': row[1], 'passenger_id': row[2]}
                    return jsonify(d)
                else:
                    return make_response(jsonify({'error': 'Bad request/seat already open'}), 400)
            else:
                return make_response(jsonify({'error': 'Bad request'}), 400)
        else:
            return make_response(jsonify({'error': 'Bad request'}), 400)
    except Error as e:
        return make_response({'error': repr(e)}, 400)
    finally:
        if conn:
            conn.close()


@app.route('/v1/resources/passengers/', methods=['GET'])
def get_passenger_details():
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        query_parameters = request.args
        id = query_parameters.get('bus_ticket_id')
        if id and id.isdigit() and int(id) >= 1 and int(id) <= 40:
            cursor = conn.execute("Select * from Passenger where id = (Select passenger_id from Seat where id = ?);",
                                  [id])
            d = {}
            for row in cursor:
                d[row[0]] = {'name': row[1], 'phone': row[2]}
            return jsonify(d)
        elif not id:
            cursor = conn.execute("Select * from Passenger where id in (Select passenger_id from Seat);")
            d = {}
            for row in cursor:
                d[row[0]] = {'name': row[1], 'phone': row[2]}
            return jsonify(d)
        else:
            return make_response(jsonify({'error': 'Not found'}), 404)
    except Error as e:
        return make_response({'error': repr(e)}, 500)
    finally:
        if conn:
            conn.close()


@app.route('/v1/reset/', methods=['GET'])
def reset():
    conn = None
    try:
        conn = sqlite3.connect("ticketing_db")
        cur = conn.execute("DELETE from Passenger")
        cur = conn.execute("Update Seat set status = ?, passenger_id = ?", ["open", None])
        conn.commit()
        return make_response(jsonify({'Success': 'Reset Complete'}), 200)
    except Error as e:
        return make_response({'error': repr(e)}, 500)
    finally:
        if conn:
            conn.close()


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
    create_database()
    app.run(debug=True)