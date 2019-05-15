import urllib3
import json
from config import CONFIG

http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1.0, read=2.0))

def get(url):
    r = http.request('GET', url, headers = { "Authorization" : CONFIG["authToken"] })
    return json.loads(r.data)

def post(url, body):
    r = http.request('POST', url, headers = { "Authorization" : CONFIG["authToken"] }, body = json.dumps(body))
    return json.loads(r.data)