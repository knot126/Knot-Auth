def main(context):
	context.respond(
		context.auth.logout(
			context.get("token"),
			context.get("key"),
		)
	)
