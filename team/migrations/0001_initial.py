# Generated by Django 3.2.8 on 2022-09-20 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_type', models.CharField(choices=[('VIP', 'VIP'), ('Regular', 'Regular')], max_length=10)),
                ('price', models.IntegerField()),
                ('team_side', models.CharField(choices=[('Island', 'Island'), ('Mainland', 'Mainland')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teammate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('team_side', models.CharField(choices=[('Island', 'Island'), ('Mainland', 'Mainland')], max_length=20)),
                ('coach_name', models.CharField(max_length=255)),
                ('team_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team_mates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.teammate')),
            ],
        ),
    ]
