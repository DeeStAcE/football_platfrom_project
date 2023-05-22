from django.urls import path
from football.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
