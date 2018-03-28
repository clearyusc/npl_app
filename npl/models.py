import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Encounter(models.Model):
    MINISTRY_RESPONSES = (('RL', 'Red Light'),
                 ('YL', 'Yellow Light'), ('GL', 'Green Light'),
                 ('WT', 'Believer Wants Training'),
                 ('RT', 'Believer Rejects Training'))
    name = models.CharField(max_length=40)
    action_prayer = models.BooleanField(default=False)
    action_testimony = models.BooleanField(default=False)
    action_gospel = models.BooleanField(default=False)
    response = models.CharField(max_length=2, choices=MINISTRY_RESPONSES)
    notes = models.TextField(default="Notes...")
    date_time = models.DateTimeField()
    is_oikos = models.BooleanField(default=False)

    # Geo-Location Fields:
    street_address = models.CharField(max_length=50)
    apt_or_unit = models.CharField(blank=True, max_length=15, default='')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zip = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()


class Team(models.Model):
    date_team_created = models.DateField()
    team_name = models.CharField(max_length=40)


class User(models.Model):
    date_account_created = models.DateField()
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    encrypted_password = models.CharField(max_length=150)
    team_members = models.ManyToManyField(Team)



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
