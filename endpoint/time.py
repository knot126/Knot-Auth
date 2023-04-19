import util

def main(context):
	context.respond({
		"status": "done",
		"message": "Current server time was gotten successfully.",
		"time": util.time(),
		"year_approx": 1970 + util.time() // (60 * 60 * 24 * 365.25),
	})
