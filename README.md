# Ticket-Booking-App

Welcome to version 1 of Ticket Booking API. 

This app has been built using python 3.8 and Flask. 
It can serve as a backend API for a bus company/wherever you want it to.
Below are the list of available methods and examples to use the API. If you need help or support, please contact tarjureddy25@gmail.com

No registration is required to use this API.

## Setup:
To run this app locally you need to clone this repository and run this command in the project folder to install required packages.
```
pip install -r requirements.txt
```
• The default port on which the app runs is 5000 on localhost



## Terminology
• open ticket: Ticket hasn't been booked by anyone yet

• closed ticket: Ticket has been booked by someone already



## Available Functionalities

• View all tickets

• View all open tickets

• View all closed tickets

• View individual Ticket Status

• View details of all passengers with a booking

• View details of person owning a ticket.

• Update the ticket status (open/close ticket)

• Reset the server (opens up all the tickets)



## Syntax and Examples



• View all tickets

```
GET api/v1/resources/tickets     Shows all the open and closed tickets
```
> Example

```
http://127.0.0.1:5000/v1/resources/tickets
```
> Returns
```
"id": {
    "passenger_id": null or int, 
    "status": "open" or "closed"
  }
```
---

• View all open tickets

```
GET api/v1/resources/tickets?status=open           Shows all open tickets
```
> Example
```
http://127.0.0.1:5000/v1/resources/tickets?status=open
```
> Returns
```
{
  "id": {
    "passenger_id": null,
    "status": "open"
  }
}
```

---


• View all closed tickets

```
GET api/v1/resources/tickets?status=closed         Shows all closed tickets
```

> Example
```
http://127.0.0.1:5000/v1/resources/tickets?status=closed
```
> Returns
```
{
  "id": {
    "passenger_id": int,
    "status": "closed"
  }
}
```

---

• View individual Ticket Status


```
GET api/v1/resources/tickets/?id=ticket_id(int)        Shows the ticket status
```
> Example
```
http://127.0.0.1:5000/v1/resources/tickets/?id=1
```
> Returns
```
{
  "id": {
    "passenger_id": int,
    "status": "open" or "closed"
  }
}
```

---

• View details of all passengers with a booking


```
GET api/v1/resources/passengers/      Shows all the passengers with a booking
```
> Example
```
http://127.0.0.1:5000/v1/resources/passengers/
```
> Returns
```
{
  "1": {
    "name": "passenger's name", 
    "phone": "passenger's phone"
  }
}
```

---

• View details of person owning a ticket.

```
GET api/v1/resources/passengers?bus_ticket_id=int     Shows the details of a single passenger
```

> Example
```
http://127.0.0.1:5000/v1/resources/passengers?bus_ticket_id=1
```
> Returns
```
{
  "passenger_id": {
    "name": "passenger's name", 
    "phone": "passenger's phone"
  }
}
```
---

• Update the ticket status (close ticket)

```
PUT api/v1/resources/tickets     Insert data of a passenger and mark as closed by sending status as closed
```
> Example
```
http://127.0.0.1:5000/v1/resources/tickets
```

Data
```
{
	"seat_id": 1,                 (Ticket id)
	"name": "passenger's name",
	"status": "closed",
	"phone": "1234567890"
}
```

> Returns
```
{
  "passenger_id": {
    "name": "passenger's name", 
    "phone": "passenger's phone"
  }
}
```

---

• Update the ticket status (open ticket)


```
PUT api/v1/resources/tickets     Mark as open by passing status as open
```
> Example
```
http://127.0.0.1:5000/v1/resources/tickets
```
Data
```
{
	"seat_id": 1,                 (Ticket id)
	"status": "open"
}
```

> Returns
```
{
  "seat_id": {
    "passenger_id": int,
    "status": "closed"
  }
}
```

---


• Reset the server (opens up all the tickets)


```
GET api/v1/reset      Reset's the passenger list and open up all tickets and sets passenger id to null
```
> Example
```
http://127.0.0.1:5000/v1/reset
```
> Returns
```
{
  "seat_id": {
    "passenger_id": null,
    "status": "open"
  }
}
```
