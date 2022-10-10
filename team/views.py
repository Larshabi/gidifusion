from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from .serializer import  TeamSerializer, TicketSerializer
from rest_framework.permissions import AllowAny
from .models import Team, Booking
from .utils import Util
from rest_framework import status
from django.conf import settings
import requests
import json


class Teams(ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes =  [AllowAny]
    queryset = Team.objects.all()
    
    def post(self, request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = 'https://api.paystack.co/transaction/initialize'
            serializer.save()
            coach_name = serializer.data['coach_name']
            # team_name = serializer.data['team_name']
            team = Team.objects.get(team_name=serializer.data['team_name'])
            headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}', 'Content-Type':'application/json'}
            payload = {
                'email':team.email,
                'amount': team.amount * 100,
                'first_name' : team.coach_name 
            }
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            result = res.json()
            data["data"] = serializer.data
            data["payment_redirect"] = result
            email_body = f"Hi {coach_name},\n\nYou are all set! Your team has successfully registered for the fusion cup competition.\n\nThere would be a single elimination playoff on the 11th of November at the Ogudu recreational center by 11am where each teams compete to qualify for the finals. Come prepared in uniformity and with your proper kits.\n\nThis email serves as an access pass for entry therefore should be presented at the venue.\n\nWe are looking forward to a good game of basketball. For questions and enquiries please reach out to us at contact@gidifusion.ng.\n\nBest Regards,\nTeam Gidifusion."
            email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":serializer.data['email']}
            Util.send_email(email_data)
            return Response(data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
class Ticket(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()
    
    def post(self, request):
        data = {}
        url = 'https://api.paystack.co/transaction/initialize'
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tickets = Booking.objects.filter(email=serializer.data['email']).order_by('-created_at')
            print(tickets)
            ticket = tickets[0]
            headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}', 'Content-Type':'application/json'}
            payload = {
                    'amount':ticket.price * 100,
                    'email':ticket.email,
                }
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            result = res.json()
            data["data"] = serializer.data
            data["payment_redirect"] = result
            email_body = f'Hi There,\nWelcome to Gidifusion! You have successfully registered for the first edition of the Gidifusion rave 2022.\n\nThis email serves as an access pass and should be presented at the venue.\n\nWe are looking forward to seeing you.\nIf you have any questions, reach out to us at contact@gidifusion.ng\n\nBest Regards,\nTeam Gidifusion\n\n.......\nDetails of Ticket purchased here\n{ticket.email}\n{ticket.quantity}\n{ticket.ticket_type}'
            email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":ticket.email}
            Util.send_email(email_data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class PayCallback(GenericAPIView):
    serializer_class=TicketSerializer
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get('trxref')
        url = f'https://api.paystack.co/transaction/verify/{query}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}'}
        res = requests.get(url, headers=headers)
        result=res.json()
        return Response({'message': result["message"]}, status=status.HTTP_200_OK)
    
class PaymentVerify(GenericAPIView):
    serializer_class =TicketSerializer
    permission_classes = [AllowAny]
    def get(self, reuest, tref):
        url = f'https://api.paystack.co/transaction/verify/{tref}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}'}
        res = requests.get(url, headers=headers)
        result=res.json()
        return Response({'message': result["message"]}, status=status.HTTP_200_OK)
    
    
    