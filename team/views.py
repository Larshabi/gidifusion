from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .serializer import  TeamSerializer, TicketSerializer
from rest_framework.permissions import AllowAny
from .models import Team, Booking

class Team(ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes =  [AllowAny]
    queryset = Team.objects.all()
    
class Ticket(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()
    
    