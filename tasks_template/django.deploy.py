def deploy():
	"Deploy do projeto para os ambientes"
	print('JAVA_HOME: %s'% os.environ['JAVA_HOME'])
	print('checkout_dir: %s' % config.checkout_dir)
	print('')
	print("tag: %s" % config.tag)
	print("clone_name: %s"  % config.clone_name)
	print("repository: %s" % config.repository)
	print('*' * 60)
	invoke(checkout)
	print('*' * 60)
	print("deploy_to: %s" % config.deploy_to)
	print('current_path: %s' % config.current_path)
	print('release_path: %s' % config.release_path)
	print('shared_path: %s' % config.shared_path)
	print('*' * 60)
	put('%s' % config.filename, '%s' % config.filename)
	print('tar.gz enviado')
	print('apagando o temporario %s' % config.filename)
	local('rm -rf %s' % config.filename)
	print('done')
	cmd = """
	mkdir -p $(release_path) &&
	cd $(release_path) &&
	tar xvzf $(filename) &&
	for dir in `ls`; do rm -rf $(deploy_to)/$dir > /dev/null; done &&
	cd $(deploy_to) && 
	tar xvzf $(filename) && 
	rm $(filename) && 
	cd $(release_path) && 
	cp -rp * $(current_path)/ && 
	rm -rf $(filename) &&
	cd $(deploy_to)/ &&
	rm -rf pubclient > /dev/null &&
	ln -s delivery/pubclient
	"""
	run(cmd)
	invoke(restart)