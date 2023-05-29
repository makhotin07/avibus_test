from django.urls import path

from .views import find_bus

urlpatterns = [
    path("", find_bus),
]