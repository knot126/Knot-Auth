def main(context):
	context.respond(
		context.auth.validate_token(
			context.get("token"),
			context.get("key"),
		)
	)
