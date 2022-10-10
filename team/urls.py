from .views import Teams
from django.urls import path

urlpatterns = [
    path('', Teams.as_view())
]