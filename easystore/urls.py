# helloworld/urls.py
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from easystore import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',
                                           redirect_authenticated_user=True), 
         name='login'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('verify/', views.UserVerify.as_view()),
    path('verify/<slug:username>/', views.UserVerify.as_view(), 
         name='verify_user'),
    path('api/delete/', views.Delete.as_view(), name='delete'),
    path('api/contents/', views.Contents.as_view(), name='contents'),
    path('health/', views.health, name='health')
]