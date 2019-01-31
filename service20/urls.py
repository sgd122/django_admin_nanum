from django.urls import path
from service20.views import Service20ListView 

app_name = 'service20'

urlpatterns = [
    path('', Service20ListView.as_view(), name='msch'),
]