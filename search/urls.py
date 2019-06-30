from django.contrib import admin
from django.urls import path
from .views import searchposts

urlpatterns = [
    path('', searchposts , name='search'),
]
