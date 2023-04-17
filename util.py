import importlib
import importlib.util
import sys
import random
import json
import time
import os
import pathlib

def sanitisePath(unsafe_path):
	"""
	Sanitise a file path by removing any harmful or erronious chars
	"""
	
	ALLOWED_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_."
	new_path = ""
	
	for c in unsafe_path:
		if (c in ALLOWED_CHARS):
			new_path += c
	
	return new_path

def loadModule(path):
	"""
	Load the given python module
	"""
	
	name = f"MODULE{random.randint(1, 10000000)}"
	
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[name] = module
	spec.loader.exec_module(module)
	
	return module

def loadJson(path, *, sanitise = True):
	"""
	Load a json file, returning the contents or none if it does not exist
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	content = ""
	
	try:
		with open(path, "r") as f:
			content = json.load(f)
	except FileNotFoundError:
		return None
	
	return content

def saveJson(path, content, *, sanitise = True):
	"""
	Save a json file
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	with open(path, "w") as f:
		json.dump(content, f)

def loadFile(path, decode = True, *, sanitise = True):
	"""
	Load file contents, optionally decoding it
	"""
	
	path = sanitisePath(path) if sanitise else path
	f = open(path, "rb")
	c = f.read()
	c = c.decode('utf-8') if decode else c
	f.close()
	return c

def file_length(path, *, sanitise = True):
	"""
	Get the size of the file at path
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	# get file size
	return os.path.getsize(path)

def file_read_part(path, start, end, *, sanitise = True):
	"""
	Read part of a file's contents. Only intended for binary files
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	# Get end if None
	if (end == None):
		end = file_length(path, sanitise = False) # Already sanitised if that is wanted
	
	# Find length to read
	length = end - start
	
	# Read content
	f = open(path, "rb")
	f.seek(start)
	c = f.read(length)
	f.close()
	
	return c

def file_append(path, content, encode = False, *, sanitise = True):
	"""
	Append more content to the end of a file, optionally encoding it
	"""
	
	path = sanitisePath(path) if sanitise else path
	f = open(path, "a") if encode else open(path, "ab")
	c = content.encode('utf-8') if encode else c
	f.write(c)
	f.close()

def create_folder(path, *, sanitise = True):
	"""
	Create a folder, including any folders needed to create that folder
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	os.makedirs(path, exist_ok = True)

def delete(path, *, sanitise = True):
	"""
	Delete a file
	"""
	
	path = sanitisePath(path) if sanitise else path
	
	os.remove(path)


def parse_path(path):
	"""
	Parse the URL path into (real_path, params)
	"""
	
	# Parse file paths and parameters
	# For example: /get-video-file/part?video=8frTtoQ46HXDJNEe&player=short
	# Result: path = ["get-video-file", "part"], params = {"video": "8frTtoQ46HXDJNEe", "player": "short"}
	
	# Remove leading '/'
	path = path[1:]
	
	# Split into path/params
	left_and_right = path.split("?")
	
	# Check if URI has any parameters
	has_params = (len(left_and_right) >= 2)
	
	# Init path/params final variables
	path = left_and_right[0]
	params = None
	
	# Parse parameters
	if (has_params):
		tmpparams = {}
		params = left_and_right[1].split("&")
		
		# Parse params
		for p in params:
			key, value = p.split("=")
			tmpparams[key] = value.replace("/", "&#47;") # NOTE: '/' could be problematic and should not be used so we filter it here
		
		params = tmpparams
		del tmpparams
	
	path = path.split("/")
	
	#print("server.parsePath", path, params)
	
	return (path, params)

def time():
	return int(time.time())

def load_binary(path):
	return pathlib.Path(path).read_bytes()
