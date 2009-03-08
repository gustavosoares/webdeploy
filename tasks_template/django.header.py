import os
import shutil
import datetime

#CONFIGS
config.fab_user = 'portal'
config.application = "publicacao-delivery"
config.tag = ''
config.clone_name = ''

if len(config.tag) == 0:
  config.tag = 'master'

if len(config.clone_name) == 0:
  config.clone_name = 'mainline'

config.checkout_dir =  "/tmp/%s_checkedout/%s" % (config.application, config.tag)
config.repository = "git://git.globoi.com/%s/%s.git" % (config.application, config.clone_name)

#config.deploy_to = "/usr/local/glbdjango"
config.deploy_to = "/tmp"
config.appdjango = 'delivery'
config.time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
config.current_path = '%s/%s' % (config.deploy_to, config.appdjango)
config.release_path = '%s/releases/%s/%s' % (config.deploy_to, config.appdjango, config.time)
config.shared_path = '%s/shared/%s' % (config.deploy_to, config.appdjango)
config.filename = '/tmp/%s.tar.gz' % config.time