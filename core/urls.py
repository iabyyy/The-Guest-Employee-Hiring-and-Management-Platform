from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('contractor/', views.contractor_dashboard, name='contractor'),
    path('guest/', views.guest_dashboard, name='guest'),

    path('post-job/', views.post_job, name='post_job'),
    path('search-guest/', views.search_guest, name='search_guest'),
    path('feedback/', views.feedback, name='feedback'),
]
