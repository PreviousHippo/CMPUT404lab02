#!/usr/bin/env python
#cd Desktop/404/lab2
#curl 127.0.0.1:8000

import socket
import os


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.bind(("0.0.0.0", 8000))
#for address used student:
#clientSocket.setsocketopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
clientSocket.listen(5)

while True:

	(incomingSocket, address) = clientSocket.accept()
	print "we got a connection from %s!" % (str(address))

	pid = os.fork()
	#we must be the child(clone)process, so we will handle proxying for this client
	if (pid == 0):
		

		googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		googleSocket.connect(("www.google.com", 80))

		incomingSocket.setblocking(0)
		googleSocket.setblocking(0)

		while True:
			skip = False
			#this half of the loop forwars from client to google
			try:
			    part = incomingSocket.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
				    skip = True
				else:
					raise
			if not skip:
				if(len(part)>0):
					print " > " + part
					googleSocket.sendall(part)
				else: #part will be "" when the connection is done	
					exit(0)
		

			skip = False
			try:
			    part = googleSocket.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
					skip = True
				else:
					raise
		   
			#this half of the loop forwards from google to the client
			if not skip:
				if(len(part)>0):
					print " < " + part
					incomingSocket.sendall(part)
				else: #part will be "" when the connection is done	
					exit(0)
