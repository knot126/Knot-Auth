import json
import database
import auth
import traceback
import util

class ContextFinished(BaseException):
	def __init__(self):
		pass

class SanitiseType:
	Disabled = 0
	AllHTML = 1
	DangerousHTML = 2

class ValidateType:
	Disabled = 0
	Handle = 1
	Email = 2

class Context:
	def __init__(self, request, method, path, params):
		"""
		Initialise the context for the request
		"""
		
		self.request = request
		self.host = request.headers["Host"]
		self.method = method
		self.path = path
		self.params = params
		self.code = 200
		self.db = database.Database()
		self.auth = auth.Auth()
		self.data = {}
		
		if (method == "POST"):
			try:
				self.data = json.loads(request.rfile.read(int(request.headers['Content-Length'])))
			except:
				print(traceback.format_exc())
	
	def get(self, key, default = NotImplemented, *, length = 10000, sanitise = SanitiseType.Disabled, validate = ValidateType.Disabled):
		"""
		Get a value from a POST/GET request
		
		If default value is NotImplemented, then an error response is sent
		"""
		
		value_get = self.params.get(key, NotImplemented) if self.params else NotImplemented
		value_post = self.data.get(key, NotImplemented)
		
		value = NotImplemented
		
		# Use the POST value first, then the GET value, lastly the default
		if (value_post != NotImplemented):
			value = value_post
		elif (value_get != NotImplemented):
			value = value_post
		else:
			value = default
		
		# If we are still NotImplemented then we error response
		if (value == NotImplemented):
			self.respond({"status": "missing_data", "message": f"An error occured with the API: Parameter '{key}' is missing. Please contact the developer about this error."})
		
		return value
	
	def set_status_code(self, code):
		"""
		Set status code for the response
		"""
		
		self.code = code
	
	def respond(self, data, contenttype = "application/json"):
		"""
		Respond with data. If data is an object it's converted to json, and if it
		is bytes then it is kept as bytes.
		"""
		
		message = (json.dumps(data) if type(data) == dict else data)
		
		self.request.send_response(200, "OK")
		self.request.send_header("Content-Length", str(len(message)))
		self.request.send_header("Content-Type", contenttype)
		self.request.send_header("X-Yube-API", "1")
		self.request.end_headers()
		self.request.wfile.write(message.encode("utf-8") if (type(message) == str) else message)
		
		raise ContextFinished()
	
	def respondWithFile(self, path):
		"""
		Respond with the contents of a file
		"""
		
		data = None
		
		try:
			data = util.load_binary("res/" + path.replace("/", "").replace("\\", ""))
		except FileNotFoundError:
			self.respond("404 Not Found", "text/plain")
		
		contenttype = ""
		
		if (path.find(".json") >= 0): contenttype = "application/json"
		if (path.find(".html") >= 0): contenttype = "text/html"
		if (path.find(".css") >= 0): contenttype = "text/css"
		if (path.find(".js") >= 0): contenttype = "text/javascript"
		if (path.find(".txt") >= 0): contenttype = "text/plain"
		if (path.find(".xml") >= 0): contenttype = "application/xml"
		if (path.find(".zip") >= 0): contenttype = "application/zip"
		if (path.find(".svg") >= 0): contenttype = "image/svg+xml"
		if (path.find(".png") >= 0): contenttype = "image/png"
		if (path.find(".webp") >= 0): contenttype = "image/webp"
		if (path.find(".jpg") >= 0): contenttype = "image/jpeg"
		if (path.find(".jpeg") >= 0): contenttype = "image/jpeg"
		
		self.respond(data, contenttype)
	
	def redirect(self, url):
		"""
		Send a redirect
		"""
		
		self.request.send_response(301, "Moved permanently")
		self.request.send_header("Location", url)
		self.request.send_header("Content-Length", "0")
		self.request.end_headers()
		self.request.wfile.write(message.encode("utf-8"))
		
		raise ContextFinished()
