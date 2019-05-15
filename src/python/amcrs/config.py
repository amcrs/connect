import os
import json

CONFIG = None
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../config.json')) as json_file:  
    CONFIG = json.load(json_file)