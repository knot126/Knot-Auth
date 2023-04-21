#!/usr/bin/env python
"""
yu.be server
"""

import os, os.path, sys, util
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from context import Context, ContextFinished
import traceback
import ssl
import config

def call_endpoint(self, type):
	"""
	Handle an endpoint by preparing the context and calling its function
	"""
	
	path, params = util.parse_path(self.path)
	after_path = "/".join(path[1:]) if (len(path) > 1) else ""
	filename_path = after_path.replace("/", "-").replace("\\", "-")
	
	context = Context(self, type, path[1:], params)
	
	# Try is so we can catch the exception thrown when things like repsond are
	# called.
	try:
		# Access the given api endpoint
		if (path[0] == "api" and len(path) >= 2):
			modname = "endpoint/" + filename_path + ".py"
			
			if (not os.path.exists(modname)):
				modname = "endpoint/__default__.py"
			
			f = util.loadModule(modname).main
			
			try:
				f(context)
			except Exception as e:
				trace = traceback.format_exc()
				response = {
					"status": "failed",
					"message": "The action can't be completed at the moment. Please try again later. If this keeps happening, please let the server owner know.",
				}
				
				print(trace)
				context.respond(response)
		
		# Access a static resouce
		elif (path[0] == "res"):
			context.respondWithFile(path[1])
		
		# Load the web app
		else:
			context.respondWithFile("index.html")
	except ContextFinished as e:
		pass

class YuHandler(BaseHTTPRequestHandler):
	"""
	YuBe request handler
	"""
	
	def do_GET(self):
		"""
		Handle a GET request
		"""
		
		call_endpoint(self, "GET")
	
	def do_HEAD(self):
		"""
		Handle a HEAD request
		"""
		
		call_endpoint(self, "HEAD")
	
	def do_POST(self):
		"""
		Handle a POST request
		"""
		
		call_endpoint(self, "POST")

def main():
	print("Basic test server")
	
	server = ThreadingHTTPServer(('0.0.0.0', 8000), YuHandler)
	
	if (config.get("https")):
		server.socket = ssl.wrap_socket(server.socket, keyfile = config.get("cert_key"), certfile = config.get("cert_path"), server_side = True)
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		return 0
	
	return 1

if (__name__ == "__main__"):
	sys.exit(main())
