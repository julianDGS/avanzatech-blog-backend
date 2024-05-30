from django.urls import path
from . import views

urlpatterns = [
    path('', views.PermissionView.as_view(), name='permission'),
    path('category/', views.CategoryView.as_view(), name='category'),

]