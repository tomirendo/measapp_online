from base64 import b32encode
from urllib import request
from json import loads
class PrologixConnection:
    def __init__(self, GPIB_port, prologix_server_host = "http://localhost:1337"):
        self.port = GPIB_port
        self.host = prologix_server_host

    def open(self, *args):
    	pass

    def close(self):
    	pass

    def __enter__(self):
    	return self

    def __exit__(self, *args):
    	pass


    def write(self, command):
        if isinstance(command, str):
            command = command.encode()
        encoded_command = b32encode(command).decode()
        url = "{}/write/{}/{}/".format(self.host, self.port, encoded_command)
        response = loads(request.urlopen(url).read().decode())
        if response['error']:
            raise Exception(response['error_description'])

    def query(self, command):
        if isinstance(command, str):
            command = command.encode()
        encoded_command = b32encode(command).decode()
        url = "{}/query/{}/{}/".format(self.host, self.port, encoded_command)
        response = loads(request.urlopen(url).read().decode())
        if response['error']:
            raise Exception(response['error_description'])
        else :
            return response['result']['data']
    def read(self):
        url = "{}/read/{}/".format(self.host, self.port)
        response = loads(request.urlopen(url).read().decode())
        if response['error']:
            raise Exception(response['error_description'])
        else :
        	return response['result']['data']

