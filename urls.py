from django.conf.urls.defaults import *
from deploy.webfabric.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #(r'^admin/', include('admin.site.urls')),
    # Example:
    # (r'^deploy/', include('deploy.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^project/save/?$', project_save),
    (r'^project/(?P<project_id>\d+)/stage/?$', project_stage),
    (r'^project/(?P<project_id>\d+)/fabfile/?$', project_fabfile),
    (r'^project/(?P<project_id>\d+)/fabfile/view/?$', project_fabfile_view),
    (r'^project/(?P<project_id>\d+)/fabfile/save/?$', project_fabfile_save),
    (r'^project/(?P<action>\w+)/?(?P<step>\d+)?/?$', project_create_list),
    #(r'^project/create/?(?P<step>\d+)?/?$', project_create),

)

from django.conf import settings
import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
