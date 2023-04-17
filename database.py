import util
import os
import os.path
import shutil

def loadDatabaseConfig():
	"""
	Load the database configuration
	"""
	
	config = util.loadJson("config.json")
	
	return config

class Database:
	"""
	A utility class to control the main database
	"""
	
	def __init__(self):
		"""
		Load information about the database
		"""
		
		# Load the database config
		config = loadDatabaseConfig()
		
		# Set the database folder path
		self.path = config.get("database", "database")
		
		# Create the folder if not already done
		util.create_folder(self.path, sanitise = False) # Path does not need to be sanitised
	
	def create(self, folder, schema = None):
		"""
		Create a database with an optional shcema
		"""
		
		raise NotImplemented
	
	def open(self, table):
		"""
		Open a given table
		"""
		
		return Table(table)
	
	def backup(self, postfix):
		"""
		Backup the database to a ZIP file with a specific prefix
		"""
		
		shutil.make_archive(self.path + "/../database_backup_" + util.sanitisePath(postfix), "zip", self.path)

class DatabaseFolder:
	"""
	A "connection" to the database for a specific "table"/folder
	
	The "database types" comment indicates which types of databases the
	operations can be used on.
	
	 - Object: Object databases store JSON files and should only read or write
	           full JSON files at once.
	
	 - Storage: Storage databases store raw data, like video util.
	"""
	
	def __init__(self, folder):
		"""
		Load information about the database
		"""
		
		# Load global database config
		config = loadDatabaseConfig()
		
		# Load folder for database - does not include slash at end
		self.path = config.get("database", "database") + "/" + folder
		
		# Create the table if it doesn't exist
		util.create_folder(self.path, sanitise = False) # Path does not need to be sanitised
	
	def get_path(self, node):
		"""
		Get the path to the node
		
		Database types: Object, Storage
		"""
		
		return (self.path + "/" + util.sanitisePath(node))
	
	def read(self, node):
		"""
		Read an object from the database
		
		Database types: Object
		"""
		
		return util.loadJson(self.get_path(node), sanitise = False) # Path was already sanitised
	
	def write(self, node, content):
		"""
		Write an object to the database
		
		Database types: Object
		"""
		
		util.saveJson(self.get_path(node), content, sanitise = False) # Path was already sanitised
	
	def has(self, node):
		"""
		Check if a node exists
		
		Database types: Object, Storage
		"""
		
		return os.path.exists(self.get_path(node))
	
	def enumerate(self):
		"""
		Enumerate all id's in the database
		
		Note: This is a really bad idea for big ones
		
		Database types: Object
		"""
		
		return []
	
	def where(self, constraints):
		"""
		Preform a really basic GET * WHERE {"k1": "v1", ...} on the database
		
		Note: This is a really bad idea for flat file databases
		
		Database types: Object
		"""
		
		return []
	
	def delete(self, node):
		"""
		Delete an object from the database
		
		Database types: Object, Storage
		"""
		
		util.delete(self.get_path(node), sanitise = False) # Path was already sanitised
	
	def get_size(self, node):
		"""
		Get the size of a node file in bytes
		
		Database types: Storage
		"""
		
		return util.file_length(self.get_path(node), sanitise = False) # Path was already sanitised
	
	def read_bytes(self, node, start = 0, end = None):
		"""
		Read an object as bytes
		
		Database types: Storage
		"""
		
		return util.file_read_part(self.get_path(node), start, end, sanitise = False) # Path was already sanitised
	
	def append_bytes(self, node, content):
		"""
		Append bytes to an object
		
		Database types: Storage
		"""
		
		return util.file_append(self.get_path(node), content, sanitise = False) # Path was already sanitised

Table = DatabaseFolder
