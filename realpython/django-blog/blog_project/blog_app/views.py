from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from blog_app.models import Post
from django.shortcuts import get_object_or_404, render_to_response, redirect
from blog_app.forms import PostForm

# Create your views here.

def encode_url(url):
	return url.replace(" ", "_")

def template(page):
	return loader.get_template("blog/" + page)

def index(request):
	latest_posts = Post.objects.all().order_by('-created_at')
	popular_posts = Post.objects.order_by('-views')[:5]
	t = template("index.html")
	context_dict = {
		'latest_posts': latest_posts,
		'popular_posts': popular_posts,
  }
	for post in latest_posts:
		post.url = encode_url(post.title)
	for post in popular_posts:
		post.url = encode_url(post.title)
	c = Context(context_dict)
	return HttpResponse(t.render(c))

def post(request, post_url):
	single_post = get_object_or_404(Post, 
		title = post_url.replace("_", " "))
	single_post.views += 1
	single_post.save()
	t = template("post.html")
	c = Context({'single_post': single_post, })
	return HttpResponse(t.render(c))


def add_post(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit = True)
			return HttpResponse(post(request, Post.objects.order_by('-created_at')[0].title))
		else:
			print form.errors
	else:
		form = PostForm()
	return render_to_response('blog/add_post.html', {'form': form},
		context)