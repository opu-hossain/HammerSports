from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib import messages



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
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile_update.html', {'form':form})

