from django.shortcuts import render
from Blog.models import Post, Comment
from django.http import HttpResponseRedirect
from Blog.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages

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
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    author=request.user,
                    body=form.cleaned_data["body"],
                    post=post,
                )
                comment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            messages.add_message(request, messages.ERROR, 'You must be logged in to comment.')

    comments = Comment.objects.filter(post=post)

    post_tags = post.tags.values_list('id', flat=True)
    post_categories = post.categories.values_list('id', flat=True)
    
    # Get the slug of the previous post from the session
    previous_slug = request.session.get('previous_slug')

    related_posts = Post.objects.filter(
        Q(categories__in=post_categories) |
        Q(tags__in=post_tags) |
        Q(title__icontains=post.title)
    ).exclude(id=post.id)

    # Exclude the previous post if it exists
    if previous_slug:
        related_posts = related_posts.exclude(slug=previous_slug)

    related_posts = related_posts.distinct()[:2]

    # Store the current post's slug in the session
    request.session['previous_slug'] = slug


    context = {
        'post': post,
        'comments': comments,
        'form': CommentForm(),
        'related_posts': related_posts,
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
