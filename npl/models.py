from django.db import models
from django.contrib.auth.models import User

# Create your models here.
MINISTRY_RESPONSES = (('RL', 'Red Light'),
                      ('YL', 'Yellow Light'), ('GL', 'Green Light'),
                      ('WT', 'Believer Wants Training'),
                      ('EB', 'Existing Believer'))


class Laborer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()

    def __str__(self):
        name = str(self.user.first_name) + str(self.user.last_name)
        if name != '' and name is not None:
            return name

        return self.user.username


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

    def __str__(self):
        return self.name + ' (' + self.response + ')'


class Team(models.Model):
    team_name = models.CharField(max_length=40, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(Laborer)
    number_of_members = models.IntegerField(default=1)
    # leaders = models.ManyToManyField(Laborer)

    def __str__(self):
        return self.team_name

