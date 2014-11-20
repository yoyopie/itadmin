from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'itadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'disk.views.index', name='index'),
    url(r'^add/$', 'disk.views.adddata', name='adddata'),
    url(r'^show/$', 'disk.views.show', name='show'),
    url(r'^register/$', 'disk.views.register', name='register'),
    url(r'^check/$', 'disk.views.check', name='check'),
    url(r'^login/$', 'disk.views.login', name='login'),
    url(r'^logout/$', 'disk.views.logout', name='logout'),
    url(r'^reit/$', 'disk.views.registeritadmin', name='registeritadmin'),
)
