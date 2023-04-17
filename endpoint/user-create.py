def main(context):
	context.respond(
		context.auth.create_account(
			context.get("email"),
			context.get("handle"),
			context.get("password"),
		)
	)
