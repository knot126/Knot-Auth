from database import DatabaseFolder
import secrets, hashlib
import time
import random
import enum
import util

def validate_handle(handle):
	if (type(handle) != str):
		return False
	
	for c in handle:
		if (c not in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789_-"):
			return False
	
	if (len(handle) < 3 or len(handle) > 30):
		return False
	
	return True

def validate_email(email):
	# TODO: Improve this
	return ("@" in email and "." in email)

def validate_password(password):
	if (len(password) < 16):
		return False
	
	cset = []
	
	for c in password:
		if (c not in cset):
			cset.append(c)
	
	if (len(cset) < 12):
		return False
	
	return True

def password_hash():
	pass

class Auth():
	"""
	Class which wraps around the authentication database and provides single
	implementations of helpful methods
	"""
	
	def __init__(self):
		"""
		Initialise authdb connections
		"""
		
		# Database for users
		self.user_db = DatabaseFolder("user")
		
		# Database for handle -> id mappings
		self.handle_db = DatabaseFolder("handle")
		
		# Database for active sessions
		self.token_db = DatabaseFolder("token")
	
	def get_id(self, handle):
		"""
		Get the user's ID by their handle.
		"""
		
		user = self.handle_db.read(handle)
		
		return user["user_id"]
	
	def make_id(self, handle):
		"""
		Make a user id given a user's handle
		"""
		
		# Generate a unique UID
		uid = None
		
		while (uid == None):
			uid = secrets.token_urlsafe(64)
			
			# If we land on one that exists, we try again.
			if (self.user_db.has(uid)):
				uid = None
		
		self.handle_db.write(handle, {"user_id": uid})
		
		return uid
	
	def generate_token(self, uid, *, areas = ["webbasic"], expire = 2419200, extra = None):
		"""
		Generate a token for a given uid, aeras and expiry time
		
		Returns a tuple of (token id, special key)
		"""
		
		# Generate a unique TID
		tk = None
		
		while (tk == None):
			tk = secrets.token_urlsafe(128)
			
			# If we land on one that exists, we try again.
			if (self.token_db.has(tk)):
				tk = None
		
		# Time the token was created
		created = int(time.time())
		
		# Calculate real expiry time
		expire += created
		
		# Generate special key
		key = secrets.token_urlsafe(32)
		keyhash = key
		
		# Save the token!
		# TODO Hashing
		self.token_db.write(tk, {
			"uid": uid,
			"created": created,
			"expire": expire,
			"aeras": areas,
			"key": keyhash,
			"extra": extra,
		})
		
		return (tk, key)
	
	def get_valid_token(self, token, key):
		"""
		Check that a token is valid and return the token data if so
		"""
		
		token_id = token
		token = self.token_db.read(token_id)
		
		# If the token doesn't exist, reject it.
		if (not token):
			return None
		
		# If the token's key is wrong, reject it.
		# TODO Hashing
		if (token["key"] != key):
			return None
		
		# If it has expired, reject it and delete it.
		if (util.time() >= token["expire"]):
			self.token_db.delete(token_id)
			return None
		
		# If this token is newer than expected, reject it.
		if (util.time() < token["created"]):
			return None
		
		return token
	
	def invalidate_token(self, token):
		self.token_db.delete(token)
	
	def generate_alt_handles(self, base_handle):
		"""
		Generate alternate handles
		"""
		
		new_handles = []
		
		digits = 3
		iteration = 0
		
		# Try some random handles
		while (True):
			number = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
			
			cand = base_handle + str(number)
			
			if (not self.handle_db.has(cand)):
				new_handles.append(cand)
			
			if (iteration > 50):
				digits += 1
			
			if (len(new_handles) >= 3):
				break
		
		# Return found handles
		return new_handles
	
	def create_account(self, email, handle, password):
		"""
		Create a new user account, generating a password if not provided
		
		Returns dict with {"status": ..., "message": ..., ?"username": ..., ?"password": ...}
		"""
		
		# Check if the user already exists
		if (self.handle_db.has(handle)):
			return {
				"status": "already_exists",
				"message": "A user already exists with this handle.",
				"alternates": self.generate_alt_handles(handle),
			}
		
		# Validate handle
		if (not validate_handle(handle)):
			return {
				"status": "invalid_handle",
				"message": "The handle you have chosen does not match our handle guidelines.",
			}
		
		# Check that the email is valid
		if (not validate_email(email)):
			return {
				"status": "invalid_email",
				"message": "The email you provided is not a valid email.",
			}
		
		# Generate a password if one does not exist
		if (not password):
			password = secrets.token_urlsafe(25)
		
		# Check that we have a good password
		if (not validate_password(password)):
			return {
				"status": "invalid_password",
				"message": "This isn't a very good password. Please try a different one.",
			}
		
		## TODO: Hash and salt passwords!
		
		# Make a user's uid
		uid = self.make_id(handle)
		
		# Save the user's properties
		self.user_db.write(uid, {"handle": handle, "email": email, "password": password})
		
		# Success!
		return {
			"status": "done",
			"message": "The action completed successfully!",
			"handle": handle,
			"email": email,
			"password": password,
		}
	
	def check_password(self, uid, password):
		"""
		Check that a password matches the user's password.
		"""
		
		# TODO Password hashing! Password hasing!
		
		user = self.user_db.read(uid)
		
		return (user["password"] == password)
	
	def login(self, handle, password, areas, expire = 2419200):
		"""
		Log in to this user's account. Returns the standard response format.
		"""
		
		# Validate that handle exists
		if (not self.handle_db.has(handle)):
			return {
				"status": "failed",
				"message": "Something went wrong! Your username or password might be incorrect.",
			}
		
		uid = self.get_id(handle)
		
		# Check password
		if (not self.check_password(uid, password)):
			return {
				"status": "failed",
				"message": "Something went wrong! Your username or password might be incorrect.",
			}
		
		# Check that expiry isn't too long away
		if (expire > 2419200):
			return {
				"status": "too_much_time",
				"message": "The lifetime of this token is too long.",
			}
		
		token, key = self.generate_token(uid, areas = areas, expire = expire)
		
		return {
			"status": "done",
			"message": "You have been logged in!",
			"tf_required": False,
			"tf_id": None,
			"token": token,
			"key": key,
		}
	
	def logout(self, token, key):
		"""
		Log the user out of their account
		"""
		
		token_id = token
		token = self.get_valid_token(token, key)
		
		if (not token):
			return {
				"status": "bad_token",
				"message": "Your session token is not valid.",
			}
		
		self.invalidate_token(token_id)
		
		return {
			"status": "done",
			"message": "You have been logged out successfully.",
		}
