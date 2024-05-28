from django.shortcuts import render
from Blog.models import Post, Comment
from django.http import HttpResponseRedirect
from Blog.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

def Blog_index(request):
    posts = Post.objects.all().order_by("-created_on").prefetch_related('categories')

    context = {
        'posts': posts,
    }
    return render(request, 'Blog/index.html', context)


def Blog_category(request , category):
    posts = Post.objects.filter(
        categories__name__contains = category
    ).order_by("-created_on")

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'Blog/category.html', context)

def Blog_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
        'form': CommentForm(),
    }
    return render(request, 'Blog/details.html', context)


def search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) | Q(body__icontains=query)
    )
    context = {
        'results':results
    }
    return render(request, 'components/search_components/search_results.html', context)
