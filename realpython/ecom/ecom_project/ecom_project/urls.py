from django.conf.urls import patterns, include, url

# Enabled the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecom_project.views.home', name='home'),
    # url(r'^ecom_project/', include('ecom_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index', name = 'home') ,
    url(r'^contact/', 'contact.views.contact', name = 'contact') ,
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)
