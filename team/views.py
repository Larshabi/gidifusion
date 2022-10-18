from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, GenericAPIView, ListAPIView, CreateAPIView
from .serializer import  TeamSerializer, TicketSerializer, TeamsSerializer
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
     
class TeamMates(CreateAPIView):
    serializer_class = TeamsSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        data = {}
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            serializer.save()
            url = 'https://api.paystack.co/transaction/initialize'
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
        amount =  result['data']['amount']
        amount = amount/100
        email = result['data']['customer']['email']
        if result['message'] == 'Verification successful':
            if amount == 40000:
                teams = Team.objects.filter(email=email).order_by('-created_at')
                team = teams[0]
                team.paid = True
                team.save()
                email_body = f"Hi {team.coach_name},\n\nYou are all set! Your team has successfully registered for the fusion cup competition.\n\nThere would be a single elimination playoff on the 11th of November at the Ogudu recreational center by 11am where each teams compete to qualify for the finals. Come prepared in uniformity and with your proper kits.\n\nThis email serves as an access pass for entry therefore should be presented at the venue.\n\nWe are looking forward to a good game of basketball. For questions and enquiries please reach out to us at contact@gidifusion.ng.\n\nBest Regards,\nTeam Gidifusion."
                email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":email}
                # Util.send_email(email_data)
            else:
                tickets = Booking.objects.filter(email=email).order_by('-created_at')
                ticket = tickets[0]
                ticket.paid = True
                ticket.save()
                email_body = f'Hi There,\nWelcome to Gidifusion! You have successfully registered for the first edition of the Gidifusion rave 2022.\n\nThis email serves as an access pass and should be presented at the venue.\n\nWe are looking forward to seeing you.\nIf you have any questions, reach out to us at contact@gidifusion.ng\n\nBest Regards,\nTeam Gidifusion\n\n.......\nDetails of Ticket purchased here\n{ticket.email}\n{ticket.quantity}\n{ticket.ticket_type}'
                email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":ticket.email}
                # Util.send_email(email_data)
            return Response({'message': result["message"]}, status=status.HTTP_200_OK)
        else:
            return Response({'message': result['message']}, status=status.HTTP_200_OK)
    
class PaymentVerify(GenericAPIView):
    serializer_class =TicketSerializer
    permission_classes = [AllowAny]
    def get(self, request, tref):
        url = f'https://api.paystack.co/transaction/verify/{tref}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}'}
        res = requests.get(url, headers=headers)
        result=res.json()
        amount =  result['data']['amount']
        amount = amount/100
        email = result['data']['customer']['email']
        if result['message'] == 'Verification successful':
            if amount == 40000:
                teams = Team.objects.filter(email=email).order_by('-created_at')
                team = teams[0]
                team.paid = True
                team.save()
                email_body = f"Hi {team.coach_name},\n\nYou are all set! Your team has successfully registered for the fusion cup competition.\n\nThere would be a single elimination playoff on the 11th of November at the Ogudu recreational center by 11am where each teams compete to qualify for the finals. Come prepared in uniformity and with your proper kits.\n\nThis email serves as an access pass for entry therefore should be presented at the venue.\n\nUpbeat Center, lekki phase 1.\n19th November, 2022. 12pm.\n\nWe are looking forward to a good game of basketball. For questions and enquiries please reach out to us at contact@gidifusion.ng.\n\nBest Regards,\nTeam Gidifusion."
                email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":email}
                Util.send_email(email_data)
            else:
                tickets = Booking.objects.filter(email=email).order_by('-created_at')
                ticket = tickets[0]
                ticket.paid = True
                ticket.save()
                email_body = f'Hi There,\nWelcome to Gidifusion! You have successfully registered for the first edition of the Gidifusion rave 2022.\n\nThis email serves as an access pass and should be presented at the venue.\n\nUpbeat Center, lekki phase 1.\n19th November, 2022. 12pm.\n\nWe are looking forward to seeing you.\nIf you have any questions, reach out to us at contact@gidifusion.ng\n\nBest Regards,\nTeam Gidifusion\n\n.......\nDetails of Ticket purchased here\n{ticket.email}\n{ticket.quantity}\n{ticket.ticket_type}'
                email_data = {"email_body":email_body, "email_subject":"Team Registration", "to_email":ticket.email}
                Util.send_email(email_data)
            return Response({'message': result["message"]}, status=status.HTTP_200_OK)
        else:
            return Response({'message': result['message']}, status=status.HTTP_200_OK)
    
class Paid_ticket(ListAPIView):
    serializer_class = TicketSerializer
    queryset = Booking.objects.filter(paid=True)
    
class Paid_Teams(ListAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.filter(paid=True)
    
    