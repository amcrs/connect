from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import socket
import datetime
import traceback
import os

from config import CONFIG

class ConnectServer(object):
    def __init__(self, handler_class):
        self.handler_class = handler_class

    def start(self):
        port = self.findport()
        self.daemon = threading.Thread(None, lambda: self.run(port))
        self.daemon.setDaemon(True)
        self.daemon.start()
        print 'amcrs: running connect on port %s' % port

    def run(self, port):
        server_address = ('', port)
        httpd = HTTPServer(server_address, self.handler_class)
        httpd.serve_forever()

    def findport(self):
        port = CONFIG["portRangeStart"]
        search = True
        while(search):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            if result != 0:
                search = False
            else:
                port += 1
        return port


class ConnectRequestHandler(BaseHTTPRequestHandler):
    started_at = datetime.datetime.now().isoformat()

    def do_HEAD(self):
        if self.is_authenticated():
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers',
                        'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, Authorization')
        self.end_headers()

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')
    
    def do_PATCH(self):
        self.handle_request('PATCH')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method):
        if self.is_authenticated():
            try:
                body = None
                if 'Content-Length' in self.headers:
                    content_length = int(self.headers['Content-Length'])
                    raw = self.rfile.read(content_length)
                    body = json.loads(raw)
                self.api(method, body)
            except:
                traceback.print_exc()
                self.json('internal_server_error', 500)
                
    def json(self, data, statusCode = 200):
        if isinstance(data, str):
            data = { "code": data }
        
        data["error"] = False if statusCode < 400 else True
        
        self.send_response(statusCode)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data))

    def api(self, method, data):
        self.json("unknown_command", 400)

    def is_authenticated(self):
        if self.headers.get('Authorization') == CONFIG["authToken"]:
            return True
        else:
            self.json('unauthorized', 401)
            return False
