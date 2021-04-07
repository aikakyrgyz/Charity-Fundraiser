
from django.contrib import admin
from django.urls import path, include

from main.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name = 'home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name = 'category'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name = 'article'),
    path('create-post/', create_post, name ='create_post'),
    path('update-post/<int:pk>/', update_post, name = 'update_post'),
    path('delete-post/<int:pk>/', DeleteArticleView.as_view(), name = 'delete_post'),
]