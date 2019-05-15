from config import CONFIG
import request

class ConnectClientManager(object):
    def __init__(self):
        self.applications = []

    def reload(self):
        self.applications = []
        for port in range(CONFIG["portRangeStart"],CONFIG["portRangeEnd"]):
            try:
                url = 'http://localhost:{0}'.format(port)
                data = request.post(url, { "command": "get_application_info" })
                self.applications.append(ConnectClient(url, data["application"], data["startedAt"]))
            except:
                pass


class ConnectClient(object):
    def __init__(self, url, application, started_at):
        self.url = url
        self.application = application
        self.started_at = started_at

    def get_current_filename(self):
        return request.post(self.url, { "command": "get_current_filename" })["filename"]

    def open_file(self, filename):
        request.post(self.url, { "command": "open_file", "path": filename })

    def save_file(self, filename):
        request.post(self.url, { "command": "save_file", "path": filename })
    

if __name__ == '__main__':
    manager = ConnectClientManager()
    manager.reload()
    apps = manager.applications
    print apps[0].get_current_filename()