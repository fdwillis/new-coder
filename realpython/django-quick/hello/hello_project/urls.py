from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
	'',
  # Examples:
  # url(r'^$', 'hello.views.home', name='home'),
  # url(r'^blog/', include('blog.urls')),

  url(r'^admin/', include(admin.site.urls)),
  url(r'^', include("hellow_app.urls")),
)