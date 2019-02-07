from django.urls import path
from service20.views import *
from . import views

app_name = 'service20'

urlpatterns = [
    
    #path('', views.stdApplyIns, name='stdApplyIns'),
    path('stdApplyStdView/', stdApplyStdView, name='detail'),
    path('Service20_01/', Service20_01_View, name='detail'),
    path('', Service20ListView.as_view(), name='Service20ListView'),

    path('authUserInfo/', post_user_info, name='post_user_info'),
]