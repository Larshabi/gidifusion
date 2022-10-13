from .views import Teams, TeamMates
from django.urls import path

urlpatterns = [
    path('', Teams.as_view()),
    path('teammates/', TeamMates.as_view())
]