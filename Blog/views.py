from django.shortcuts import render
from Blog.models import Post, Comment

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

def Blog_details(request, pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comment': comment,
    }
    return render(request, 'Blog/details.html', context)
