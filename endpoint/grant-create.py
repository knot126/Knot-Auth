def main(context):
	context.respond({
		"status": "done",
		"message": "The app has been granted the user's authorisation.",
		"grant_id": "TestGrantID",
		"grant_key": "TestGrantKey",
	})
