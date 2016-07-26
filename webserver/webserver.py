import socket
import os
import sys
import time
import cgi
import subprocess

HOST, PORT = '', 8080
MAX_PACKET = 1024
CONTENT_TYPES = {
		'html': 'text/html; encoding=utf8',
		'php': 'text/html; encoding=utf8',
		'css': 'text/css',
		'js': 'application/javascript',
		'jpg': 'image/jpg',
		'gif': 'image/gif',
		'mp4': 'video/mp4',
		'mkv': 'video/webm'
	}

def recv_all(sock):
    r'''Receive everything from `sock`, until timeout occurs, meaning sender
    is exhausted, return result as string.'''

    # dirty hack to simplify this stuff - you should really use zero timeout,
    # deal with async socket and implement finite automata to handle incoming data

    prev_timeout = sock.gettimeout()
    try:
        sock.settimeout(0.01)

        rdata = []
        while True:
            try:
                rdata.append(sock.recv(MAX_PACKET))
            except socket.timeout:
                return ''.join(rdata)

        # unreachable
    finally:
        sock.settimeout(prev_timeout)

def recv_basic(socket):
	total_data = []
	lastfour = ''

	while True:
		data = socket.recv(MAX_PACKET)
		if lastfour.endswith('\r\n\r') and data.startswith('\n'):
			total_data.append('\n')
			break
		elif lastfour.endswith('\r\n') and data.startswith('\r\n'):
			total_data.append('\r\n')
			break
		elif lastfour.endswith('\r') and data.startswith('\n\r\n'):
			total_data.append('\n\r\n')
			break
		elif data.count('\r\n\r\n') >= 1:
			total_data.append(data.split('\r\n\r\n')[0]+'\r\n\r\n')
			break
		lastfour = data[-4:]
		total_data.append(data)

	return ''.join(total_data)

def normalizeLineEndings(s):
	r'''Convert string containing various line endings like \n, \r or \r\n,
	to uniform \n.'''

	return ''.join((line + '\n') for line in s.splitlines())

def sendResponseHead(socket, proto, status, status_text, headers):
	response = '%s %s %s' % (proto, status, status_text)
	if headers != '':
		response += '\n'
		response += headers
	response += '\n\n'
	client_socket.send(response)

def sendNotFound(socket):
        response_proto = 'HTTP/1.0'
        response_status = '404'
        response_status_text = 'Not Found'
	sendResponseHead(socket, response_proto, response_status, response_status_text, '')
	socket.close()

def doGET(client_socket, request_uri):


	# Parse out the arguments.
	# The arguments follow a '?' in the URL. Here is an example:
	# http://example.com?arg1=val1
	args = {}
	idx = request_uri.find('?')
	if idx >= 0:
		request_path = request_uri[:idx]
		args = cgi.parse_qs(request_uri[idx+1:])
	else:
		request_path = request_uri

	filename = request_path[1:]
	print 'File name: '+filename
	extension = os.path.splitext(filename)[1][1:]
	print 'Extension: '+extension
	print "Args: %s" % args

	try:
		content_type = CONTENT_TYPES[extension]
		openedfile = open(filename, 'rb')	
	except:
		sendNotFound(client_socket)
		return		

	response_headers = 'Content-Type: %s' % content_type
	print response_headers


        # Reply as HTTP/1.0 server, saying "HTTP OK" (code 200).
        response_proto = 'HTTP/1.0'
        response_status = '200'
        response_status_text = 'OK'


	sendResponseHead(socket, response_proto, response_status, response_status_text, response_headers)

	readfile = openedfile.read(MAX_PACKET)

	while readfile:
		if filename == 'add.html' and args != {} and readfile.count('<div>') > 0:
			data = readfile.split('<div>')
			result = subprocess.check_output(['python', 'add.py', args['num1'][0], args['num2'][0]])
			print "Result: %s" % result
			client_socket.send(data[0]+'<div>')
			client_socket.send(result)
			client_socket.send(''.join(data[1:]))
		elif filename == 'add.html' and args != {} and readfile.count('</div>') > 0:
			data = readfile.split('</div>')
			result = subprocess.check_output(['python', 'add.py', args['num1'][0], args['num2'][0]])
			print "Result: %s" % result
			client_socket.send(data[0])
			client_socket.send(result)
			client_socket.send('</div>'+''.join(data[1:]))
		else:
			
		#try:
			client_socket.send(readfile)
		#except Exception as e:
		#	print e
		#	break
		readfile = openedfile.read(MAX_PACKET)

	openedfile.close()
	client_socket.close()
	time.sleep(10)

def handleRequest(client_socket):
	


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
	# Accept connection
	client_socket,  client_address = serversocket.accept()

	# Headers and body are divided with \n\n (or \r\n\r\n - that's why we
	# normalize endings).
	request = recv_basic(client_socket)
#	request = normalizeLineEndings(recv_basic(client_socket))
#	request = normalizeLineEndings(client_socket.recv(1024))
	print "-"
	print "-"
	print "-"
	print 'Request: '+request
	request_head, request_body = request.split('\r\n\r\n', 1)

	# First line is request headline, and others are headers
	request_head = request_head.splitlines()
	request_headline = request_head[0]
	# Headers have their name up to first ': '
        request_headers = dict(x.split(': ', 1) for x in request_head[1:])

	# Headline has form of "POST /some/requests HTTP/1.0"
	request_method, request_uri, request_proto = request_headline.split(' ', 3)

	if request_method == 'GET':
		doGET(client_socket, request_uri)
	else:
		client_socket.close()
		continue
