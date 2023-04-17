def main(context):
	context.respond(
		context.auth.login(
			context.get("handle"),
			context.get("password"),
			context.get("areas"),
		)
	)
