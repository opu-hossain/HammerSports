from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from Blog.models import Post, Comment, Category
from django.http import HttpResponseRedirect, Http404
from Blog.forms import CommentForm, BlogPostForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.views.generic import TemplateView


def is_admin(user):
    """
    Check if the user is an admin.

    Args:
        user (User): The user object.

    Returns:
        bool: True if the user is an admin, False otherwise.

    Raises:
        TypeError: If the user argument is None.
    """
    if user is None:
        raise TypeError("User object is None")
    return user.is_superuser

# Robots.txt
class RobotstxtView(TemplateView):
    """
    View for the Robots.txt file.

    This view serves the content of the Robots.txt file which is used by web
    crawlers to determine which pages they are allowed to crawl.
    """
    template_name = "components/robots.txt"
    # The content type of the response. It is set to text/plain.
    content_type = "text/plain"



def Blog_index(request):
    """
    View function for the Blog Index page.

    This function retrieves all approved posts from the database and renders
    them in the Blog Index page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML response containing the Blog Index page with the retrieved posts.
    """

    try:
        # Retrieve all approved posts from the database
        # Order them by creation date in descending order
        # Prefetch related categories for efficiency
        posts = (
            Post.objects.filter(approved=True)
            .order_by("-created_on")
            .prefetch_related("categories")
        )

        # Create a context dictionary with the retrieved posts
        context = {
            "posts": posts,
        }

        # Render the Blog Index page with the posts in the context
        return render(request, "Blog/index.html", context)

    except Post.DoesNotExist:
        # Handle the case when no approved posts are found
        context = {
            "posts": [],
        }
        return render(request, "Blog/index.html", context)

    except Exception as e:
        # Handle any other exceptions that may occur
        messages.error(request, "An error occurred: " + str(e))
        return redirect("Blog_index")


def Blog_category(request, category):
    """
    View function for displaying blog posts in a specific category.

    Parameters:
    - request: The HTTP request object.
    - category: The name of the category.

    Returns:
    - Rendered HTML response containing the Blog Category page with the retrieved posts.
    """

    try:
        # Retrieve all posts in the specified category from the database
        # Order them by creation date in descending order
        # Prefetch related categories for efficiency
        posts = (
            Post.objects.filter(categories__name__contains=category)
            .order_by("-created_on")
            .prefetch_related("categories")
        )

        # Get the category object
        category_obj = Category.objects.get(name=category)

        # If the request method is POST and the user is authenticated
        if request.method == "POST" and request.user.is_authenticated:
            # If the user wants to follow the category
            if "follow" in request.POST:
                request.user.followed_categories.add(category_obj)
                messages.success(
                    request, f"You are now following {category_obj.name}."
                )

            # If the user wants to unfollow the category
            elif "unfollow" in request.POST:
                request.user.followed_categories.remove(category_obj)
                messages.success(
                    request, f"You have unfollowed {category_obj.name}."
                )

        # Create a context dictionary with the category and posts
        context = {
            "category": category_obj,
            "posts": posts,
        }

        # Render the Blog Category page with the category and posts in the context
        return render(request, "Blog/category.html", context)

    except Category.DoesNotExist:
        # Handle the case when the category does not exist
        messages.error(request, "Category does not exist.")
        return redirect("Blog_index")

    except Exception as e:
        # Handle any other exceptions that may occur
        messages.error(request, "An error occurred: " + str(e))
        return redirect("Blog_index")


def Blog_details(request, slug):
    """
    View function for displaying details of a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the blog post.

    Returns:
        HttpResponse: The HTTP response object.
    """

    try:
        # Get the blog post object or raise 404 error if it does not exist
        post = Post.objects.get(slug=slug)

        # Create a form instance for adding comments
        form = CommentForm()

        # If the request method is POST and the user is authenticated
        if request.method == "POST" and request.user.is_authenticated:
            # Create a form instance with the POST data
            form = CommentForm(request.POST)

            # If the form is valid, create a new comment object and save it
            if form.is_valid():
                comment = Comment(
                    author=request.user,
                    body=form.cleaned_data["body"],
                    post=post,
                )
                comment.save()
                return HttpResponseRedirect(request.path_info)

        # Get the list of approved comments
        comments = Comment.objects.filter(approved=True, post=post)

        # Get the list of tag IDs and category IDs of the post
        post_tags = post.tags.values_list("id", flat=True)
        post_categories = post.categories.values_list("id", flat=True)

        # Get the slug of the previous post from the session
        previous_slug = request.session.get("previous_slug")

        # Get the list of related posts
        related_posts = Post.objects.filter(
            Q(categories__in=post_categories) | Q(tags__in=post_tags) | Q(title__icontains=post.title),
            approved=True
        ).exclude(id=post.id).distinct()

        # Exclude the previous post if it exists
        if previous_slug:
            related_posts = related_posts.exclude(slug=previous_slug)

        # Now slice the QuerySet
        related_post = related_posts[:2]

        # Store the current post's slug in the session
        request.session["previous_slug"] = slug

        # Filter comments based on approved status and user's superuser status
        if request.user.is_superuser:
            comments = Comment.objects.filter(post=post)
        else:
            comments = Comment.objects.filter(post=post, approved=True, parent__isnull=True)

        # Create the context dictionary with the necessary data
        context = {
            "post": post,
            "comments": comments,
            "form": form,
            "related_posts": related_post,
        }

        # Render the Blog Details page with the context
        return render(request, "Blog/details.html", context)

    except Post.DoesNotExist as e:
        # Handle the case when the post does not exist
        messages.error(request, "Post does not exist.")
        return redirect("Blog_index")

    except Exception as e:
        # Handle any other exceptions that may occur
        messages.error(request, "An error occurred: " + str(e))
        return redirect("Blog_index")


def search(request):
    """
    Search for posts based on the query string parameter 'q'.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the search results.

    Raises:
        Http404: If the query string parameter 'q' is not provided.
    """
    # Check if the query string parameter 'q' is provided
    query = request.GET.get("q")
    if not query:
        raise Http404("Query string parameter 'q' is required.")

    # Filter the Post objects based on the query string
    try:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    except Exception as e:
        # Handle any exceptions that may occur during the database query
        messages.error(request, "An error occurred: " + str(e))
        return redirect("Blog_index")

    # Create the context dictionary with the search results
    context = {"results": results}

    # Render the search results template with the context
    return render(request, "components/search_components/search_results.html", context)


def comment_create(request, slug):
    """
    Create a new comment for a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the blog post.

    Returns:
        HttpResponse: The HTTP response object redirecting to the blog post details page.

    Raises:
        Http404: If the blog post object is not found.
        ValueError: If the parent comment object is not found.
    """
    try:
        # Get the blog post object based on the slug
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Blog post does not exist.")

    if request.method == "POST":
        # Create a form instance with the submitted data
        form = CommentForm(request.POST)

        if form.is_valid():
            # Save the comment without committing to the database
            comment = form.save(commit=False)

            # Associate the comment with the blog post and the current user
            comment.post = post
            comment.author = request.user

            # Check if the comment is a reply to another comment
            parent_id = request.POST.get("parent_id")
            if parent_id:
                try:
                    # Get the parent comment object and associate it with the comment
                    parent_obj = Comment.objects.get(id=parent_id)
                    comment.parent = parent_obj
                except Comment.DoesNotExist:
                    raise ValueError("Parent comment does not exist.")

            # Save the comment to the database
            comment.save()

            # Redirect to the blog post details page
            return redirect("Blog_details", slug=post.slug)
    else:
        # Create an empty form if the request method is not POST
        form = CommentForm()

    # Redirect to the blog post details page even if the form is not valid
    return redirect("Blog_details", slug=post.slug)


def comment_thread(request, comment_id):
    """
    Redirects to the blog post details page with the comment thread displayed.

    Args:
        request (HttpRequest): The HTTP request object.
        comment_id (int): The ID of the comment.

    Returns:
        HttpResponseRedirect: Redirects to the blog post details page.

    Raises:
        Http404: If the comment object is not found.
    """
    try:
        # Get the comment object based on the ID
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist.")

    # Get the associated blog post object
    post = comment.post

    # Redirect to the blog post details page with the comment thread displayed
    return redirect("Blog_details", slug=post.slug)  # adjust this as needed


@login_required
def comment_approve(request, id):
    """
    Approve a comment and redirect to the blog post details page.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the comment.

    Returns:
        HttpResponseRedirect: Redirects to the blog post details page.

    Raises:
        Http404: If the comment object is not found.
        ValueError: If the user is not authorized to approve the comment.
    """
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist.")

    if request.user.is_superuser:
        comment.approved = True  # set the approved field to True
        comment.save()  # save the comment
    else:
        raise ValueError("You do not have permission to approve comments.")

    return redirect("Blog_details", slug=comment.post.slug)  # redirect to the blog post details page


@login_required
def reply_approve(request, id):
    """
    Approve a reply comment and redirect to the blog post details page.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the reply comment.

    Returns:
        HttpResponseRedirect: Redirects to the blog post details page.

    Raises:
        Http404: If the reply comment object is not found.
    """
    # Get the reply comment object
    try:
        reply = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise Http404("Reply comment does not exist.")

    # Check if the user is authorized to approve the reply comment
    if request.user.is_superuser or request.user.is_staff:
        # Set the approved field to True
        reply.approved = True
        # Save the reply comment
        reply.save()
        # Redirect to the blog post details page
        return redirect("Blog_details", slug=reply.post.slug)
    else:
        # Display an error message and redirect to the blog post details page
        messages.error(request, "You do not have permission to approve replies.")
        return redirect("Blog_details", slug=reply.post.slug)


# i need to work on this later
@user_passes_test(is_admin)
@login_required
def approve_blog_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user.is_superuser or request.user.is_staff:
        post.approved = True
        post.save()
        messages.success(request, "The blog post has been approved.")
    else:
        messages.error(request, "You do not have permission to approve blog posts.")
    return redirect("Blog_details", slug=post.slug)


@login_required
def create_blog_post(request):
    """
    Create a new blog post.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the view_my_posts page if the form is valid,
        otherwise renders the blog_post.html template with the form.
    """
    # Check if the request method is POST
    if request.method == "POST":
        # Create a new BlogPostForm instance with the POST data
        form = BlogPostForm(request.POST, request.FILES)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to a new Post object and set the user field to the current user
            post = form.save(commit=False)
            post.user = request.user
            # Save the post object to the database
            post.save()
            # Save the many-to-many fields to the database
            form.save_m2m()
            # Display a success message and redirect to the view_my_posts page
            messages.success(request, "Your blog post has been published.")
            return redirect("view_my_posts")
    # If the request method is not POST, create a new BlogPostForm instance
    else:
        form = BlogPostForm()

    # Render the blog_post.html template with the form
    return render(request, "components/user/blog_post.html", {"form": form})


@login_required
def edit_post(request, slug):
    """
    Edit a blog post.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the blog post to edit.

    Returns:
        HttpResponse: The response object.
    """
    # Get the blog post to edit
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post not found.")

    if request.method == "POST":
        # Handle form submission
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Update only the modified fields
            for field in form.changed_data:
                if field in ["categories", "tags"]:
                    # Update many-to-many fields
                    getattr(post, field).set(form.cleaned_data[field])
                else:
                    # Update other fields
                    setattr(post, field, form.cleaned_data[field])
            post.save()
            return redirect("view_my_posts")
        else:
            # Display form with errors
            return render(
                request,
                "components/user/blog_update.html",
                {"form": form, "post": post, "edit_mode": True, "errors": form.errors},
            )
    else:
        # Display form for editing
        form = BlogPostForm(instance=post)

    return render(
        request,
        "components/user/blog_update.html",
        {"form": form, "post": post, "edit_mode": True},
    )


@login_required
def delete_post(request, slug):
    """
    Deletes a blog post.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the blog post to delete.

    Returns:
        HttpResponseRedirect: Redirects to the 'view_my_posts' page if the post is deleted.
        HttpResponse: Renders the 'blog_delete.html' template if the request method is not POST.

    """
    # Check if the slug is provided
    if slug is None:
        raise Http404("Post not found.")

    try:
        # Get the blog post to delete
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post not found.")

    if request.method == "POST":
        # Delete the post if the request method is POST
        post.delete()
        # Add a success message
        messages.success(request, "Your post was successfully deleted.")
        # Redirect to the 'view_my_posts' page
        return redirect("view_my_posts")

    # Render the 'blog_delete.html' template if the request method is not POST
    return render(request, "components/user/blog_delete.html", {"post": post})
