from django.db import models

class Team(models.Model):
    
    SIDE_CHOICE = (
        ('Island', 'Island'),
        ('Mainland', 'Mainland'),
    )
    email = models.EmailField(max_length=255)
    team_side = models.CharField(max_length=20, choices=SIDE_CHOICE)
    coach_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.team_name

class Teammate(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name= 'team_mates', null=True, blank=True)
    
    def __str__(self):
        return self.name


    
class Booking(models.Model):
    SIDE_CHOICE = (
        ('Island', 'Island'),
        ('Mainland', 'Mainland'),
    )
    CHOICE = (
        ('VIP', 'VIP'),
        ('Regular', 'Regular'),
    )
    email = models.EmailField(max_length=255, null=True, blank=True)
    ticket_type = models.CharField(max_length=10, choices=CHOICE)
    price = models.IntegerField()
    team_side = models.CharField(max_length=10, choices=SIDE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.email}'
{
    "email": "lekanlasabi@gmail.com",
    "coach_name": "Lasabi",
    "team_name": "Lash",
    "team_mates": [
    {
       "name":"Kola Ladoke",
       "phone":"09059642793"
    },
   {
       "name":"Omolola Precious",
       "phone":"08035991349"
   }
],
    "team_side": "Mainland"
}