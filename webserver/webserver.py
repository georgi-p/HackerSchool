import socket
import os
import sys
import time
import cgi
import subprocess


class WebServer:
	print "Created server"
	HOST, PORT = '', 8080
	MAX_PACKET = 1024
	print "Packet size: "+str(MAX_PACKET)
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

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(1)

	def recv_all(self, sock):
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
		        rdata.append(sock.recv(self.MAX_PACKET))
		    except socket.timeout:
		        return ''.join(rdata)

		# unreachable
	    finally:
		sock.settimeout(prev_timeout)

	def recv_basic(self, socket):
		request = []
		body = []
		lastfour = ''

		while True:
			data = socket.recv(self.MAX_PACKET)
			if lastfour.endswith('\r\n\r') and data.startswith('\n'):
				request.append('\n')
				body.append(data[1:])
				break
			elif lastfour.endswith('\r\n') and data.startswith('\r\n'):
				request.append('\r\n')
				body.append(data[2:])
				break
			elif lastfour.endswith('\r') and data.startswith('\n\r\n'):
				request.append('\n\r\n')
				body.append(data[3:])
				break
			elif data.count('\r\n\r\n') >= 1:
				datasplit = data.split('\r\n\r\n')
				request.append(datasplit[0]+'\r\n\r\n')
				body.append('\r\n\r\n'.join(datasplit[1:]))
				break
			lastfour = data[-4:]
			request.append(data)

		request = ''.join(request)[:-4]
		request_headers = request.splitlines()[1:]
		content_length = 0

		for header in request_headers:
			if header.split(': ', 1)[0] == 'Content-Length':
				content_length = int(header.split(': ', 1)[1])
				break


		datacount = len(''.join(body))

		while datacount < content_length:
			data = socket.recv(self.MAX_PACKET)
			body.append(data)
			datacount += len(data)

		body = ''.join(body)

		print "Length of body: %s" % (len(body))

		return request, body

	def normalizeLineEndings(self, s):
		r'''Convert string containing various line endings like \n, \r or \r\n,
		to uniform \n.'''

		return ''.join((line + '\n') for line in s.splitlines())

	def sendResponseHead(self, client_socket, proto, status, status_text, headers):
		response = '%s %s %s' % (proto, status, status_text)
		if headers != '':
			response += '\n'
			response += headers
		response += '\n\n'
		client_socket.send(response)

	def sendNotFound(self, socket):
		response_proto = 'HTTP/1.0'
		response_status = '404'
		response_status_text = 'Not Found'
		self.sendResponseHead(socket, response_proto, response_status, response_status_text, '')
		socket.close()

	def doGET(self, client_socket, request_uri):

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
		print "-"
		print "File name: "+filename
		extension = os.path.splitext(filename)[1][1:]
		print "Extension: "+extension
		print "Args: %s" % args

		try:
			content_type = self.CONTENT_TYPES[extension]
			openedfile = open(filename, 'rb')	
		except:
			self.sendNotFound(client_socket)
			return		

		response_headers = 'Content-Type: %s' % content_type
		print response_headers


		# Reply as HTTP/1.0 server, saying "HTTP OK" (code 200).
		response_proto = 'HTTP/1.0'
		response_status = '200'
		response_status_text = 'OK'


		self.sendResponseHead(client_socket, response_proto, response_status, response_status_text, response_headers)

		readfile = openedfile.read(self.MAX_PACKET)

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
			readfile = openedfile.read(self.MAX_PACKET)

		openedfile.close()
		client_socket.close()

	def doPOST(self, client_socket, headers, body):

		content_type, pdict = cgi.parse_header(headers['Content-Type'])
		'''
		if content_type == 'multipart/form-data':
			postvars = cgi.parse_multipart(body, pdict)
		elif content_type == 'application/x-www-form-urlencoded':
			postvars = cgi.parse_qs(body, keep_blank_values=1)
		else:
			postvars = {}

		print "Args: "+str(postvars)
		'''

		response_headers = 'Content-Type: %s' % content_type
		print response_headers
		print pdict

		# Reply as HTTP/1.0 server, saying "HTTP OK" (code 200).
		response_proto = 'HTTP/1.0'
		response_status = '200'
		response_status_text = 'OK'

		self.sendResponseHead(client_socket, response_proto, response_status, response_status_text, response_headers)

		print "Response sent"

#		client_socket.sendall(body)

		print len(body)

		openedfile = open(os.getcwd()+'/files/test', 'wb')
		writefile = openedfile.write('\n'.join(body.split(pdict['boundary'])[1].split('\n')[4:]))

#		first = '\n'.join(body.split('\n')[:5])
#		last = '\n'.join(body.split('\n')[-6:])
#		print "First:\n"+first
#		print "Last:\n"+last

		openedfile.close()

		client_socket.close()

	def handleRequest(self, client_socket):
		'''
		i = 0
		total_data = []
		while i<1000:
			try:
				request = client_socket.recv(8192)
				total_data.append(request)
			except:
				break
			i += 1
		if i == 1000:
			print "NE STAA BRAT"
			return
		print ''.join(total_data)
		return


		request = self.recv_all(client_socket)
		print request
		self.doGET(client_socket, "/upload.html")
		return
		'''

		# Headers and body are divided with \n\n (or \r\n\r\n - that's why we
		# normalize endings).
		request_head, request_body = self.recv_basic(client_socket)
	#	request = normalizeLineEndings(recv_basic(client_socket))
	#	request = normalizeLineEndings(client_socket.recv(1024))
		print "-"
		print "-"
		print "-"
		print "Request:\n"+request_head
		print "-"
		#print "Body:\n"+request_body

		# First line is request headline, and others are headers
		request_head = request_head.splitlines()
		request_headline = request_head[0]

		print "-"
		print "Headers:"
		i = 0
		for x in request_head[1:]:
			print ("Header %s: " % i)+x
			i +=1

		# Headers have their name up to first ': '
		request_headers = dict(x.split(': ', 1) for x in request_head[1:])

		# Headline has form of "POST /some/requests HTTP/1.0"
		request_method, request_uri, request_proto = request_headline.split(' ', 3)

		if request_method == "GET":
			self.doGET(client_socket, request_uri)
		elif request_method == "POST":
			self.doPOST(client_socket, request_headers, request_body)
		else:
			client_socket.close()

	def serveForever(self):
		print 'Serving HTTP on port %s ...' % self.PORT
		while True:
			# Accept connection
			client_socket,  client_address = self.server_socket.accept()
			self.handleRequest(client_socket)	


if __name__ == '__main__':
	server = WebServer()
	server.serveForever()
	print "Done"
