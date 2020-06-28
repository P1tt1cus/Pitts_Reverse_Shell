from datetime import datetime
import os
import json

class ClientMethods:

    def __init__(self):
        pass

    def last_checkin(self, clientid):
        clientfile = os.path.join("clients", clientid)
        with open(clientfile, "r") as cfile:
            data = json.load(cfile)
            data["last_checkin"] = str(datetime.now())
        with open(clientfile, "w") as cfile:
            cfile.write(json.dumps(data))
