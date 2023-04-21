def main(context):
	context.respond({
		"status": "done",
		"message": "The app's information was retrived successfully.",
		"title": "Placeholder",
		"areas": ["userinfo"],
		"auth_mode": "get_with_qs",
		"auth_url": "https://example.com/my_auth_url?grant={grant_id}&key={grant_key}",
	})
