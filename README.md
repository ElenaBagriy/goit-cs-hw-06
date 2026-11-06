# goit-cs-hw-06
# Web Application with Socket Server and MongoDB

## Project Description

This project implements a simple web application using Python's built-in HTTP server, a TCP Socket server, and MongoDB.

The application allows users to submit messages through a web form. Messages are transferred from the HTTP server to the Socket server using TCP and then stored in MongoDB together with the date and time when they are received.

The application is containerized using Docker and Docker Compose.

## Architecture

The application consists of three main components:

- **HTTP Server** — handles HTTP requests on port `3000`, serves HTML pages and static files, and processes form submissions.
- **Socket Server** — listens on port `5000` and receives messages from the HTTP server via TCP.
- **MongoDB** — stores submitted messages in the `web_app` database, in the `user_messages` collection.

The HTTP and Socket servers run in separate processes within the Python application container.

## Message Format

Each submitted message is stored as a separate MongoDB document:

```json
{
  "date": "2026-11-06 11:52:14.288513",
  "username": "Someone",
  "message": "Something"
}
```

The `date` field contains the date and time when the Socket server receives the message.

## Project Structure

```text
web_app/
├── main.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .dockerignore
├── README.md
├── templates/
│   ├── index.html
│   ├── message.html
│   └── error.html
└── static/
    ├── style.css
    └── logo.png
```

## Requirements

- Docker
- Docker Compose

## How to Run

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd goit-cs-hw-06
```

3. Build and start the application:

```bash
docker compose up --build
```

Docker Compose starts the Python application and MongoDB containers.

4. Open the application in your browser:

- Main page: http://localhost:3000
- Message form: http://localhost:3000/message.html

5. Submit a message using the form.

## How to Check Stored Messages

Open a new terminal and run:

```bash
docker compose exec mongo mongosh
```

Then execute:

```javascript
use web_app
db.user_messages.find().pretty()
```

All submitted messages will be displayed.

## How to Stop the Application

Press `Ctrl+C` in the terminal running Docker Compose, then execute:

```bash
docker compose down
```

MongoDB data is stored in a named Docker volume and is preserved when containers are stopped and removed.

## Technologies Used

- Python
- HTTP Server (`http.server`)
- TCP Sockets (`socket`)
- Multiprocessing
- MongoDB
- PyMongo
- Docker
- Docker Compose