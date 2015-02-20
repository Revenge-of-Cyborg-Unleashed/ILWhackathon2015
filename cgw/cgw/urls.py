from django.conf.urls import patterns, include, url
from django.contrib import admin
from travel.views import search, polltable, pollview, submit

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cgw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', search),
    url(r'^poll/$', polltable),
    url(r'^group/([^/]+)/$', pollview),
    url(r'^submitform/$', submit),
    url(r'', search)
)
