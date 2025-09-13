from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register', views.RegisterView.as_view(), name='register_no_slash'),
    path('login/', views.login_view, name='login'),
    path('login', views.login_view, name='login_no_slash'),
    path('logout/', views.logout_view, name='logout'),
    path('logout', views.logout_view, name='logout_no_slash'),
    path('profile/', views.profile_view, name='profile'),
    path('profile', views.profile_view, name='profile_no_slash'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('profile/update', views.update_profile_view, name='update_profile_no_slash'),
]