from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Blog.models import Post, Comment, Category
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
    category_obj = get_object_or_404(Category, name=category)

    if request.method == 'POST' and request.user.is_authenticated:
        if 'follow' in request.POST:
            request.user.followed_categories.add(category_obj)
            messages.success(request, f"You are now following {category_obj.name}.")
            
        elif 'unfollow' in request.POST:
            request.user.followed_categories.remove(category_obj)
            messages.success(request, f"You have unfollowed {category_obj.name}.")


    context = {
        'category': category_obj,
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

    comments = Comment.objects.filter(approved=True)

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

    # Filter comments based on approved status and user's superuser status
    if request.user.is_superuser:
        comments = Comment.objects.filter(post=post)
    else:
        comments = Comment.objects.filter(post=post, approved=True)


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


def comment_create(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # Spam Check Algorithm will be used here
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                comment.parent = parent_obj
            comment.save()
            return redirect('Blog_details', slug=post.slug)  # adjust this as needed
    else:
        form = CommentForm()
    return redirect('Blog_details', slug=post.slug)  # adjust this as needed

def comment_thread(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    return redirect('Blog_details', slug=post.slug)  # adjust this as needed


@login_required
def comment_approve(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user.is_superuser:
        comment.approved = True
        comment.save()
        return redirect('Blog_details', slug=comment.post.slug)
    else:
        messages.error(request, 'You do not have permission to approve comments.')
        return redirect('Blog_details', slug=comment.post.slug)
    
@login_required
def reply_approve(request, id):
    reply = get_object_or_404(Comment, id=id)
    if request.user.is_superuser or request.user.is_staff:
        reply.approved = True
        reply.save()
        return redirect('Blog_details', slug=reply.post.slug)
    else:
        messages.error(request, 'You do not have permission to approve replies.')
        return redirect('Blog_details', slug=reply.post.slug)