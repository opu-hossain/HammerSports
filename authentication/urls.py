from django.urls import path
from . import views

# Define the URL patterns for the authentication app
urlpatterns = [
    # Register a new user
    path('register/', views.register, name='register'),
    # Login a user
    path('login/', views.login_view, name='login'),
    # Logout a user
    path('logout/', views.logout_view, name='logout'),
    # View a user's own profile
    path('my-profile/', views.my_profile, name='my-profile'),
    # View a user's profile
    path('profile/<str:username>/', views.profile, name='profile'),
    # Update a user's profile
    path('profile_update/', views.profile_update, name='profile_update'),
    # View the posts of a user
    path('my_posts/', views.view_my_posts, name='view_my_posts'),
    # Create a new guest post
    path('guest_post/', views.guest_post, name='guest_post'),
    # Reset a user's password
    path('password_reset/', views.CustomPasswordResetView.as_view(),
        name='password_reset'),
    # Page shown after a user requests a password reset
    path('password_reset/done/',
        views.CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'),
    # Confirm a new password for a user
    path('reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    # Page shown after a user has reset their password
    path('reset/done/',
        views.CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    # Follow a user
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    # Unfollow a user
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    # View the users who follow a user
    path('followers/<str:username>/', views.followers_list, name='followers_list'),
]
