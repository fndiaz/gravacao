@auth.requires_membership("admin")
def users():
	grid = SQLFORM.grid(db.auth_user)
	return response.render("initial/show_grid.html", grid=grid)

@auth.requires_membership("admin")
def groups():
    grid = SQLFORM.grid(db.auth_group)
    return response.render("initial/show_grid.html", grid=grid)

@auth.requires_membership("admin")
def membership():
    grid = SQLFORM.grid(db.auth_membership)
    return response.render("initial/show_grid.html", grid=grid)
