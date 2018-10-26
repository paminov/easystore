# helloworld/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from easystore import views

urlpatterns = [
    path('', views.Home.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',
                                           redirect_authenticated_user=True), 
         name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('verify/', views.UserVerify.as_view()),
    path('verify/<slug:username>/', views.UserVerify.as_view(), 
         name='verify_user'),
    path('api/upload', views.Upload.as_view()),
    path('api/contents', views.Contents.as_view()),
]
