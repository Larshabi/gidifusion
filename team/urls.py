from .views import Team
from django.urls import path

urlpatterns = [
    path('', Team.as_view())
]