from django.urls import path
from . import views

app_name = 'post2'

urlpatterns = [
        path('', views.index, name='index'),  # index view at /
        path('likepost/', views.likePost, name='likepost'),   # likepost view at /likepost
   ]