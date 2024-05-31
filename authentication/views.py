from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CustomUser
from Blog.models import Post
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    print(followed_categories)
    print(followed_categories.count())

    context = {
        'profile_user': profile_user,
        'followed_categories': followed_categories,
    }
    return render(request, 'profile.html', context)

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

def view_my_posts(request):
    approved_posts = Post.objects.filter(user=request.user, approved=True)
    pending_posts = Post.objects.filter(user=request.user, approved=False)

    context = {
        'approved_posts': approved_posts,
        'pending_posts': pending_posts,
    }

    return render(request, 'view_my_posts.html', context)