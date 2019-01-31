from django.urls import path
from service20.views import Service20ListView ,stdApplyStdView
from . import views

app_name = 'service20'

urlpatterns = [
    
    #path('', views.stdApplyIns, name='stdApplyIns'),
    path('stdApplyStdView/', stdApplyStdView, name='detail'),
    path('', Service20ListView.as_view(), name='Service20ListView'),
]