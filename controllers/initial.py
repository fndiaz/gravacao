# coding=UTF-8
import datetime, os, commands

def principal():
	response.title = 'Backup'

	form = SQLFORM.factory(
    		Field('mes', requires=IS_IN_SET(['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])),
    		Field("ano", requires=IS_IN_SET(session.form_ano)),
    		formstyle="divs",
    		)
	tabela=[]

	if form.process().accepted:
		ano = form.vars.ano
		mes = form.vars.mes
		session.ano = ano
		session.mes = mes
		lista_pastas = commands.getoutput("ls /var/spool/asterisk/monitor | grep %s%s" %(ano, mes))
		print 'lista_pastas :%s:' %(lista_pastas)
		if not lista_pastas:  ##checa se existem gravacoes
			print 'vazio'
			session.flash = 'Busca não encontrada'
			redirect(URL("initial", "/principal"))
		else: ##checa se existem gravacoes
			response.flash = 'Gravações encontradas'	
			f = open('pastas_grav','w')
			f.write(lista_pastas)
			f = open('pastas_grav', 'r')
			pastas = f.readlines()
			print pastas
			session.pastas = pastas

			commands.getoutput("rm -r -f /var/spool/asterisk/monitor/temp_grava")
			commands.getoutput("mkdir /var/spool/asterisk/monitor/temp_grava")
			for pasta in pastas:
				pasta=pasta.split('\n')[0]
				print 'copiando pasta :%s:' %(pasta)
				saida_cp = os.system("cp -r /var/spool/asterisk/monitor/%s /var/spool/asterisk/monitor/temp_grava" %(pasta))
				print 'saida cp:%s' %(saida_cp)

			arq = commands.getoutput("find /var/spool/asterisk/monitor/temp_grava/ -type f | wc -l")
			tabela = [mes, ano, arq]
			print tabela

	return response.render("initial/show_form2.html", form=form, tabela=tabela)


def gera_pdf():
	response.title = 'Backup'
	opc = request.vars['opc']
	data = "'%"+session.ano+'-'+session.mes+"%'"
	print data

	cdr = db.executesql("SELECT calldate, origem, src, dst, duration, disposition, userfield, uniqueid  from cdr WHERE calldate like %s;" %(data))

    # define header and footers:
	head = THEAD(TR(TH("Data",_width="20%"), 
                    TH("O",_width="12%"),
                    TH("Src",_width="14%"),
                    TH("Dst",_width="14%"),
                    TH("D",_width="10%"),
                    TH("S",_width="12%"),
                    TH("U",_width="18%"), 
                    _bgcolor="#A0A0A0"))
	foot = TFOOT(TR(TH("Data",_width="20%"), 
                    TH("O",_width="12%"),
                    TH("Src",_width="14%"),
                    TH("Dst",_width="14%"),
                    TH("D",_width="10%"),
                    TH("S",_width="12%"),
                    TH("U",_width="18%"),
                    _bgcolor="#E0E0E0"))
    
    # create several rows:
	rows = []
	i=0
	for row in cdr:
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		col2="#000000"
		i=i+1
		#print i
		rows.append(TR(TD(row[0]),
                       TD(row[1]),
                       TD(row[2]),
                       TD(row[3]),
                       TD(row[4]),
                       TD(row[5]),
                       TD(row[7]),
                       _bgcolor=col))  

    # make the table object
	body = TBODY(*rows)
	#print body
	table = TABLE(*[head,foot, body], 
                  _border="5", _align="center", _width="100%")

	from gluon.contrib.pyfpdf import FPDF, HTMLMixin

	# define our FPDF class (move to modules if it is reused  frequently)
	class MyFPDF(FPDF, HTMLMixin):
		def header(self):
			self.set_font('Arial','B',15)
			self.cell(0,10, response.title ,1,0,'C')
			self.ln(20)
			
               
		def footer(self):
			self.set_y(-15)
			self.set_font('Arial','I',8)
			txt = 'Pag. %s de %s' % (self.page_no(), self.alias_nb_pages())
			self.cell(0,10,txt,0,0,'C')
                    
	pdf=MyFPDF()
	# first page:
	pdf.add_page()
	pdf.write_html(str(XML(table, sanitize=False)))
	#response.headers['Content-Type']='application/agenda/principal'
	pdf.output(name='applications/gravacao/static/pdf/relatorio.pdf', dest='F')
	print 'relatorio pdf gerado'
	commands.getoutput("cp applications/gravacao/static/pdf/relatorio.pdf /var/spool/asterisk/monitor/temp_grava")
	print session.pastas
	return response.render("initial/show_form.html", opc=opc)


def gera_zip():
	opc = 'dfq'
	commands.getoutput("rm -f applications/gravacao/static/grava_down/grava.zip")
	zip = commands.getoutput("zip -r applications/gravacao/static/grava_down/grava.zip /var/spool/asterisk/monitor/temp_grava")

	pastas = "%s-%s" %(session.mes, session.ano)
	now = str(datetime.datetime.now())
	now=now.split('.')[0]
	teste = db.executesql("INSERT INTO gravacao_lg (datetime, acao, pastas) VALUES('%s', 'gerou backup', '%s');" %(now, pastas ))
	return response.render("initial/show_form.html", opc=opc)

def remover():
	#commands.getoutput("rm -f applications/gravacao/static/grava_down/grava.zip")
	for pasta in session.pastas:
		pasta=pasta.split('\n')[0]
		rm = commands.getoutput("rm -r -f /var/spool/asterisk/monitor/%s" %(pasta))
		f = open('/tmp/debug','w')
                f.write(rm)
		print 'removido :%s:' %(pasta)

	pastas = "%s-%s" %(session.mes, session.ano)
	now = str(datetime.datetime.now())
	now=now.split('.')[0]
	teste = db.executesql("INSERT INTO gravacao_lg (datetime, acao, pastas) VALUES('%s', 'remoção', '%s');" %(now, pastas ))		

	session.flash = 'gravações removidas com sucesso'
	redirect(URL("initial", "/principal"))

def log_eventos():
	log = db.executesql("SELECT * from gravacao_lg order by id desc")

	return response.render("initial/log.html", log=log)

