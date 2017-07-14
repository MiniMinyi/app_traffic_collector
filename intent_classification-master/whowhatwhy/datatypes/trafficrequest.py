import json

class trafficrequest:
    def __init__(self):
        self.app = ""
        self.version = ""
        self.host = ""
        self.path = ""
        self.data = {}

    def load_data(self, data_json):
        obj = json.loads(data_json)
        self.app = obj["app"]
        self.version = obj["version"]
        self.host = obj["host"]