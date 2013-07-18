##Agenda
#db.agenda.empresa.requires = IS_NOT_EMPTY(error_message=
#						T("valor não pode ser nulo"))

#db.agenda.telefone.requires = [IS_NOT_EMPTY(error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_NOT_IN_DB(db, 'agenda.telefone', error_message=T("este número está em uso")),
#IS_LENGTH(minsize=9, maxsize=11, error_message=T("o telefone deve conter de 9 a 11 números")),
#IS_MATCH('[0-9]+', error_message=T("somente números"))]


