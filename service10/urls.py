from django.urls import path
from service10.views import *
from . import views

app_name = 'service10'

urlpatterns = [
    
    #path('', views.stdApplyIns, name='stdApplyIns'),
    path('auth/', authView, name='authView'),
    path('authChk/', post_login, name='post_login'),
    

]