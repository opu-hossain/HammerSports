from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from Blog.models import Post
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse , reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseServerError, Http404



# Create your views here.

#password reset views

class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view that uses specified templates and success URL.

    Attributes:
        template_name (str): The name of the template to use for the password reset form.
        email_template_name (str): The name of the template to use for the password reset email.
        subject_template_name (str): The name of the template to use for the password reset email subject.
        success_url (str): The name of the URL to redirect to after the email is sent.
    """
    template_name = 'pass_reset/password_reset_form.html'  # your template
    email_template_name = 'pass_reset/password_reset_email.html'  # your template
    subject_template_name = 'pass_reset/password_reset_subject.txt'  # your template
    success_url = reverse_lazy('password_reset_done')  # name of the URL for the page to be shown after the email is sent


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirm view that uses specified templates and success URL.

    Attributes:
        template_name (str): The name of the template to use for the password reset confirm form.
        success_url (str): The name of the URL to redirect to after the password is reset.
    """
    template_name = 'pass_reset/password_reset_confirm.html'  # your template
    success_url = reverse_lazy('password_reset_complete')  # name of the URL for the page to be shown after the password is reset



class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Custom password reset done view that uses specified template.

    Attributes:
        template_name (str): The name of the template to use for the password reset done page.
    """
    template_name = 'pass_reset/password_reset_done.html'  # your template


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Custom password reset complete view that uses specified template.

    Attributes:
        template_name (str): The name of the template to use for the password reset complete page.
    """
    template_name = 'pass_reset/password_reset_complete.html'  # your template


def register(request):
    """
    Register a new user.

    If the request method is POST, create a new form instance with the
    request data. If the form is valid, create a new user instance from
    the form data and authenticate the user. If the user is authenticated
    successfully, log the user in and redirect them to the Blog index page.
    If an exception occurs during user creation or authentication, handle
    the exception and display an error message. If the form is not valid,
    render the form with errors.

    If the request method is not POST, create a new form instance.
    Render the registration form template with the form context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user = authenticate(request, username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                    return redirect('Blog_index')
                else:
                    messages.error(request, "Failed to authenticate user.")
            except Exception as e:
                messages.error(request, f"Failed to register user: {str(e)}")
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handle user login.

    If the request method is POST, attempt to authenticate the user with
    the provided username and password. If the authentication is successful,
    log the user in and redirect them to the Blog index page. If the
    authentication fails, display an error message and redirect back to the
    login page. If the request method is not POST, render the login form template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # If the request method is POST, attempt to authenticate the user
    if request.method == 'POST':
        # Get the username and password from the request data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If the username or password is missing, display an error message and redirect back to the login page
        if not username or not password:
            messages.error(request, 'Please enter a username and password.')
            return redirect('login')

        # Add '@' symbol to username for authentication
        username = '@' + username

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated, log them in and redirect to the Blog index page
        if user is not None:
            login(request, user)
            return redirect('Blog_index')

        # If the authentication fails, display an error message and redirect back to the login page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    # If the request method is not POST, render the login form template
    return render(request, 'login.html')

def profile(request, username):
    """
    Render the profile page for a given user.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Get the user object for the given username. If it doesn't exist, raise a 404 error.
    try:
        profile_user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist")

    # Get all the categories that the user is following. If it doesn't exist, set followed_categories to an empty queryset.
    try:
        followed_categories = profile_user.followed_categories.all()
    except CustomUser.DoesNotExist:
        followed_categories = CustomUser.objects.none()

    # Get all the approved posts by the user. If it doesn't exist, set approved_posts to an empty queryset.
    try:
        approved_posts = Post.objects.filter(user=profile_user, approved=True)
    except Post.DoesNotExist:
        approved_posts = Post.objects.none()

    # Create a context dictionary with the necessary data
    context = {
        'profile_user': profile_user,  # The user object of the profile
        'followed_categories': followed_categories,  # All the categories followed by the user
        'approved_posts': approved_posts,  # All the approved posts by the user
    }

    # Render the profile.html template with the context
    return render(request, 'profile.html', context)



def guest_post(request):
    """
    Redirect authenticated users to Blog index page.
    Otherwise, render the unauthorized.html template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    # Check if the request object and user object exist
    if request and request.user:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Redirect to Blog index page
            return redirect('Blog_index')
        else:
            # Render the unauthorized.html template
            return render(request, 'unauthorized.html')
    else:
        # Return a 500 error if request or user object is None
        return HttpResponseServerError('Invalid request or user object')

def view_my_posts(request):
    """
    View the posts of the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    
    # Check if the request object and user object exist
    if request and request.user:
        # Get the approved and pending posts of the authenticated user
        try:
            approved_posts = Post.objects.filter(user=request.user, approved=True)
            pending_posts = Post.objects.filter(user=request.user, approved=False)
        except Post.DoesNotExist:
            approved_posts = Post.objects.none()
            pending_posts = Post.objects.none()

        # Create a context dictionary with the necessary data
        context = {
            'approved_posts': approved_posts,  # All the approved posts by the user
            'pending_posts': pending_posts,  # All the pending posts by the user
        }

        # Render the view_my_posts.html template with the context
        return render(request, 'view_my_posts.html', context)
    else:
        # Return a 500 error if request or user object is None
        return HttpResponseServerError('Invalid request or user object')

@login_required
def logout_view(request):
    """
    Logs out the user and redirects to the Blog index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the Blog index page.

    Raises:
        ValueError: If the request object is None.
    """
    if request is None:
        raise ValueError("Request object cannot be None")

    # Log out the user
    logout(request)

    # Redirect to the Blog index page
    return redirect('Blog_index')

@login_required
def my_profile(request):
    """
    View the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the user is not authenticated.
    """

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If the user is not authenticated, display an error message and redirect to the login page
        messages.error(request, 'You must be logged in to view this page.')
        raise Http404('User not authenticated')

    # Get the categories followed by the user
    followed_categories = request.user.followed_categories.all()

    # Create a context dictionary with the necessary data
    context = {
        'profile_user': request.user,  # The user object
        'followed_categories': followed_categories,  # The categories followed by the user
    }

    # Render the my_profile.html template with the context
    return render(request, 'my_profile.html', context)


@login_required
def profile_update(request):
    """
    View to update the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the user is not authenticated.
        ValueError: If the request method is not POST or GET.
    """

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If the user is not authenticated, display an error message and redirect to the login page
        messages.error(request, 'You must be logged in to view this page.')
        raise Http404('User not authenticated')

    # Check if the request method is POST or GET
    if request.method not in ['POST', 'GET']:
        # If the request method is not POST or GET, raise a ValueError
        raise ValueError('Invalid request method')

    # Get the user object
    user = request.user

    # Check if the request method is POST
    if request.method == 'POST':
        # Create an instance of the ProfileUpdateForm with the POST data and files
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        # Check if the form is valid
        if form.is_valid():
            # Save the form
            form.save()
            # Redirect to the user's profile page
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        # Create an instance of the ProfileUpdateForm with the user object as the instance
        form = ProfileUpdateForm(instance=user)

    # Render the profile_update.html template with the form
    return render(request, 'profile_update.html', {'form': form})

@login_required
def unfollow_user(request, username):
    """
    Remove a user from the current user's following list.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user to unfollow.

    Returns:
        HttpResponseRedirect: A redirect to the referrer page.

    Raises:
        Http404: If the user to unfollow does not exist.
    """
    # Get the user object of the user to unfollow
    try:
        user_to_unfollow = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("User to unfollow does not exist")

    # Remove the user to unfollow from the current user's following list
    request.user.following.remove(user_to_unfollow)

    # Display a success message to the user
    messages.success(request, f"You have unfollowed {username}!")

    # Redirect the user to the page they were on before
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def follow_user(request, username):
    """
    Add a user to the current user's following list.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user to follow.

    Returns:
        HttpResponseRedirect: A redirect to the referrer page.

    Raises:
        Http404: If the user to follow does not exist.
    """
    # Get the user object of the user to follow
    try:
        user_to_follow = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("User to follow does not exist")
    
    # Check if the current user is already following the user to follow
    if request.user in user_to_follow.user_followers.all():
        # If the current user is already following the user to follow, display an error message
        messages.error(request, f"You are already following {username}!")
    else:
        # Add the user to follow to the current user's following list
        request.user.following.add(user_to_follow)
        # Display a success message to the user
        messages.success(request, f"You are now following {username}!")

    # Redirect the user to the page they were on before
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def followers_list(request, username):
    """
    View function to display a list of followers for a given user.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose followers are to be displayed.

    Returns:
        HttpResponse: A rendered HTML response containing the list of followers.

    Raises:
        Http404: If the user whose followers are to be displayed does not exist.
    """
    try:
        # Get the user object of the user whose followers are to be displayed
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist")
    
    # Get the list of users who are following the user
    followers = user.user_followers.all()
    
    # Render the 'followers.html' template with the list of followers
    return render(request, 'followers.html', {'followers': followers})
