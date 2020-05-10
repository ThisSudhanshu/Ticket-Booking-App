import requests
import json

def test_exceptions():

    url = "http://localhost:5000/v1/resources/tickets/123"
    headers = {'Content-Type': 'application/json'}

    resp = requests.get(url)
    assert resp.status_code == 404

    url = "http://localhost:5000/v1/resources/passengers/asd"
    resp = requests.get(url)
    assert resp.status_code == 404


    url = "http://localhost:5000/v1/resources/tickets?status=something"
    resp = requests.get(url)
    assert resp.status_code == 400


    url = "http://localhost:5000/v1/resources/tickets?id=50"
    resp = requests.get(url)
    assert resp.status_code == 400


    url = "http://localhost:5000/v1/resources/passengers?bus_ticket_id=500"
    resp = requests.get(url)
    assert resp.status_code == 400


    url = "http://localhost:5000/v1/resources/tickets/"
    payload = {"seat_id": 20, "name": "test", "phone": "12354567899", "status": "open"}
    resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 400

    url = "http://localhost:5000/v1/reset"
    requests.get(url)

if __name__ == '__main__':
    test_exceptions()
