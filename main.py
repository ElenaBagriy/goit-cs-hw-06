from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
import json
import multiprocessing
from pymongo import MongoClient
from datetime import datetime, timezone


TCP_IP = "0.0.0.0"
TCP_PORT = 5000
HTTP_PORT = 3000
TCP_HOST = "localhost"


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/":
            self.send_html('templates/index.html')
        elif url.path == "/message.html":
            self.send_html('templates/message.html')
        else:
            filename = f"static{url.path}"
            if pathlib.Path(filename).exists():
                self.send_html(filename)
            else:
                self.send_html('templates/error.html', 404)


    def send_html(self, filename, status=200):
        self.send_response(status)
        mt = mimetypes.guess_type(filename)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'{filename}', 'rb') as file:
            response = file.read()
            self.wfile.write(response)


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(body.decode())
        data_dict = {key: value[0] for key, value in data.items()}
        message = json.dumps(data_dict).encode()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((TCP_HOST, TCP_PORT))
            sock.sendall(message)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run_server(port, server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', port)
    server = server_class(server_address, handler_class)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


def run_socket(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    client = MongoClient("mongodb://mongo:27017/")
    db = client["web_app"]
    collection = db["user_messages"]
    while True:
        with server_socket.accept()[0] as new_sock:
            received = new_sock.recv(1024)
            data = received.decode()
            data_dict = json.loads(data)
            data_dict["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            collection.insert_one(data_dict)


if __name__ == '__main__':
    http_process = multiprocessing.Process(target=run_server, args=(HTTP_PORT,))
    socket_process = multiprocessing.Process(target=run_socket, args=(TCP_IP, TCP_PORT))

    http_process.start()
    socket_process.start()

    http_process.join()
    socket_process.join()