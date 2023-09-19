from django.contrib import admin
from django.urls import path, include
from aws_s3 import views

urlpatterns = [
    path('', views.home, name='base.html'),
    path('create', views.create_bucket, name='index.html'),
    path('list', views.list_bucket, name='list_bucket'),
    path('upload', views.upload, name='upload.html'),
    path('create_folder', views.create_folder, name='create_folder.html'),
    path('delete', views.delete, name='delete.html'),
    path('delete_bucket', views.delete_bucket, name='delete_bucket.html'),
    path('copy_object', views.copy_object, name='copy_object.html'),
    path('move_object', views.move_object, name='move_object.html'),
]
