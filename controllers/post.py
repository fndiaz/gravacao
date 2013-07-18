def show():
	return "post"

def edit():
	return "edit post"

def delete():
	return "delete"

@auth.requires_login()
def add():
#	logger.debug("execute funcao add")
#	logger.info(str(request.vars))
	logger.info(auth.user)	
	logger.info(auth.user_id)
#	try:
#		1/0
#	except ZeroDivisionError as erro:
#		logger.error(str(erro))
	
	return SQLFORM(Post).process()

