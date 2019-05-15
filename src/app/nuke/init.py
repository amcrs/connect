import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../python'))

from amcrs.server import ConnectServer, ConnectRequestHandler

import nuke
from nukescripts.utils import executeInMainThread

def get_current_filename():
    return nuke.Root()["name"].value()

def save_file(path):
    nuke.scriptSaveAs(path,overwrite=1)

def open_file(path):
    nuke.scriptClose()
    nuke.scriptOpen(path)

class NukeConnectRequestHandler(ConnectRequestHandler):
    def execute(self, func, args = None):
        executeInMainThread(func, (args,))

    def api(self, method, data):
        if method == 'POST':
            if data["command"] == "get_application_info":
                return  self.json({
                    "application": 'nuke',
                    "startedAt": self.started_at, 
                    "filename": get_current_filename()
                })
            elif data["command"] == 'get_current_filename':
                return self.json({ "filename": get_current_filename() })
            elif data["command"] == 'save_file':
                self.execute(save_file, data["path"])
                return self.json('success')
            elif data["command"] == 'open_file':
                self.execute(open_file, data["path"])
                return self.json('success')

        self.json('unknown_command', 400)

server = None

def init():
    server = ConnectServer(NukeConnectRequestHandler)
    server.start()

if __name__ == '__main__':
    init()