import util

gConfig = {
	"database": "./database",
	"https": False,
}

def load():
	"""
	Load config
	"""
	
	global gConfig
	
	gConfig = util.loadJson("config.json")

def get(key):
	"""
	Get an option from the config
	"""
	
	global gConfig
	
	return gConfig.get(key, None)

load()
