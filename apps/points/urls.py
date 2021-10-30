from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('applications/', views.MyFirstAPIView.as_view(), name='MyFirstAPIView'),
]