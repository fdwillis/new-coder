from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from blog_app.models import Post
from django.shortcuts import get_object_or_404, render_to_response, redirect
from blog_app.forms import PostForm

# helpers

def encode_url(url):
	return url.replace(" ", "_")

def template(page):
	return loader.get_template("blog/" + page)

def popular_posts():
	popular_posts = Post.objects.order_by('-views')[:5]
	return popular_posts


# views

def index(request):
	latest_posts = Post.objects.all().order_by('-created_at')
	t = template("index.html")
	context_dict = {
		'latest_posts': latest_posts,
		'popular_posts': popular_posts(),
  }
	c = Context(context_dict)
	return HttpResponse(t.render(c))

def post(request, slug):
	single_post = get_object_or_404(Post, slug=slug)
	single_post.views += 1
	single_post.save()
	t = template("post.html")
	context_dict = {
		'single_post': single_post,
		'popular_posts': popular_posts(),
	}
	c = Context({'single_post': single_post, })
	return HttpResponse(t.render(c))


def add_post(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit = True)
			return HttpResponse(post(request, Post.objects.order_by('-created_at')[0].slug))
		else:
			print form.errors
	else:
		form = PostForm()
	return render_to_response('blog/add_post.html', {'form': form},
		context)