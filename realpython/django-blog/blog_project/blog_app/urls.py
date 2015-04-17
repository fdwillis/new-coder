from django.conf.urls import patterns, url
from blog_app import views

urlpatterns = patterns(
	'blog_app.views',
	url(r'^$', views.index, name = 'index'),
	url(r'^add_post/', views.add_post, name = "add_post"),
	url(r"^(?P<post_url>\w+)/$", views.post, name='post'),
)