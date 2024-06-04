from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('my_posts/', views.view_my_posts, name='view_my_posts'),
]
