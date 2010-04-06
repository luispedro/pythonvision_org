import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import gitcms.simplecms.urls
import gitcms.blog.urls
import gitcms.files.urls
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include(gitcms.blog.urls)),
)
urlpatterns += gitcms.files.urls.urlpatterns
urlpatterns += gitcms.simplecms.urls.urlpatterns
