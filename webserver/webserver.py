import socket
from os import curdir, sep
import sys

HOST, PORT = '', 8080

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
	client, address = serversocket.accept()
	request = client.recv(1024)
	print request


	response = """\
HTTP/1.1 200 OK
Content-Type: text/html

"""
	client.send(response)

	openedfile = open("index.html")
	readfile = openedfile.read()

	while readfile:
		client.send(readfile)
		readfile = openedfile.read(1024)

	openedfile.close()
	client.close()
