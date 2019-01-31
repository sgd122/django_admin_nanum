from django.urls import path
from api.views import MoimListView 

app_name = 'api'

urlpatterns = [
    path('moim/', MoimListView.as_view(), name='moim'),
]