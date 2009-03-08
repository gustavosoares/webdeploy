def restart():
	"Restart do webserver"
	print('Dando graceful no apache')
	run("sudo /usr/local/httpd-2.2/bin/apachectl graceful")
	print('graceful feito')