from .models import Team, Teammate, Booking
from rest_framework import serializers
from .utils import Util

class TeammateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teammate
        fields = [
            'name',
            'phone',
            'team'
        ]
        read_only_fields = ['team']
        
class TeamSerializer(serializers.ModelSerializer):
    team_mates = TeammateSerializer(many=True)
    class Meta:
        model = Team
        fields = [
            'id',
            'email',
            'coach_name',
            'team_name',
            'team_mates',
            'team_side'
        ]
    
    def create(self, validated_data):
        team_mates = validated_data.pop('team_mates')
        team = Team.objects.create(**validated_data)
        for team_mate in team_mates:
            Teammate.objects.create(team=team, **team_mate)
        return team
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'email',
            'ticket_type',
            'team_side',
            'quantity',
            'price'
        ]
        read_only_fields =  ['price']
    
    def create(self, validated_data):
        if validated_data['ticket_type'] == 'VIP':
            price = 5000
        if validated_data['ticket_type'] == 'Regular':
            price = 2000
        actual_price = validated_data['quantity'] * price
        # data = {'to_email':validated_data['email'], 'email_subject':'Gidifusion Ticket', 'email_body':'something'}
        # Util.send_email(data)
        return Booking.objects.create(price=actual_price, **validated_data)    
        