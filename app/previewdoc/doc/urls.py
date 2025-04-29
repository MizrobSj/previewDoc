from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_file, name='file'),
    path('upload/page/<int:page>/', views.upload_file_paginated, name='file_page'),
]