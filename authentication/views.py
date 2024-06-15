from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CustomUser
from Blog.models import Post
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse , reverse_lazy
from django.http import HttpResponseRedirect



# Create your views here.

#password reset views

class CustomPasswordResetView(PasswordResetView):
    template_name = 'pass_reset/password_reset_form.html'  # your template
    email_template_name = 'pass_reset/password_reset_email.html'  # your template
    subject_template_name = 'pass_reset/password_reset_subject.txt'  # your template
    success_url = reverse_lazy('password_reset_done')  # name of the URL for the page to be shown after the email is sent


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pass_reset/password_reset_confirm.html'  # your template
    success_url = reverse_lazy('password_reset_complete')  # name of the URL for the page to be shown after the password is reset

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pass_reset/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pass_reset/password_reset_complete.html'  # your template

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'HaHammerBlog.backends.CustomUserModelBackend'
            user.backend = backend
            login(request, user)
            return redirect('Blog_index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = '@' + request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Blog_index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    return render(request, 'login.html')

def profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    followed_categories = profile_user.followed_categories.all()

    # Approved posts
    approved_posts = Post.objects.filter(user=profile_user, approved=True)

    context = {
        'profile_user': profile_user,
        'followed_categories': followed_categories,
        'approved_posts': approved_posts,
    }
    return render(request, 'profile.html', context)

def guest_post(request):
    if request.user.is_authenticated:
        return redirect('Blog_index')  # or wherever you want to redirect authenticated users
    else:
        return render(request, 'unauthorized.html')

def view_my_posts(request):
    approved_posts = Post.objects.filter(user=request.user, approved=True)
    pending_posts = Post.objects.filter(user=request.user, approved=False)

    context = {
        'approved_posts': approved_posts,
        'pending_posts': pending_posts,
    }

    return render(request, 'view_my_posts.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('Blog_index')

@login_required
def my_profile(request):
    if request.user.is_authenticated:
        followed_categories = request.user.followed_categories.all()

        context = {
            'profile_user': request.user,
            'followed_categories': followed_categories,
        }
        return render(request, 'my_profile.html', context)
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('login') 
    # return render(request, 'my_profile.html', {'user': request.user})

@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            changed_fields = form.changed_data  # Get the fields that have been changed
            user = form.save(commit=False)  # Don't save the form yet
            user.save(update_fields=changed_fields)  # Save only the changed fields
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'profile_update.html', {'form':form})

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(CustomUser, username=username)
    request.user.following.remove(user_to_unfollow)
    messages.success(request, f"You have unfollowed {username}!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(CustomUser, username=username)
    if request.user in user_to_follow.user_followers.all():
        messages.error(request, f"You are already following {username}!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    request.user.following.add(user_to_follow)
    messages.success(request, f"You are now following {username}!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def followers_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    followers = user.user_followers.all()
    return render(request, 'followers.html', {'followers': followers})