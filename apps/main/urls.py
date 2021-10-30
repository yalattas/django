from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainView.as_view())
]