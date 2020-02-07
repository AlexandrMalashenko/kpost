from django.contrib import admin
from django.urls import path

from .views import index, add_comment, vote, ratings

urlpatterns = [
    path('', index),
    path('add_comment', add_comment, name='add_comment'),
    path('vote', vote, name='vote'),
    path('ratings', ratings, name='ratings'),
]