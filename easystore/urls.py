# helloworld/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from easystore import views

urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url('api/upload', views.Upload.as_view()),
    url('api/contents', views.Contents.as_view()),
]
