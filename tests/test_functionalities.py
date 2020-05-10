import requests
import json


def test_functionalities():
    url = "http://localhost:5000/v1/reset"
    requests.get(url)

    url = "http://localhost:5000/v1/resources/tickets"
    headers = {'Content-Type': 'application/json'}

    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 40


    url = "http://localhost:5000/v1/resources/passengers"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 0
    assert resp.status_code == 200

    url = "http://localhost:5000/v1/resources/tickets?status=open"
    resp = requests.get(url)
    assert len(resp.json()) == 40
    assert resp.status_code == 200

    url = "http://localhost:5000/v1/resources/tickets?status=closed"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 0


    url = "http://localhost:5000/v1/resources/tickets?id=12"
    resp = requests.get(url)
    assert resp.status_code == 200
    resp = resp.json()
    assert '12' in resp
    assert resp["12"]["status"] == "open"

    url = "http://localhost:5000/v1/resources/passengers?bus_ticket_id?=15"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 0

    url = "http://localhost:5000/v1/resources/tickets/"
    payload = {"seat_id": 39, "name":"Arjun", "phone": "12354567890", "status":"closed"}
    resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 200
    assert '39' in resp.json()

    url = "http://localhost:5000/v1/resources/tickets/"
    payload = {"seat_id":12, "name":"test", "phone": "12354567899", "status":"closed"}
    resp = requests.put(url, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 200
    assert '12' in resp.json()

    url = "http://localhost:5000/v1/resources/tickets?status=open"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 38

    url = "http://localhost:5000/v1/resources/tickets?status=closed"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    url = "http://localhost:5000/v1/resources/tickets?id=12"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert resp.json()["12"]["status"] == "closed"

    url = "http://localhost:5000/v1/resources/passengers?bus_ticket_id=39"
    resp = requests.get(url)
    assert resp.status_code == 200
    resp = resp.json()
    assert resp["1"]["name"] == "Arjun"
    assert resp["1"]["phone"] == 12354567890


if __name__ == '__main__':
    test_functionalities()
