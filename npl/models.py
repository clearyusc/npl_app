from django.db import models
from django.contrib.auth.models import User

# Create your models here.
MINISTRY_RESPONSES = (('RL', 'Red Light'),
                      ('YL', 'Yellow Light'), ('GL', 'Green Light'),
                      ('WT', 'Believer Wants Training'),
                      ('RT', 'Believer Rejects Training'))


class Laborer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateField()


class Encounter(models.Model):
    laborer = models.ForeignKey(Laborer, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    action_prayer = models.BooleanField(default=False)
    action_testimony = models.BooleanField(default=False)
    action_gospel = models.BooleanField(default=False)
    phone_number = models.IntegerField(blank=True, null=True)
    response = models.CharField(max_length=2, choices=MINISTRY_RESPONSES)
    response_description = models.CharField(max_length=40, null=True)
    notes = models.TextField(blank=True)
    date_time = models.DateTimeField(blank=True)
    is_oikos = models.BooleanField(default=False)

    # Geo-Location Fields (can all be null if it is an oikos encounter)
    street_address_number = models.CharField(max_length=10, blank=True, null=True)
    street_address_name = models.CharField(max_length=50, blank=True, null=True)
    apt_or_unit = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    full_address = models.CharField(max_length=300, blank=True, null=True)


class Team(models.Model):
    team_name = models.CharField(max_length=40)
    creation_date = models.DateField()
    members = models.ManyToManyField(Laborer)
    # leaders = models.ManyToManyField(Laborer)
