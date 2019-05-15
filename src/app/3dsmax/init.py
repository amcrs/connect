import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../python'))

from amcrs.server import ConnectServer, ConnectRequestHandler

import MaxPlus

def get_current_filename():
    return MaxPlus.FileManager.GetFileNameAndPath()

def save_file(path):
    MaxPlus.FileManager.Save(path)

def open_file(path):
    MaxPlus.FileManager.Open(path)

class MaxConnectRequestHandler(ConnectRequestHandler):
    def api(self, method, data):
        if method == 'POST':
            if data["command"] == "get_application_info":
                return  self.json({
                    "application": '3dsmax',
                    "startedAt": self.started_at, 
                    "filename": get_current_filename()
                })
            elif data["command"] == 'get_current_filename':
                return self.json({
                    "filename": get_current_filename()
                })
            elif data["command"] == 'save_file':
                save_file(data["path"])
                return self.json('success')
            elif data["command"] == 'open_file':
                open_file(data["path"])
                return self.json('success')

        self.json('unknown_command', 400)


server = None

def init():
    server = ConnectServer(MaxConnectRequestHandler)
    server.start()

if __name__ == '__main__':
    init()