def checkout():
	"Compiles, builds and packages our project locally."
	print("iniciando o checkout")
	if os.path.exists('%s' % config.checkout_dir):
	  shutil.rmtree('%s' % config.checkout_dir)
	  print('diretorio %s antigo apagado' % config.checkout_dir)

	local('mkdir -p %s' % config.checkout_dir)
	print('Fazendo checkout do git')
	#GIT
	cmd = """
	git clone $(repository) $(checkout_dir)/$(application) &&
	cd $(checkout_dir)/$(application) &&
	git checkout $(tag)
	"""
	local(cmd)

	print('*' * 60)
	cmd = """
	cd $(checkout_dir) &&
	pwd &&
	rm -rf config Capfile &&
	cd src &&
	cd delivery &&
	rm -rf __init__.py &&
	rm -rf setup.py &&
	cp -rp delivery/* . &&
	rm -rf delivery &&
	cd - &&
	for dir in `ls`; do touch $dir/$(tag).tag; done &&
	tar cvfz $(filename) *
	"""
	local(cmd)